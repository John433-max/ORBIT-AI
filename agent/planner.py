"""
Simple planner for multi-step agent workflows.

Produces a list of planned steps; the executor/tool router carries them out.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class PlanStep:
    action: str                # "tool" | "respond" | "retrieve" | "reason"
    tool: Optional[str] = None
    arguments: Dict[str, Any] = field(default_factory=dict)
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Plan:
    goal: str
    steps: List[PlanStep] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"goal": self.goal, "steps": [s.to_dict() for s in self.steps]}


class Planner:
    """
    Heuristic planner (stand-in until the LLM does structured planning).
    """

    def plan(self, user_message: str) -> Plan:
        msg = user_message.strip()
        low = msg.lower()
        steps: List[PlanStep] = []

        if re.search(r"\d", msg) and any(c in msg for c in "+-*/") and re.search(
            r"[\d\s\+\-\*/\(\)]{3,}", msg
        ):
            expr = re.sub(r"[^0-9\+\-\*/\(\)\.\s]", "", msg).strip()
            if expr and any(c.isdigit() for c in expr):
                steps.append(PlanStep(
                    action="tool",
                    tool="calculator",
                    arguments={"expression": expr},
                    note="evaluate arithmetic",
                ))
                steps.append(PlanStep(action="respond", note="return calculator result"))
                return Plan(goal=msg, steps=steps)

        if low.startswith(('search', 'look up', 'google', 'web')):
            q = msg
            for prefix in ('search:', 'search ', 'look up ', 'google ', 'web:', 'web '):
                if low.startswith(prefix):
                    q = msg[len(prefix):].strip()
                    break
            steps.append(PlanStep(
                action="tool",
                tool="web.search",
                arguments={"query": q or msg},
                note="web search",
            ))
            steps.append(PlanStep(action="respond", note="summarize search results"))
            return Plan(goal=msg, steps=steps)

        if low.startswith("read ") or "open file" in low:
            path = msg.split(maxsplit=1)[-1].strip().strip("'\"")
            steps.append(PlanStep(
                action="tool",
                tool="filesystem.read",
                arguments={"path": path},
                note="read file",
            ))
            steps.append(PlanStep(action="respond", note="present file contents"))
            return Plan(goal=msg, steps=steps)

        if any(w in low for w in ("remember that", "remember this", "note that", "store memory")):
            text = msg
            for prefix in ("remember that ", "remember this ", "note that ", "store memory "):
                if low.startswith(prefix):
                    text = msg[len(prefix):].strip()
                    break
            steps.append(PlanStep(
                action="tool",
                tool="memory.add",
                arguments={"text": text or msg},
                note="store memory",
            ))
            steps.append(PlanStep(action="respond", note="confirm stored"))
            return Plan(goal=msg, steps=steps)

        if any(w in low for w in ("what do you remember", "recall", "search memory", "from memory")):
            steps.append(PlanStep(
                action="tool",
                tool="memory.search",
                arguments={"query": msg},
                note="search memory",
            ))
            steps.append(PlanStep(action="respond", note="present memories"))
            return Plan(goal=msg, steps=steps)

        steps.append(PlanStep(action="respond", note="direct answer"))
        return Plan(goal=msg, steps=steps)
