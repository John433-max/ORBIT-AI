"""
OpenAI-compatible chatbot API (spec Part 15), wired to:
- the agent orchestrator (agents.py) — handles ALL response content now,
  including plain chat (retrieval-first against ORBIT's persona knowledge
  base, honest hedge on miss — see agents.py's MainChatAgent docstring for
  why raw token generation isn't the primary path anymore)
- the memory store (memory_store.py, exposed for inspect/export/delete per
  Part 11's requirement that the user can manage their own memory)

Run: uvicorn api:app --reload --port 8000
Then: curl -N -X POST localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"orbit-toy","messages":[{"role":"user","content":"what is your name"}],"stream":true}'
"""
import json
import time
import uuid
import base64
import logging
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import StreamingResponse, JSONResponse, Response
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

from bpe_tokenizer import BPETokenizer
from model import TinyLM
from agents import Orchestrator
from sampling import sample_next_token, find_stop_sequence

logger = logging.getLogger("orbit.api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ORBIT AI — Local AI Agent Runtime API")

# Optional API key: set ORBIT_API_KEY to require Authorization: Bearer <key>
# or header X-API-Key. Default unset = open on bind host (use 127.0.0.1).
import os as _os
_ORBIT_API_KEY = (_os.environ.get("ORBIT_API_KEY") or "").strip()
if _ORBIT_API_KEY:
    from fastapi import Request as _Request
    from fastapi.responses import JSONResponse as _JSONResponse

    @app.middleware("http")
    async def _api_key_gate(request: _Request, call_next):
        if request.url.path in ("/health", "/healthz", "/", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)
        auth = request.headers.get("authorization") or ""
        xkey = request.headers.get("x-api-key") or ""
        token = ""
        if auth.lower().startswith("bearer "):
            token = auth[7:].strip()
        elif xkey:
            token = xkey.strip()
        if token != _ORBIT_API_KEY:
            return _JSONResponse({"error": "unauthorized"}, status_code=401)
        return await call_next(request)


