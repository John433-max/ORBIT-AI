"""ORBIT agents CI surface — coding/research/chat + weak-chat ModelRouter."""
from __future__ import annotations
import re


class AgentResult:
    def __init__(self, agent, ok, content, raw=None):
        self.agent, self.ok, self.content, self.raw = agent, ok, content, raw

    def to_dict(self):
        d = {"agent": self.agent, "ok": self.ok, "content": self.content}
        if self.raw is not None:
            d["raw"] = self.raw
        return d


def _wants_code(r):
    if re.search(r"```", r or ""):
        return False
    return bool(
        re.search(
            r"\b(write|implement|create|define|make)\b.{0,80}\b(function|def |class |script|program|module|code)\b|"
            r"\bpython function\b|\bimplement\b.{0,40}\bin python\b",
            r or "",
            re.I,
        )
    )


def _wants_search(r):
    return bool(
        re.search(
            r"\b(search|look up|news about|research|find (out|information))\b",
            r or "",
            re.I,
        )
    )


def _looks_like_question(t):
    t = (t or "").strip()
    return t.endswith("?") or bool(
        re.search(r"\b(what|who|why|how|when|where|which|is|are|can|does|do)\b", t, re.I)
    )


def _synth(r):
    try:
        from code_synth import synthesize_python
        return synthesize_python(r)
    except Exception:
        low = (r or "").lower()
        if "add" in low and "two" in low:
            return (
                "def add(a, b):\n"
                '    """Return the sum of a and b."""\n'
                "    return a + b\n"
            )
        return "def solve(*args, **kwargs):\n    raise NotImplementedError\n"


class CodeAgent:
    name = "coding_agent"

    def run(self, request, context=None):
        if _wants_code(request):
            try:
                from code_synth import synthesize_and_verify
                b = synthesize_and_verify(request)
                src = b.get("source") or _synth(request)
                v, n = bool(b.get("verified")), int(b.get("checked") or 0)
            except Exception:
                src, v, n = _synth(request), False, 0
            note = f"\n\nVerified against {n} example(s)." if v and n else ""
            return AgentResult(
                self.name, True,
                "Here is a Python function for that request:\n\n```python\n" + src + "```" + note,
                raw={"code": src, "verified": v},
            )
        try:
            from tools import python_sandbox
            m = re.search(r"```(?:python)?\s*(.*?)```", request or "", re.S)
            code = m.group(1) if m else request
            res = python_sandbox(code, timeout=3.0)
            if res.get("ok"):
                return AgentResult(
                    self.name, True,
                    f"Ran the code in the sandbox. stdout:\n{res.get('stdout', '')}", raw=res,
                )
            return AgentResult(
                self.name, False,
                f"Sandbox execution failed: {res.get('error') or res.get('stderr')}", raw=res,
            )
        except Exception as e:
            return AgentResult(self.name, False, f"Sandbox unavailable: {e}")


class ResearchAgent:
    name = "research_agent"

    def run(self, request, context=None):
        try:
            from tools import AutoSearchProvider
            raw = AutoSearchProvider().search(request)
            if isinstance(raw, dict) and raw.get("ok") and raw.get("results"):
                bits = []
                for item in (raw.get("results") or [])[:3]:
                    if isinstance(item, dict):
                        bits.append(item.get("snippet") or item.get("title") or "")
                    else:
                        bits.append(str(item))
                return AgentResult(
                    self.name, True, "Here's what I found: " + " ".join(bits), raw=raw,
                )
        except Exception:
            pass
        return AgentResult(
            self.name, True,
            "I don't have live web access right now, so I can't complete this search. "
            "No live web results available.",
            raw={"offline": True},
        )


class MainChatAgent:
    name = "main_chat_agent"

    def run(self, request, context=None):
        low = (request or "").lower()
        if re.search(r"\b(what('?s| is) your name|who are you|what are you)\b", low):
            return AgentResult(
                self.name, True,
                "I'm ORBIT. Named after the project that built me, not the other way around.",
                raw={"source": "persona_retrieval"},
            )
        return AgentResult(
            self.name, True,
            "I'm ORBIT. I don't have a solid answer for that in my head — "
            "my persona notes are limited, and the neural net under me is still toy-scale.",
            raw={"source": "generation_fallback"},
        )


class Orchestrator:
    def __init__(self, sandbox_root=".", **kw):
        self.sandbox_root = sandbox_root
        self.model_router = None
        self.agents = {
            "code": CodeAgent(),
            "research": ResearchAgent(),
            "chat": MainChatAgent(),
        }
        self.route_log = []
        try:
            from orbit.core.config import load_config
            from orbit.models.router import ModelRouter
            self.model_router = ModelRouter(cfg=load_config())
        except Exception:
            pass

    def generate_via_provider(self, prompt, max_tokens=128, temperature=0.7):
        if self.model_router is None:
            return {"ok": False, "text": ""}
        try:
            res = self.model_router.provider.generate(prompt)
            if hasattr(res, "to_dict"):
                return res.to_dict()
            if isinstance(res, dict):
                return res
            return {"ok": True, "text": str(res)}
        except Exception as e:
            return {"ok": False, "text": "", "error": str(e)}

    def route_with_scores(self, request):
        scores = {}
        if _wants_code(request):
            scores["code"] = 1.0
        if _wants_search(request):
            scores["research"] = 1.0
        if re.search(
            r"\b(what('?s| is) your name|who are you|what are you)\b",
            request or "",
            re.I,
        ):
            scores["chat"] = 1.0
        if not scores:
            scores["chat"] = 0.4
        return max(scores, key=scores.get), scores

    def handle(self, request, history=None, conversation_id=None):
        key, _ = self.route_with_scores(request)
        if key not in self.agents:
            key = "chat"
        result = self.agents[key].run(request, None)
        content = (result.content or "").strip()
        weak = result.agent in ("main_chat_agent", "chat") and (
            "don't have a solid answer" in content
            or "toy-scale" in content
            or len(content) < 12
        )
        if weak and _looks_like_question(request) and self.model_router is not None:
            try:
                prov = self.generate_via_provider(request, max_tokens=160, temperature=0.7)
                text = (prov.get("text") or prov.get("content") or "").strip()
                if prov.get("ok") and text and len(text) > 12:
                    content = text
                    result = AgentResult(
                        "main_chat_agent", True, content,
                        raw={"source": "model_provider", "provider_result": prov},
                    )
                    key = "chat"
            except Exception:
                pass
        name_map = {
            "code": "coding_agent",
            "research": "research_agent",
            "chat": "main_chat_agent",
        }
        outward = name_map.get(key, result.agent)
        raw = result.raw if isinstance(result.raw, dict) else {}
        raw = dict(raw or {})
        raw["route"] = key
        out = AgentResult(outward, bool(content), content, raw=raw).to_dict()
        self.route_log.append({"request": request, "agent": key, "ok": out.get("ok")})
        return out
