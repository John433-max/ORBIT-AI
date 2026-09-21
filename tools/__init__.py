"""ORBIT tools package (v2).

Re-exports BaseTool primitives, concrete tools when importable, and legacy
sandbox helpers. Optional imports keep sparse checkouts usable for unit tests.
"""

from tools.base import BaseTool, ToolResult, ToolCall, ToolRegistry

from tools_legacy import (
    IS_WINDOWS,
    python_sandbox,
    read_sandboxed_file,
    MockSearchProvider,
    SearchProvider,
    AUDIT_LOG,
    _audit,
    _static_check,
)

try:
    from tools_legacy import resource  # type: ignore
except ImportError:
    resource = None  # type: ignore

# Optional concrete tools (export names for agents.py imports)
_optional_exports = {}

def _try(mod_name: str, *names: str) -> None:
    try:
        mod = __import__(mod_name, fromlist=list(names))
        for n in names:
            _optional_exports[n] = getattr(mod, n)
            globals()[n] = getattr(mod, n)
    except Exception:
        for n in names:
            globals().setdefault(n, None)

_try("tools.web", "WebSearchTool", "WebFetchTool", "AutoSearchProvider", "StubSearchProvider", "DuckDuckGoSearchProvider")
_try("tools.calculator", "CalculatorTool")
_try("tools.filesystem", "FilesystemTool")
_try("tools.python", "PythonTool")
_try("tools.memory_tool", "MemoryAddTool", "MemorySearchTool")
_try("tools.document_tool", "DocumentListTool", "DocumentTextTool", "DocumentSummarizeTool", "DocumentAnswerTool")
_try("tools.tinylm_lab", "TinyLMLabTool")
_try("tools.finance_tool", "FinanceBacktestTool")
_try("tools.debug_tool", "DebugDiagnoseTool")
_try("tools.file_tool", "FileReadTool")
_try("tools.data_tool", "DataStatsTool")
_try("tools.design_tool", "DesignLayoutTool")
_try("tools.chat_tool", "ChatRetrieveTool", "ChatGenerateTool")

# Fallbacks if web providers failed
if globals().get("AutoSearchProvider") is None:
    AutoSearchProvider = MockSearchProvider
if globals().get("StubSearchProvider") is None:
    StubSearchProvider = MockSearchProvider
if globals().get("DuckDuckGoSearchProvider") is None:
    DuckDuckGoSearchProvider = MockSearchProvider


def default_registry(permission_level: str = "SAFE") -> ToolRegistry:
    """Build a registry with whichever concrete tools are importable."""
    reg = ToolRegistry(permission_level=permission_level)
    for name, cls in list(_optional_exports.items()):
        if name.endswith("Provider") or cls is None:
            continue
        try:
            reg.register(cls())
        except Exception:
            continue
    return reg


__all__ = [
    "BaseTool",
    "ToolResult",
    "ToolCall",
    "ToolRegistry",
    "default_registry",
    "python_sandbox",
    "read_sandboxed_file",
    "MockSearchProvider",
    "SearchProvider",
    "AutoSearchProvider",
    "StubSearchProvider",
    "DuckDuckGoSearchProvider",
    "MemoryAddTool",
    "MemorySearchTool",
    "DocumentListTool",
    "DocumentTextTool",
    "DocumentSummarizeTool",
    "DocumentAnswerTool",
    "ChatRetrieveTool",
    "ChatGenerateTool",
    "CalculatorTool",
    "AUDIT_LOG",
    "_audit",
    "_static_check",
    "IS_WINDOWS",
    "resource",
]
