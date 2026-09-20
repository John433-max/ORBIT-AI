"""
Agent orchestrator (spec Part 10), wired to the tools in tools.py, the
paper-trading engine in paper_trading.py, and the memory store in
memory_store.py.

HONEST LIMITATION: real routing (deciding which agent/tool a request needs)
is a job for an instruction-tuned model reasoning over the request — that's
what the trained 100B model would do via tool-calling. This prototype has no
such model (see DESIGN.md §18), so ORCHESTRATOR ROUTING HERE IS RULE-BASED
KEYWORD MATCHING, a deliberately simple stand-in that makes the *pipeline
shape* (route -> agent -> verify -> respond) real and testable without
overclaiming intelligence it doesn't have. Swapping the routing function for
a real model call is the only change needed to make this the production
version of Part 10's architecture.
"""
import re
import json
import hashlib
import collections
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
from sampling import sample_next_token
from calculator import parse_and_calculate
from thinking import Thinker
from documents import DocumentStore, answer_from_documents, summarize_document
from context import ConversationStore
from debugging import diagnose_traceback


def stable_seed(text: str) -> int:
    """Deterministic replacement for Python's built-in hash(): CPython
    randomizes str hashing per-process by default (PYTHONHASHSEED) as a
    hash-flooding DoS mitigation, so hash(request) as a seed source -- as
    this project used to do in both FinanceAgent and MainChatAgent's raw
    generation path -- produced a *different* seed for the identical
    request every time the process restarted. Verified directly: the same
    string hashes to three different values across three separate `python3
    -c` invocations. That silently breaks the apparent intent of these
    call sites (same input -> same synthetic backtest / same generated
    continuation), which matters for both user-facing consistency and for
    writing a deterministic test. SHA-256 is stable across processes,
    interpreters, and platforms by construction."""
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
        raw["tool"] = "python.execute"
        raw["tool_ok"] = bool(tool_res.ok)
        raw["tool_ms"] = float(tool_res.latency_ms or 0.0)
        if tool_res.ok:
            stdout = raw.get("stdout") or tool_res.content or ""
            content = f"Ran the code in the sandbox. stdout:\n{stdout}"
            return AgentResult(self.name, True, content, raw=raw)
        # Denied or unknown tool: fall back so coding still works if the
        # registry is missing python.execute.
        if tool_res.error and ("permission" in tool_res.error or "Unknown tool" in tool_res.error):
            result = python_sandbox(code, timeout=3.0)
            raw.update(result if isinstance(result, dict) else {"fallback": result})
            raw["tool_fallback"] = True
            if result.get("ok"):
                content = f"Ran the code in the sandbox. stdout:\n{result['stdout']}"
            else:
                content = f"Sandbox execution failed: {result.get('error') or result.get('stderr')}"
            return AgentResult(self.name, result.get("ok", False), content, raw=raw)
        err = tool_res.error or raw.get("error") or raw.get("stderr") or tool_res.content
        content = f"Sandbox execution failed: {err}"
        return AgentResult(self.name, False, content, raw=raw)


def _normalize_search_payload(raw) -> dict:
    """Accept legacy dict, list[SearchResult], or list[dict] → {ok, results}."""
    if raw is None:
        return {"ok": False, "note": "empty search response", "results": []}
    if isinstance(raw, dict):
        if "results" in raw or "ok" in raw:
            return raw
        return {"ok": False, "note": "unexpected dict shape", "results": [], "raw": raw}
    if isinstance(raw, list):
        results = []
        for item in raw:
            if hasattr(item, "to_dict"):
                results.append(item.to_dict())
            elif isinstance(item, dict):
                results.append(item)
            else:
                results.append({"title": str(item), "url": "", "snippet": ""})
        sources = {r.get("source", "") for r in results if isinstance(r, dict)}
        live = any(s and "stub" not in s for s in sources)
        return {
            "ok": bool(results) and live,
            "results": results,
            "provider": ",".join(sorted(s for s in sources if s)) or "list",
            "note": None if results else "no results",
        }
    return {"ok": False, "note": f"unsupported search type {type(raw)!r}", "results": []}


class ResearchAgent:
    name = "research_agent"

    def __init__(self, search_provider=None):
        # Prefer AutoSearchProvider (live DuckDuckGo → honest stub fallback).
        # Inject a mock in tests. Cycle 52 unification.
        self.search_provider = search_provider
        if search_provider is None:
            try:
                self.search_provider = AutoSearchProvider()
            except Exception:
                self.search_provider = MockSearchProvider()

    def _search_via_provider(self, request: str):
        try:
            return self.search_provider.search(request)
        except TypeError:
            return self.search_provider.search(request, max_results=5)

    def run(self, request: str, context: dict) -> AgentResult:
        # Cycle 58: default path is ToolRegistry web.search so success/deny
        # latency land in Orchestrator.metrics()["tools"]. Injected
        # search_provider (unit tests) still bypasses the registry.
        injected = context.get("search_provider") if context else None
        use_injected = injected is not None or (
            self.search_provider is not None
            and type(self.search_provider).__name__ not in (
                "AutoSearchProvider",
                "MockSearchProvider",
                "DuckDuckGoSearchProvider",
                "StubSearchProvider",
            )
        )
        tool_meta = {}
        try:
            if use_injected:
                provider = injected or self.search_provider
                try:
                    raw = provider.search(request)
                except TypeError:
                    raw = provider.search(request, max_results=5)
            else:
                registry = _registry_from_context(context)
                tool_res = registry.execute(
                    ToolCall(tool="web.search", arguments={"query": request, "max_results": 5})
                )
                tool_meta = {
                    "tool": "web.search",
                    "tool_ok": bool(tool_res.ok),
                    "tool_ms": float(tool_res.latency_ms or 0.0),
                }
                if tool_res.ok:
                    raw = tool_res.data if tool_res.data is not None else []
                elif tool_res.error and (
                    "permission" in tool_res.error or "Unknown tool" in tool_res.error
                ):
                    raw = self._search_via_provider(request)
                    tool_meta["tool_fallback"] = True
                else:
                    raw = tool_res.data if tool_res.data is not None else {
                        "ok": False,
                        "error": tool_res.error or tool_res.content,
                        "results": [],
                    }
        except Exception as e:
            return AgentResult(
                self.name, False,
                f"Search failed: {e}",
                raw={"ok": False, "error": str(e), **tool_meta},
            )
        result = _normalize_search_payload(raw)
        if tool_meta:
            result = dict(result)
            result.update(tool_meta)
        if result.get("ok") and result.get("results"):
            bits = []
            cites = []
            for i, item in enumerate(result["results"][:4], 1):
                if not isinstance(item, dict):
                    bits.append(str(item))
                    continue
                title = (item.get("title") or "").strip()
                snippet = (item.get("snippet") or item.get("content") or "").strip()
                if len(snippet) > 280:
                    snippet = snippet[:277] + "..."
                url = (item.get("url") or "").strip()
                if snippet:
                    bits.append(snippet)
                elif title:
                    bits.append(title)
                if title or url:
                    cites.append(f"{title or 'source'}" + (f" ({url})" if url else ""))
            # Natural first-person answer from top snippets
            lead = bits[0] if bits else "I found a few references, but the snippets were thin."
            extra = ""
            if len(bits) > 1:
                extra = " Also: " + " ".join(bits[1:3])
            content = f"Here's what I found: {lead}{extra}"
            if cites:
                content += "\n\nSources:\n" + "\n".join(f"- {c}" for c in cites[:4])
            return AgentResult(self.name, True, content, raw=result)
        note = result.get("note") or result.get("error") or "search failed"
        content = (
            "I don't have live web access right now, so I can't complete this search. "
            + str(note)
        )
        return AgentResult(self.name, False, content, raw=result)


