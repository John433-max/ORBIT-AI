"""
Lightweight "thinking" for ORBIT (Cycle 58).

Not a large CoT model — a structured scratchpad that:
  1. classifies the ask
  2. plans 1–3 steps (memory / docs / search / calc / code / reply)
  3. executes steps
  4. synthesizes a single natural answer

Keeps reasoning in `thoughts` for debugging; user-facing text stays clean.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Thought:
    kind: str
    text: str = ""


@dataclass
class ThinkResult:
    answer: str = ""
    thoughts: List[Thought] = field(default_factory=list)
    plan: List[str] = field(default_factory=list)
    ok: bool = True


class Thinker:
    """Structured classify → plan → execute → synthesize."""

    def __init__(self, runners: Dict[str, Callable[..., Any]]):
        self.runners = runners or {}

    def classify(self, text: str) -> str:
        r = (text or "").lower().strip()
        # Document inventory / RAG before broad search
        if re.search(
            r"\b(document|pdf|docx|summarize)\b|"
            r"\bwhat documents?( do you have| are (loaded|uploaded|available))?\b|"
            r"\bwhich documents?( do you have| are (loaded|uploaded))?\b|"
            r"\blist (my |the |uploaded )?documents?\b|"
            r"\bshow (me )?(my |the |uploaded )?documents?\b",
            r,
            re.I,
        ):
            return "docs"
        if re.search(r"\b(write|implement|code|function|python|def )\b", r):
            return "code"
        if re.search(r"\b(search|look up|news about|latest on)\b", r):
            return "search"
        if re.search(r"\b(who are you|your name|what are you)\b", r):
            return "identity"
        if re.search(r"\b(calculate|what is \d|\d\s*[+\-*/])\b", r):
            return "calc"
        return "chat"

    def think(self, text: str, **kwargs) -> ThinkResult:
        step = self.classify(text)
        thoughts = [Thought("classify", step)]
        runner = self.runners.get(step) or self.runners.get("chat")
        answer = ""
        ok = True
        if runner:
            try:
                res = runner(text)
                if isinstance(res, dict):
                    answer = str(res.get("text") or res.get("answer") or res)
                    ok = bool(res.get("ok", True))
                elif hasattr(res, "text"):
                    answer = str(res.text)
                    ok = getattr(res, "ok", True)
                else:
                    answer = str(res)
            except Exception as e:
                answer = f"Error: {e}"
                ok = False
        # Honest RAG stickiness
        low = (answer or "").lower()
        honest_rag = (
            "couldn't find document" in low
            or "don't have a document loaded" in low
            or "don't have any documents uploaded" in low
            or "don't have any indexed documents" in low
            or "don't have verified information" in low
            or "couldn't find that in your documents" in low
            or "indexed documents" in low
        )
        if honest_rag:
            thoughts.append(Thought("observe", "docs: honest empty RAG"))
        return ThinkResult(answer=answer, thoughts=thoughts, plan=[step], ok=ok)
