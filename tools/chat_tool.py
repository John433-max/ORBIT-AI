"""Persona retrieval + optional generation for MainChatAgent.

Retrieval-first chat is the documented quality path for the toy model.
Generation is opt-in; this module's retrieve path has no TinyLM dependency
so unit tests collect without torch.
"""

from __future__ import annotations

from tools.base import BaseTool, ToolResult


def query_persona(store, query: str, top_k: int = 3, threshold: float = 0.42):
    """Search a VectorStore of persona Q/A rows.

    Returns a dict with hits, best match, and whether it clears `threshold`.
    """
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


class ChatGenerateTool(BaseTool):
    """Legacy/stub generate path used when TinyLM is not bound."""

    name = "chat.generate"
    description = "Generate a short chat reply (stub unless TinyLM is bound)."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "prompt": {"type": "string"},
            "max_new_tokens": {"type": "integer", "default": 24},
        },
        "required": ["prompt"],
    }
    timeout_s = 30.0

    def __init__(self, generate_fn=None):
        self.generate_fn = generate_fn

    def execute(self, prompt: str = "", max_new_tokens: int = 24, **_) -> ToolResult:
        prompt = (prompt or "").strip()
        if not prompt:
            return ToolResult(ok=False, content="", error="prompt is required")
        if self.generate_fn is not None:
            text = self.generate_fn(prompt, max_new_tokens=max_new_tokens)
            return ToolResult(ok=True, content=str(text or ""), data={"backend": "bound"})
        return ToolResult(
            ok=True,
            content="I'm here. Ask me to calculate, search, run code, or work with a document.",
            data={"backend": "legacy"},
        )
