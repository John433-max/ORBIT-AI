"""TEMPORARY stub — full Cycle 93 agents.py is local at orbit/agents.py (~68KB).

GitHub MCP could not upload the full file in one shot after a bad overwrite.
Re-upload the local file (or ORBIT-AI-github-ready.zip agents.py + apply Cycle 93).

Cycle 93 changes (in local full file):
- Chat weak answer → ModelRouter.generate_via_provider (Ollama/OpenAI/tinylm)
- ORBIT_THINK=1 → Thinker multi-step for questions
"""
from __future__ import annotations


class AgentResult:
    def __init__(self, agent: str, ok: bool, content: str, raw=None):
        self.agent, self.ok, self.content, self.raw = agent, ok, content, raw

    def to_dict(self):
        d = {"agent": self.agent, "ok": self.ok, "content": self.content}
        if self.raw is not None:
            d["raw"] = self.raw
        return d


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

    def handle(self, request: str, history=None):
        return {
            "agent": "main_chat_agent",
            "ok": True,
            "content": (
                "ORBIT GitHub agents.py is a temporary stub. "
                "Restore full agents.py from local project (Cycle 93)."
            ),
            "raw": {"stub": True},
        }

    def think(self, request: str, history=None):
        return self.handle(request, history)

    def route(self, request: str) -> str:
        return "chat"

    def route_with_scores(self, request: str):
        return "chat", {"chat": 1.0}

    def ensure_tinylm(self, preset=None):
        return None

    def generate_via_provider(self, prompt, max_tokens=128, temperature=0.7):
        return {"ok": False, "text": "", "error": "stub"}

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