@app.exception_handler(RequestValidationError)
async def safe_validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for a real crash found while fuzzing: FastAPI's default
    RequestValidationError handler echoes the rejected input value back
    into the error detail (helpful for debugging), then hands it to
    Starlette's JSONResponse, which serializes with
    json.dumps(..., ensure_ascii=False) and then .encode("utf-8") with no
    errors= argument. If the rejected input itself is the kind of value
    pydantic correctly rejects -- e.g. a string containing an unpaired
    UTF-16 surrogate, which pydantic-core validates against but which
    cannot be represented in UTF-8 at all -- that final .encode("utf-8")
    crashes with UnicodeEncodeError. So a request that should cleanly get
    a 422 instead crashes the framework's own error-reporting path with an
    unhandled 500. Verified directly with a raw JSON body containing an
    unpaired surrogate escape sequence, against the *default* handler.

    Fix: run errors through jsonable_encoder() (the same utility FastAPI's
    own default handler uses -- needed because a custom field_validator
    that raises ValueError, e.g. ChatMessage's role validator, embeds the
    raw exception object in pydantic's error context, and plain
    json.dumps() alone can't serialize that), then serialize the result
    with json.dumps(..., ensure_ascii=True) ourselves. ensure_ascii=True
    forces every non-ASCII character -- valid or not -- into a uXXXX
    escape sequence in the output text, which is then trivially safe to
    encode as plain ASCII bytes. Returning a plain Response with that
    pre-encoded body bypasses JSONResponse.render()'s less defensive
    encoding path entirely.
    """
    from fastapi.encoders import jsonable_encoder
    try:
        detail = jsonable_encoder(exc.errors())
    except Exception:
        detail = [{"msg": "request validation failed and the error detail itself "
                           "could not be serialized"}]
    body = json.dumps({"detail": detail}, ensure_ascii=True).encode("ascii")
    return Response(content=body, status_code=422, media_type="application/json")


# Model/tokenizer selection: prefer a checkpoint produced by train_large.py
# (bigger, trained on more real text) if one exists, falling back to
# train.py's default small checkpoint, falling back further to an untrained
# model + byte-level tokenizer if neither exists yet. Each (tokenizer,
# checkpoint) pair is tried as a matched set -- never mixing a tokenizer
# from one training run with a checkpoint from another, since vocab size
# (and therefore embedding table shape) has to match exactly. The actual
# model architecture is read from the checkpoint's own .json metadata via
# build_model_from_checkpoint (train.py), not hardcoded here -- this is
# the fix for a real bug where this file used to hardcode d_model=64 etc.
# regardless of which checkpoint was actually present, which would either
# silently misload a differently-shaped checkpoint or just never notice a
# bigger trained model sitting right next to it.
from train import build_model_from_checkpoint

CANDIDATE_RUNS = [
    ("bpe_tokenizer_large.json", "checkpoint_large.npz"),
    ("bpe_tokenizer.json", "checkpoint_base.npz"),
]

MODEL = None
TOK = None
MODEL_LOADED = False
TOKENIZER_LOADED = False
ACTIVE_CHECKPOINT = None

for tok_path, ckpt_path in CANDIDATE_RUNS:
    try:
        candidate_tok = BPETokenizer.load(tok_path)
    except FileNotFoundError:
        continue
    try:
        candidate_model, ckpt_meta = build_model_from_checkpoint(ckpt_path)
    except FileNotFoundError:
        continue
    except ValueError as e:
        logger.warning("found %s + %s but they don't match: %s", tok_path, ckpt_path, e)
        continue
    if candidate_model.vocab_size != candidate_tok.VOCAB_SIZE:
        logger.warning("skipping %s + %s: tokenizer vocab_size=%d but checkpoint vocab_size=%d",
                        tok_path, ckpt_path, candidate_tok.VOCAB_SIZE, candidate_model.vocab_size)
        continue
    TOK, MODEL, MODEL_LOADED, TOKENIZER_LOADED = candidate_tok, candidate_model, True, True
    ACTIVE_CHECKPOINT = ckpt_path
    logger.info("loaded %s + %s (%s params, val_ppl=%.1f)",
                tok_path, ckpt_path, f"{ckpt_meta.get('n_params', '?'):,}" if isinstance(ckpt_meta.get('n_params'), int) else '?',
                ckpt_meta.get("val_ppl", float("nan")))
    break

if TOK is None:
    # Nothing trained yet at all: fall back to the always-available
    # byte-level tokenizer and an untrained model, so the API can still
    # start (health checks, /v1/models, memory/document endpoints all work)
    # -- chat just falls back to the honest hedge path instead of real
    # generation. See MainChatAgent in agents.py for that fallback.
    from tokenizer import ByteTokenizer
    from model import get_preset
    TOK = ByteTokenizer()
    _fb = get_preset("development").model
    MODEL = TinyLM(
        vocab_size=TOK.VOCAB_SIZE,
        d_model=_fb.d_model,
        n_layers=_fb.n_layers,
        n_heads=_fb.n_heads,
        n_kv_heads=_fb.n_kv_heads,
        max_seq_len=min(_fb.context_length, 64),
        use_recursive_reasoning=False,
        seed=0,
    )
    logger.warning(
        "no matching (tokenizer, checkpoint) pair found -- falling back to untrained "
        "development preset + ByteTokenizer. Run train.py or train_large.py first."
    )

ORCH = Orchestrator(chat_model=MODEL if MODEL_LOADED else None, chat_tokenizer=TOK)


class ChatMessage(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=8000)

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v):
        if v not in ("system", "user", "assistant", "tool", "function"):
            raise ValueError(f"role must be one of system/user/assistant/tool/function, got {v!r}")
        return v


class ChatCompletionRequest(BaseModel):
    model: str = "orbit-toy"
    messages: List[ChatMessage] = Field(min_length=1, max_length=50)
    stream: Optional[bool] = False
    max_tokens: Optional[int] = Field(default=40, ge=1, le=512)
    temperature: Optional[float] = Field(default=0.8, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=0.9, gt=0.0, le=1.0)
    top_k: Optional[int] = Field(default=0, ge=0)
    stop: Optional[List[str]] = Field(default=None, max_length=4)
    # Optional server-side conversation persistence (Phase 31): when set,
    # prior turns are pulled from ORCH.conversations instead of from
    # `messages` (so a client can send just the newest message rather than
    # resending full history each time), and both the new user message and
    # the assistant's reply are saved under this id for future requests.
    # Omit it for the standard stateless behavior (client resends full
    # history in `messages` every request, nothing persisted server-side).
    conversation_id: Optional[str] = Field(default=None, min_length=1, max_length=200)

    @field_validator("messages")
    @classmethod
    def messages_not_empty(cls, v):
        if not v:
            raise ValueError("messages must not be empty")
        return v


class MemoryAddRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4096)
    importance: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    ttl_seconds: Optional[float] = Field(default=None, gt=0)


class MemoryUpdateRequest(BaseModel):
    text: Optional[str] = Field(default=None, min_length=1, max_length=4096)
    importance: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    ttl_seconds: Optional[float] = Field(default=None, gt=0)


class DocumentUploadRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    # base64 inflates size by ~4/3, so this caps raw document size at
    # roughly 10MB -- documents.py's DocumentStore.search() re-embeds every
    # chunk of every stored document on every query (no persistent vector
    # index), so upload size directly drives per-query cost; an unbounded
    # upload endpoint was a real, uncapped DoS vector before this.
    content_base64: str = Field(min_length=1, max_length=14_000_000)


@app.get("/v1/models")
def list_models():
    """OpenAI-compatible model list."""
    created = 1720000000
    data = [
        {
            "id": "orbit-toy",
            "object": "model",
            "created": created,
            "owned_by": "orbit",
            "permission": [],
            "root": "orbit-toy",
            "parent": None,
        },
        {
            "id": "orbit-tiny",
            "object": "model",
            "created": created,
            "owned_by": "orbit",
            "permission": [],
            "root": "orbit-tiny",
            "parent": None,
        },
        {
            "id": "text-embedding-orbit-hash",
            "object": "model",
            "created": created,
            "owned_by": "orbit",
            "permission": [],
            "root": "text-embedding-orbit-hash",
            "parent": None,
        },
    ]
    return {"object": "list", "data": data}


@app.post("/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    # Find the LAST user message by index (not just by content) so history
    # is captured correctly even if two messages happen to share the same
    # text. Historically this only ever extracted that single message and
    # discarded everything else in `req.messages` -- see Orchestrator.handle's
    # docstring for why that was a real bug, not a deliberate simplification.
    last_user_idx = None
    for i in range(len(req.messages) - 1, -1, -1):
        if req.messages[i].role == "user":
            last_user_idx = i
            break
    last_user = req.messages[last_user_idx].content if last_user_idx is not None else ""
    if not last_user.strip():
        raise HTTPException(status_code=400, detail="no user message found in `messages`")

    if req.conversation_id:
        # Stateful mode: server-stored history takes precedence over
        # whatever else is in `messages` (the client is expected to just
        # send the newest turn in this mode -- mixing both stateless and
        # stateful history in one request would be ambiguous about which
        # wins, so this makes the precedence explicit rather than silently
        # picking one).
        history = ORCH.conversations.get_recent(req.conversation_id, limit=20)
    else:
        history = [{"role": m.role, "content": m.content} for m in req.messages[:last_user_idx]]

    logger.info("chat_completions request: %d messages, stream=%s", len(req.messages), req.stream)
    try:
        agent_result = ORCH.handle(last_user, history=history)
    except Exception as e:
        logger.exception("orchestrator failed handling request")
        raise HTTPException(status_code=500, detail=f"internal agent error: {e}")

    prefix = ""  # Cycle 54: ORBIT speaks in one voice; no [agent] brackets
    content = agent_result["content"]
    is_raw_generation = agent_result["agent"] == "main_chat_agent" and not agent_result["ok"]
    will_stream_real_generation = req.stream and is_raw_generation and MODEL_LOADED

    if req.conversation_id and not will_stream_real_generation:
        # Safe to save immediately here: `content` is accurate for the
        # non-streaming case and for the precomputed-streaming case (the
        # response is already fully resolved either way). For the
        # will_stream_real_generation case, saving happens instead inside
        # _sse_stream_real_generation once the actual stream completes --
        # `content` here comes from a SEPARATE internal generation
        # (ORCH.handle()'s own call into MainChatAgent) that isn't
        # guaranteed to match what gets streamed to the client, so saving
        # it here would risk persisting text the user never actually saw.
        ORCH.conversations.add_message(req.conversation_id, "user", last_user)
        ORCH.conversations.add_message(req.conversation_id, "assistant", content)

    if req.stream:
        if will_stream_real_generation:
            # This is the one path where content is actually produced by the
            # LM token-by-token, so this streams real generation instead of
            # chunking an already-finished string (see api.py module
            # docstring / DESIGN.md Part 15 on why the old version didn't).
            return StreamingResponse(
                _sse_stream_real_generation(req, prefix, last_user, history, req.conversation_id),
                media_type="text/event-stream")
        # For retrieval/tool-agent paths the content is genuinely already
        # fully resolved (not generated token-by-token by an LM at all), so
        # it's sent as a single SSE chunk rather than artificially split up
        # to look like live generation it isn't.
        return StreamingResponse(_sse_stream_precomputed(req, content), media_type="text/event-stream")
    return _respond(req, content)


def _respond(req: ChatCompletionRequest, content: str):
    # Approximate token usage for OpenAI client compatibility
    prompt_txt = " ".join(m.content for m in req.messages)
    pt = max(1, len(prompt_txt.split()) + len(prompt_txt) // 8)
    ct = max(1, len(content.split()) + len(content) // 8)
    return JSONResponse({
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": content},
            "finish_reason": "stop",
            "logprobs": None,
        }],
        "usage": {
            "prompt_tokens": pt,
            "completion_tokens": ct,
            "total_tokens": pt + ct,
        },
        "system_fingerprint": "orbit_v2",
    })


def _sse_chunk(completion_id, req, delta, finish_reason=None):
    payload = {
        "id": completion_id, "object": "chat.completion.chunk", "created": int(time.time()),
        "model": req.model,
        "choices": [{"index": 0, "delta": delta, "finish_reason": finish_reason}],
    }
    return f"data: {json.dumps(payload)}\n\n"


def _sse_stream_precomputed(req: ChatCompletionRequest, content: str):
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    yield _sse_chunk(completion_id, req, {"role": "assistant", "content": content})
    yield _sse_chunk(completion_id, req, {}, finish_reason="stop")
    yield "data: [DONE]\n\n"


def _sse_stream_real_generation(req: ChatCompletionRequest, prefix: str, user_text: str, history: list = None,
                                 conversation_id: str = None):
    """Actual token-by-token generation and streaming: generate one token,
    send it, generate the next — not a completed string chopped into pieces.
    Stops on max_tokens, a stop sequence, or EOS."""
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    if prefix:
        yield _sse_chunk(completion_id, req, {"role": "assistant", "content": prefix})

    persona_preamble = (
        "You are ORBIT, a small toy-scale prototype model. You are direct, "
        "a little dry, and upfront about being small and untrained on real data.\n"
    )
    history_lines = "".join(f"{h.get('role', 'user')}: {h.get('content', '')}\n" for h in (history or []))
    prompt = persona_preamble + history_lines + f"user: {user_text}\nassistant:"
    ids = TOK.encode(prompt, add_bos=False, add_eos=False)
    # Seeded deterministically (same stable_seed() used by
    # MainChatAgent._generate_raw in agents.py), not left as an unseeded
    # RNG -- found while wiring up conversation persistence: ORCH.handle()
    # already runs its own internal generation (deterministically seeded)
    # to build the hedge/fallback text, and this function runs a SEPARATE
    # generation for what's actually streamed to the client. With two
    # different RNG states, those two generations would produce different
    # text -- meaning whatever got saved to conversation history wouldn't
    # match what the user actually saw streamed. Same seed source removes
    # the mismatch (both generations become identical given the same
    # prompt/history, matching this project's existing
    # same-input-same-output convention -- see stable_seed's own docstring
    # in agents.py for why that property matters here).
    from agents import stable_seed
    rng = np.random.default_rng(stable_seed(user_text))
    emitted = ""
    finish_reason = "length"
    for _ in range(req.max_tokens):
        x = np.array(ids[-MODEL.max_seq_len:])[None, :]
        logits = MODEL(x)
        next_id = sample_next_token(logits.data[-1], recent_ids=ids[-16:], temperature=req.temperature,
                                     top_p=req.top_p, top_k=req.top_k, repetition_penalty=1.3, rng=rng)
        if next_id == TOK.EOS:
            finish_reason = "stop"
            break
        ids.append(next_id)
        piece = TOK.decode([next_id])
        emitted += piece
        cut = find_stop_sequence(emitted, req.stop) if req.stop else -1
        if cut != -1:
            finish_reason = "stop"
            break
        yield _sse_chunk(completion_id, req, {"content": piece})
    yield _sse_chunk(completion_id, req, {}, finish_reason=finish_reason)
    if conversation_id:
        # Save the ACTUALLY-EMITTED text, not whatever ORCH.handle()
        # separately computed for the non-streaming hedge/fallback path --
        # those are genuinely different generations (different call site,
        # different RNG state, different sampling params), so persisting
        # the other one would save text the user never actually saw.
        ORCH.conversations.add_message(conversation_id, "user", user_text)
        ORCH.conversations.add_message(conversation_id, "assistant", prefix + emitted)
    yield "data: [DONE]\n\n"


@app.get("/v1/memory")
def list_memory():
    return {"items": ORCH.store.export()}


@app.post("/v1/memory")
def add_memory(req: MemoryAddRequest):
    item_id = ORCH.store.add(req.text, importance=req.importance, ttl_seconds=req.ttl_seconds)
    return {"id": item_id, "stored": True}


@app.delete("/v1/memory/{item_id}")
def delete_memory(item_id: int):
    ok = ORCH.store.delete(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"memory item {item_id} not found")
    return {"deleted": ok}


@app.put("/v1/memory/{item_id}")
def update_memory(item_id: int, req: MemoryUpdateRequest):
    if req.text is None and req.importance is None and req.ttl_seconds is None:
        raise HTTPException(status_code=400, detail="provide at least one of text/importance/ttl_seconds")
    ok = ORCH.store.update(item_id, text=req.text, importance=req.importance, ttl_seconds=req.ttl_seconds)
    if not ok:
        raise HTTPException(status_code=404, detail=f"memory item {item_id} not found")
    return {"updated": True, "id": item_id}


@app.post("/v1/documents")
def upload_document(req: DocumentUploadRequest):
    try:
        raw_bytes = base64.b64decode(req.content_base64, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="content_base64 is not valid base64")
    try:
        info = ORCH.documents.add_document(req.filename, raw_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return info


@app.get("/v1/documents")
def list_documents():
    return {"documents": ORCH.documents.list_documents()}


@app.delete("/v1/documents/{document_id}")
def delete_document(document_id: int):
    ok = ORCH.documents.delete_document(document_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"document {document_id} not found")
    return {"deleted": ok}


@app.get("/v1/conversations")
def list_conversations():
    return {"conversations": ORCH.conversations.list_conversations()}


@app.get("/v1/conversations/{conversation_id}")
def get_conversation(conversation_id: str, limit: int = 50):
    messages = ORCH.conversations.get_recent(conversation_id, limit=min(max(limit, 1), 500))
    if not messages:
        raise HTTPException(status_code=404, detail=f"no conversation found with id {conversation_id!r}")
    return {"conversation_id": conversation_id, "messages": messages}


@app.delete("/v1/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    n = ORCH.conversations.delete_conversation(conversation_id)
    if n == 0:
        raise HTTPException(status_code=404, detail=f"no conversation found with id {conversation_id!r}")
    return {"deleted": True, "messages_removed": n}


@app.get("/v1/conversations/{conversation_id}/export")
def export_conversation(conversation_id: str, format: str = "json"):
    if format not in ("json", "txt", "md", "markdown"):
        raise HTTPException(status_code=400, detail="format must be one of: json, txt, md")
    if not ORCH.conversations.get_recent(conversation_id, limit=1):
        raise HTTPException(status_code=404, detail=f"no conversation found with id {conversation_id!r}")
    body = ORCH.conversations.export_conversation(conversation_id, fmt=format)
    media_type = {"json": "application/json", "txt": "text/plain",
                  "md": "text/markdown", "markdown": "text/markdown"}[format]
    return Response(content=body, media_type=media_type)


@app.get("/health")
def health():
    agents = list(ORCH.agents.keys()) if ORCH is not None else []
    lab = {}
    try:
        from tinylm import TinyLMConfig
        lab = {"available": True, "modern_params": TinyLMConfig.preset("modern").estimate_parameters()}
    except Exception as e:
        lab = {"available": False, "error": str(e)}
    return {
        "ok": True,
        "product": "ORBIT unified AI",
        "model_loaded": MODEL_LOADED,
        "tokenizer_loaded": TOKENIZER_LOADED,
        "active_checkpoint": ACTIVE_CHECKPOINT,
        "vocab_size": getattr(TOK, "VOCAB_SIZE", None) if TOK is not None else None,
        "model_params": MODEL.param_count() if MODEL is not None and hasattr(MODEL, "param_count") else None,
        "agents": agents,
        "tinylm_lab": lab,
        "webui": True,
        "metrics": ORCH.metrics() if ORCH is not None and hasattr(ORCH, "metrics") else {},
    }


@app.get("/healthz")
def healthz():
    # kept as an alias for backwards compatibility with anything already
    # calling the old path
    return health()


# ---------------------------------------------------------------------------
# Web UI (ORBIT v2 Phase 24)
# ---------------------------------------------------------------------------
from pathlib import Path
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

_WEBUI_DIR = Path(__file__).resolve().parent / "webui"
_STATIC_DIR = Path(__file__).resolve().parent / "static"


@app.get("/", response_class=HTMLResponse)
def webui_root():
    """Serve the ORBIT chat Web UI."""
    index = _WEBUI_DIR / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text(encoding="utf-8"))
    return HTMLResponse(
        "<h1>ORBIT</h1><p>Web UI not found. API is up — try "
        "<a href='/health'>/health</a> or <a href='/docs'>/docs</a>.</p>",
        status_code=200,
    )


@app.get("/ui", response_class=HTMLResponse)
def webui_alias():
    return webui_root()


if _STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")


# ---------------------------------------------------------------------------
# ORBIT v2 modular routes
# ---------------------------------------------------------------------------
try:
    from api_routes.routes_extra import router as v2_router
    app.include_router(v2_router)
except Exception as _v2_exc:  # pragma: no cover
    logging.getLogger("orbit.api").warning("v2 routes not loaded: %s", _v2_exc)

try:
    from api_routes.openai_compat import router as openai_router
    app.include_router(openai_router)
except Exception as _oai_exc:  # pragma: no cover
    logging.getLogger("orbit.api").warning("openai compat routes not loaded: %s", _oai_exc)
