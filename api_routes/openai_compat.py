"""
OpenAI-compatible endpoints for ORBIT.

Implements (where practical):
  GET  /v1/models
  GET  /v1/models/{model_id}
  POST /v1/chat/completions   (already in api.py — not duplicated)
  POST /v1/completions
  POST /v1/embeddings

Response shapes follow OpenAI's public API closely enough for common
clients (curl, openai-python with base_url override, LM-studio-style tools).
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator

router = APIRouter(tags=["openai-compatible"])

from api_routes.openai_helpers import model_catalog as _model_catalog, usage as _usage, estimate_tokens as _estimate_tokens


@router.get("/v1/models/{model_id}")
def retrieve_model(model_id: str):
    for m in _model_catalog():
        if m["id"] == model_id:
            return m
    raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found")


class CompletionsRequest(BaseModel):
    model: str = "orbit-toy"
    prompt: Union[str, List[str]] = ""
    max_tokens: Optional[int] = Field(default=40, ge=1, le=512)
    temperature: Optional[float] = Field(default=0.8, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=0.9, gt=0.0, le=1.0)
    top_k: Optional[int] = Field(default=0, ge=0)
    n: Optional[int] = Field(default=1, ge=1, le=4)
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    echo: Optional[bool] = False
    presence_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    frequency_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    suffix: Optional[str] = None
    logprobs: Optional[int] = None
    user: Optional[str] = None

    @field_validator("prompt")
    @classmethod
    def prompt_ok(cls, v):
        if isinstance(v, list) and not v:
            raise ValueError("prompt list must not be empty")
        return v


def _normalize_stop(stop) -> Optional[List[str]]:
    if stop is None:
        return None
    if isinstance(stop, str):
        return [stop]
    return list(stop)[:4]


def _generate_completion_text(prompt: str, max_tokens: int, temperature: float,
                              top_p: float, top_k: int, stop: Optional[List[str]]) -> Dict[str, Any]:
    try:
        import api as api_mod
        if getattr(api_mod, "MODEL_LOADED", False) and api_mod.MODEL is not None and api_mod.TOK is not None:
            import numpy as np
            from sampling import sample_next_token, find_stop_sequence
            from agents import stable_seed

            ids = api_mod.TOK.encode(prompt, add_bos=False, add_eos=False)
            rng = np.random.default_rng(stable_seed(prompt))
            emitted = ""
            finish = "length"
            for _ in range(max_tokens):
                x = np.array(ids[-api_mod.MODEL.max_seq_len :])[None, :]
                logits = api_mod.MODEL(x)
                next_id = sample_next_token(
                    logits.data[-1],
                    recent_ids=ids[-16:],
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k or 0,
                    repetition_penalty=1.3,
                    rng=rng,
                )
                if next_id == getattr(api_mod.TOK, "EOS", -1):
                    finish = "stop"
                    break
                ids.append(next_id)
                piece = api_mod.TOK.decode([next_id])
                emitted += piece
                if stop and find_stop_sequence(emitted, stop) != -1:
                    finish = "stop"
                    break
            return {
                "text": emitted,
                "finish_reason": finish,
                "prompt_tokens": len(api_mod.TOK.encode(prompt, add_bos=False, add_eos=False)),
                "completion_tokens": max(0, len(ids) - len(api_mod.TOK.encode(prompt, add_bos=False, add_eos=False))),
            }
    except Exception:
        pass

    try:
        import api as api_mod
        result = api_mod.ORCH.handle(prompt, history=[])
        text = result.get("content", str(result))
        return {
            "text": text,
            "finish_reason": "stop",
            "prompt_tokens": _estimate_tokens(prompt),
            "completion_tokens": _estimate_tokens(text),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"completion failed: {e}")


@router.post("/v1/completions")
def create_completion(req: CompletionsRequest):
    prompts = req.prompt if isinstance(req.prompt, list) else [req.prompt]
    stop = _normalize_stop(req.stop)
    n = req.n or 1

    if req.stream:
        prompt = prompts[0]

        def event_stream():
            cid = f"cmpl-{uuid.uuid4().hex[:12]}"
            result = _generate_completion_text(
                prompt, req.max_tokens or 40, req.temperature or 0.8,
                req.top_p or 0.9, req.top_k or 0, stop,
            )
            text = result["text"]
            if req.echo:
                text = prompt + text
            chunk_size = max(1, len(text) // 8) or 1
            for i in range(0, len(text), chunk_size):
                piece = text[i : i + chunk_size]
                payload = {
                    "id": cid,
                    "object": "text_completion",
                    "created": int(time.time()),
                    "model": req.model,
                    "choices": [{
                        "text": piece,
                        "index": 0,
                        "logprobs": None,
                        "finish_reason": None,
                    }],
                }
                yield f"data: {__import__('json').dumps(payload)}\n\n"
            final = {
                "id": cid,
                "object": "text_completion",
                "created": int(time.time()),
                "model": req.model,
                "choices": [{
                    "text": "",
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": result["finish_reason"],
                }],
                "usage": _usage(result["prompt_tokens"], result["completion_tokens"]),
            }
            yield f"data: {__import__('json').dumps(final)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    choices = []
    total_prompt = 0
    total_completion = 0
    for pi, prompt in enumerate(prompts):
        for ni in range(n):
            result = _generate_completion_text(
                prompt, req.max_tokens or 40, req.temperature or 0.8,
                req.top_p or 0.9, req.top_k or 0, stop,
            )
            text = result["text"]
            if req.echo:
                text = prompt + text
            choices.append({
                "text": text,
                "index": pi * n + ni,
                "logprobs": None,
                "finish_reason": result["finish_reason"],
            })
            total_prompt += result["prompt_tokens"]
            total_completion += result["completion_tokens"]

    return {
        "id": f"cmpl-{uuid.uuid4().hex[:12]}",
        "object": "text_completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": choices,
        "usage": _usage(total_prompt, total_completion),
    }


class EmbeddingsRequest(BaseModel):
    model: str = "text-embedding-orbit-hash"
    input: Union[str, List[str]]
    encoding_format: Optional[str] = "float"
    user: Optional[str] = None
    dimensions: Optional[int] = Field(default=None, ge=8, le=4096)

    @field_validator("input")
    @classmethod
    def input_ok(cls, v):
        if isinstance(v, list) and len(v) == 0:
            raise ValueError("input must not be empty")
        if isinstance(v, str) and len(v) == 0:
            raise ValueError("input must not be empty")
        return v


@router.post("/v1/embeddings")
def create_embeddings(req: EmbeddingsRequest):
    try:
        from memory_store import hash_embed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"embedding backend unavailable: {e}")

    texts = req.input if isinstance(req.input, list) else [req.input]
    if len(texts) > 128:
        raise HTTPException(status_code=400, detail="max 128 inputs per request")

    dim = req.dimensions or 256
    data = []
    total_tokens = 0
    for i, text in enumerate(texts):
        vec = hash_embed(text, dim=dim)
        data.append({
            "object": "embedding",
            "embedding": vec.tolist(),
            "index": i,
        })
        total_tokens += _estimate_tokens(text)

    return {
        "object": "list",
        "data": data,
        "model": req.model,
        "usage": {
            "prompt_tokens": total_tokens,
            "total_tokens": total_tokens,
        },
    }
