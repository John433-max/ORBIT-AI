"""
ORBIT tools package (v2).

Provides a standard BaseTool interface and concrete tools.
Also re-exports the legacy symbols from tools_legacy.py so that existing
code (`from tools import python_sandbox`, etc.) continues to work.
"""

# ---- v2 interface ----
from tools.base import BaseTool, ToolResult, ToolCall, ToolRegistry
from tools.calculator import CalculatorTool
from tools.filesystem import FilesystemTool
from tools.python import PythonTool
from tools.memory_tool import MemoryAddTool, MemorySearchTool
from tools.document_tool import (
    DocumentListTool,
    DocumentTextTool,
    DocumentSummarizeTool,
    DocumentAnswerTool,
)
from tools.web import (
    WebSearchTool,
    WebFetchTool,
    StubSearchProvider,
    DuckDuckGoSearchProvider,
    AutoSearchProvider,
    SearchProvider as WebSearchProvider,
)
from tools.tinylm_lab import TinyLMLabTool
from tools.finance_tool import FinanceBacktestTool
from tools.debug_tool import DebugDiagnoseTool
from tools.file_tool import FileReadTool
from tools.data_tool import DataStatsTool
from tools.design_tool import DesignLayoutTool
from tools.chat_tool import ChatRetrieveTool, ChatGenerateTool

# ---- legacy re-exports (backward compatibility) ----
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

__all__ = [
    "BaseTool",
    "ToolResult",
    "ToolCall",
    "ToolRegistry",
    "CalculatorTool",
    "FilesystemTool",
    "PythonTool",
    "WebSearchTool",
    "WebFetchTool",
    "MemoryAddTool",
    "MemorySearchTool",
    "DocumentListTool",
    "DocumentTextTool",
    "DocumentSummarizeTool",
    "DocumentAnswerTool",
    "TinyLMLabTool",
    "FinanceBacktestTool",
    "DebugDiagnoseTool",
    "FileReadTool",
    "DataStatsTool",
    "DesignLayoutTool",
    "ChatRetrieveTool",
    "ChatGenerateTool",
    "StubSearchProvider",
    "DuckDuckGoSearchProvider",
    "AutoSearchProvider",
    "WebSearchProvider",
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


def default_registry(permission_level: str = "SAFE") -> ToolRegistry:
    """Build a registry with the standard tools."""
    reg = ToolRegistry(permission_level=permission_level)
    reg.register(CalculatorTool())
    reg.register(FilesystemTool())
    reg.register(PythonTool())
    reg.register(WebSearchTool())
    reg.register(WebFetchTool())
    reg.register(MemoryAddTool())
    reg.register(MemorySearchTool())
    reg.register(DocumentListTool())
    reg.register(DocumentTextTool())
    reg.register(DocumentSummarizeTool())
    reg.register(DocumentAnswerTool())
    reg.register(TinyLMLabTool())
    reg.register(FinanceBacktestTool())
    reg.register(DebugDiagnoseTool())
    reg.register(FileReadTool())
    reg.register(DataStatsTool())
    reg.register(DesignLayoutTool())
    reg.register(ChatRetrieveTool())
    reg.register(ChatGenerateTool())
    return reg
