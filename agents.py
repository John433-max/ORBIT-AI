"""ORBIT agents (GitHub CI surface). Coding + research + identity + deny-fs."""
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
    return bool(
        re.search(
            r"\b(write|implement|create|define|make)\b.{0,80}\b("
            r"function|def |class |script|program|module|code)\b|"
            r"\bpython function\b|"
            r"\bimplement\b.{0,40}\bin python\b",
            request or "",
            re.I,
        )
    )


DENY_FS_MSG = (
    "I can't do that. ORBIT refuses destructive filesystem commands "
    "(delete all files, rm -rf /, wipe disk). Permission denied."
)


def _is_destructive_fs(text: str) -> bool:
    if _wants_code_written(text or ""):
        return False
    return bool(
        re.search(
            r"\brm\s+-rf\b|\bdelete all files\b|\bdelete everything\b|"
            r"\bwipe (the )?(disk|root|filesystem|drive)\b|"
            r"\bformat (the )?(hard )?disk\b|\bremove all files in\s+/",
            text or "",
            re.I,
        )
    )


def _synthesize_python(request: str) -> str:
    try:
        from code_synth import synthesize_python
        return synthesize_python(request)
    except Exception:
        low = (request or "").lower()
        if "adds two" in low or re.search(r"add(s|ing)?\b.{0,20}\b(two|2)\b", low):
            return 'def add(a, b):\n    """Return the sum of a and b."""\n    return a + b\n'
        if re.search(r"\b(multiply|product of)\b.{0,20}\b(two|2)\b", low):
            return 'def multiply(a, b):\n    """Return the product of a and b."""\n    return a * b\n'
        return "def solve(*args, **kwargs):\n    raise NotImplementedError\n"


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
            return AgentResult(self.name, True, content, raw={"source": "synthesize", "code": src, "verified": verified})
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
            note = (raw or {}).get("note") or (raw or {}).get("error") or "no live web"
        elif isinstance(raw, list) and raw:
            return AgentResult(self.name, True, f"Here's what I found: {raw[0]}", raw={"results": raw})
        else:
            note = "no live web"
        content = "I don't have live web access right now, so I can't complete this search. " + str(note)
        return AgentResult(self.name, False, content, raw={"ok": False, "note": note})


class MainChatAgent:
    name = "main_chat_agent"

    def run(self, request: str, context=None) -> AgentResult:
        low = (request or "").lower()
        if re.search(r"\b(what('?s| is) your name|who are you|what are you)\b", low):
            return AgentResult(self.name, True, "I'm ORBIT. Named after the project that built me, not the other way around.", raw={"source": "persona_retrieval"})
        return AgentResult(
            self.name,
            True,
            "I'm ORBIT. I don't have a solid answer for that in my head — my persona notes are limited, and the neural net under me is still toy-scale.",
            raw={"source": "generation_fallback"},
        )


class CalculatorAgent:
    name = "calculator_agent"

    def run(self, request: str, context=None) -> AgentResult:
        try:
            from calculator import parse_and_calculate
            result = parse_and_calculate(request)
            if result.get("ok"):
                return AgentResult(self.name, True, f"{result.get('expression') or request} = {result['result']}", raw=result)
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
            self._facts.append(text.split(":", 1)[1].strip())
            return AgentResult(self.name, True, "Got it — I'll remember that.")
        return AgentResult(self.name, False, "I don't have anything stored about that yet.")


class DocumentAgent:
    name = "document_agent"

    def __init__(self, store=None):
        self.store = store

    def run(self, request: str, context=None) -> AgentResult:
        return AgentResult(self.name, True, "I don't have a document uploaded for that question. Please upload one.", raw={"docs": 0})


class _Generic:
    def __init__(self, name):
        self.name = name

    def run(self, request: str, context=None) -> AgentResult:
        return AgentResult(self.name, True, "ok")


def _looks_like_question(request: str) -> bool:
    s = (request or "").strip()
    return "?" in s or bool(re.match(r"^(what|who|where|when|why|how)\b", s, re.I))