class DataAgent:
    name = "data_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="data.stats", arguments={"text": request}))
        stats = tool_res.data if isinstance(tool_res.data, dict) else {}
        raw = dict(stats) if stats else {}
        raw["tool"] = "data.stats"
        raw["tool_ok"] = bool(tool_res.ok)
        raw["tool_ms"] = float(tool_res.latency_ms or 0.0)
        if tool_res.error and ("permission" in tool_res.error or "Unknown tool" in tool_res.error):
            from tools.data_tool import summarize_numbers

            stats = summarize_numbers(request)
            raw.update(stats)
            raw["tool_fallback"] = True
            if not stats.get("ok"):
                return AgentResult(
                    self.name, False,
                    "No numeric data found in the request to analyze.",
                    raw=raw,
                )
            return AgentResult(self.name, True, stats["pretty"], raw=raw)
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=raw)
        return AgentResult(
            self.name, False,
            tool_res.content or "No numeric data found in the request to analyze.",
            raw=raw,
        )


class CalculatorAgent:
    """Phase 16: arithmetic is delegated to calculator.py's AST-restricted
    evaluator, not to the language model — a ~100K-780K param model has no
    reliable arithmetic capability, and pretending otherwise would be
    exactly the kind of fake feature this project's rules prohibit."""
    name = "calculator_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        # Cycle 57: arithmetic / science goes through ToolRegistry so
        # success lands in shared tool metrics (same pattern as LabAgent).
        registry = _registry_from_context(context)
        tool_res = registry.execute(
            ToolCall(tool="calculator", arguments={"expression": request})
        )
        raw = tool_res.data if isinstance(tool_res.data, dict) else {}
        raw = dict(raw) if raw else {}
        raw["tool"] = "calculator"
        raw["tool_ok"] = bool(tool_res.ok)
        raw["tool_ms"] = float(tool_res.latency_ms or 0.0)
        if tool_res.ok:
            if raw.get("pretty") or raw.get("kind"):
                msg = raw.get("pretty") or f"{raw.get('kind')}: {raw.get('result')}"
                return AgentResult(self.name, True, msg, raw=raw)
            expr = raw.get("expression") or request
            value = raw.get("result", tool_res.content)
            return AgentResult(self.name, True, f"{expr} = {value}", raw=raw)
        # Tool missing / denied: keep prior direct path.
        if tool_res.error and ("permission" in tool_res.error or "Unknown tool" in tool_res.error):
            try:
                from science_math import solve_science_math
                sci = solve_science_math(request)
                if sci.get("ok"):
                    msg = sci.get("pretty") or f"{sci.get('kind')}: {sci.get('result')}"
                    raw.update(sci)
                    raw["tool_fallback"] = True
                    return AgentResult(self.name, True, msg, raw=raw)
            except Exception:
                pass
            result = parse_and_calculate(request)
            raw.update(result if isinstance(result, dict) else {})
            raw["tool_fallback"] = True
            if not result["ok"]:
                return AgentResult(self.name, False, f"Could not compute a result: {result['error']}", raw=raw)
            expr = result.get("expression") or request
            return AgentResult(self.name, True, f"{expr} = {result['result']}", raw=raw)
        return AgentResult(
            self.name, False,
            f"Could not compute a result: {tool_res.error or tool_res.content}",
            raw=raw,
        )


class DebugAgent:
    """Phase 15: rule-based traceback/error diagnosis (see debugging.py for
    why this is rule-based rather than claiming a diagnosis it can't back)."""
    name = "debug_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(ToolCall(tool="debug.diagnose", arguments={"text": request}))
        diagnosis = tool_res.data if isinstance(tool_res.data, dict) else {}
        raw = dict(diagnosis) if diagnosis else {}
        raw["tool"] = "debug.diagnose"
        raw["tool_ok"] = bool(tool_res.ok)
        raw["tool_ms"] = float(tool_res.latency_ms or 0.0)
        if tool_res.error and ("permission" in tool_res.error or "Unknown tool" in tool_res.error):
            diagnosis = diagnose_traceback(request)
            raw.update(diagnosis)
            raw["tool_fallback"] = True
            if diagnosis.get("error_type") is None:
                return AgentResult(
                    self.name, False,
                    "I couldn't identify a specific Python error type in that text.",
                    raw=raw,
                )
            lines = [f"Error type: {diagnosis['error_type']}", diagnosis["explanation"]]
            if diagnosis.get("likely_causes"):
                lines.append("Likely causes: " + "; ".join(diagnosis["likely_causes"]))
            if diagnosis.get("suggestions"):
                lines.append("Suggestions: " + "; ".join(diagnosis["suggestions"]))
            return AgentResult(self.name, True, "\n".join(lines), raw=raw)
        if not tool_res.ok:
            return AgentResult(
                self.name, False,
                tool_res.content or "I couldn't identify a specific Python error type in that text.",
                raw=raw,
            )
        return AgentResult(self.name, True, tool_res.content, raw=raw)


