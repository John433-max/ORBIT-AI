"""ORBIT agents (GitHub CI surface).

Implements routing + Cycle 93 chat→ModelRouter fallback required by
tests/unit/test_provider_fallback.py. Coding and research paths return
real sandbox/search results or an honest no-live-web message.
"""
from __future__ import annotations

import collections
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
    low = (request or "").lower()
    if re.search(
        r"\b(write|implement|create|define|make|code)\b.{0,80}\b("
        r"function|def |class |script|program|module|code|factorial)\b|"
        r"\bpython function\b|"
        r"\bimplement\b.{0,40}\bin python\b|"
        r"\b(binary search|recover binary search tree|factorial function)\b|"
        # "implement reverseString", "implement twoSum for ..." — identifier after verb
        r"\b(implement|write|create|define)\b\s+[a-z_][a-z0-9_]{2,}\b",
        low,
    ):
        return True
    return False
