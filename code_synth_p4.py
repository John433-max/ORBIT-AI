"""Cycle expand: additional verified Python templates (pack 4)."""

from __future__ import annotations

import re
from code_synth import Template as T


def templates():
    return [
        T(
            "clamp_list",
            "def clamp_list(items, lo, hi):\n"
            '    """Clamp each value into [lo, hi]."""\n'
            "    return [lo if x < lo else hi if x > hi else x for x in items]\n",
            lambda low: bool(re.search(r"\bclamp (list|array|values)\b", low)),
            ((([0, 5, 10], 1, 8), [1, 5, 8]),),
        ),
        # median_of_two_sorted removed: find_median_sorted_arrays (p3) is the
        # canonical LeetCode matcher; the merge-then-pick body was winning on
        # equal token score and breaking test_cycle245_hard_dp_stack_templates.
        T(
            "count_bits",
            "def count_bits(n):\n"
            '    """Number of set bits in non-negative integer n."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        raise ValueError('n must be >= 0')\n"
            "    return bin(n).count('1')\n",
            lambda low: bool(
                re.search(r"\b(count bits|counting bits|hamming weight|set bits|popcount)\b", low)
            ),
            (((7,), 3), ((0,), 0)),
        ),
    ]