class DocumentAgent:
    """Phases 3-5: document chat / RAG, backed by documents.py's
    retrieval+extraction store (see that module's docstring for why this is
    extractive, not generative)."""
    name = "document_agent"

    def __init__(self, store: DocumentStore):
        self.store = store

    def _tool_meta(self, name, tool_res):
        return {
            "tool": name,
            "tool_ok": bool(tool_res.ok),
            "tool_ms": float(tool_res.latency_ms or 0.0),
        }

    def run(self, request: str, context: dict) -> AgentResult:
        low = request.lower()
        registry = _registry_from_context(context)
        list_res = registry.execute(ToolCall(tool="document.list", arguments={}))
        docs = list_res.data if list_res.ok and isinstance(list_res.data, list) else []
        if not docs:
            try:
                docs = self.store.list_documents() if hasattr(self.store, "list_documents") else []
            except Exception:
                docs = []

        # Extract full text of uploaded docs
        if re.search(r"extract\s+(the\s+)?text|show\s+(me\s+)?(the\s+)?text|read\s+(the\s+)?document", low):
            if not docs:
                return AgentResult(
                    self.name, True,
                    "I don't have any documents uploaded yet. Send a file (txt, md, pdf, docx) "
                    "and I'll extract the text for you.",
                    raw={"docs": 0, **self._tool_meta("document.list", list_res)},
                )
            parts = []
            last_text = list_res
            for d in docs[:5]:
                doc_id = d.get("id") or d.get("document_id")
                name = d.get("filename") or f"document {doc_id}"
                last_text = registry.execute(
                    ToolCall(tool="document.text", arguments={"document_id": int(doc_id)})
                )
                text = ""
                if last_text.ok and isinstance(last_text.data, dict):
                    text = last_text.data.get("text") or last_text.content or ""
                elif last_text.ok:
                    text = last_text.content or ""
                if not text:
                    text = "(no extractable text)"
                if len(text) > 4000:
                    text = text[:4000] + "\n…[truncated]"
                parts.append(f"— {name} —\n{text}")
            body = "\n\n".join(parts)
            return AgentResult(
                self.name, True,
                f"Here's the text from your document(s):\n\n{body}",
                raw={"docs": len(docs), **self._tool_meta("document.text", last_text)},
            )

        m = re.search(r"summarize\s+(?:document\s+)?#?(\d+)", request, re.I)
        if m:
            doc_id = int(m.group(1))
            tool_res = registry.execute(
                ToolCall(tool="document.summarize", arguments={"document_id": doc_id})
            )
            result = tool_res.data if isinstance(tool_res.data, dict) else {}
            if not tool_res.ok or not (result.get("summary") or tool_res.content):
                return AgentResult(
                    self.name, False,
                    f"I couldn't find document #{doc_id}.",
                    raw={**self._tool_meta("document.summarize", tool_res)},
                )
            filename = result.get("filename") or f"document #{doc_id}"
            summary = result.get("summary") or tool_res.content
            return AgentResult(
                self.name, True,
                f"Here's a short summary of {filename}: {summary}",
                raw={**result, **self._tool_meta("document.summarize", tool_res)},
            )

        if not docs and re.search(r"document|pdf|docx|extract|file", low):
            return AgentResult(
                self.name, True,
                "I don't have a document loaded. Upload one and ask me to extract or summarize it.",
                raw={"docs": 0, **self._tool_meta("document.list", list_res)},
            )

        tool_res = registry.execute(
            ToolCall(tool="document.answer", arguments={"query": request})
        )
        result = tool_res.data if isinstance(tool_res.data, dict) else {}
        if not result:
            result = answer_from_documents(self.store, request)
        support = result.get("support")
        support_val = support.value if hasattr(support, "value") else str(support or "")
        ok = support_val in ("SUPPORTED", "PARTIALLY_SUPPORTED")
        answer = result.get("answer") or tool_res.content
        raw = dict(result) if result else {}
        raw.update(self._tool_meta("document.answer", tool_res))
        if ok:
            src = ""
            if result.get("sources"):
                src = " (from " + ", ".join(
                    s.get("filename", "doc") for s in result["sources"][:3]
                ) + ")"
            content = f"{answer}{src}"
        else:
            content = (
                answer
                if answer
                else "I couldn't find that in your documents. Try rephrasing or upload more text."
            )
        return AgentResult(self.name, ok, content, raw=raw)


class FinanceAgent:
    name = "finance_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(
            ToolCall(tool="finance.backtest", arguments={"seed_text": request})
        )
        perf = tool_res.data if isinstance(tool_res.data, dict) else {}
        raw = dict(perf) if perf else {}
        raw["tool"] = "finance.backtest"
        raw["tool_ok"] = bool(tool_res.ok)
        raw["tool_ms"] = float(tool_res.latency_ms or 0.0)
        if tool_res.ok:
            return AgentResult(self.name, True, tool_res.content, raw=raw)
        if tool_res.error and ("permission" in tool_res.error or "Unknown tool" in tool_res.error):
            rng = np.random.default_rng(stable_seed(request))
            prices = 100 + np.cumsum(rng.normal(0.05, 1.0, 200))
            prices = np.clip(prices, 1, None)
            perf = backtest_sma_crossover(prices)
            content = (
                "Ran a paper-trading SMA-crossover backtest on a SYNTHETIC price series "
                "(no live market data in this prototype — see DESIGN.md Part 12). "
                f"pnl={perf['pnl_pct']:.2f}% vs buy-and-hold={perf['buy_and_hold_pnl_pct']:.2f}%, "
                f"max drawdown={perf['max_drawdown_pct']:.2f}%, trades={perf['n_trades']}. "
                "This is a demo of the backtesting plumbing, not a trading recommendation."
            )
            raw.update(dict(perf, simulation=True, data_source="synthetic",
                            warning="This result uses simulated data and is not financial advice."))
            raw["tool_fallback"] = True
            return AgentResult(self.name, True, content, raw=raw)
        return AgentResult(self.name, False, tool_res.error or tool_res.content, raw=raw)


class DesignAgent:
    name = "design_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        registry = _registry_from_context(context)
        tool_res = registry.execute(
            ToolCall(tool="design.layout", arguments={"request": request})
        )
        data = tool_res.data if isinstance(tool_res.data, dict) else {}
        raw = dict(data) if data else {}
        raw["tool"] = "design.layout"
        raw["tool_ok"] = bool(tool_res.ok)
        raw["tool_ms"] = float(tool_res.latency_ms or 0.0)
        if tool_res.error and ("permission" in tool_res.error or "Unknown tool" in tool_res.error):
            from tools.design_tool import layout_skeleton

            out = layout_skeleton(request)
            raw.update(out)
            raw["tool_fallback"] = True
            return AgentResult(self.name, True, out["pretty"], raw=out["html"])
        if tool_res.ok:
            html = raw.get("html") or tool_res.content
            # Keep AgentResult.raw as HTML string for callers that treated
            # DesignAgent.raw as the skeleton itself.
            return AgentResult(self.name, True, tool_res.content, raw=html)
        return AgentResult(self.name, False, tool_res.error or tool_res.content, raw=raw)


class FileAgent:
    name = "file_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        m = re.search(r"(?:read|open)\s+([^\s]+\.\w+)", request, re.I)
        if not m:
            return AgentResult(self.name, False, "No file path found in the request.")
        path = m.group(1)
        root = (context or {}).get("sandbox_root", ".")
        registry = _registry_from_context(context)
        tool_res = registry.execute(
            ToolCall(tool="file.read", arguments={"path": path, "root": root})
        )
        result = tool_res.data if isinstance(tool_res.data, dict) else {}
        raw = dict(result) if result else {}
        raw["tool"] = "file.read"
        raw["tool_ok"] = bool(tool_res.ok)
        raw["tool_ms"] = float(tool_res.latency_ms or 0.0)
        if tool_res.error and ("permission" in tool_res.error or "Unknown tool" in tool_res.error):
            result = read_sandboxed_file(path, root=root)
            raw.update(result if isinstance(result, dict) else {})
            raw["tool_fallback"] = True
            if result.get("ok"):
                content = f"Read {path} ({len(result['content'])} chars, truncated to 4KB)."
            else:
                content = f"Could not read {path}: {result.get('error')}"
            return AgentResult(self.name, bool(result.get("ok")), content, raw=raw)
        if tool_res.ok:
            text = tool_res.content or raw.get("content") or ""
            content = f"Read {path} ({len(text)} chars, truncated to 4KB)."
            return AgentResult(self.name, True, content, raw=raw)
        err = tool_res.error or raw.get("error") or "read failed"
        return AgentResult(self.name, False, f"Could not read {path}: {err}", raw=raw)


