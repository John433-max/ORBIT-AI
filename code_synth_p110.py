"""Cycle 389: Easy prompts still absent from the template index.

LeetCode 3678, 3684, 3692, 3701, 3606, and 3616 were not referenced by any
pack. Matchers stay ID- or title-specific so alternating-bits, missing-multiple,
and at-most-k templates keep their prompts.
Loaded before p109.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "smallest_absent_above_average",
            "def smallest_absent_above_average(nums):\n"
            '    """Smallest positive absent integer strictly above the mean (LeetCode 3678)."""\n'
            "    avg = sum(nums) / len(nums)\n"
            "    present = set(nums)\n"
            "    x = int(avg) + 1\n"
            "    if x < 1:\n"
            "        x = 1\n"
            "    while x in present:\n"
            "        x += 1\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3678\b|"
                    r"\bsmallest absent positive greater than average\b|"
                    r"\babsent positive greater than average\b",
                    low,
                )
            ),
            (
                (([3, 5],), 6),
                (([-1, 1, 2],), 3),
                (([4, -1],), 2),
            ),
        ),
        T(
            "max_sum_k_distinct",
            "def max_sum_k_distinct(nums, k):\n"
            '    """At most k distinct values, descending, max sum (LeetCode 3684)."""\n'
            "    vals = sorted(set(nums), reverse=True)\n"
            "    return vals[: int(k)]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3684\b|"
                    r"\bat most k distinct elements\b|"
                    r"\bmaximize sum of at most k distinct\b",
                    low,
                )
            ),
            (
                (([84, 93, 100, 77, 90], 3), [100, 93, 90]),
                (([84, 93, 100, 77, 93], 3), [100, 93, 84]),
                (([1, 1, 1, 2, 2, 2], 6), [2, 1]),
            ),
        ),
        T(
            "majority_frequency_characters",
            "def majority_frequency_characters(s):\n"
            '    """Chars in the largest frequency group; ties take higher k (LeetCode 3692)."""\n'
            "    from collections import Counter\n"
            "    groups = {}\n"
            "    for ch, k in Counter(s).items():\n"
            "        groups.setdefault(k, []).append(ch)\n"
            "    best = max(groups, key=lambda k: (len(groups[k]), k))\n"
            "    return ''.join(sorted(groups[best]))\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3692\b|"
                    r"\bmajority frequency characters\b|"
                    r"\bmajority frequency group\b",
                    low,
                )
            ),
            (
                (("aaabbbccdddde",), "ab"),
                (("abcd",), "abcd"),
                (("pfpfgi",), "fp"),
            ),
        ),
        T(
            "alternating_sum",
            "def alternating_sum(nums):\n"
            '    """Even indices added, odd indices subtracted (LeetCode 3701)."""\n'
            "    return sum(v if i % 2 == 0 else -v for i, v in enumerate(nums))\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3701\b|"
                    r"\bcompute alternating sum\b|"
                    r"\balternating sum of an array\b|"
                    r"\balternating sum\b",
                    low,
                )
            ),
            (
                (([1, 3, 5, 7],), -4),
                (([100],), 100),
                (([1, 2, 3],), 2),
            ),
        ),
        T(
            "validate_coupons",
            "def validate_coupons(code, business_line, is_active):\n"
            '    """Valid coupon codes sorted by category then code (LeetCode 3606)."""\n'
            "    order = {'electronics': 0, 'grocery': 1, 'pharmacy': 2, 'restaurant': 3}\n"
            "    valid = []\n"
            "    for c, b, active in zip(code, business_line, is_active):\n"
            "        if not active or not c:\n"
            "            continue\n"
            "        if any(not (ch.isalnum() or ch == '_') for ch in c):\n"
            "            continue\n"
            "        if b not in order:\n"
            "            continue\n"
            "        valid.append((order[b], c))\n"
            "    valid.sort()\n"
            "    return [c for _, c in valid]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3606\b|"
                    r"\bcoupon code validator\b|"
                    r"\bvalid coupon codes\b",
                    low,
                )
            ),
            (
                (
                    (
                        ["SAVE20", "", "PHARMA5", "SAVE@20"],
                        ["restaurant", "grocery", "pharmacy", "restaurant"],
                        [True, True, True, True],
                    ),
                    ["PHARMA5", "SAVE20"],
                ),
                (
                    (
                        ["GROCERY15", "ELECTRONICS_50", "DISCOUNT10"],
                        ["grocery", "electronics", "invalid"],
                        [False, True, True],
                    ),
                    ["ELECTRONICS_50"],
                ),
            ),
        ),
        T(
            "student_replacements",
            "def student_replacements(ranks):\n"
            '    """Count strict rank improvements over the current pick (LeetCode 3616)."""\n'
            "    cur = ranks[0]\n"
            "    n = 0\n"
            "    for x in ranks[1:]:\n"
            "        if x < cur:\n"
            "            cur = x\n"
            "            n += 1\n"
            "    return n\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3616\b|"
                    r"\bstudent replacement\b|"
                    r"\bnumber of student replacements\b",
                    low,
                )
            ),
            (
                (([4, 1, 2],), 1),
                (([2, 2, 3],), 0),
                (([5, 4, 3, 6, 1],), 3),
            ),
        ),
    ]
