"""
Tools available to agents. Spec Part 8 requires: containers, resource
limits, filesystem isolation, network restrictions, process limits,
timeouts, allowlists, audit logs. This prototype implements the subset that
doesn't require container infrastructure this sandbox doesn't have access
to (no Docker-in-Docker here) — CPU time limit, memory limit, wall-clock
timeout, an import allowlist, output-size bounding, and an audit log. It
does NOT implement filesystem/network namespace isolation or a true
container boundary — see the module docstring warning below. Do not treat
this as production-grade; it is defense-in-depth for a local research
prototype, not a security boundary for hostile/untrusted code at scale.
"""
import subprocess
import sys
import time
import platform
import threading
import logging
import collections
import ast

# `resource` (rlimit-based CPU/memory limiting) is POSIX-only and does not
# exist on Windows -- importing it unconditionally would crash `import
# tools` (and therefore `import agents`, `import api`) on native Windows
# before any of this module's code even runs. This was a real bug: nothing
# caught it because the sandbox this project has been developed in is
# Linux, so it was never exercised. `preexec_fn` (used to apply those
# limits to the child process) is *also* unsupported on Windows --
# subprocess.run raises ValueError if it's passed there at all. Both are
# handled below by detecting the platform once and skipping OS-level
# resource limiting entirely on Windows, with an explicit warning rather
# than silently pretending the same protection applies (see DESIGN.md Part
# 8 and SETUP.md's Windows section).
IS_WINDOWS = platform.system() == "Windows"
if not IS_WINDOWS:
    import resource

AUDIT_LOG = collections.deque(maxlen=1000)
# Bounded, not a plain list: this used to grow without limit for the
# lifetime of the process (every sandbox execution appended, nothing ever
# read or trimmed it -- verified by grepping the whole project: nothing
# consumes AUDIT_LOG anywhere, so it was pure unbounded memory growth with
# zero benefit). A deque(maxlen=...) keeps the most recent N events and
# silently drops older ones instead of growing forever. Security events are
# also emitted through the stdlib logging module below so they aren't lost
# entirely once they age out of this in-memory ring buffer -- persisted log
# output (e.g. a file/rotating handler configured by whoever runs this
# process) is the durable record; this deque is just for cheap recent-
# history introspection.
_security_logger = logging.getLogger("orbit.security")

# Import ALLOWLIST, not a blocklist. A blocklist only stops the specific
# names someone thought to list (the previous version missed nothing
# structurally wrong, but a blocklist is architecturally weaker than an
# allowlist: every module NOT explicitly reasoned about here is rejected by
# default, rather than every module NOT explicitly reasoned about being
# silently permitted). Every entry below is deliberately compute/data-only
# -- no filesystem, network, process, or system-introspection capability.
SAFE_IMPORTS = {
    "math", "statistics", "decimal", "fractions", "random", "itertools",
    "functools", "collections", "re", "json", "string", "datetime",
    "textwrap", "heapq", "bisect", "copy", "enum", "dataclasses", "typing",
    "numpy", "array", "cmath", "operator",
}
# Explicitly NOT included, with reasons (so the exclusion is a decision,
# not an oversight): os/sys/subprocess/socket/shutil/ctypes/multiprocessing/
# importlib/pathlib (filesystem/network/process/system access); io (file
# handles); threading/asyncio (concurrency + can dodge CPU rlimits);
# pickle/marshal (can execute arbitrary code on load); code/pty/signal/mmap
# (process/memory manipulation); urllib/http/ftplib/requests (network).


def _audit(event: str, **fields):
    AUDIT_LOG.append({"ts": time.time(), "event": event, **fields})
    # blocked/rejected events are the security-relevant ones worth a real
    # log line; routine start/end events would just be noise at INFO level
    # for every single sandbox call
    if "blocked" in event or "rejected" in event:
        _security_logger.warning("sandbox event=%s %s", event, fields)


def _static_check(code: str):
    """Reject obviously dangerous code before execution. Import checking is
    now allowlist-based (SAFE_IMPORTS); eval/exec/compile/__import__ and
    os.system-style attribute calls remain explicitly blocked on top of
    that as defense-in-depth, not as the primary control. Blocklist,
    allowlist, and rlimits together are still not a real sandbox boundary
    -- see the module docstring."""
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
        # Also catch bare-name calls (eval(...), exec(...), __import__(...)),
        # which the Attribute check above misses since these are ast.Name,
        # not ast.Attribute, nodes.
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec", "compile", "__import__"):
                return ("blocked_operation", f"blocked call pattern: {node.func.id}(...)")
    return None