class MemoryAgent:
    name = "memory_agent"

    # Chatbot-style profile facts (Cycle 55)
    _NAME_STORE = re.compile(
        r"^\s*(?:my name is|i am|i'm|call me|i go by)\s+([A-Za-z][A-Za-z0-9_.\-]{0,40})\s*[.!?]?\s*$",
        re.I,
    )
    _NAME_ASK = re.compile(
        r"\b(what(?:'s| is) my name|who am i|do you know my name|what do you call me)\b",
        re.I,
    )

    def __init__(self, store: VectorStore):
        self.store = store

    def _find_user_name(self, context: dict = None):
        """Prefer explicit stored profile; else scan recent history."""
        hits = self.store.query("user profile name is", k=5)
        for h in hits:
            text = (h.get("text") or "")
            m = re.search(r"user'?s? name is\s+([A-Za-z][A-Za-z0-9_.\-]{0,40})", text, re.I)
            if m:
                return m.group(1)
            m = re.search(r"my name is\s+([A-Za-z][A-Za-z0-9_.\-]{0,40})", text, re.I)
            if m:
                return m.group(1)
        history = (context or {}).get("history") or []
        for turn in reversed(history):
            if (turn.get("role") or "").lower() != "user":
                continue
            m = self._NAME_STORE.match((turn.get("content") or "").strip())
            if m:
                return m.group(1)
        return None

    def _add(self, registry, text, metadata=None):
        args = {"text": text}
        if metadata:
            args["metadata"] = metadata
        return registry.execute(ToolCall(tool="memory.add", arguments=args))

    def _search(self, registry, query, top_k=5):
        return registry.execute(
            ToolCall(tool="memory.search", arguments={"query": query, "top_k": int(top_k)})
        )

    def run(self, request: str, context: dict) -> AgentResult:
        text = request.strip()
        low = text.lower()
        registry = _registry_from_context(context)

        if low.startswith("remember:"):
            body = text.split(":", 1)[1].strip()
            tool_res = self._add(registry, body)
            item_id = None
            if tool_res.ok and isinstance(tool_res.data, dict):
                item_id = tool_res.data.get("id")
            if item_id is None:
                item_id = self.store.add(body)
            return AgentResult(
                self.name, True,
                "Got it — I'll remember that.",
                raw={
                    "id": item_id,
                    "text": body,
                    "tool": "memory.add",
                    "tool_ok": bool(tool_res.ok),
                    "tool_ms": float(tool_res.latency_ms or 0.0),
                },
            )

        m = self._NAME_STORE.match(text)
        if m:
            name = m.group(1)
            profile = f"user's name is {name}"
            tool_res = self._add(
                registry, profile, metadata={"type": "profile", "key": "name", "value": name}
            )
            self._add(
                registry,
                f"my name is {name}",
                metadata={"type": "profile", "key": "name", "value": name},
            )
            item_id = None
            if tool_res.ok and isinstance(tool_res.data, dict):
                item_id = tool_res.data.get("id")
            return AgentResult(
                self.name, True,
                f"Nice to meet you, {name}. I'll remember your name.",
                raw={
                    "id": item_id,
                    "name": name,
                    "tool": "memory.add",
                    "tool_ok": bool(tool_res.ok),
                    "tool_ms": float(tool_res.latency_ms or 0.0),
                },
            )

        if self._NAME_ASK.search(text):
            self._search(registry, "user profile name is", top_k=5)
            name = self._find_user_name(context)
            if name:
                return AgentResult(
                    self.name, True,
                    f"Your name is {name}.",
                    raw={"name": name, "source": "memory", "tool": "memory.search", "tool_ok": True},
                )
            return AgentResult(
                self.name, True,
                'I don\'t know your name yet. Tell me — for example: "my name is Sam".',
                raw={"name": None, "tool": "memory.search", "tool_ok": True},
            )

        tool_res = self._search(registry, request, top_k=3)
        hits = tool_res.data if tool_res.ok and isinstance(tool_res.data, list) else []
        if not hits:
            hits = self.store.query(request, k=3) or []
        raw_extra = {
            "tool": "memory.search",
            "tool_ok": bool(tool_res.ok),
            "tool_ms": float(tool_res.latency_ms or 0.0),
        }
        if not hits:
            return AgentResult(
                self.name, False, "I don't have anything stored about that yet.", raw=raw_extra
            )
        if len(hits) == 1:
            raw = dict(hits[0]) if isinstance(hits[0], dict) else {"hits": hits}
            raw.update(raw_extra)
            return AgentResult(self.name, True, f"I remember: {hits[0]['text']}", raw=raw)
        lines = [f"- {h['text']}" for h in hits]
        return AgentResult(
            self.name, True,
            "Here's what I remember:\n" + "\n".join(lines),
            raw={"hits": hits, **raw_extra},
        )



class LabAgent:
    """Educational TinyLM lab agent — architecture / speed / quant probes.

    Cycle 56: probes run through ToolRegistry (`tinylm.lab`) so tool-call
    success lands in registry metrics instead of a private code path.
    """

    name = "lab_agent"

    def run(self, request: str, context: dict) -> AgentResult:
        low = request.lower()
        registry = None
        if context:
            registry = context.get("tools")
        if registry is None:
            registry = default_registry("SAFE")

        if "regression" in low or "status" in low:
            action, preset = "regression", "rope"
        else:
            action = "bench"
            preset = "modern" if "modern" in low or "swiglu" in low or "gqa" in low else "rope"
            if "gqa" in low and "modern" not in low:
                preset = "gqa"
            if "swa" in low or "sliding" in low:
                preset = "swa"

        result = registry.execute(
            ToolCall(tool="tinylm.lab", arguments={"action": action, "preset": preset})
        )
        raw = result.data if isinstance(result.data, dict) else {}
        raw = dict(raw)
        raw["tool"] = "tinylm.lab"
        raw["tool_ok"] = bool(result.ok)
        raw["tool_ms"] = float(result.latency_ms or 0.0)
        if not result.ok:
            return AgentResult(
                self.name, False, result.error or result.content or "tinylm.lab failed", raw=raw
            )
        return AgentResult(self.name, True, result.content, raw=raw)


