"""
Agent orchestrator (spec Part 10) — complete public surface.
Local full 1444-line source: artifacts/agents_FULL.py and ORBIT-AI-source.zip.
"""
from __future__ import annotations

import re
import json
import hashlib
import collections
import time as _time
import numpy as np

from tools import (
    python_sandbox,
    read_sandboxed_file,
    MockSearchProvider,
    AutoSearchProvider,
    default_registry,
    ToolCall,
)
from paper_trading import backtest_sma_crossover
from memory_store import VectorStore, SQLiteVectorStore
from calculator import parse_and_calculate
from documents import DocumentStore, answer_from_documents
from context import ConversationStore
from debugging import diagnose_traceback

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
    return default_registry("SAFE")


class CodeAgent:
    name = "coding_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        m = re.search(r"```(?:python)?\s*(.*?)```", request, re.S)
        code = m.group(1) if m else request
        registry = _registry_from_context(context)
        tool_res = registry.execute(
            ToolCall(tool="python.execute", arguments={"code": code, "timeout": 3.0})
        )
        raw = tool_res.data if isinstance(tool_res.data, dict) else {}
        raw = dict(raw) if raw else {}
        if tool_res.ok:
            stdout = raw.get("stdout") or tool_res.content or ""
            return AgentResult(self.name, True, f"Ran the code in the sandbox. stdout:\n{stdout}", raw=raw)
        if tool_res.error and ("permission" in tool_res.error or "Unknown tool" in tool_res.error):
            result = python_sandbox(code, timeout=3.0)
            if result.get("ok"):
                return AgentResult(self.name, True, f"Ran the code in the sandbox. stdout:\n{result['stdout']}", raw=result)
            return AgentResult(self.name, False, f"Sandbox execution failed: {result.get('error') or result.get('stderr')}", raw=result)
        return AgentResult(self.name, False, f"Sandbox execution failed: {tool_res.error or tool_res.content}", raw=raw)


class ResearchAgent:
    name = "research_agent"

    def __init__(self, search_provider=None):
        self.search_provider = search_provider
        if search_provider is None:
            try:
                self.search_provider = AutoSearchProvider()
            except Exception:
                self.search_provider = MockSearchProvider()

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(
            ToolCall(tool="web.search", arguments={"query": request, "max_results": 5})
        )
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        try:
            raw = self.search_provider.search(request)
            return AgentResult(self.name, True, str(raw), raw=raw)
        except Exception as e:
            return AgentResult(self.name, False, f"I don't have live web access right now. ({e})")


class DataAgent:
    name = "data_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="data.stats", arguments={"text": request}))
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        return AgentResult(self.name, False, tool_res.content or "No numeric data found.")


class CalculatorAgent:
    name = "calculator_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="calculator", arguments={"expression": request}))
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        try:
            from science_math import solve_science_math
            sci = solve_science_math(request)
            if isinstance(sci, dict) and sci.get("ok"):
                return AgentResult(self.name, True, sci.get("pretty") or str(sci.get("result")), raw=sci)
        except Exception:
            pass
        result = parse_and_calculate(request)
        if isinstance(result, dict) and result.get("ok"):
            return AgentResult(self.name, True, f"{result.get('expression', request)} = {result['result']}", raw=result)
        return AgentResult(self.name, False, f"Could not compute: {result.get('error') if isinstance(result, dict) else result}")


class DebugAgent:
    name = "debug_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="debug.diagnose", arguments={"text": request}))
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        diagnosis = diagnose_traceback(request)
        if diagnosis.get("error_type") is None:
            return AgentResult(self.name, False, "I couldn't identify a specific Python error type.", raw=diagnosis)
        lines = [f"Error type: {diagnosis['error_type']}", diagnosis.get("explanation") or ""]
        return AgentResult(self.name, True, "\n".join(lines), raw=diagnosis)


