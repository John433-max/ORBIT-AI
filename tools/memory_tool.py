"""Memory tools — add and search conversation/long-term memory."""

from __future__ import annotations

from tools.base import BaseTool, ToolResult

_SHARED_MM = None


def _mm():
    global _SHARED_MM
    if _SHARED_MM is None:
        from memory import MemoryManager
        try:
            _SHARED_MM = MemoryManager(backend="sqlite", sqlite_path="orbit_memory.db")
        except Exception:
            _SHARED_MM = MemoryManager(backend="memory")
    return _SHARED_MM


class MemoryAddTool(BaseTool):
    name = "memory.add"
    description = "Store a short text fact in long-term memory."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Fact or note to remember"},
            "importance": {"type": "number", "default": 0.5},
        },
        "required": ["text"],
    }
    timeout_s = 5.0

    def __init__(self, store=None):
        self.store = store

    def execute(self, text: str = "", importance: float = 0.5, metadata=None, **_) -> ToolResult:
        text = (text or "").strip()
        if not text:
            return ToolResult(ok=False, content="", error="text is required")
        try:
            meta = dict(metadata or {})
            if importance is not None:
                meta.setdefault("importance", float(importance))
            if self.store is not None and hasattr(self.store, "add"):
                mid = self.store.add(text, metadata=meta or None, importance=float(importance or 0.5))
            else:
                mm = _mm()
                mid = mm.add_memory(text, metadata=meta)
            return ToolResult(
                ok=True,
                content=f"Stored memory id={mid}: {text[:120]}",
                data={"id": mid, "text": text},
            )
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))


class MemorySearchTool(BaseTool):
    name = "memory.search"
    description = "Search long-term memory for relevant notes."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "top_k": {"type": "integer", "default": 5},
        },
        "required": ["query"],
    }
    timeout_s = 5.0

    def __init__(self, store=None):
        self.store = store

    def execute(self, query: str = "", top_k: int = 5, **_) -> ToolResult:
        query = (query or "").strip()
        if not query:
            return ToolResult(ok=False, content="", error="query is required")
        try:
            k = int(top_k or 5)
            if self.store is not None and hasattr(self.store, "query"):
                hits = self.store.query(query, k=k) or []
            else:
                hits = _mm().search_memory(query, top_k=k)
            if not hits:
                return ToolResult(ok=True, content="No matching memories.", data=[])
            lines = []
            for h in hits:
                score = h.get("score")
                text = h.get("text", "")
                if score is not None:
                    try:
                        lines.append(f"- (score={float(score):.3f}) {text}")
                    except (TypeError, ValueError):
                        lines.append(f"- {text}")
                else:
                    lines.append(f"- {text}")
            return ToolResult(ok=True, content="\n".join(lines), data=hits)
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))
