"""Document tools — list / extract / summarize / answer from DocumentStore."""

from __future__ import annotations

from tools.base import BaseTool, ToolResult


class DocumentListTool(BaseTool):
    name = "document.list"
    description = "List uploaded documents (id and filename)."
    permission_level = "SAFE"
    parameters = {"type": "object", "properties": {}}
    timeout_s = 5.0

    def __init__(self, store=None):
        self.store = store

    def execute(self, **_) -> ToolResult:
        if self.store is None:
            return ToolResult(ok=False, content="", error="no document store bound")
        try:
            docs = self.store.list_documents() if hasattr(self.store, "list_documents") else []
            return ToolResult(ok=True, content=f"{len(docs)} document(s)", data=docs or [])
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))


class DocumentTextTool(BaseTool):
    name = "document.text"
    description = "Extract raw text from an uploaded document by id."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {"document_id": {"type": "integer"}},
        "required": ["document_id"],
    }
    timeout_s = 5.0

    def __init__(self, store=None):
        self.store = store

    def execute(self, document_id: int = 0, **_) -> ToolResult:
        if self.store is None:
            return ToolResult(ok=False, content="", error="no document store bound")
        try:
            text = self.store.get_document_text(int(document_id)) or ""
            return ToolResult(
                ok=True,
                content=text or "(no extractable text)",
                data={"document_id": int(document_id), "text": text, "chars": len(text)},
            )
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))


class DocumentSummarizeTool(BaseTool):
    name = "document.summarize"
    description = "Extractive summary of an uploaded document by id."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {"document_id": {"type": "integer"}},
        "required": ["document_id"],
    }
    timeout_s = 10.0

    def __init__(self, store=None):
        self.store = store

    def execute(self, document_id: int = 0, **_) -> ToolResult:
        if self.store is None:
            return ToolResult(ok=False, content="", error="no document store bound")
        try:
            from documents import summarize_document
            result = summarize_document(self.store, int(document_id))
            summary = (result or {}).get("summary") or ""
            ok = bool(summary)
            return ToolResult(
                ok=ok, content=summary, data=result,
                error=None if ok else f"document #{document_id} not found",
            )
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))


class DocumentAnswerTool(BaseTool):
    name = "document.answer"
    description = "Answer a question using extractive retrieval over uploaded documents."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    }
    timeout_s = 10.0

    def __init__(self, store=None):
        self.store = store

    def execute(self, query: str = "", **_) -> ToolResult:
        if self.store is None:
            return ToolResult(ok=False, content="", error="no document store bound")
        query = (query or "").strip()
        if not query:
            return ToolResult(ok=False, content="", error="query is required")
        try:
            from documents import answer_from_documents
            result = answer_from_documents(self.store, query)
            return ToolResult(ok=True, content=result.get("answer") or "", data=result)
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))
