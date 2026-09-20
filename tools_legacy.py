"""
Legacy tools: python sandbox, sandboxed file read, mock search providers.

Spec requires containers/resource limits; this prototype implements the subset
that works without Docker-in-Docker: CPU/time bounds, import allowlist,
output-size bounding, audit log.
"""
from __future__ import annotations

import ast
import io
import os
import sys
import threading
import time
import traceback
from typing import Any, Dict, List

IS_WINDOWS = sys.platform.startswith("win")

try:
    import resource
except ImportError:
    resource = None  # type: ignore

AUDIT_LOG: List[dict] = []
_AUDIT_MAX = 500


def _audit(event: str, **fields):
    AUDIT_LOG.append({"event": event, "ts": time.time(), **fields})
    if len(AUDIT_LOG) > _AUDIT_MAX:
        del AUDIT_LOG[: len(AUDIT_LOG) - _AUDIT_MAX]


_ALLOWED_IMPORTS = {
    "math", "json", "re", "collections", "itertools", "functools",
    "statistics", "decimal", "fractions", "string", "textwrap",
}


def _static_check(code: str):
    """Reject dangerous AST nodes / imports before exec."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"syntax error: {e}"
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            else:
                names = [(node.module or "").split(".")[0]]
            for n in names:
                if n and n not in _ALLOWED_IMPORTS:
                    return f"import not allowed: {n}"
        if isinstance(node, ast.Attribute) and isinstance(node.attr, str):
            if node.attr.startswith("__") and node.attr not in ("__name__", "__doc__"):
                return f"dunder attribute blocked: {node.attr}"
    return None


def python_sandbox(code: str, timeout: float = 3.0, mem_limit_mb: int = 128,
                   max_output: int = 8000) -> Dict[str, Any]:
    """Best-effort restricted exec (not a real container)."""
    err = _static_check(code)
    if err:
        _audit("sandbox_deny", reason=err)
        return {"ok": False, "error": err, "stdout": "", "stderr": err}

    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    result: Dict[str, Any] = {"ok": False, "stdout": "", "stderr": "", "error": None}
    done = threading.Event()

    def _run():
        try:
            if resource is not None and not IS_WINDOWS:
                try:
                    resource.setrlimit(resource.RLIMIT_CPU, (max(1, int(timeout)), max(1, int(timeout))))
                    bytes_lim = mem_limit_mb * 1024 * 1024
                    resource.setrlimit(resource.RLIMIT_AS, (bytes_lim, bytes_lim))
                except Exception:
                    pass
            safe_builtins = {
                "abs": abs, "min": min, "max": max, "sum": sum, "len": len,
                "range": range, "enumerate": enumerate, "zip": zip, "map": map,
                "filter": filter, "sorted": sorted, "list": list, "dict": dict,
                "set": set, "tuple": tuple, "str": str, "int": int, "float": float,
                "bool": bool, "print": print, "round": round, "pow": pow,
                "isinstance": isinstance, "type": type, "repr": repr,
            }
            g = {"__builtins__": safe_builtins}
            old_out, old_err = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = stdout_buf, stderr_buf
            try:
                exec(compile(code, "<sandbox>", "exec"), g, g)
                result["ok"] = True
            finally:
                sys.stdout, sys.stderr = old_out, old_err
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            result["stderr"] = traceback.format_exc()[-2000:]
        finally:
            done.set()

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    if not done.wait(timeout + 0.5):
        result["error"] = f"timeout after {timeout}s"
        result["ok"] = False
        _audit("sandbox_timeout", timeout=timeout)
    out = stdout_buf.getvalue()[:max_output]
    err_s = (result.get("stderr") or stderr_buf.getvalue())[:max_output]
    result["stdout"] = out
    result["stderr"] = err_s
    _audit("sandbox_exec", ok=result["ok"], n=len(code))
    return result


def read_sandboxed_file(path: str, root: str = ".") -> Dict[str, Any]:
    """Read a text file under root; block path traversal."""
    root_abs = os.path.abspath(root)
    target = os.path.abspath(os.path.join(root_abs, path))
    if not (target == root_abs or target.startswith(root_abs + os.sep)):
        return {"ok": False, "error": "path escapes sandbox root"}
    if not os.path.isfile(target):
        return {"ok": False, "error": f"not a file: {path}"}
    try:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(4100)
        truncated = len(content) >= 4100
        return {"ok": True, "content": content[:4096], "truncated": truncated, "path": path}
    except Exception as e:
        return {"ok": False, "error": str(e)}


class SearchProvider:
    def search(self, query: str, max_results: int = 5):
        raise NotImplementedError


class MockSearchProvider(SearchProvider):
    def search(self, query: str, max_results: int = 5):
        return [{
            "title": "[mock result]",
            "url": "",
            "snippet": f"Mock search for: {query!r}",
            "source": "mock",
        }]


class UnconfiguredRealSearchProvider(SearchProvider):
    def search(self, query: str, max_results: int = 5):
        raise RuntimeError("Real search not configured")


def web_search_stub(query: str):
    return MockSearchProvider().search(query)