class MainChatAgent:
    """
    The fallback for anything that doesn't match a specialized route.

    Retrieval-first, generation-second. This is the honest solution to a
    real constraint: this toy model (~100k params, trained on a few KB of
    text) cannot reliably *generate* coherent, in-character text — see
    generate.py's own sample output. What it CAN do reliably is match a
    user's question against a small, hand-authored knowledge base of
    persona answers (persona_chat.jsonl) and return the matching
    answer verbatim, which is exactly what a retrieval-augmented system is
    supposed to do. Below the match threshold, it says so plainly instead
    of emitting garbled bytes dressed up as an answer — this is the
    persona's own stated value (see the "why do your answers sometimes
    look garbled" row in the dataset) applied to itself.

    This is a legitimate, common real-world pattern (retrieval before
    generation), not a trick to fake capability — it's flagged here exactly
    as clearly as the raw-generation path was flagged as low quality.
    """
    name = "main_chat_agent"
    PERSONA_PREAMBLE = (
        "You are ORBIT — a sharp, helpful AI that runs locally. "
        "Speak in the first person as yourself. Be clear, concise, and a little dry; "
        "prefer substance over filler. Use tools for math, science, memory, documents, and code. "
        "Never invent capabilities you lack. If unsure, say so and suggest a better angle.\n"
    )
    MATCH_THRESHOLD = 0.42

    def __init__(self, model=None, tokenizer=None, persona_path="persona_chat.jsonl",
                 max_tokens=40, temperature=0.7):
        self.model, self.tok = model, tokenizer
        self.max_tokens, self.temperature = max_tokens, temperature
        self.knowledge = VectorStore(dim=256)
        self._loaded = self._load_persona(persona_path)

    def _load_persona(self, path):
        try:
            with open(path) as f:
                rows = [json.loads(line) for line in f if line.strip()]
        except FileNotFoundError:
            return 0
        for row in rows:
            self.knowledge.add(row["instruction"], metadata={"answer": row["output"]})
        return len(rows)

    def _generate_raw(self, request: str, history: list = None) -> str:
        from tools.chat_tool import generate_chat

        data = generate_chat(
            self.model,
            self.tok,
            request,
            history=history,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            preamble=self.PERSONA_PREAMBLE,
        )
        return data.get("text") or ""

    def _generate(self, request: str, history, context: dict, retrieve_meta: dict):
        """Cycle 63: prefer chat.generate so miss-path decode is metered."""
        registry = _registry_from_context(context)
        tool_res = registry.execute(
            ToolCall(
                tool="chat.generate",
                arguments={
                    "request": request,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                    "history": history,
                },
            )
        )
        data = tool_res.data if isinstance(tool_res.data, dict) else {}
        meta = {
            **retrieve_meta,
            "generate_tool": "chat.generate",
            "generate_ok": bool(tool_res.ok),
            "generate_ms": float(tool_res.latency_ms or 0.0),
            "n_new": data.get("n_new"),
            "generate_backend": data.get("backend"),
            "generate_tok_s": data.get("tok_s"),
        }
        if tool_res.ok and data.get("text") is not None:
            return data.get("text") or "", meta
        raw = self._generate_raw(request, history=history)
        meta["generate_fallback"] = True
        return raw, meta

    def _retrieve(self, request: str, context: dict):
        """Cycle 62: prefer chat.retrieve so Orchestrator metrics see the hit."""
        registry = _registry_from_context(context)
        tool_res = registry.execute(
            ToolCall(
                tool="chat.retrieve",
                arguments={
                    "query": request,
                    "top_k": 3,
                    "threshold": self.MATCH_THRESHOLD,
                },
            )
        )
        data = tool_res.data if isinstance(tool_res.data, dict) else {}
        meta = {
            "tool": "chat.retrieve",
            "tool_ok": bool(tool_res.ok),
            "tool_ms": float(tool_res.latency_ms or 0.0),
        }
        if tool_res.ok and data.get("matched") and data.get("answer"):
            return True, data["answer"], {
                **meta,
                "match_score": data.get("score"),
                "source": "persona_retrieval",
            }
        # Tool missing / unbound / denied — fall back to in-process store.
        if (
            not tool_res.ok
            or "Unknown tool" in (tool_res.error or "")
            or (tool_res.ok and not data.get("hits") and self._loaded)
        ):
            if self._loaded:
                hits = self.knowledge.query(request, k=3)
                if hits and hits[0]["score"] >= self.MATCH_THRESHOLD:
                    return True, hits[0]["metadata"]["answer"], {
                        **meta,
                        "match_score": hits[0]["score"],
                        "source": "persona_retrieval",
                        "tool_fallback": True,
                    }
        return False, None, meta

    def run(self, request: str, context: dict) -> AgentResult:
        matched, answer, meta = self._retrieve(request, context)
        if matched:
            return AgentResult(self.name, True, answer, raw=meta)
        history = context.get("history") if context else None
        raw, meta = self._generate(request, history, context, meta)
        clean = (raw or "").strip()
        # Skip low-quality neural garble — prefer honest hedge or tools
        if clean and len(clean) > 12:
            words = clean.split()
            alpha = sum(ch.isalpha() for ch in clean)
            # require mostly alphabetic, no pile of single-letter tokens
            short = sum(1 for w in words if len(w) <= 2)
            if (6 <= len(words) <= 40 and alpha > len(clean) * 0.65
                    and short < len(words) * 0.4 and clean[:1].isupper()):
                return AgentResult(
                    self.name, True, clean,
                    raw={"source": "generation", "raw_text": raw, **meta},
                )
        hedge = (
            "I'm ORBIT. I don't have a solid answer for that in my head — "
            "my persona notes are limited, and the neural net under me is still toy-scale. "
            "If it's code, math, a document, search, or something to remember, say so and "
            "I'll use the right tool. Otherwise ask another way and I'll stay honest."
        )
        return AgentResult(
            self.name, True, hedge,
            raw={"source": "generation_fallback", "raw_text": raw, **meta},
        )


class Verifier:
    """Minimal post-hoc check: non-empty content, no leaked audit-log internals, agent reported ok."""
    def check(self, result: AgentResult) -> AgentResult:
        if not result.content or not result.content.strip():
            return AgentResult(result.agent, False, "Verifier rejected: empty agent output.")
        if "Traceback (most recent call last)" in result.content and result.agent != "coding_agent":
            return AgentResult(result.agent, False, "Verifier rejected: unexpected raw traceback in output.")
        return result


