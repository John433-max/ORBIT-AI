"""Numeric summary stats as a ToolRegistry tool (Cycle 61)."""

from __future__ import annotations

import re

import numpy as np

from tools.base import BaseTool, ToolResult


def summarize_numbers(text: str) -> dict:
    numbers = [float(x) for x in re.findall(r"-?\d+\.?\d*", text or "")]
    if not numbers:
        return {"ok": False, "error": "No numeric data found", "n": 0}
    arr = np.array(numbers, dtype=np.float64)
    stats = {
        "ok": True,
        "n": int(len(arr)),
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "min": float(arr.min()),
        "max": float(arr.max()),
        "numbers": numbers,
    }
    stats["pretty"] = (
        f"Found {stats['n']} numbers. mean={stats['mean']:.3f} "
        f"std={stats['std']:.3f} min={stats['min']:.3f} max={stats['max']:.3f}"
    )
    return stats


class DataStatsTool(BaseTool):
    name = "data.stats"
    description = "Extract numbers from text and report count/mean/std/min/max."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Text that may contain numbers"},
        },
        "required": ["text"],
    }
    timeout_s = 5.0

    def execute(self, text: str = "", **_):
        stats = summarize_numbers(text or "")
        if not stats.get("ok"):
            return ToolResult(
                ok=False,
                content="No numeric data found in the request to analyze.",
                error=stats.get("error"),
                data=stats,
            )
        return ToolResult(ok=True, content=stats["pretty"], data=stats)
