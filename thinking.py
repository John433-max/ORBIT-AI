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
    text: str

    def to_dict(self) -> dict:
        return {"kind": self.kind, "text": self.text}


@dataclass
class ThinkResult:
    answer: str
    thoughts: List[Thought] = field(default_factory=list)
    plan: List[str] = field(default_factory=list)
    ok: bool = True

    def to_dict(self) -> dict:
        return {
            "answer": self.answer,
            "thoughts": [t.to_dict() for t in self.thoughts],
            "plan": self.plan,
            "ok": self.ok,
        }


def _is_question(text: str) -> bool:
    s = (text or "").strip()
    if not s:
        return False
    if "?" in s:
        return True
    return bool(
        re.match(
            r"^(what|who|where|when|why|how|is|are|was|were|do|does|did|"
            r"can|could|should|would|tell|explain|define|list|name|which)\b",
            s,
            re.I,
        )
    )


def _is_math(text: str) -> bool:
    try:
        from science_math import looks_like_science_math
        if looks_like_science_math(text):
            return True
    except Exception:
        pass
    return bool(
        re.search(
            r"\d+\s*[\+\-\*/×÷%^xX]\s*\d+"
            r"|%\s*of|sqrt\s*\(|what is \d"
            r"|\d+\s*(times|plus|minus|divided\s+by|divide|multiplied\s+by|modulo|mod)\s*\d+"
            r"|(calculate|what is|what\'s)\s+\d"
            r"|\d+\s*(km|m|kg|celsius|fahrenheit|°c|°f)\b",
            text,
            re.I,
        )
    )


def _is_code(text: str) -> bool:
    return bool(re.search(r"```|^\s*def |import |print\(|write (a |some )?code", text, re.I))


def _is_capability(text: str) -> bool:
    return bool(re.search(
        r"\bwhat can you do\b|\bcapabilities\b|\bwhat are you\b|\bwho are you\b|\bhelp\b",
        text or "",
        re.I,
    ))


def _is_self_identity(text: str) -> bool:
    """Questions about ORBIT's own name/identity — not user profile, not web research."""
    return bool(
        re.search(
            r"\bwhat(?:'s| is) your name\b|\btell me (about )?yourself\b|"
            r"\bintroduce yourself\b|\byour name\b",
            text or "",
            re.I,
        )
    )


def _is_name_profile(text: str) -> bool:
    return bool(
        re.search(
            r"\bmy name is\b|\bcall me\b|\bwhat(?:'s| is) my name\b|\bwho am i\b",
            text,
            re.I,
        )
    )


def _wants_extract(text: str) -> bool:
    return bool(
        re.search(r"extract\s+(the\s+)?text|show\s+(me\s+)?(the\s+)?text|read\s+(the\s+)?document", text, re.I)
    )


class Thinker:
    """
    Plan → act → answer.

    `runners` maps step names to callables(request, context) -> str answer.
    """

    def __init__(self, runners: Dict[str, Callable[..., Any]]):
        self.runners = runners

    def classify(self, request: str) -> str:
        r = request.strip()
        if _is_capability(r) or _is_self_identity(r):
            return "chat"
        if _is_name_profile(r) or r.lower().startswith("remember:"):
            return "memory"
        if _is_math(r):
            return "calc"
        if _is_code(r):
            return "code"
        if _wants_extract(r) or re.search(r"\b(document|pdf|docx|summarize)\b", r, re.I):
            return "docs"
        if _is_question(r):
            return "question"
        if re.match(r"^(hi|hello|hey|thanks|thank you|bye|good (morning|night))\b", r, re.I):
            return "chat"
        if not _is_question(r) and len(r.split()) < 40:
            return "statement"
        return "question"

    def plan(self, request: str, kind: str) -> List[str]:
        if kind == "memory":
            return ["memory"]
        if kind == "calc":
            return ["calc", "search"]
        if kind == "code":
            return ["code"]
        if kind == "docs":
            return ["docs"]
        if kind == "chat":
            return ["chat"]
        if kind == "statement":
            return ["memory", "chat"]
        return ["memory_check", "docs_check", "search", "chat"]

    def think(self, request: str, context: Optional[dict] = None) -> ThinkResult:
        context = context or {}
        thoughts: List[Thought] = []
        kind = self.classify(request)
        thoughts.append(Thought("classify", f"This looks like: {kind}"))
        steps = self.plan(request, kind)
        thoughts.append(Thought("plan", " → ".join(steps)))

        answer = ""
        used = []

        for step in steps:
            fn = None
            if step in ("memory", "memory_check"):
                fn = self.runners.get("memory")
            elif step in ("docs", "docs_check"):
                fn = self.runners.get("docs")
            elif step == "search":
                fn = self.runners.get("search")
            elif step == "calc":
                fn = self.runners.get("calc")
            elif step == "code":
                fn = self.runners.get("code")
            elif step == "chat":
                fn = self.runners.get("chat")

            if fn is None:
                thoughts.append(Thought("skip", f"no runner for {step}"))
                continue

            try:
                result = fn(request, context)
            except Exception as e:
                thoughts.append(Thought("error", f"{step}: {e}"))
                continue

            if isinstance(result, dict):
                text = (result.get("content") or "").strip()
                ok = bool(result.get("ok", True))
            else:
                text = str(result or "").strip()
                ok = bool(text)

            thoughts.append(
                Thought("observe", f"{step}: {'ok' if ok and text else 'empty'} ({len(text)} chars)")
            )

            if not text:
                continue
            if not ok and step in ("calc", "code", "memory", "docs", "search", "memory_check", "docs_check"):
                thoughts.append(Thought("reject", f"{step} not ok — continue"))
                continue

            weak = any(
                w in text.lower()
                for w in (
                    "don't have a solid answer",
                    "toy-scale",
                    "don't have any documents",
                    "don't know your name yet",
                    "no relevant memories",
                    "don't have anything stored",
                    "can't complete this search",
                    "don't have live web",
                )
            )
            if step in ("memory_check", "docs_check") and weak:
                thoughts.append(Thought("reject", f"{step} weak — continue"))
                continue
            if step == "memory_check" and text and _is_question(request):
                q_toks = {w.lower() for w in re.findall(r"[a-zA-Z]{3,}", request)}
                a_toks = {w.lower() for w in re.findall(r"[a-zA-Z]{3,}", text)}
                if not (q_toks & a_toks):
                    thoughts.append(Thought("reject", "memory unrelated to question"))
                    continue
            if step == "chat" and weak and answer:
                thoughts.append(Thought("reject", "chat hedge — keep prior"))
                continue

            answer = text
            used.append(step)
            if step in ("calc", "code", "memory", "docs") and ok and not weak:
                thoughts.append(Thought("decide", f"use {step}"))
                break
            if step == "search" and ok and not weak:
                thoughts.append(Thought("decide", "use search"))
                break

        if not answer:
            answer = (
                "I'm still thinking that through, but I don't have a solid answer yet. "
                "Try rephrasing, or point me at code, math, a document, or something to remember."
            )
            thoughts.append(Thought("fallback", "empty pipeline"))

        thoughts.append(Thought("answer", f"steps used: {used or ['fallback']}"))
        return ThinkResult(answer=answer, thoughts=thoughts, plan=steps, ok=bool(answer))
