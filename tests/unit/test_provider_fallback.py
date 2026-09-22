"""Cycle 93: chat miss → ModelRouter provider fallback."""

from agents import Orchestrator, AgentResult


class _FakeProv:
    def generate(self, req):
        class R:
            def to_dict(self):
                return {"ok": True, "text": "Provider says forty-two is the answer to life."}

        return R()


class _FakeRouter:
    def __init__(self):
        self.provider = _FakeProv()


def test_weak_chat_uses_model_provider():
    orch = Orchestrator(sandbox_root=".")
    orch.model_router = _FakeRouter()

    class _HedgeChat:
        name = "main_chat_agent"

        def run(self, request, context):
            return AgentResult(
                self.name,
                True,
                "I don't have a solid answer for that — toy-scale.",
                raw={"source": "generation_fallback"},
            )

    orch.agents["chat"] = _HedgeChat()
    orch.route_with_scores = lambda request: ("chat", {"chat": 1.0})
    orch.agents.pop("research", None)

    out = orch.handle("What is the meaning of life according to deep lore?")
    assert out.get("ok"), out
    body = (out.get("content") or "").lower()
    assert "forty-two" in body, body
    raw = out.get("raw") or {}
    assert raw.get("source") == "model_provider", raw
