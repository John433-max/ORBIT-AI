"""Sandboxed file read at SAFE permission (Cycle 60)."""

from __future__ import annotations

from tools.base import BaseTool, ToolResult


class FileReadTool(BaseTool):
    name = "file.read"
    description = "Read a text file inside the sandbox root (path-traversal blocked)."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path relative to sandbox root"},
            "root": {"type": "string", "description": "Sandbox root", "default": "."},
        },
        "required": ["path"],
    }
    timeout_s = 10.0

    def execute(self, path: str = "", root: str = ".", **_):
        from tools_legacy import read_sandboxed_file

        raw = read_sandboxed_file(path, root=root or ".")
        if not isinstance(raw, dict):
            return ToolResult(ok=True, content=str(raw), data={"path": path})
        if not raw.get("ok"):
            return ToolResult(
                ok=False,
                content="",
                error=str(raw.get("error") or "read failed"),
                data=raw,
            )
        content = str(raw.get("content", ""))
        return ToolResult(ok=True, content=content, data=raw)
