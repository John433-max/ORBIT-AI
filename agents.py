"""
Agent orchestrator (spec Part 10), wired to tools, paper_trading, memory, documents.

Routing is rule-based keyword matching (honest prototype stand-in).
Full 1443-line source also in ORBIT-AI-source.zip.
"""
from __future__ import annotations

import re
import hashlib
from typing import Any, Dict

try:
    from tools import (
        python_sandbox,
        MockSearchProvider,
        AutoSearchProvider,
        default_registry,
        ToolCall,
    )
except Exception:  # pragma: no cover
    python_sandbox = None
    MockSearchProvider = object
    AutoSearchProvider = object
    default_registry = None
    ToolCall = None

try:
    from paper_trading import backtest_sma_crossover
except Exception:
    backtest_sma_crossover = None

try:
    from memory_store import VectorStore, SQLiteVectorStore
except Exception:
    VectorStore = object
    SQLiteVectorStore = object

try:
    from calculator import parse_and_calculate
except Exception:
    parse_and_calculate = None

try:
    from documents import DocumentStore, answer_from_documents, summarize_document
except Exception:
    DocumentStore = object
    answer_from_documents = None
    summarize_document = None

try:
    from context import ConversationStore
except Exception:
    ConversationStore = object

try:
    from debugging import diagnose_traceback
except Exception:
    diagnose_traceback = None

try:
    from thinking import Thinker
except Exception:
    Thinker = None


def stable_seed(text: str) -> int:
    digest = hashlib.sha256(text.encode("utf-8", errors="replace")).digest()
    return int.from_bytes(digest[:8], "big") % (2**32)


class AgentResult:
    def __init__(self, agent: str, ok: bool, content: str, raw=None):
        self.agent, self.ok, self.content, self.raw = agent, ok, content, raw

    def to_dict(self):
        d = {"agent": self.agent, "ok": self.ok, "content": self.content}
        if self.raw is not None:
            d["raw"] = self.raw
        return d


def _registry_from_context(context: dict):
    if context:
        registry = context.get("tools")
        if registry is not None:
            return registry
    if default_registry is not None:
        return default_registry("SAFE")
    return None


class CodeAgent:
    name = "coding_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        m = re.search(r"```(?:python)?\s*(.*?)```", request, re.S)
        code = m.group(1) if m else request
        registry = _registry_from_context(context)
        if registry is not None and ToolCall is not None:
            tool_res = registry.execute(
                ToolCall(tool="python.execute", arguments={"code": code, "timeout": 3.0})
            )
            if tool_res.ok:
                return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
            if tool_res.error and "permission" not in (tool_res.error or ""):
                return AgentResult(self.name, False, tool_res.error or tool_res.content)
        if python_sandbox is not None:
            result = python_sandbox(code, timeout=3.0)
            if result.get("ok"):
                return AgentResult(self.name, True, f"Ran the code in the sandbox. stdout:\n{result.get('stdout','')}", raw=result)
            return AgentResult(self.name, False, f"Sandbox failed: {result.get('error') or result.get('stderr')}", raw=result)
        return AgentResult(self.name, False, "Code sandbox unavailable")


class ResearchAgent:
    name = "research_agent"

    def __init__(self, search_provider=None):
        self.search_provider = search_provider
        if search_provider is None:
            try:
                self.search_provider = AutoSearchProvider()
            except Exception:
                try:
                    self.search_provider = MockSearchProvider()
                except Exception:
                    self.search_provider = None

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        if registry is not None and ToolCall is not None:
            tool_res = registry.execute(
                ToolCall(tool="web.search", arguments={"query": request, "max_results": 5})
            )
            if tool_res.ok:
                return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        if self.search_provider is not None:
            try:
                raw = self.search_provider.search(request)
                return AgentResult(self.name, True, str(raw), raw=raw)
            except Exception as e:
                return AgentResult(self.name, False, f"Search failed: {e}")
        return AgentResult(self.name, False, "I don't have live web access right now.")