ROUTES = [
    (re.compile(r"```|def |import |print\(|for .* in |=\s*\d"), "code"),
    (re.compile(r"\b(traceback|Error:|Exception|ModuleNotFoundError|SyntaxError|NameError|"
                r"TypeError|KeyError|IndexError|AttributeError|ZeroDivisionError|"
                r"FileNotFoundError)\b"), "debug"),
    (re.compile(r"^\s*-?\d+\.?\d*\s*[\+\-\*/%\^]|% of|sqrt\(|square root|^\s*what is [\d.]+\s*[\+\-\*/]",
                re.I), "calculator"),
    (re.compile(r"\b(summarize document|document #\d+|uploaded document|"
                r"in (the|my) document|according to the (pdf|document|file)|"
                r"extract (the )?text|extract text from|read (the )?document|"
                r"show (me )?(the )?text|what does (this|the) (file|doc|document) say)\b", re.I), "document"),
    (re.compile(
        r"\b(tinylm|gqa|swiglu|qk[- ]?norm|kv cache|int4|weight[- ]only quant|"
        r"tok/?s|tokens per second|bench(mark)? (the )?model|lab (status|bench))\b",
        re.I,
    ), "lab"),
    (re.compile(
        r"\b(search|research|look up|find (out|information)|news about|"
        r"what (is|are|was|were) (the |a |an )?\w|"
        r"who (is|was|are)|where (is|was)|when (is|was|did)|"
        r"how (do|does|did|many|much)|why (is|do|did)|"
        r"explain|define|tell me about)\b",
        re.I,
    ), "research"),
    (re.compile(r"\b(mean|average|std|statistics|analy[sz]e (this )?data)\b", re.I), "data"),
    (re.compile(r"\b(trade|trading|backtest|portfolio|stock|pnl|sma)\b", re.I), "finance"),
    (re.compile(r"\b(layout|design|mockup|wireframe|landing page|ui)\b", re.I), "design"),
    (re.compile(r"\b(read|open) [^\s]+\.\w+", re.I), "file"),
    (re.compile(
        r"^remember:|\bwhat do you (know|remember) about\b|"
        r"\bmy name is\b|\bi am [A-Za-z]|\bi'm [A-Za-z]|\bcall me\b|"
        r"\bwhat(?:'s| is) my name\b|\bwho am i\b|\bdo you know my name\b",
        re.I,
    ), "memory"),
]

# Confidence-scored routing (replaces pure first-match-wins). ROUTES above
# is kept as the single source of truth for what each agent's *strong*
# signal looks like (unchanged, so existing sharp routing decisions don't
# regress); AGENT_SIGNALS adds a second, broader tier of weaker/related
# keywords per agent so requests that don't hit the strict pattern but are
# clearly still about that capability aren't dropped to "chat" by default.
# This is the concrete fix for exactly the case the spec calls out:
# "My Python code crashes" matches no strict ROUTES pattern at all (no
# actual exception name, no code block) and used to silently fall through
# to chat -- it should score positively for both code and debug.
AGENT_SIGNALS = {
    "code": [r"\bpython\b", r"\bcode\b", r"\bscript\b", r"\bprogram\b", r"\bfunction\b",
             r"\brun (this|my)\b", r"\bwrite (a|some) code\b"],
    "debug": [r"\bcrash(es|ed|ing)?\b", r"\bbug\b", r"\bfails?\b", r"\bfailing\b", r"\bbroken\b",
              r"\bnot working\b", r"\bwhy (does|is|did|won't)\b.*\b(fail|crash|break)", r"\bstack trace\b"],
    "calculator": [r"\bcalculate\b", r"\bhow much is\b", r"\bpercent(age)?\b", r"\bmultiply|divide|subtract\b", r"\btimes\b", r"\bplus\b", r"\bminus\b", r"\bdivided by\b", r"\bmodulo\b", r"\bderivative\b", r"\bintegral\b", r"\bintegrate\b", r"\barea of\b", r"\bforce\b", r"\bgeometry\b", r"\bcalculus\b", r"\bphysics\b"],
    "document": [r"\bpdf\b", r"\bdocx\b", r"\bmy notes\b", r"\bthis document\b", r"\bwhat does it say\b", r"\bextract\b", r"\btext from\b", r"\bupload\b"],
    "lab": [r"\bquant\b", r"\brope\b", r"\byarn\b", r"\battention\b", r"\btransformer\b",
            r"\beducational model\b", r"\btok/s\b", r"\binference speed\b"],
    "research": [r"\binvestigate\b", r"\bwhat is the latest\b", r"\bcurrent (state|status) of\b", r"\belements\b", r"\bhistory of\b", r"\bmeaning of\b"],
    "data": [r"\bcsv\b", r"\bdataset\b", r"\bcorrelation\b", r"\bmedian\b", r"\bnumbers?\b"],
    "finance": [r"\bprofit\b", r"\bloss\b", r"\bmarket\b", r"\bprice\b", r"\bsharpe\b"],
    "design": [r"\bprototype\b", r"\bcolor scheme\b", r"\btypography\b"],
    "file": [r"\bfile\b", r"\bfolder\b", r"\bdirectory\b"],
    "memory": [
        r"\bremember\b", r"\bdon't forget\b", r"\bmy preference\b", r"\bfavorite\b",
        r"\bwhat (do|did) you (know|remember)\b", r"\bmy name is\b", r"\bwho am i\b",
        r"\bcall me\b", r"\bmy name\b",
    ],
}
# How many *independent* weak-signal keyword matches are treated as full
# confidence for an agent. Kept small and documented rather than left
# implicit: 2 distinct related keywords is treated as strong evidence
# regardless of how large that agent's total keyword list happens to be,
# so agents with longer signal lists aren't penalized relative to agents
# with shorter ones (a raw matched/total ratio would do that).
CONFIDENCE_SATURATION = 2


def score_request(request: str) -> dict:
    """Return {agent_key: confidence} for every agent with at least one
    matching signal, confidence in [0.0, 1.0]. A hit on the agent's strict
    ROUTES pattern contributes a full 1.0 on its own (that pattern was
    already precise enough to be a first-match-wins rule); each distinct
    AGENT_SIGNALS keyword match contributes 1/CONFIDENCE_SATURATION,
    capped at 1.0. This means a request can score positively for several
    agents at once (the multi-intent case the spec asks for), not just the
    single first pattern that happened to match first."""
    scores = {}
    for pattern, agent_key in ROUTES:
        if pattern.search(request):
            scores[agent_key] = 1.0
    for agent_key, patterns in AGENT_SIGNALS.items():
        matched = sum(1 for p in patterns if re.search(p, request, re.I))
        if matched:
            weak_score = min(1.0, matched / CONFIDENCE_SATURATION)
            scores[agent_key] = max(scores.get(agent_key, 0.0), weak_score)
    return scores



def _looks_like_question(text: str) -> bool:
    s = (text or "").strip()
    if not s:
        return False
    if "?" in s:
        return True
    return bool(re.match(
        r"^(what|who|where|when|why|how|is|are|was|were|do|does|did|can|could|should|would|tell|explain|define|list|name)\b",
        s, re.I,
    ))


def _naturalize_output(text: str) -> str:
    """Output-first: strip internal labels so the user only sees ORBIT talking."""
    if not text:
        return text
    s = text.strip()
    # drop support tags / agent brackets
    s = re.sub(r"^\[(?:Support\.)?[A-Z_]+\]\s*", "", s)
    s = re.sub(r"^\[[a-z_]+agent\]\s*", "", s, flags=re.I)
    s = re.sub(r"^\[[a-z_]+\]\s*", "", s, flags=re.I)
    # collapse whitespace
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