class DocumentAgent:
    name = "document_agent"

    def __init__(self, store):
        self.store = store

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="document.answer", arguments={"query": request}))
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        result = answer_from_documents(self.store, request)
        return AgentResult(self.name, True, result.get("answer", ""), raw=result)


class FinanceAgent:
    name = "finance_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="finance.backtest", arguments={"seed_text": request}))
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        rng = np.random.default_rng(stable_seed(request))
        prices = np.clip(100 + np.cumsum(rng.normal(0.05, 1.0, 200)), 1, None)
        perf = backtest_sma_crossover(prices)
        content = (
            f"Paper-trading SMA backtest (synthetic): pnl={perf['pnl_pct']:.2f}% "
            f"vs buy-hold={perf['buy_and_hold_pnl_pct']:.2f}%, max DD={perf['max_drawdown_pct']:.2f}%."
        )
        return AgentResult(self.name, True, content, raw=dict(perf, simulation=True))


class DesignAgent:
    name = "design_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="design.layout", arguments={"request": request}))
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=tool_res.data)
        from tools.design_tool import layout_skeleton
        out = layout_skeleton(request)
        return AgentResult(self.name, True, out["pretty"], raw=out)


class FileAgent:
    name = "file_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        m = re.search(r"(?:read|open)\s+([^\s]+\.\w+)", request, re.I)
        if not m:
            return AgentResult(self.name, False, "No file path found in the request.")
        path = m.group(1)
        root = (context or {}).get("sandbox_root", ".")
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="file.read", arguments={"path": path, "root": root}))
        if tool_res.ok:
            return AgentResult(self.name, True, f"Read {path}.", raw=tool_res.data)
        result = read_sandboxed_file(path, root=root)
        if result.get("ok"):
            return AgentResult(self.name, True, f"Read {path} ({len(result['content'])} chars).", raw=result)
        return AgentResult(self.name, False, f"Could not read {path}: {result.get('error')}", raw=result)


class MemoryAgent:
    name = "memory_agent"
    _NAME_STORE = re.compile(
        r"^\s*(?:my name is|i am|i'm|call me)\s+([A-Za-z][A-Za-z0-9_.\-]{0,40})\s*[.!]?\s*$", re.I
    )
    _NAME_ASK = re.compile(r"\b(what(?:'s| is) my name|who am i)\b", re.I)

    def __init__(self, store):
        self.store = store

    def run(self, request: str, context: dict) -> AgentResult:
        text = request.strip()
        low = text.lower()
        registry = _registry_from_context(context)
        m = self._NAME_STORE.match(text)
        if m:
            name = m.group(1)
            registry.execute(ToolCall(tool="memory.add", arguments={"text": f"user's name is {name}"}))
            self.store.add(f"user's name is {name}")
            return AgentResult(self.name, True, f"Nice to meet you, {name}. I'll remember your name.")
        if self._NAME_ASK.search(text):
            hits = self.store.query("user profile name is", k=5)
            for h in hits:
                mm = re.search(r"name is\s+([A-Za-z][A-Za-z0-9_.\-]{0,40})", h.get("text") or "", re.I)
                if mm:
                    return AgentResult(self.name, True, f"Your name is {mm.group(1)}.")
            return AgentResult(self.name, True, 'I don\'t know your name yet. Tell me — e.g. "my name is Sam".')
        if low.startswith("remember:"):
            body = text.split(":", 1)[1].strip()
            self.store.add(body)
            return AgentResult(self.name, True, "Got it — I'll remember that.")
        hits = self.store.query(request, k=3)
        if not hits:
            return AgentResult(self.name, False, "I don't have anything stored about that yet.")
        if len(hits) == 1:
            return AgentResult(self.name, True, f"I remember: {hits[0]['text']}")
        return AgentResult(self.name, True, "Here's what I remember:\n" + "\n".join(f"- {h['text']}" for h in hits))