def _read_stream_bounded(stream, max_bytes: int, chunks: list, stop_event: threading.Event):
    """Read a subprocess pipe incrementally, stopping once max_bytes is
    reached, rather than letting subprocess.run's capture_output=True read
    to EOF unconditionally. This is what actually enforces an output-size
    limit -- a limit that's only checked *after* the fact (post-hoc string
    truncation on an already-fully-buffered read) doesn't bound the memory
    the parent process uses while reading, which is the actual risk from a
    program like `while True: print("A"*1000)`."""
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
        pass  # stream closed underneath us (process was killed) -- not an error


def python_sandbox(code: str, timeout: float = 3.0, mem_limit_mb: int = 128,
                    max_stdout_bytes: int = 1_000_000, max_stderr_bytes: int = 1_000_000):
    """
    Run untrusted Python in a separate subprocess with:
    - an import ALLOWLIST (SAFE_IMPORTS) plus an eval/exec/compile/__import__/
      os.system blocklist on top, both best-effort and not a security boundary
    - CPU time + address-space limits via resource.setrlimit (POSIX only --
      see IS_WINDOWS; skipped with a warning on Windows, not silently faked)
    - a wall-clock timeout
    - bounded stdout/stderr capture (max_stdout_bytes/max_stderr_bytes),
      with the process killed early if a stream exceeds its cap, rather
      than buffering unboundedly until timeout
    - no stdin, non-zero exit surfaced as an error
    - structured error_type classification (see the return value's
      "error_type" field: syntax_error / blocked_operation / timeout /
      resource_limit / output_limit / runtime_error / sandbox_error) so
      callers don't have to guess a cause from a free-text message, and so
      a resource-limit kill is never misreported as a timeout or vice versa
    WARNING (see DESIGN.md Part 8): this is a prototype-scale approximation.
    A real deployment needs an actual container/gVisor/firecracker boundary,
    not just rlimits in a subprocess on the same host.
    """
    checked = _static_check(code)
    if checked:
        error_type, reason = checked
        _audit("python_sandbox.blocked", reason=reason)
        return {"ok": False, "error_type": error_type, "error": f"rejected before execution: {reason}"}

    if IS_WINDOWS:
        preexec_fn = None
        _audit("python_sandbox.no_resource_limits", platform="windows")
    else:
        def preexec_fn():
            resource.setrlimit(resource.RLIMIT_CPU, (int(timeout) + 1, int(timeout) + 1))
            resource.setrlimit(resource.RLIMIT_AS, (mem_limit_mb * 1024 * 1024, mem_limit_mb * 1024 * 1024))

    _audit("python_sandbox.start", code_len=len(code))
    try:
        proc = subprocess.Popen(
            [sys.executable, "-I", "-c", code],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, preexec_fn=preexec_fn,
        )
    except Exception as e:  # process spawn itself failed -- not the sandboxed code's fault
        _audit("python_sandbox.spawn_error", error=str(e))
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
        stdout_bytes = sum(len(c) for c in stdout_chunks)
        stderr_bytes = sum(len(c) for c in stderr_chunks)
        if stdout_bytes >= max_stdout_bytes or stderr_bytes >= max_stderr_bytes:
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
            pass  # best-effort; process is at least sent SIGKILL

    t_out.join(timeout=2)
    t_err.join(timeout=2)
    stdout = "".join(stdout_chunks)
    stderr = "".join(stderr_chunks)
    returncode = proc.poll()

    if output_limit_hit:
        result = {"ok": False, "error_type": "output_limit",
                  "error": f"output exceeded the configured limit (stdout={max_stdout_bytes}B, stderr={max_stderr_bytes}B)",
                  "stdout": stdout, "stderr": stderr}
    elif timed_out:
        result = {"ok": False, "error_type": "timeout", "error": f"timed out after {timeout}s",
                   "stdout": stdout, "stderr": stderr}
    elif returncode != 0:
        # Distinguish "hit a configured resource limit" from an ordinary
        # Python exception exit two ways, since testing showed either can
        # happen depending on how the limit gets hit:
        #  (a) the OS kills the process outright with a signal (POSIX:
        #      returncode is reported as -signum) -- e.g. some CPU-limit
        #      kills land here.
        #  (b) RLIMIT_AS makes malloc() fail, which Python's own allocator
        #      catches and raises as an ordinary in-process MemoryError --
        #      this exits *cleanly* (returncode 1, real traceback in
        #      stderr), so it looks identical to any other exception at the
        #      returncode level. Verified directly: `bytearray(400MB)`
        #      under a 64MB limit produces returncode=1 with "MemoryError"
        #      in stderr, not a signal -- a signal-only check would
        #      misclassify this as a generic runtime_error.
        signaled = returncode is not None and returncode < 0
        memory_error_text = "MemoryError" in stderr
        if signaled or memory_error_text:
            result = {"ok": False, "error_type": "resource_limit",
                      "error": f"process terminated by signal {-returncode}" if signaled
                      else "process exceeded the configured memory limit (MemoryError)",
                      "stdout": stdout, "stderr": stderr, "returncode": returncode}
        else:
            result = {"ok": False, "error_type": "runtime_error", "stdout": stdout, "stderr": stderr,
                      "returncode": returncode}
    else:
        result = {"ok": True, "stdout": stdout, "stderr": stderr, "returncode": returncode}
    _audit("python_sandbox.end", ok=result.get("ok"), error_type=result.get("error_type"))
    return result


