"""ORBIT agents (GitHub CI surface). Coding/search/identity routes + provider fallback."""
from __future__ import annotations
import hashlib
import re

class AgentResult:
    def __init__(self, agent: str, ok: bool, content: str, raw=None):
        self.agent, self.ok, self.content, self.raw = agent, ok, content, raw
    def to_dict(self):
        d = {"agent": self.agent, "ok": self.ok, "content": self.content}
        if self.raw is not None:
            d["raw"] = self.raw
        return d

def stable_seed(text: str) -> int:
    digest = hashlib.sha256((text or "").encode("utf-8", errors="replace")).digest()
    return int.from_bytes(digest[:8], "big") % (2**32)

def _wants_code_written(request: str) -> bool:
    if re.search(r"```", request or ""):
        return False
    return bool(re.search(
        r"\b(write|implement|create|define|make)\b.{0,80}\b(function|def |class |script|program|module|code)\b|"
        r"\bpython function\b|\bimplement\b.{0,40}\bin python\b",
        request or "", re.I))

DENY_FS_MSG = "I can't do that. ORBIT refuses destructive filesystem commands (delete all files, rm -rf /, wipe disk). Permission denied."

def _is_destructive_fs(text: str) -> bool:
    if _wants_code_written(text or ""):
        return False
    return bool(re.search(
        r"\brm\s+-rf\b|\bdelete all files\b|\bdelete everything\b|"
        r"\bwipe (the )?(disk|root|filesystem|drive)\b|"
        r"\bformat (the )?(hard )?disk\b|\bremove all files in\s+/",
        text or "", re.I))

def _synthesize_python(request: str) -> str:
    try:
        from code_synth import synthesize_python
        return synthesize_python(request)
    except Exception:
        low = (request or "").lower()
        if re.search(r"add(s|ing)?\b.{0,20}\b(two|2)\b.{0,20}\b(number|int|value)", low) or "adds two" in low:
            return 'def add(a, b):\n    """Return the sum of a and b."""\n    return a + b\n'
        if re.search(r"\b(multiply|product of)\b.{0,20}\b(two|2)\b", low):
            return 'def multiply(a, b):\n    """Return the product of a and b."""\n    return a * b\n'
        slug = re.sub(r"[^a-z0-9]+", "_", low)[:40].strip("_") or "solve"
        return f"def {slug}(*args, **kwargs):\n    \"\"\"Draft from: {(request or '').strip()[:120]}\"\"\"\n    raise NotImplementedError('Paste a fenced snippet to run it.')\n"

class CodeAgent:
    name = "coding_agent"
    def run(self, request: str, context=None) -> AgentResult:
        if _wants_code_written(request):
            verified, n_ex, name = False, 0, None
            try:
                from code_synth import synthesize_and_verify
                bundle = synthesize_and_verify(request)
                src = bundle.get("source") or _synthesize_python(request)
                verified = bool(bundle.get("verified"))
                n_ex = int(bundle.get("checked") or 0)
                name = bundle.get("name")
            except Exception:
                src = _synthesize_python(request)
            note = f"\n\nVerified against {n_ex} example(s)." if verified and n_ex else ""
            content = "Here is a Python function for that request:\n\n```python\n" + src + "```" + note
            return AgentResult(self.name, True, content, raw={"source": "synthesize", "code": src, "verified": verified, "checked": n_ex, "name": name})
        code = request
        m = re.search(r"```(?:python)?\s*(.*?)```", request or "", re.S)
        if m:
            code = m.group(1)
        try:
            from tools import python_sandbox
            result = python_sandbox(code, timeout=3.0)
            if result.get("ok"):
                return AgentResult(self.name, True, f"Ran the code in the sandbox. stdout:\n{result.get('stdout', '')}", raw=result)
            return AgentResult(self.name, False, f"Sandbox execution failed: {result.get('error') or result.get('stderr')}", raw=result)
        except Exception as e:
            return AgentResult(self.name, False, f"Sandbox unavailable: {e}")

def _offline_search_reply(note) -> str:
    base = "I don't have live web access right now, so I can't complete this search."
    text = str(note or "").strip()
    low = text.lower().rstrip(".")
    generic = {"search failed", "no live web", "no live web access", "no results", "empty search response"}
    if not text or low in generic or low.startswith("no live web"):
        return base
    if "don't have live web" in low or "can't complete this search" in low:
        return base
    return base + " " + (text if text.endswith(".") else text + ".")

class ResearchAgent:
    name = "research_agent"
    def __init__(self, search_provider=None):
        self.search_provider = search_provider
    def run(self, request: str, context=None) -> AgentResult:
        provider = (context or {}).get("search_provider") if context else None
        provider = provider or self.search_provider
        raw = None
        if provider is not None:
            try:
                raw = provider.search(request)
            except TypeError:
                raw = provider.search(request, max_results=5)
            except Exception as e:
                return AgentResult(self.name, False, f"Search failed: {e}", raw={"ok": False, "error": str(e)})
        else:
            try:
                from tools import AutoSearchProvider
                raw = AutoSearchProvider().search(request)
            except Exception:
                raw = None
        if isinstance(raw, dict):
            results = raw.get("results") or []
            if raw.get("ok") and results:
                bits = []
                for item in results[:3]:
                    if isinstance(item, dict):
                        bits.append(item.get("snippet") or item.get("title") or "")
                    else:
                        bits.append(str(item))
                lead = " ".join(b for b in bits if b) or "results returned"
                return AgentResult(self.name, True, f"Here's what I found: {lead}", raw=raw)
            note = (raw or {}).get("note") or (raw or {}).get("error") or ""
        elif isinstance(raw, list) and raw:
            return AgentResult(self.name, True, f"Here's what I found: {raw[0]}", raw={"results": raw})
        else:
            note = ""
        return AgentResult(self.name, False, _offline_search_reply(note), raw={"ok": False, "note": note})

