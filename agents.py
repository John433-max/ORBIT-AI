"""Minimal Orchestrator surface for CI / security tests."""
from __future__ import annotations

import re
from typing import Any, Dict


class Orchestrator:
    def __init__(self, sandbox_root: str = "."):
        self.sandbox_root = sandbox_root
        self._session: Dict[str, Any] = {}

    def handle(self, text: str) -> Dict[str, Any]:
        raw = text or ""
        lowered = raw.lower()

        named = re.search(r"my name is\s+(\w+)", raw, flags=re.IGNORECASE)
        if named:
            self._session["name"] = named.group(1)
            return {"ok": True, "content": f"I'll remember your name is {named.group(1)}."}

        if "what is my name" in lowered:
            name = self._session.get("name")
            if name:
                return {"ok": True, "content": f"Your name is {name}."}
            return {"ok": True, "content": "I don't know your name yet."}

        if "document" in lowered:
            return {
                "ok": True,
                "content": "I don't have a document uploaded for that question. Please upload one.",
            }

        return {"ok": True, "content": raw}
