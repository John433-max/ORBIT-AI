"""ORBIT tools package (v2).

Re-exports BaseTool primitives and legacy sandbox helpers. Concrete tool
classes are imported lazily so a sparse GitHub checkout can still collect
unit tests that only need tools.base.
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

# ResearchAgent imports AutoSearchProvider from this package.
try:
    from tools.web import (  # noqa: F401
        AutoSearchProvider,
        StubSearchProvider,
        DuckDuckGoSearchProvider,
    )
except Exception:
    AutoSearchProvider = MockSearchProvider
    StubSearchProvider = MockSearchProvider
    DuckDuckGoSearchProvider = MockSearchProvider


def default_registry(permission_level: str = "SAFE") -> ToolRegistry:
    """Build a registry with whichever concrete tools are importable."""
    reg = ToolRegistry(permission_level=permission_level)
    _optional = (
        ("tools.calculator", "CalculatorTool"),
        ("tools.filesystem", "FilesystemTool"),
        ("tools.python", "PythonTool"),
        ("tools.web", "WebSearchTool"),
        ("tools.web", "WebFetchTool"),
        ("tools.memory_tool", "MemoryAddTool"),
        ("tools.memory_tool", "MemorySearchTool"),
        ("tools.document_tool", "DocumentListTool"),
        ("tools.document_tool", "DocumentTextTool"),
        ("tools.document_tool", "DocumentSummarizeTool"),
        ("tools.document_tool", "DocumentAnswerTool"),
        ("tools.tinylm_lab", "TinyLMLabTool"),
        ("tools.finance_tool", "FinanceBacktestTool"),
        ("tools.debug_tool", "DebugDiagnoseTool"),
        ("tools.file_tool", "FileReadTool"),
        ("tools.data_tool", "DataStatsTool"),
        ("tools.design_tool", "DesignLayoutTool"),
        ("tools.chat_tool", "ChatRetrieveTool"),
        ("tools.chat_tool", "ChatGenerateTool"),
    )
    seen = set()
    for mod_name, cls_name in _optional:
        key = (mod_name, cls_name)
        if key in seen:
            continue
        seen.add(key)
        try:
            mod = __import__(mod_name, fromlist=[cls_name])
            cls = getattr(mod, cls_name)
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
    "AUDIT_LOG",
    "_audit",
    "_static_check",
    "IS_WINDOWS",
    "resource",
]
