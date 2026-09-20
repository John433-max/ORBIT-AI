"""
Compatibility shim for the original top-level `tools.py`.

ORBIT v2 moved the implementation to `tools_legacy.py` and exposed a
modular package at `tools/` (BaseTool, ToolRegistry, calculator, web, …).

This file exists so that:
  - `ls tools.py` / docs / scripts that expect the classic path still work
  - imports continue to resolve via the `tools/` package (package takes
    precedence when both exist)

Prefer:
  from tools import python_sandbox, read_sandboxed_file, default_registry
"""

from tools_legacy import (  # noqa: F401
    python_sandbox,
    read_sandboxed_file,
    MockSearchProvider,
    SearchProvider,
    AUDIT_LOG,
    _audit,
    _static_check,
    IS_WINDOWS,
)

try:
    from tools_legacy import resource  # noqa: F401
except ImportError:  # pragma: no cover
    resource = None  # type: ignore

# v2 API (also available from the tools package)
try:
    from tools.base import BaseTool, ToolResult, ToolCall, ToolRegistry  # noqa: F401
    from tools import default_registry  # noqa: F401
except Exception:  # pragma: no cover
    pass

__all__ = [
    "python_sandbox",
    "read_sandboxed_file",
    "MockSearchProvider",
    "SearchProvider",
    "AUDIT_LOG",
    "_audit",
    "_static_check",
    "IS_WINDOWS",
    "resource",
]