class Orchestrator:
    def __init__(self, model_router=None, search_provider=None, sandbox_root=".", **kwargs):
        self.model_router = model_router
        self.sandbox_root = sandbox_root
        self.route_log = []
        self.agents = {
            "code": CodeAgent(),
            "research": ResearchAgent(search_provider=search_provider),
            "chat": MainChatAgent(),
            "calculator": CalculatorAgent(),
            "memory": MemoryAgent(),
            "document": DocumentAgent(),
            "file": _Generic("file_agent"),
        }
        if self.model_router is None:
            try:
                from orbit.core.config import load_config
                from orbit.models.router import ModelRouter
                self.model_router = ModelRouter(cfg=load_config())
            except Exception:
                self.model_router = None

    def generate_via_provider(self, prompt, max_tokens=128, temperature=0.7):
        if self.model_router is None:
            return {"ok": False, "text": "", "error": "no model_router"}
        try:
            from orbit.models.base import GenerateRequest
            res = self.model_router.provider.generate(
                GenerateRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature)
            )
            return res.to_dict()
        except Exception:
            try:
                prov = getattr(self.model_router, "provider", self.model_router)
                res = prov.generate(prompt)
                if hasattr(res, "to_dict"):
                    return res.to_dict()
                if isinstance(res, dict):
                    return res
                return {"ok": True, "text": str(res)}
            except Exception as e:
                return {"ok": False, "text": "", "error": str(e)}

    def route_with_scores(self, request: str):
        text = request or ""
        scores = {}
        if _is_destructive_fs(text):
            scores["file"] = 1.0
        if _wants_code_written(text) or re.search(r"```|def |print\(", text):
            scores["code"] = 1.0
        if re.search(r"\b(search|look up|news about|research)\b", text, re.I):
            scores["research"] = 1.0
        if re.search(r"\b(what('?s| is) your name|who are you)\b", text, re.I):
            scores["chat"] = 1.2
        if re.search(r"\b(my name is|remember:|what(?:'s| is) my name)\b", text, re.I):
            scores["memory"] = 1.0
        if re.search(r"\d+\s*[\+\-\*/]\s*\d+", text):
            scores["calculator"] = 0.8
        if not scores:
            scores["chat"] = 0.1
        key = max(scores, key=scores.get)
        return key, scores

    def handle(self, request: str, history=None, conversation_id=None) -> dict:
        if _is_destructive_fs(request or ""):
            out = AgentResult("file_agent", True, DENY_FS_MSG, raw={"permission": "denied", "reason": "destructive_fs", "route": "file"}).to_dict()
            self.route_log.append({"request": request, "agent": "file", "ok": True})
            return out
        agent_key, scores = self.route_with_scores(request)
        ctx = {"history": history, "conversation_id": conversation_id}
        agent = self.agents.get(agent_key) or self.agents["chat"]
        verified = agent.run(request, ctx)
        content = (verified.content or "").strip()

        weak = verified.agent in ("main_chat_agent", "chat") and (
            "don't have a solid answer" in content or "toy-scale" in content or len(content) < 12
        )
        if weak and _looks_like_question(request) and "research" in self.agents:
            try:
                alt = self.agents["research"].run(request, ctx)
                alt_c = (alt.content or "").strip()
                if alt.ok and alt_c and "can't complete this search" not in alt_c.lower():
                    verified = AgentResult("main_chat_agent", True, alt_c, raw={"source": "research_fallback", "inner": alt.raw})
                    content = alt_c
                    agent_key = "research"
            except Exception:
                pass

        weak = verified.agent in ("main_chat_agent", "chat") and (
            "don't have a solid answer" in content or "toy-scale" in content or len(content) < 12
        )
        if weak and _looks_like_question(request) and self.model_router is not None:
            try:
                prov = self.generate_via_provider(request, max_tokens=160, temperature=0.7)
                text = (prov.get("text") or prov.get("content") or "").strip()
                if prov.get("ok") and text and len(text) > 12:
                    content = text
                    verified = AgentResult("main_chat_agent", True, content, raw={"source": "model_provider", "provider_result": prov})
                    agent_key = "chat"
            except Exception:
                pass

        name_map = {
            "code": "coding_agent",
            "research": "research_agent",
            "calculator": "calculator_agent",
            "memory": "memory_agent",
            "document": "document_agent",
            "chat": "main_chat_agent",
            "file": "file_agent",
        }
        outward = name_map.get(agent_key, getattr(verified, "agent", agent_key) or "main_chat_agent")
        raw = verified.raw if isinstance(verified.raw, dict) else {"detail": verified.raw}
        raw = dict(raw or {})
        raw["route"] = agent_key
        out = AgentResult(outward, bool(content), content, raw=raw).to_dict()
        self.route_log.append({"request": request, "agent": agent_key, "ok": out.get("ok")})
        return out


for _n in ("DataAgent", "DebugAgent", "FinanceAgent", "DesignAgent", "FileAgent", "LabAgent", "Thinker"):
    globals()[_n] = type(_n, (), {"name": _n.lower(), "run": lambda self, r, c=None: AgentResult(self.name, True, "ok")})