class CalculatorAgent:
    name = "calculator_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        if registry is not None and ToolCall is not None:
            tool_res = registry.execute(
                ToolCall(tool="calculator", arguments={"expression": request})
            )
            if tool_res.ok:
                return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        try:
            from science_math import solve_science_math
            sci = solve_science_math(request)
            if isinstance(sci, dict) and sci.get("ok"):
                return AgentResult(self.name, True, sci.get("pretty") or str(sci.get("result")), raw=sci)
        except Exception:
            pass
        if parse_and_calculate is not None:
            result = parse_and_calculate(request)
            if isinstance(result, dict) and result.get("ok"):
                return AgentResult(self.name, True, f"{result.get('expression', request)} = {result['result']}", raw=result)
            err = result.get("error") if isinstance(result, dict) else str(result)
            return AgentResult(self.name, False, f"Could not compute: {err}", raw=result)
        return AgentResult(self.name, False, "Calculator unavailable")


class DataAgent:
    name = "data_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        if registry is not None and ToolCall is not None:
            tool_res = registry.execute(ToolCall(tool="data.stats", arguments={"text": request}))
            if tool_res.ok:
                return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        return AgentResult(self.name, False, "No numeric data found.")


class DebugAgent:
    name = "debug_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        if diagnose_traceback is None:
            return AgentResult(self.name, False, "Debug helpers unavailable")
        diagnosis = diagnose_traceback(request)
        if diagnosis.get("error_type") is None:
            return AgentResult(self.name, False, "Could not identify a Python error type.", raw=diagnosis)
        lines = [f"Error type: {diagnosis['error_type']}", diagnosis.get("explanation") or ""]
        return AgentResult(self.name, True, "\n".join(lines), raw=diagnosis)


class DocumentAgent:
    name = "document_agent"

    def __init__(self, store=None):
        self.store = store

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        if registry is not None and ToolCall is not None:
            tool_res = registry.execute(ToolCall(tool="document.answer", arguments={"query": request}))
            if tool_res.ok:
                return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        if self.store is not None and answer_from_documents is not None:
            result = answer_from_documents(self.store, request)
            return AgentResult(self.name, True, result.get("answer", ""), raw=result)
        return AgentResult(self.name, True, "I don't have a document loaded. Upload one and ask me to extract or summarize it.")


class MemoryAgent:
    name = "memory_agent"

    def __init__(self, store=None):
        self.store = store

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        low = request.lower()
        if registry is not None and ToolCall is not None:
            if "remember" in low or "store" in low:
                tool_res = registry.execute(ToolCall(tool="memory.add", arguments={"text": request}))
                if tool_res.ok:
                    return AgentResult(self.name, True, tool_res.content or "Remembered.", raw=tool_res.data)
            tool_res = registry.execute(ToolCall(tool="memory.search", arguments={"query": request}))
            if tool_res.ok:
                return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        if self.store is not None:
            hits = self.store.query(request, k=3) if hasattr(self.store, "query") else []
            if hits:
                return AgentResult(self.name, True, "\n".join(h.get("text", "") for h in hits), raw=hits)
        return AgentResult(self.name, True, "Nothing in memory for that yet.")


class MainChatAgent:
    name = "main_chat_agent"

    def __init__(self, model=None, tokenizer=None, knowledge=None):
        self.model = model
        self.tokenizer = tokenizer
        self.knowledge = knowledge or {}

    def run(self, request: str, context: dict) -> AgentResult:
        low = (request or "").lower()
        if "what can you do" in low or "who are you" in low:
            return AgentResult(
                self.name, True,
                "I'm ORBIT — a local agent runtime. I can calculate, search the web, "
                "run sandboxed Python, work with documents, and remember facts across turns.",
            )
        if "what is my name" in low:
            name = (context or {}).get("session", {}).get("name")
            if name:
                return AgentResult(self.name, True, f"Your name is {name}.")
            return AgentResult(self.name, True, "I don't know your name yet. Tell me and I'll remember.")
        m = re.search(r"my name is\s+(\w+)", request or "", re.I)
        if m:
            if context is not None:
                context.setdefault("session", {})["name"] = m.group(1)
            return AgentResult(self.name, True, f"I'll remember your name is {m.group(1)}.")
        return AgentResult(
            self.name, True,
            "I'm here. Ask me to calculate, search, run code, or work with a document.",
        )


