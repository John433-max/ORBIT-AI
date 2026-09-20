"""Sandboxed Python execution tool."""

from __future__ import annotations

import ast
import subprocess
import sys
import time

from tools.base import BaseTool, ToolResult

_SAFE_IMPORTS = {
    "math",
    "statistics",
    "decimal",
    "fractions",
    "random",
    "itertools",
    "functools",
    "collections",
    "re",
    "json",
    "string",
    "datetime",
    "textwrap",
    "heapq",
    "bisect",
    "copy",
    "enum",
    "dataclasses",
    "typing",
    "numpy",
    "array",
    "cmath",
    "operator",
}


def _static_check(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"syntax error: {e}"
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [n.name for n in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
            )
            for n in names:
                root = (n or "").split(".")[0]
                if root not in _SAFE_IMPORTS:
                    return f"import not in allowlist: {root}"
        if isinstance(node, ast.Attribute) and node.attr in ("system", "popen", "eval", "exec"):
            return f"blocked call pattern: .{node.attr}"
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec", "compile", "__import__"):
                return f"blocked call pattern: {node.func.id}(...)"
    return None


def _fallback_sandbox(code: str, timeout: float = 5.0) -> dict:
    """Minimal sandbox used when tools_legacy.python_sandbox is unavailable."""
    blocked = _static_check(code)
    if blocked:
        return {"ok": False, "error_type": "blocked_operation", "error": blocked}
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-c", code],
            capture_output=True,
            text=True,
            timeout=max(0.1, float(timeout)),
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error_type": "timeout", "error": f"timed out after {timeout}s"}
    except Exception as e:
        return {"ok": False, "error_type": "sandbox_error", "error": str(e)}
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "runtime error").strip()
        return {
            "ok": False,
            "error_type": "runtime_error",
            "error": err,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    return {"ok": True, "stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}


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
        out = None
        try:
            from tools_legacy import python_sandbox

            out = python_sandbox(code, timeout=timeout)
        except Exception:
            out = _fallback_sandbox(code, timeout=timeout)
        if isinstance(out, dict):
            ok = out.get("ok", True)
            content = out.get("stdout", "") or out.get("content", "" if not ok else str(out))
            err = out.get("error") or out.get("stderr")
            return ToolResult(ok=ok, content=content or "", error=err, data=out)
        return ToolResult(ok=True, content=str(out), data=out)