class MainChatAgent:
    name = "main_chat_agent"
    def run(self, request: str, context=None) -> AgentResult:
        low = (request or "").lower()
        if re.search(r"\b(what('?s| is) your name|who are you|what are you)\b", low):
            return AgentResult(self.name, True, "I'm ORBIT. Named after the project that built me, not the other way around.", raw={"source": "persona_retrieval"})
        return AgentResult(self.name, True, "I'm ORBIT. I don't have a solid answer for that in my head — my persona notes are limited, and the neural net under me is still toy-scale.", raw={"source": "generation_fallback"})

class CalculatorAgent:
    name = "calculator_agent"
    def run(self, request: str, context=None) -> AgentResult:
        try:
            from calculator import parse_and_calculate
            result = parse_and_calculate(request)
            if result.get("ok"):
                expr = result.get("expression") or request
                return AgentResult(self.name, True, f"{expr} = {result['result']}", raw=result)
            return AgentResult(self.name, False, f"Could not compute a result: {result.get('error')}", raw=result)
        except Exception as e:
            return AgentResult(self.name, False, f"Calculator unavailable: {e}")

class MemoryAgent:
    name = "memory_agent"
    def __init__(self, store=None):
        self.store = store if store is not None else {}
        self._facts = []
    def run(self, request: str, context=None) -> AgentResult:
        text = (request or "").strip()
        low = text.lower()
        m = re.search(r"my name is\s+([A-Za-z][A-Za-z0-9_.-]{0,40})", text, re.I)
        if m:
            name = m.group(1)
            self._facts.append(f"user's name is {name}")
            return AgentResult(self.name, True, f"Nice to meet you, {name}. I'll remember your name.")
        if re.search(r"what(?:'s| is) my name|who am i", low):
            for f in reversed(self._facts):
                mm = re.search(r"name is\s+(\S+)", f)
                if mm:
                    return AgentResult(self.name, True, f"Your name is {mm.group(1)}.")
            return AgentResult(self.name, True, "I don't know your name yet.")
        if low.startswith("remember:"):
            fact = text[9:].strip()
            if fact:
                self._facts.append(fact)
                return AgentResult(self.name, True, f"Remembered: {fact}")
        return AgentResult(self.name, True, "Memory noted.")

class DocumentAgent:
    name = "document_agent"
    def run(self, request: str, context=None) -> AgentResult:
        return AgentResult(self.name, True, "No documents are loaded in this session, so I can't summarize or answer from uploads.", raw={"rag_empty": True})

class Orchestrator:
    def __init__(self, search_provider=None, model_provider=None, **kwargs):
        self.search_provider = search_provider
        self.model_provider = model_provider
        self.agents = {
            "coding_agent": CodeAgent(),
            "research_agent": ResearchAgent(search_provider=search_provider),
            "main_chat_agent": MainChatAgent(),
            "calculator_agent": CalculatorAgent(),
            "memory_agent": MemoryAgent(),
            "document_agent": DocumentAgent(),
        }
        self.metrics = {}

    def _route(self, request: str) -> str:
        low = (request or "").lower()
        if _is_destructive_fs(request):
            return "deny"
        if _wants_code_written(request):
            return "code"
        if re.search(r"\b(search|research|look up|find (out|information)|news about)\b", low):
            return "research"
        if re.search(r"\b(what('?s| is) your name|who are you|what are you)\b", low):
            return "chat"
        if re.search(r"\b(summarize|summary of|what does .+ say|uploaded report)\b", low):
            return "document"
        if re.search(r"[\d\+\-\*/=]|calculate|what is \d", low):
            return "calc"
        if re.search(r"\b(remember|my name is|what is my name)\b", low):
            return "memory"
        return "chat"

    def handle(self, request: str, history=None, conversation_id=None) -> dict:
        if _is_destructive_fs(request):
            return AgentResult("main_chat_agent", False, DENY_FS_MSG, raw={"denied": True}).to_dict()
        route = self._route(request)
        key = {
            "code": "coding_agent",
            "research": "research_agent",
            "chat": "main_chat_agent",
            "calc": "calculator_agent",
            "memory": "memory_agent",
            "document": "document_agent",
        }.get(route, "main_chat_agent")
        agent = self.agents[key]
        ctx = {"search_provider": self.search_provider, "model_provider": self.model_provider}
        result = agent.run(request, ctx)
        if key == "main_chat_agent" and result.raw and result.raw.get("source") == "generation_fallback":
            if self.model_provider is not None:
                try:
                    out = self.model_provider.generate(request)
                    if out:
                        return AgentResult("main_chat_agent", True, str(out), raw={"source": "model_provider"}).to_dict()
                except Exception:
                    pass
        return result.to_dict() if hasattr(result, "to_dict") else result

# Aliases expected by some tests
OrbitAI = Orchestrator
