"""Cycle 479: running min, strictly decreasing, right pad, list span, pairwise sums, digit count.

Matchers stay phrase-specific so running maximum, strictly increasing, left pad,
and character-frequency templates keep their asks.
Cycle 480: count_digits_in_string requires a count verb and excludes equal/same/
adjacent/leetcode/operation so 3461, 2264, and 3438 keep their templates.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "running_minimum",
            "def running_minimum(nums):\n"
            '    """Prefix minima: each position is the min seen so far."""\n'
            "    out = []\n"
            "    best = None\n"
            "    for x in nums:\n"
            "        best = x if best is None else min(best, x)\n"
            "        out.append(best)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"running[- ]min(?:imum)?|prefix[- ]min(?:imum|ima)?", low)
            ),
            (
                (([3, 1, 4, 1],), [3, 1, 1, 1]),
                (([],), []),
                (([2],), [2]),
            ),
        ),
        T(
            "is_strictly_decreasing",
            "def is_strictly_decreasing(nums):\n"
            '    """True when each value is strictly less than the previous."""\n'
            "    return all(nums[i] > nums[i + 1] for i in range(len(nums) - 1))\n",
            lambda low: (
                "strictly" in low
                and "decreasing" in low
                and "non-increasing" not in low
                and "subsequence" not in low
            ),
            (
                (([4, 2, 1],), True),
                (([3, 3, 1],), False),
                (([],), True),
            ),
        ),
        T(
            "right_pad",
            "def right_pad(s, width, fill=\" \"):\n"
            '    """Pad s on the right with fill until len(s) >= width."""\n'
            "    s = str(s)\n"
            "    fill = str(fill) or \" \"\n"
            "    if len(s) >= int(width):\n"
            "        return s\n"
            "    return s + (fill[0] * (int(width) - len(s)))\n",
            lambda low: bool(
                re.search(r"right[- ]?pad|pad(?:s|ding)? (?:a |the )?string on the right", low)
            )
            and "left" not in low,
            (
                (("ab", 4, "."), "ab.."),
                (("abcd", 2, "."), "abcd"),
                (("", 3, "x"), "xxx"),
            ),
        ),
        T(
            "list_span",
            "def list_span(nums):\n"
            '    """Statistical range: max(nums) - min(nums). Empty list is None."""\n'
            "    if not nums:\n"
            "        return None\n"
            "    return max(nums) - min(nums)\n",
            lambda low: (
                (
                    "statistical range" in low
                    or ("range of a list" in low)
                    or ("range of the list" in low)
                )
                and "python range" not in low
                and "subarray" not in low
            ),
            (
                (([1, 5, 3],), 4),
                (([7],), 0),
                (([],), None),
            ),
        ),
        T(
            "pairwise_sums",
            "def pairwise_sums(nums):\n"
            '    """Sums of adjacent pairs. Empty or singleton returns []."""\n'
            "    return [nums[i] + nums[i + 1] for i in range(len(nums) - 1)]\n",
            lambda low: bool(re.search(r"pairwise[- ]sums?|adjacent[- ]pair sums?", low)),
            (
                (([1, 2, 3, 4],), [3, 5, 7]),
                (([9],), []),
                (([],), []),
            ),
        ),
        T(
            "count_digits_in_string",
            "def count_digits_in_string(s):\n"
            '    """How many digit characters appear in s."""\n'
            "    return sum(ch.isdigit() for ch in str(s))\n",
            lambda low: (
                bool(re.search(r"\bcounts?\b|\bcounting\b", low))
                and "digit" in low
                and ("string" in low or "text" in low)
                and "sum" not in low
                and "root" not in low
                and "frequency" not in low
                and "equal" not in low
                and "same" not in low
                and "adjacent" not in low
                and "leetcode" not in low
                and "operation" not in low
            ),
            (
                (("a1b23",), 3),
                (("",), 0),
                (("99",), 2),
            ),
        ),
    ]