class Orchestrator:
    """Routes requests to specialized agents; meters tool usage."""

    def __init__(self, chat_model=None, chat_tokenizer=None, sandbox_root: str = "."):
        self.chat_model = chat_model
        self.chat_tokenizer = chat_tokenizer
        self.sandbox_root = sandbox_root
        self._session: Dict[str, Any] = {}
        try:
            self.memory = VectorStore()
        except Exception:
            self.memory = None
        try:
            self.documents = DocumentStore()
        except Exception:
            self.documents = None
        try:
            self.conversations = ConversationStore()
        except Exception:
            self.conversations = None
        try:
            self.tools = default_registry("SAFE") if default_registry else None
        except Exception:
            self.tools = None
        self.agents = {
            "coding_agent": CodeAgent(),
            "research_agent": ResearchAgent(),
            "calculator_agent": CalculatorAgent(),
            "data_agent": DataAgent(),
            "debug_agent": DebugAgent(),
            "document_agent": DocumentAgent(self.documents),
            "memory_agent": MemoryAgent(self.memory),
            "main_chat_agent": MainChatAgent(chat_model, chat_tokenizer),
        }

    def handle(self, message: str, conversation_id: str = None, text: str = None) -> dict:
        raw = message if message is not None else (text or "")
        low = raw.lower()
        ctx = {"tools": self.tools, "session": self._session}

        named = re.search(r"my name is\s+(\w+)", raw, flags=re.IGNORECASE)
        if named:
            self._session["name"] = named.group(1)
            return {"ok": True, "content": f"I'll remember your name is {named.group(1)}.", "agent": "main_chat_agent"}

        if "what is my name" in low:
            name = self._session.get("name")
            if name:
                return {"ok": True, "content": f"Your name is {name}.", "agent": "main_chat_agent"}
            return {"ok": True, "content": "I don't know your name yet.", "agent": "main_chat_agent"}

        if any(k in low for k in ("traceback", "exception", "error type", "diagnose")):
            r = self.agents["debug_agent"].run(raw, ctx)
            return {"ok": r.ok, "content": r.content, "agent": r.agent, "raw": r.raw}

        if any(c.isdigit() for c in raw) and any(op in raw for op in "+-*/^="):
            r = self.agents["calculator_agent"].run(raw, ctx)
            return {"ok": r.ok, "content": r.content, "agent": r.agent, "raw": r.raw}

        if "```" in raw or "run this" in low or "execute" in low:
            r = self.agents["coding_agent"].run(raw, ctx)
            return {"ok": r.ok, "content": r.content, "agent": r.agent, "raw": r.raw}

        if any(k in low for k in ("search", "look up", "who is", "latest news")):
            r = self.agents["research_agent"].run(raw, ctx)
            return {"ok": r.ok, "content": r.content, "agent": r.agent, "raw": r.raw}

        if any(k in low for k in ("document", "pdf", "docx", "summarize", "extract")):
            r = self.agents["document_agent"].run(raw, ctx)
            return {"ok": r.ok, "content": r.content, "agent": r.agent, "raw": r.raw}

        if any(k in low for k in ("remember", "recall", "memory")):
            r = self.agents["memory_agent"].run(raw, ctx)
            return {"ok": r.ok, "content": r.content, "agent": r.agent, "raw": r.raw}

        r = self.agents["main_chat_agent"].run(raw, ctx)
        return {"ok": r.ok, "content": r.content, "agent": r.agent}

    def metrics(self) -> dict:
        tools_m = {}
        if self.tools is not None and hasattr(self.tools, "metrics"):
            try:
                tools_m = self.tools.metrics()
            except Exception:
                tools_m = {}
        return {"tools": tools_m, "session_keys": list(self._session.keys())}
