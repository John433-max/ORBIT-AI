"""Sandboxed Python execution tool."""

from __future__ import annotations

from tools.base import BaseTool, ToolResult


class PythonTool(BaseTool):
    name = "python.execute"
    description = "Execute a short Python snippet in a restricted sandbox."
    permission_level = "EXECUTION"
    parameters = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python source to run"},
            "timeout": {"type": "number", "description": "Seconds", "default": 5},
        },
        "required": ["code"],
    }
    timeout_s = 15.0

    def execute(self, code: str = "", timeout: float = 5.0, **_) -> ToolResult:
        try:
            from tools_legacy import python_sandbox
            out = python_sandbox(code, timeout=timeout)
            if isinstance(out, dict):
                ok = out.get("ok", True)
                content = out.get("stdout", "") or out.get("content", str(out))
                err = out.get("error") or out.get("stderr")
                return ToolResult(ok=ok, content=content, error=err, data=out)
            return ToolResult(ok=True, content=str(out), data=out)
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))
