"""Filesystem tool — sandboxed read (and optional limited write)."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from tools.base import BaseTool, ToolResult


class FilesystemTool(BaseTool):
    name = "filesystem.read"
    description = "Read a text file from an allowed path."
    permission_level = "WRITE"
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Relative or absolute path"},
            "max_bytes": {"type": "integer", "description": "Max bytes to return", "default": 65536},
        },
        "required": ["path"],
    }
    timeout_s = 10.0

    def __init__(self, allowed_roots: Optional[List[str]] = None):
        self.allowed_roots = [Path(p).resolve() for p in (allowed_roots or ["."])]

    def _is_allowed(self, path: Path) -> bool:
        try:
            resolved = path.resolve()
            return any(str(resolved).startswith(str(root)) for root in self.allowed_roots)
        except Exception:
            return False

    def execute(self, path: str = "", max_bytes: int = 65536, **_) -> ToolResult:
        try:
            from tools_legacy import read_sandboxed_file
            raw = read_sandboxed_file(path)
            if isinstance(raw, dict):
                if not raw.get("ok", True):
                    return ToolResult(ok=False, content="", error=str(raw.get("error") or raw), data=raw)
                content = str(raw.get("content", ""))[:max_bytes]
                return ToolResult(ok=True, content=content, data=raw)
            return ToolResult(ok=True, content=str(raw)[:max_bytes], data={"path": path})
        except Exception:
            p = Path(path)
            if not self._is_allowed(p):
                return ToolResult(ok=False, content="", error=f"Path not allowed: {path}")
            if not p.is_file():
                return ToolResult(ok=False, content="", error=f"Not a file: {path}")
            data = p.read_text(encoding="utf-8", errors="replace")[:max_bytes]
            return ToolResult(ok=True, content=data, data={"path": path})