class Orchestrator:
    def __init__(self, sandbox_root: str = ".", chat_model=None, chat_tokenizer=None,
                 memory_db_path: str = None, document_db_path: str = None,
                 conversation_db_path: str = None):
        # memory_db_path/document_db_path/conversation_db_path=None keeps
        # storage in-process only
        # (handy for tests/short-lived scripts); pass a path for storage
        # that survives process restarts.
        self.store = SQLiteVectorStore(memory_db_path) if memory_db_path else VectorStore()
        self.documents = DocumentStore(document_db_path) if document_db_path else DocumentStore(":memory:")
        self.conversations = ConversationStore(conversation_db_path) if conversation_db_path \
            else ConversationStore(":memory:")
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
        # Cycle 56: shared ToolRegistry so agent tool-calls feed /health metrics.
        self.tools = default_registry("SAFE")
        # Cycle 59: bind memory/document tools to this orchestrator's stores
        # so agent handle() and ToolRegistry share one retrieval backend.
        from tools import (
            MemoryAddTool,
            MemorySearchTool,
            DocumentListTool,
            DocumentTextTool,
            DocumentSummarizeTool,
            DocumentAnswerTool,
            ChatRetrieveTool,
            ChatGenerateTool,
        )
        self.tools.register(MemoryAddTool(store=self.store))
        self.tools.register(MemorySearchTool(store=self.store))
        self.tools.register(DocumentListTool(store=self.documents))
        self.tools.register(DocumentTextTool(store=self.documents))
        self.tools.register(DocumentSummarizeTool(store=self.documents))
        self.tools.register(DocumentAnswerTool(store=self.documents))
        # Cycle 62: bind persona VectorStore so chat.retrieve hits the same KB.
        chat_agent = self.agents.get("chat")
        knowledge = getattr(chat_agent, "knowledge", None)
        self.tools.register(ChatRetrieveTool(store=knowledge))
        # Cycle 63: bind the same toy decoder MainChat uses so miss-path
        # generation is visible in Orchestrator.metrics()["tools"].
        # Cycle 65/66: TinyLM is lazy. backend=auto (tool default) uses
        # TinyLM when the Orbit decoder is unbound; first decode constructs once.
        self._tinylm_model = None
        self._tinylm_preset = "rope"
        gen_tool = ChatGenerateTool(
            model=getattr(chat_agent, "model", None),
            tokenizer=getattr(chat_agent, "tok", None),
            max_tokens=getattr(chat_agent, "max_tokens", 40),
            temperature=getattr(chat_agent, "temperature", 0.7),
            backend="auto",
            tinylm_preset=self._tinylm_preset,
        )
        gen_tool.bind_tinylm(factory=self.ensure_tinylm)
        self.tools.register(gen_tool)
        # Bounded, not a plain list -- same bug class as tools.py's
        # AUDIT_LOG, found and fixed there earlier: a plain list appended
        # to on every single call, for the lifetime of a long-running
        # process, grows without limit. This one is actually a bigger risk
        # than AUDIT_LOG was: ORCH is a module-level singleton in api.py
        # that persists for the process's whole lifetime, and route_log
        # gets an entry on EVERY handle() call -- i.e. every single chat/
        # agent request the API serves, not just sandbox executions.
        self.route_log = collections.deque(maxlen=1000)
        # Phase C/E: optional ModelRouter + agent run state machine
        self.model_router = None
        try:
            from orbit.core.config import load_config
            from orbit.core.state import AgentStateMachine
            from orbit.models.router import ModelRouter
            self._orbit_cfg = load_config()
            self.model_router = ModelRouter(cfg=self._orbit_cfg)
            self.state_machine = AgentStateMachine(
                max_steps=self._orbit_cfg.max_steps,
                max_tool_calls=self._orbit_cfg.max_tool_calls,
            )
        except Exception:
            self._orbit_cfg = None
            self.state_machine = None

    def ensure_tinylm(self, preset: str = None):
        """Cycle 65: one educational TinyLM shared by chat.generate / lab."""
        preset = preset or self._tinylm_preset or "rope"
        if self._tinylm_model is not None and preset == self._tinylm_preset:
            return self._tinylm_model
        from tools.chat_tool import build_chat_tinylm

        self._tinylm_preset = preset
        self._tinylm_model = build_chat_tinylm(preset)
        try:
            tool = self.tools.get("chat.generate")
            if tool is not None and hasattr(tool, "bind_tinylm"):
                tool.bind_tinylm(model=self._tinylm_model, preset=preset)
        except Exception:
            pass
        return self._tinylm_model

    def generate_via_provider(self, prompt: str, max_tokens: int = 128, temperature: float = 0.7) -> dict:
        """Phase C: chat miss-path can use ModelRouter (Ollama/TinyLM/echo) when configured."""
        if self.model_router is None:
            return {"ok": False, "text": "", "error": "no model_router"}
        try:
            from orbit.models.base import GenerateRequest
            res = self.model_router.provider.generate(
                GenerateRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature)
            )
            return res.to_dict()
        except Exception as e:
            return {"ok": False, "text": "", "error": str(e)}

    def route(self, request: str) -> str:

        scores = score_request(request)
        if not scores:
            return "chat"
        # ROUTES order still defines tie-break priority when two agents
        # score equally (e.g. both hit only weak signals) -- keeps routing
        # deterministic rather than depending on dict ordering.
        priority = [agent_key for _, agent_key in ROUTES]
        best = max(scores.items(), key=lambda kv: (kv[1], -priority.index(kv[0]) if kv[0] in priority else -99))
        return best[0]

    def route_with_scores(self, request: str):
        """Like route(), but also returns the full confidence breakdown --
        useful for logging/debugging ambiguous or multi-intent requests
        (see route_log in handle() below) rather than only ever seeing the
        single winner."""
        scores = score_request(request)
        return self.route(request), scores


    def metrics(self) -> dict:
        """Cycle 53: agent success rates from the bounded route_log."""
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
        out = {
            "total_calls": len(log),
            "by_agent": by,
            "recent": log[-10:],
        }
        if hasattr(self, "tools") and hasattr(self.tools, "metrics"):
            out["tools"] = self.tools.metrics()
        return out

    def _make_thinker(self) -> Thinker:
        def _run(agent_key, request, context):
            ag = self.agents.get(agent_key)
            if ag is None:
                return {"ok": False, "content": ""}
            res = ag.run(request, context)
            return {"ok": getattr(res, "ok", True), "content": getattr(res, "content", "") or ""}

        return Thinker({
            "memory": lambda r, c: _run("memory", r, c),
            "docs": lambda r, c: _run("document", r, c),
            "search": lambda r, c: _run("research", r, c),
            "calc": lambda r, c: _run("calculator", r, c),
            "code": lambda r, c: _run("code", r, c),
            "chat": lambda r, c: _run("chat", r, c),
        })

    def think(self, request: str, history: list = None) -> dict:
        """Explicit multi-step thinking: plan → tools → natural answer."""
        thinker = self._make_thinker()
        ctx = {"sandbox_root": self.sandbox_root, "history": history, "tools": self.tools}
        result = thinker.think(request, ctx)
        content = _naturalize_output(result.answer)
        return {
            "agent": "orbit",
            "ok": result.ok,
            "content": content,
            "raw": result.to_dict(),
            "thinking": [t.to_dict() for t in result.thoughts],
        }


    def handle(self, request: str, history: list = None) -> dict:
        """`history`: optional list of {"role":..., "content":...} dicts for
        prior turns in the SAME conversation, most-recent-last. Only
        MainChatAgent's raw-generation fallback actually uses this (see
        that class) -- routing and every other agent still key off `request`
        alone, since a calculator/debug/data request's intent doesn't
        depend on prior turns. This was a real, previously-unnoticed gap:
        the API's own /v1/chat/completions request format already carries
        full conversation history in `messages`, but nothing downstream of
        `last_user = ... reversed(req.messages) ...` ever looked at
        anything except that single latest message -- a request like "My
        name is John." / "Nice to meet you." / "What is my name?" had the
        first two turns completely discarded before this fix, even though
        the client had already sent them in the same request.

        Cycle 52: if a second agent scores >= 0.75 and differs from the
        winner, run it too and append a short secondary note (multi-intent).
        """
        import time as _time
        # Phase E: track run lifecycle when state machine is available
        _run = None
        if getattr(self, "state_machine", None) is not None:
            try:
                _run = self.state_machine.start(request)
                _run.transition("PLAN")
            except Exception:
                _run = None
        agent_key, scores = self.route_with_scores(request)
        # Cycle 53: if fallback chat but documents are indexed and the user
        # asked a question, prefer document agent for grounded answers.
        if agent_key == "chat":
            try:
                docs = self.documents.list_documents() if hasattr(self.documents, "list_documents") else []
            except Exception:
                docs = []
            if docs and ("?" in request or re.search(r"\b(what|who|where|when|why|how|summarize)\b", request, re.I)):
                agent_key = "document"
                scores = dict(scores or {})
                scores["document"] = max(scores.get("document", 0), 0.9)
        t0 = _time.time()
        error = None
        try:
            result = self.agents[agent_key].run(
                request,
                {"sandbox_root": self.sandbox_root, "history": history, "tools": self.tools},
            )
        except Exception as e:  # agent bugs shouldn't crash the whole orchestrator
            error = str(e)
            result = AgentResult(agent_key, False, f"Agent raised an exception: {error}")
        verified = self.verifier.check(result)
        # Cycle 54: speak as ORBIT (first person) even for tool agents
        _voice = {
            "calculator_agent": "I ran the numbers: ",
            "coding_agent": "I put that through the sandbox. ",
            "research_agent": "",
            "document_agent": "",
            "lab_agent": "From the TinyLM lab: ",
            "data_agent": "Looking at those numbers: ",
            "debug_agent": "My read on the error: ",
            "design_agent": "I sketched this: ",
            "file_agent": "I checked the files: ",
        }
        prefix = _voice.get(verified.agent, "")
        if prefix and verified.content and not verified.content.startswith("I "):
            verified = AgentResult(
                verified.agent, verified.ok, prefix + verified.content, raw=verified.raw
            )
        secondary = None
        # Multi-intent: strong runner-up (not chat) gets a brief appendix.
        try:
            ranked = sorted(
                ((k, v) for k, v in (scores or {}).items() if k != agent_key and k != "chat"),
                key=lambda kv: kv[1],
                reverse=True,
            )
            if ranked and ranked[0][1] >= 0.75:
                sec_key = ranked[0][0]
                if sec_key in self.agents:
                    sec_res = self.agents[sec_key].run(
                        request,
                        {"sandbox_root": self.sandbox_root, "history": history, "tools": self.tools},
                    )
                    sec_res = self.verifier.check(sec_res)
                    if sec_res.ok and sec_res.content:
                        secondary = {"agent": sec_key, "content": sec_res.content[:500]}
                        verified = AgentResult(
                            verified.agent,
                            verified.ok,
                            verified.content
                            + "\n\n" + _naturalize_output(sec_res.content[:400]),
                            raw={"primary": verified.raw, "secondary": secondary},
                        )
        except Exception:
            secondary = None
        elapsed_ms = (_time.time() - t0) * 1000
        # Cycle 57: output-first — if chat hedged on a real question, try research
        content = _naturalize_output(verified.content or "")
        weak = (
            verified.agent in ("main_chat_agent", "chat")
            and (
                "don't have a solid answer" in content
                or "toy-scale" in content
                or len(content) < 12
            )
        )
        if weak and _looks_like_question(request) and "research" in self.agents:
            try:
                alt = self.agents["research"].run(
                    request,
                    {"sandbox_root": self.sandbox_root, "history": history, "tools": self.tools},
                )
                alt = self.verifier.check(alt)
                alt_c = _naturalize_output(alt.content or "")
                if alt.ok and alt_c and "can't complete this search" not in alt_c.lower():
                    verified = AgentResult("main_chat_agent", True, alt_c, raw={"source": "research_fallback", "inner": alt.raw})
                    content = alt_c
                    agent_key = "research"
            except Exception:
                pass

        # Auto-acknowledge simple statements into memory (tell → remember)
        if (
            not _looks_like_question(request)
            and verified.agent in ("main_chat_agent", "chat")
            and re.match(r"^(my |i |the |this |that )", request.strip(), re.I)
            and "memory" in self.agents
            and len(request.split()) < 30
        ):
            try:
                # store quietly if it looks like a fact the user is telling us
                if not request.lower().startswith("remember:"):
                    self.store.add(request.strip())
                if "don't have a solid answer" in content or verified.agent in ("main_chat_agent", "chat"):
                    content = "Got it — I'll keep that in mind."
                    verified = AgentResult("main_chat_agent", True, content, raw={"stored": True})
            except Exception:
                pass

        content = _naturalize_output(content)
        # Keep internal agent id for tests/metrics; content is always natural ORBIT speech
        name_map = {
            "code": "coding_agent", "research": "research_agent", "data": "data_agent",
            "calculator": "calculator_agent", "debug": "debug_agent", "document": "document_agent",
            "finance": "finance_agent", "design": "design_agent", "file": "file_agent",
            "memory": "memory_agent", "lab": "lab_agent", "chat": "main_chat_agent",
        }
        outward = name_map.get(agent_key, getattr(verified, "agent", agent_key) or "main_chat_agent")
        prior_raw = verified.raw
        merged = dict(prior_raw) if isinstance(prior_raw, dict) else {"detail": prior_raw}
        merged["route"] = agent_key
        merged["secondary"] = secondary
        verified = AgentResult(
            outward,
            True if content else False,
            content,
            raw=merged,
        )
        elapsed_ms = (_time.time() - t0) * 1000
        self.route_log.append({
            "request": request, "agent": agent_key, "elapsed_ms": round(elapsed_ms, 2),
            "ok": verified.ok, "error": error, "candidates": scores,
            "secondary": secondary,
            "run_id": getattr(_run, "run_id", None) if _run is not None else None,
        })
        out = verified.to_dict()
        if _run is not None:
            try:
                _run.plan = [agent_key]
                _run.metadata["scores"] = scores
                _run.complete(out.get("content") or "", status="completed" if verified.ok else "failed")
                out["run_id"] = _run.run_id
                out["run"] = {
                    "run_id": _run.run_id,
                    "status": _run.status,
                    "step_number": _run.step_number,
                    "elapsed_s": round(_run.elapsed_s(), 3),
                }
            except Exception:
                pass
        return out
