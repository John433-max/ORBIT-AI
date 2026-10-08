"""Cycle 505: unmatched write-a-function asks.

LeetCode 2870 minimum operations to empty an array, 2729 fascinating number.
Phrase gates are specific so generic min-ops and is_odd do not steal them.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "min_operations_empty",
            "def min_operations_empty(nums):\n"
            '    """Min delete-2-or-3 ops to empty nums, else -1 (LeetCode 2870)."""\n'
            "    from collections import Counter\n"
            "    ops = 0\n"
            "    for c in Counter(nums).values():\n"
            "        if c == 1:\n"
            "            return -1\n"
            "        ops += c // 3 + (c % 3 != 0)\n"
            "    return ops\n",
            lambda low: (
                "empty" in low
                and "operation" in low
                and ("array" in low or "nums" in low)
                and "equal" not in low
                and "increasing" not in low
            ),
            (
                (([2, 3, 3, 2, 2, 4, 2, 3, 4],), 4),
                (([2, 1, 2, 2, 3, 3],), -1),
            ),
        ),
        T(
            "is_fascinating",
            "def is_fascinating(n):\n"
            '    """True if n, 2n, 3n concatenate to a 1-9 pandigital (LeetCode 2729)."""\n'
            "    s = str(n) + str(2 * n) + str(3 * n)\n"
            "    return len(s) == 9 and set(s) == set('123456789')\n",
            lambda low: "fascinating" in low and "number" in low,
            (
                ((192,), True),
                ((100,), False),
                ((219,), True),
            ),
        ),
    ]
