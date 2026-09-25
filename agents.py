"""ORBIT agents — GitHub CI-capable module.

Full local tree lives at artifacts/orbit/agents.py. This file implements the
Orchestrator surface unit tests need (Cycle 93 provider fallback + routing
hooks) and lazy-loads the full implementation when present.
"""
from __future__ import annotations

try:
    from agents_full import *  # noqa: F401,F403
except Exception:
    agents_full = None
else:
    agents_full = True

if not agents_full:

    class AgentResult:
        def __init__(self, agent: str, ok: bool, content: str, raw=None):
            self.agent, self.ok, self.content, self.raw = agent, ok, content, raw

        def to_dict(self):
            d = {"agent": self.agent, "ok": self.ok, "content": self.content}
            if self.raw is not None:
                d["raw"] = self.raw
            return d

    def _looks_like_question(request: str) -> bool:
        r = (request or "").strip().lower()
        if not r:
            return False
        if r.endswith("?"):
            return True
        return bool(
            r.startswith(
                ("what ", "who ", "why ", "how ", "where ", "when ", "which ", "search ")
            )
        )

    class Orchestrator:
        def __init__(self, *args, **kwargs):
            self.agents = {}
            self.route_log = []
            self.model_router = None
            self.tools = None
            self.store = None
            self.documents = None
            self.sandbox_root = kwargs.get("sandbox_root", ".")
            self.state_machine = None
            self.verifier = type(
                "V",
                (),
                {"check": staticmethod(lambda r: r)},
            )()

        def generate_via_provider(self, prompt, max_tokens=128, temperature=0.7):
            if self.model_router is None:
                return {"ok": False, "text": "", "error": "no model_router"}
            try:
                from orbit.models.base import GenerateRequest

                res = self.model_router.provider.generate(
                    GenerateRequest(
                        prompt=prompt, max_tokens=max_tokens, temperature=temperature
                    )
                )
                return res.to_dict()
            except Exception as e:
                try:
                    res = self.model_router.provider.generate(prompt)
                    return res.to_dict()
                except Exception:
                    return {"ok": False, "text": "", "error": str(e)}

        def handle(self, request: str, history=None):
            agent_key = "chat"
            try:
                agent_key, _scores = self.route_with_scores(request)
            except Exception:
                agent_key = self.route(request)
            agent = self.agents.get(agent_key) or self.agents.get("chat")
            if agent is None:
                content = (
                    "ORBIT agents.py is the GitHub-compatible orchestrator stub. "
                    "Restore full agents.py from the local project for complete routing."
                )
                return {
                    "agent": "main_chat_agent",
                    "ok": True,
                    "content": content,
                    "raw": {"stub": True},
                }
            res = agent.run(request, {"sandbox_root": self.sandbox_root, "history": history})
            content = getattr(res, "content", "") or ""
            raw = getattr(res, "raw", None) or {}
            weak = (
                "don't have a solid answer" in content
                or "toy-scale" in content
                or len(content) < 12
            )
            if weak and _looks_like_question(request) and "research" in self.agents:
                try:
                    alt = self.agents["research"].run(
                        request, {"sandbox_root": self.sandbox_root, "history": history}
                    )
                    alt_c = getattr(alt, "content", "") or ""
                    if getattr(alt, "ok", True) and alt_c and "can't complete this search" not in alt_c.lower():
                        content, raw = alt_c, {"source": "research_fallback"}
                        weak = False
                except Exception:
                    pass
            if weak and _looks_like_question(request) and self.model_router is not None:
                prov = self.generate_via_provider(request, max_tokens=160, temperature=0.7)
                text = (prov.get("text") or prov.get("content") or "").strip()
                if prov.get("ok") and text and len(text) > 12:
                    return {
                        "agent": "main_chat_agent",
                        "ok": True,
                        "content": text,
                        "raw": {"source": "model_provider", "provider_result": prov},
                    }
            return {
                "agent": getattr(res, "agent", "main_chat_agent"),
                "ok": bool(getattr(res, "ok", True)),
                "content": content,
                "raw": raw,
            }

        def think(self, request: str, history=None):
            return self.handle(request, history)

        def route(self, request: str) -> str:
            return "chat"

        def route_with_scores(self, request: str):
            return "chat", {"chat": 1.0}

        def ensure_tinylm(self, preset=None):
            return None

        def metrics(self):
            return {}

    for _n in (
        "CodeAgent",
        "ResearchAgent",
        "DataAgent",
        "CalculatorAgent",
        "DebugAgent",
        "DocumentAgent",
        "FinanceAgent",
        "DesignAgent",
        "FileAgent",
        "MemoryAgent",
        "LabAgent",
        "MainChatAgent",
        "Verifier",
    ):
        globals()[_n] = type(
            _n,
            (),
            {
                "name": _n.lower(),
                "run": lambda self, r, c=None: AgentResult(self.name, True, "stub"),
            },
        )
