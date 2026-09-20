"""Agent sandbox tools used by CI and the tools package shim."""
from __future__ import annotations

import ast
import collections
import logging
import os
import platform
import subprocess
import sys
import time

IS_WINDOWS = platform.system() == "Windows"
if not IS_WINDOWS:
    import resource  # noqa: F401

AUDIT_LOG = collections.deque(maxlen=1000)
_security_logger = logging.getLogger("orbit.security")

SAFE_IMPORTS = {
    "math", "statistics", "decimal", "fractions", "random", "itertools",
    "functools", "collections", "re", "json", "string", "datetime",
    "textwrap", "heapq", "bisect", "copy", "enum", "dataclasses", "typing",
    "numpy", "array", "cmath", "operator",
}


def _audit(event: str, **fields):
    AUDIT_LOG.append({"ts": time.time(), "event": event, **fields})
    if "blocked" in event or "rejected" in event:
        _security_logger.warning("sandbox event=%s %s", event, fields)


def _static_check(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return ("syntax_error", f"syntax error: {e}")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [n.name for n in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for n in names:
                root = (n or "").split(".")[0]
                if root not in SAFE_IMPORTS:
                    return ("blocked_operation", f"import not in allowlist: {root}")
        if isinstance(node, ast.Attribute) and node.attr in ("system", "popen", "eval", "exec"):
            return ("blocked_operation", f"blocked call pattern: .{node.attr}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec", "compile", "__import__"):
                return ("blocked_operation", f"blocked call pattern: {node.func.id}(...)")
    return None


def python_sandbox(code: str, timeout: float = 3.0, mem_limit_mb: int = 128,
                   max_stdout_bytes: int = 1_000_000, max_stderr_bytes: int = 1_000_000):
    checked = _static_check(code)
    if checked:
        error_type, reason = checked
        _audit("python_sandbox.blocked", reason=reason)
        return {"ok": False, "error_type": error_type, "error": f"rejected before execution: {reason}"}
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
        return {"ok": False, "error_type": "sandbox_error", "error": f"failed to start sandbox process: {e}"}
    if proc.returncode != 0:
        return {
            "ok": False,
            "error_type": "runtime_error",
            "error": (proc.stderr or proc.stdout or "runtime error").strip(),
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode,
        }
    return {"ok": True, "stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}


def web_search_stub(query: str):
    _audit("web_search_stub.call", query=query)
    return {
        "ok": False,
        "note": "no live web access in this prototype process",
        "query": query,
        "results": [],
    }


class SearchProvider:
    def search(self, query: str) -> dict:
        raise NotImplementedError


class MockSearchProvider(SearchProvider):
    def search(self, query: str) -> dict:
        return web_search_stub(query)


def read_sandboxed_file(path: str, root: str = "."):
    root_real = os.path.realpath(root)
    target_real = os.path.realpath(os.path.join(root, path))
    try:
        if os.path.commonpath([root_real, target_real]) != root_real:
            raise ValueError
    except ValueError:
        _audit("file_read.blocked", path=path)
        return {"ok": False, "error": "path escapes sandbox root"}
    try:
        with open(target_real) as f:
            content = f.read(4096)
        _audit("file_read.ok", path=path)
        return {"ok": True, "content": content}
    except OSError as e:
        _audit("file_read.error", path=path, error=str(e))
        return {"ok": False, "error": str(e)}
