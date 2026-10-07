"""Cycle 499: natural-language coding misses.

LeetCode 796 — goal is some rotation of s. Matcher stays off left-rotate-by-k.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "can_rotate_to",
            "def can_rotate_to(s, goal):\n"
            '    """True when goal is a rotation of s (LeetCode 796)."""\n'
            "    s, goal = str(s), str(goal)\n"
            "    if len(s) != len(goal):\n"
            "        return False\n"
            "    return goal in (s + s)\n",
            lambda low: (
                "string" in low
                and "rotat" in low
                and any(
                    w in low
                    for w in (
                        "obtained",
                        "another",
                        "goal",
                        "can be rotated",
                        "is a rotation",
                    )
                )
                and "matrix" not in low
                and "image" not in low
                and "left by" not in low
                and "right by" not in low
                and "list" not in low
            ),
            (
                (("abcde", "cdeab"), True),
                (("abcde", "abced"), False),
                (("aa", "a"), False),
            ),
        ),
    ]