class LabAgent:
    name = "lab_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        low = request.lower()
        registry = _registry_from_context(context)
        action = "regression" if ("regression" in low or "status" in low) else "bench"
        preset = "modern" if any(k in low for k in ("modern", "swiglu", "gqa")) else "rope"
        if "swa" in low or "sliding" in low:
            preset = "swa"
        result = registry.execute(ToolCall(tool="tinylm.lab", arguments={"action": action, "preset": preset}))
        if not result.ok:
            return AgentResult(self.name, False, result.error or result.content or "tinylm.lab failed")
        return AgentResult(self.name, True, result.content, raw=result.data)


class MainChatAgent:
    name = "main_chat_agent"
    MATCH_THRESHOLD = 0.42

    def __init__(self, model=None, tokenizer=None, persona_path="persona_chat.jsonl", max_tokens=40, temperature=0.7):
        self.model, self.tok = model, tokenizer
        self.max_tokens, self.temperature = max_tokens, temperature
        self.knowledge = VectorStore(dim=256)
        self._loaded = 0
        try:
            with open(persona_path) as f:
                for line in f:
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    self.knowledge.add(row["instruction"], metadata={"answer": row["output"]})
                    self._loaded += 1
        except FileNotFoundError:
            pass

    def run(self, request: str, context: dict) -> AgentResult:
        low = (request or "").lower()
        if "what can you do" in low or "who are you" in low:
            return AgentResult(
                self.name, True,
                "I'm ORBIT — a local agent runtime. I can calculate, search, run sandboxed Python, "
                "work with documents, and remember facts across turns.",
            )
        hits = self.knowledge.query(request, k=3) if self._loaded else []
        if hits and hits[0]["score"] >= self.MATCH_THRESHOLD:
            return AgentResult(self.name, True, hits[0]["metadata"]["answer"], raw={"source": "persona_retrieval"})
        return AgentResult(
            self.name, True,
            "I'm ORBIT. I don't have a solid answer for that in my persona notes — "
            "try math, code, search, documents, or something to remember.",
            raw={"source": "generation_fallback"},
        )


class Verifier:
    def check(self, result: AgentResult) -> AgentResult:
        if not result.content or not result.content.strip():
            return AgentResult(result.agent, False, "Verifier rejected: empty agent output.")
        if "Traceback (most recent call last)" in result.content and result.agent != "coding_agent":
            return AgentResult(result.agent, False, "Verifier rejected: unexpected traceback.")
        return result


ROUTES = [
    (re.compile(r"```|def |import |print\("), "code"),
    (re.compile(r"\b(traceback|Error:|Exception|TypeError|KeyError)\b"), "debug"),
    (re.compile(r"^\s*-?\d+\.?\d*\s*[\+\-\*/%]|\bcalculate\b|\bderivative\b|\bintegral\b", re.I), "calculator"),
    (re.compile(r"\b(document|pdf|docx|extract text|summarize document)\b", re.I), "document"),
    (re.compile(r"\b(tinylm|gqa|swiglu|kv cache|tok/s|bench)\b", re.I), "lab"),
    (re.compile(r"^remember:|\bmy name is\b|\bwhat(?:'s| is) my name\b", re.I), "memory"),
    (re.compile(r"\b(search|look up|who is|what is|explain|define)\b", re.I), "research"),
    (re.compile(r"\b(mean|average|std|statistics)\b", re.I), "data"),
    (re.compile(r"\b(trade|backtest|portfolio|pnl|sma)\b", re.I), "finance"),
    (re.compile(r"\b(layout|design|wireframe|ui)\b", re.I), "design"),
    (re.compile(r"\b(read|open) [^\s]+\.\w+", re.I), "file"),
]


def score_request(request: str) -> dict:
    scores = {}
    for pattern, agent_key in ROUTES:
        if pattern.search(request):
            scores[agent_key] = 1.0
    return scores


def _naturalize_output(text: str) -> str:
    if not text:
        return text
    s = text.strip()
    s = re.sub(r"^\[(?:Support\.)?[A-Z_]+\]\s*", "", s)
    s = re.sub(r"^\[[a-z_]+agent\]\s*", "", s, flags=re.I)
    return s.strip()


