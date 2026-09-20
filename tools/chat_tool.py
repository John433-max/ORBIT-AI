"""Persona retrieval + optional generation for MainChatAgent.

Retrieval-first chat is the documented quality path. Generation is opt-in
and quality-gated by MainChatAgent. TinyLM decode is imported lazily so a
sparse GitHub checkout (no tinylm.generate / torch) still imports this module.
"""

from __future__ import annotations

from tools.base import BaseTool, ToolResult


def query_persona(store, query: str, top_k: int = 3, threshold: float = 0.42):
    """Search a VectorStore of persona Q/A rows."""
    query = (query or "").strip()
    k = max(1, int(top_k or 3))
    if store is None or not query or not hasattr(store, "query"):
        return {
            "ok": True,
            "matched": False,
            "score": 0.0,
            "answer": None,
            "hits": [],
            "query": query,
        }
    raw_hits = store.query(query, k=k) or []
    hits = []
    for h in raw_hits:
        meta = h.get("metadata") or {}
        hits.append(
            {
                "score": float(h.get("score") or 0.0),
                "text": h.get("text") or "",
                "answer": meta.get("answer"),
            }
        )
    best = hits[0] if hits else None
    score = float(best["score"]) if best else 0.0
    matched = bool(best and best.get("answer") and score >= float(threshold))
    return {
        "ok": True,
        "matched": matched,
        "score": score,
        "answer": best.get("answer") if matched else None,
        "hits": hits,
        "query": query,
        "threshold": float(threshold),
    }


class ChatRetrieveTool(BaseTool):
    name = "chat.retrieve"
    description = "Retrieve a persona-KB answer for a user chat turn."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "User message to match"},
            "top_k": {"type": "integer", "default": 3},
            "threshold": {"type": "number", "default": 0.42},
        },
        "required": ["query"],
    }
    timeout_s = 5.0

    def __init__(self, store=None):
        self.store = store

    def execute(
        self,
        query: str = "",
        top_k: int = 3,
        threshold: float = 0.42,
        **_,
    ) -> ToolResult:
        query = (query or "").strip()
        if not query:
            return ToolResult(ok=False, content="", error="query is required")
        data = query_persona(self.store, query, top_k=top_k, threshold=threshold)
        if data.get("matched"):
            content = data["answer"] or ""
        elif data.get("hits"):
            content = f"No persona match above threshold (best={data['score']:.3f})."
        else:
            content = "Persona knowledge base is empty or unmatched."
        return ToolResult(ok=True, content=content, data=data)


PERSONA_PREAMBLE = (
    "You are ORBIT \u2014 a sharp, helpful AI that runs locally. Speak in the first "
    "person as yourself. Be clear, concise, and a little dry; prefer substance "
    "over filler. Use tools for math, science, memory, documents, and code. "
    "Never invent capabilities you lack. If unsure, say so and suggest a better angle.\n"
)


def resolve_generate_backend(backend, model=None, tokenizer=None) -> str:
    chosen = (backend or "auto").strip().lower()
    if chosen in ("tinylm", "tiny"):
        return "tinylm"
    if chosen in ("legacy", "orbit"):
        return "legacy"
    if model is not None and tokenizer is not None:
        return "legacy"
    return "tinylm"


def generate_chat(
    model,
    tokenizer,
    request: str,
    history=None,
    max_tokens: int = 40,
    temperature: float = 0.7,
    preamble: str = PERSONA_PREAMBLE,
    backend: str = "auto",
    use_cache: bool = True,
    tinylm_preset: str = "rope",
    tinylm_model=None,
    ckpt_path: str = None,
) -> dict:
    request = (request or "").strip()
    if not request:
        return {"ok": False, "text": "", "error": "request is required", "n_new": 0}
    backend = resolve_generate_backend(backend, model=model, tokenizer=tokenizer)
    if backend in ("tinylm", "tiny"):
        return {
            "ok": True,
            "text": "(no model loaded)",
            "error": None,
            "n_new": 0,
            "loaded": False,
            "backend": "tinylm",
            "note": "Full TinyLM decode lives in the local tree; GitHub module is retrieval-first.",
        }
    return {
        "ok": True,
        "text": "(no model loaded)",
        "error": None,
        "n_new": 0,
        "loaded": False,
        "backend": "legacy",
    }


class ChatGenerateTool(BaseTool):
    name = "chat.generate"
    description = (
        "Run the toy MainChat decoder on a user turn. Quality is not guaranteed."
    )
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "request": {"type": "string", "description": "User message"},
            "max_tokens": {"type": "integer", "default": 40},
            "temperature": {"type": "number", "default": 0.7},
            "backend": {"type": "string", "default": "auto"},
        },
        "required": ["request"],
    }
    timeout_s = 30.0

    def __init__(
        self,
        model=None,
        tokenizer=None,
        max_tokens=40,
        temperature=0.7,
        backend="auto",
        tinylm_preset="rope",
        tinylm_model=None,
        ckpt_path=None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.backend = backend or "auto"
        self.tinylm_preset = tinylm_preset
        self.tinylm_model = tinylm_model
        self.ckpt_path = ckpt_path
        self._tinylm_factory = None

    def bind_tinylm(self, model=None, factory=None, preset=None, backend=None):
        if preset is not None:
            self.tinylm_preset = preset
        if backend is not None:
            self.backend = backend
        if factory is not None:
            self._tinylm_factory = factory
        if model is not None:
            self.tinylm_model = model
        return self.tinylm_model

    def ensure_tinylm(self):
        if self.tinylm_model is not None:
            return self.tinylm_model
        if self._tinylm_factory is not None:
            self.tinylm_model = self._tinylm_factory()
            return self.tinylm_model
        return self.tinylm_model

    def execute(
        self,
        request: str = "",
        max_tokens: int = None,
        temperature: float = None,
        history=None,
        backend: str = None,
        use_cache: bool = True,
        **_,
    ) -> ToolResult:
        request = (request or "").strip()
        if not request:
            return ToolResult(ok=False, content="", error="request is required")
        chosen = (backend if backend is not None else self.backend) or "auto"
        resolved = resolve_generate_backend(chosen, model=self.model, tokenizer=self.tokenizer)
        data = generate_chat(
            self.model,
            self.tokenizer,
            request,
            history=history,
            max_tokens=max_tokens if max_tokens is not None else self.max_tokens,
            temperature=temperature if temperature is not None else self.temperature,
            backend=resolved,
            use_cache=use_cache,
            tinylm_preset=self.tinylm_preset,
            tinylm_model=self.tinylm_model,
            ckpt_path=self.ckpt_path,
        )
        if not data.get("ok"):
            return ToolResult(
                ok=False,
                content="",
                error=data.get("error") or "generate failed",
                data=data,
            )
        return ToolResult(ok=True, content=data.get("text") or "", data=data)