def web_search_stub(query: str):
    """
    No live network access from inside this standalone prototype process
    (unlike the Claude session that built it, which does have a real
    web_search tool). Returns an explicit placeholder rather than a fake
    result — matches the spec's "must not pretend it searched if it did
    not" requirement for Part 9.
    """
    _audit("web_search_stub.call", query=query)
    return {"ok": False, "note": "no live web access in this prototype process; "
                                  "wire a real search API key here for a deployed version",
            "query": query}


class SearchProvider:
    """Abstraction point for web search, so ResearchAgent (agents.py) can
    be configured/tested against a mock without depending on a concrete
    implementation, and so a real provider can be swapped in later without
    changing ResearchAgent itself. There is deliberately no RealSearchProvider
    implementation here: this prototype process has no live network access
    to a search API, and shipping a "real" provider class with no working
    backend would itself be exactly the kind of fake functionality this
    project's rules prohibit. See MockSearchProvider below for what's
    actually usable today, and the docstring on the raise below for what a
    real implementation would need to provide."""

    def search(self, query: str) -> dict:
        """Must return {"ok": bool, "results": list, ...} -- MockSearchProvider
        and any future real implementation share this shape so callers don't
        need to know which one they're using."""
        raise NotImplementedError


class MockSearchProvider(SearchProvider):
    """Default search provider for ResearchAgent.

    Tries live DuckDuckGo (via tools.web.AutoSearchProvider) and falls back
    to web_search_stub if the network or parser fails. Return shape stays
    {"ok": bool, "results": list, ...} for agents.py compatibility.
    """

    def search(self, query: str) -> dict:
        try:
            from tools.web import AutoSearchProvider
            hits = AutoSearchProvider().search(query, max_results=5)
            results = [
                {
                    "title": h.title,
                    "url": h.url,
                    "snippet": h.snippet,
                    "source": h.source,
                }
                for h in hits
                if h.source != "stub" and h.source != "stub+error"
            ]
            if results:
                _audit("web_search.live", query=query, n=len(results))
                return {"ok": True, "results": results, "provider": "duckduckgo"}
        except Exception as e:
            _audit("web_search.live_failed", query=query, error=str(e))
        return web_search_stub(query)


class UnconfiguredRealSearchProvider(SearchProvider):
    """A concrete stand-in showing where a real provider would plug in --
    intentionally raises rather than silently behaving like the mock, so a
    caller who thinks they configured real search finds out immediately if
    they didn't, instead of getting an honest-looking-but-fake result."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def search(self, query: str) -> dict:
        if not self.api_key:
            raise NotImplementedError(
                "UnconfiguredRealSearchProvider requires a real search API key and an "
                "actual HTTP client wired to a search provider -- neither exists in this "
                "prototype. Pass search_provider=MockSearchProvider() (the default) instead, "
                "or implement a real provider class with an actual backend.")
        raise NotImplementedError("no real search backend is implemented in this prototype")


def read_sandboxed_file(path: str, root: str = "."):
    """
    Resolve `path` under `root` and refuse anything that escapes it.

    NOTE on the fix here: the previous check was
        target_abs.startswith(root_abs)
    which is unsafe two ways: (1) a sibling directory that merely shares a
    string prefix (root="/a/b", target="/a/b_evil/secret") passes the check
    even though it's outside root, and (2) it resolves ".." lexically via
    os.path.abspath but never follows symlinks, so a symlink inside root
    that points outside it sails through untouched. Fixed by using
    os.path.realpath (which resolves symlinks) on both sides and then
    checking real containment with os.path.commonpath instead of a string
    prefix comparison.
    """
    import os
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
