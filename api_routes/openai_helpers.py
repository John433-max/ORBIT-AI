"""Pure helpers for OpenAI-compatible responses (no FastAPI dependency)."""

from __future__ import annotations
from typing import Any, Dict, List


def model_catalog() -> List[Dict[str, Any]]:
    created = 1720000000
    return [
        {"id": "orbit-toy", "object": "model", "created": created, "owned_by": "orbit",
         "permission": [], "root": "orbit-toy", "parent": None},
        {"id": "orbit-tiny", "object": "model", "created": created, "owned_by": "orbit",
         "permission": [], "root": "orbit-tiny", "parent": None},
        {"id": "text-embedding-orbit-hash", "object": "model", "created": created,
         "owned_by": "orbit", "permission": [], "root": "text-embedding-orbit-hash", "parent": None},
    ]


def usage(prompt_tokens: int = 0, completion_tokens: int = 0) -> Dict[str, int]:
    return {
        "prompt_tokens": int(prompt_tokens),
        "completion_tokens": int(completion_tokens),
        "total_tokens": int(prompt_tokens + completion_tokens),
    }


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text.split()) + len(text) // 8)