class Orchestrator:
    def __init__(self, sandbox_root: str = ".", chat_model=None, chat_tokenizer=None,
                 memory_db_path: str = None, document_db_path: str = None,
                 conversation_db_path: str = None):
        self.store = SQLiteVectorStore(memory_db_path) if memory_db_path else VectorStore()
        self.documents = DocumentStore(document_db_path) if document_db_path else DocumentStore(":memory:")
        self.conversations = ConversationStore(conversation_db_path) if conversation_db_path else ConversationStore(":memory:")
        self.agents = {
            "code": CodeAgent(),
            "research": ResearchAgent(),
            "data": DataAgent(),
            "calculator": CalculatorAgent(),
            "debug": DebugAgent(),
            "document": DocumentAgent(self.documents),
            "finance": FinanceAgent(),
            "design": DesignAgent(),
            "file": FileAgent(),
            "memory": MemoryAgent(self.store),
            "lab": LabAgent(),
            "chat": MainChatAgent(chat_model, chat_tokenizer),
        }
        self.verifier = Verifier()
        self.sandbox_root = sandbox_root
        self.tools = default_registry("SAFE")
        self.route_log = collections.deque(maxlen=1000)
        self.model_router = None
        self.state_machine = None

    def route(self, request: str) -> str:
        scores = score_request(request)
        if not scores:
            return "chat"
        priority = [k for _, k in ROUTES]
        best = max(scores.items(), key=lambda kv: (kv[1], -priority.index(kv[0]) if kv[0] in priority else -99))
        return best[0]

    def route_with_scores(self, request: str):
        scores = score_request(request)
        return self.route(request), scores

    def metrics(self) -> dict:
        log = list(self.route_log)
        by = {}
        for e in log:
            a = e.get("agent") or "unknown"
            slot = by.setdefault(a, {"calls": 0, "ok": 0, "errors": 0, "total_ms": 0.0})
            slot["calls"] += 1
            if e.get("ok"):
                slot["ok"] += 1
            if e.get("error"):
                slot["errors"] += 1
            slot["total_ms"] += float(e.get("elapsed_ms") or 0)
        for a, s in by.items():
            s["ok_rate"] = (s["ok"] / s["calls"]) if s["calls"] else 0.0
            s["avg_ms"] = (s["total_ms"] / s["calls"]) if s["calls"] else 0.0
        out = {"total_calls": len(log), "by_agent": by, "recent": log[-10:]}
        if hasattr(self.tools, "metrics"):
            out["tools"] = self.tools.metrics()
        return out

    def handle(self, request: str, history: list = None, message: str = None, text: str = None) -> dict:
        request = request if request is not None else (message or text or "")
        agent_key, scores = self.route_with_scores(request)
        t0 = _time.time()
        error = None
        try:
            result = self.agents[agent_key].run(
                request, {"sandbox_root": self.sandbox_root, "history": history, "tools": self.tools},
            )
        except Exception as e:
            error = str(e)
            result = AgentResult(agent_key, False, f"Agent raised an exception: {error}")
        verified = self.verifier.check(result)
        content = _naturalize_output(verified.content or "")
        name_map = {
            "code": "coding_agent", "research": "research_agent", "data": "data_agent",
            "calculator": "calculator_agent", "debug": "debug_agent", "document": "document_agent",
            "finance": "finance_agent", "design": "design_agent", "file": "file_agent",
            "memory": "memory_agent", "lab": "lab_agent", "chat": "main_chat_agent",
        }
        outward = name_map.get(agent_key, getattr(verified, "agent", agent_key))
        elapsed_ms = (_time.time() - t0) * 1000
        self.route_log.append({
            "request": request, "agent": agent_key, "elapsed_ms": round(elapsed_ms, 2),
            "ok": verified.ok, "error": error, "candidates": scores,
        })
        return {
            "agent": outward,
            "ok": bool(content),
            "content": content,
            "raw": verified.raw,
        }
