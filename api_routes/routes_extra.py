"""
Extra modular API routes (ORBIT v2).

Mounted from api.py without removing existing endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from api_routes.schemas import (
    GenerateRequest,
    EmbedRequest,
    MemorySearchRequest,
    RAGQueryRequest,
    AgentRunRequest,
)

router = APIRouter(tags=["orbit-v2"])


@router.get("/v2/health")
def v2_health():
    return {"ok": True, "api": "orbit-v2"}


@router.post("/v2/generate")
def v2_generate(req: GenerateRequest):
    try:
        from bpe_tokenizer import BPETokenizer
        from model import TinyLM, get_preset
        from model.generation import generate
        from pathlib import Path

        tok_path = Path("bpe_tokenizer.json")
        if not tok_path.exists():
            raise HTTPException(400, "Tokenizer not found; run train.py first")
        tok = BPETokenizer.load(str(tok_path))
        cfg = get_preset("tiny")
        model = TinyLM.from_config(cfg.model, vocab_size=tok.VOCAB_SIZE)
        ckpt = Path("checkpoint_base.npz")
        if ckpt.exists():
            from train import load_into
            load_into(model, str(ckpt))
        text = generate(
            model, tok, req.prompt,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
            top_k=req.top_k,
            repetition_penalty=req.repetition_penalty,
            seed=req.seed,
        )
        return {"text": text, "model": "orbit-toy"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/v2/embed")
def v2_embed(req: EmbedRequest):
    try:
        from memory_store import hash_embed
        import numpy as np
        vec = hash_embed(req.input, dim=256)
        return {
            "object": "list",
            "data": [{"object": "embedding", "embedding": vec.tolist(), "index": 0}],
            "model": req.model,
            "dim": 256,
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/v2/memory/search")
def v2_memory_search(req: MemorySearchRequest):
    try:
        from memory import MemoryManager
        mm = MemoryManager()
        hits = mm.search_memory(req.query, top_k=req.top_k)
        return {"hits": hits}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/v2/rag/query")
def v2_rag_query(req: RAGQueryRequest):
    try:
        from rag import RAGPipeline
        pipe = RAGPipeline()
        ans = pipe.query(req.question, top_k=req.top_k)
        return ans.to_dict()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/v2/agent/run")
def v2_agent_run(req: AgentRunRequest):
    try:
        from agent import ToolCallingAgent
        agent = ToolCallingAgent(
            permission_level=req.permission_level,
            max_iterations=req.max_iterations,
        )
        return agent.run(req.message)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/v2/tools")
def v2_list_tools(permission_level: str = "SAFE"):
    """List tools in OpenAI function-calling schema format."""
    try:
        from tools import default_registry
        reg = default_registry(permission_level=permission_level)
        return {
            "tools": reg.openai_tools(),
            "permission_level": permission_level,
            "count": len(reg.openai_tools()),
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/v2/search")
def v2_search(body: dict):
    """Live web search (DuckDuckGo) with structured results."""
    try:
        from tools import default_registry, ToolCall
        query = (body.get("query") or "").strip()
        max_results = int(body.get("max_results") or 5)
        if not query:
            raise HTTPException(400, "query is required")
        reg = default_registry("SAFE")
        result = reg.execute(
            ToolCall(tool="web.search", arguments={"query": query, "max_results": max_results})
        )
        return {
            "ok": result.ok,
            "content": result.content,
            "results": result.data,
            "error": result.error,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))
