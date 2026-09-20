"""Prototype Python sandbox used by tools.python.PythonTool."""
import ast
import collections
import logging
import platform
import subprocess
import sys
import threading
import time

IS_WINDOWS = platform.system() == "Windows"
if not IS_WINDOWS:
    import resource

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


def _read_stream_bounded(stream, max_bytes, chunks, stop_event):
    total = 0
    try:
        while not stop_event.is_set():
            chunk = stream.read(4096)
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total >= max_bytes:
                break
    except (ValueError, OSError):
        pass


def python_sandbox(code: str, timeout: float = 3.0, mem_limit_mb: int = 128,
                    max_stdout_bytes: int = 1_000_000, max_stderr_bytes: int = 1_000_000):
    checked = _static_check(code)
    if checked:
        error_type, reason = checked
        _audit("python_sandbox.blocked", reason=reason)
        return {"ok": False, "error_type": error_type, "error": f"rejected before execution: {reason}"}

    if IS_WINDOWS:
        preexec_fn = None
    else:
        def preexec_fn():
            resource.setrlimit(resource.RLIMIT_CPU, (int(timeout) + 1, int(timeout) + 1))
            resource.setrlimit(resource.RLIMIT_AS, (mem_limit_mb * 1024 * 1024, mem_limit_mb * 1024 * 1024))

    try:
        proc = subprocess.Popen(
            [sys.executable, "-I", "-c", code],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, preexec_fn=preexec_fn,
        )
    except Exception as e:
        return {"ok": False, "error_type": "sandbox_error", "error": f"failed to start sandbox process: {e}"}

    stdout_chunks, stderr_chunks = [], []
    stop_event = threading.Event()
    t_out = threading.Thread(target=_read_stream_bounded, args=(proc.stdout, max_stdout_bytes, stdout_chunks, stop_event))
    t_err = threading.Thread(target=_read_stream_bounded, args=(proc.stderr, max_stderr_bytes, stderr_chunks, stop_event))
    t_out.start()
    t_err.start()

    deadline = time.time() + timeout
    output_limit_hit = False
    while True:
        if proc.poll() is not None:
            break
        if sum(len(c) for c in stdout_chunks) >= max_stdout_bytes or sum(len(c) for c in stderr_chunks) >= max_stderr_bytes:
            output_limit_hit = True
            break
        if time.time() >= deadline:
            break
        time.sleep(0.02)

    timed_out = not output_limit_hit and proc.poll() is None
    if timed_out or output_limit_hit:
        stop_event.set()
        proc.kill()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass

    t_out.join(timeout=2)
    t_err.join(timeout=2)
    stdout = "".join(stdout_chunks)
    stderr = "".join(stderr_chunks)
    returncode = proc.poll()

    if output_limit_hit:
        return {"ok": False, "error_type": "output_limit", "error": "output exceeded the configured limit", "stdout": stdout, "stderr": stderr}
    if timed_out:
        return {"ok": False, "error_type": "timeout", "error": f"timed out after {timeout}s", "stdout": stdout, "stderr": stderr}
    if returncode != 0:
        return {"ok": False, "error_type": "runtime_error", "error": stderr or "nonzero exit", "stdout": stdout, "stderr": stderr, "returncode": returncode}
    return {"ok": True, "stdout": stdout, "stderr": stderr, "returncode": returncode}
