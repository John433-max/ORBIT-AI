"""Cycle 482: running product, suffix sums, MAD, mode, uppercase count, diffs.

Matchers stay phrase-specific so list product, most-frequent-even, and
character-frequency templates keep their asks.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "running_product",
            "def running_product(nums):\n"
            '    """Prefix products: each position is the product seen so far."""\n'
            "    out = []\n"
            "    acc = 1\n"
            "    for x in nums:\n"
            "        acc *= x\n"
            "        out.append(acc)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"running[- ]product|prefix[- ]product", low)
            )
            and "except self" not in low
            and "except itself" not in low,
            (
                (([1, 2, 3, 4],), [1, 2, 6, 24]),
                (([],), []),
                (([5],), [5]),
            ),
        ),
        T(
            "suffix_sums",
            "def suffix_sums(nums):\n"
            '    """Suffix sums: each position is the sum of nums[i:]."""\n'
            "    out = [0] * len(nums)\n"
            "    acc = 0\n"
            "    for i in range(len(nums) - 1, -1, -1):\n"
            "        acc += nums[i]\n"
            "        out[i] = acc\n"
            "    return out\n",
            lambda low: bool(re.search(r"suffix[- ]sums?", low)),
            (
                (([1, 2, 3],), [6, 5, 3]),
                (([],), []),
                (([4],), [4]),
            ),
        ),
        T(
            "mean_absolute_deviation",
            "def mean_absolute_deviation(nums):\n"
            '    """Mean absolute deviation from the arithmetic mean."""\n'
            "    xs = list(nums)\n"
            "    if not xs:\n"
            "        raise ValueError('empty')\n"
            "    mean = sum(xs) / len(xs)\n"
            "    return sum(abs(x - mean) for x in xs) / len(xs)\n",
            lambda low: bool(
                re.search(r"mean[- ]absolute[- ]deviation|\bmad\b", low)
            )
            and "median" not in low,
            (
                (([1, 3],), 1.0),
                (([2, 2, 2],), 0.0),
                (([0, 10],), 5.0),
            ),
        ),
        T(
            "most_common_element",
            "def most_common_element(items):\n"
            '    """Mode: highest count, earliest item on a tie. Empty -> None."""\n'
            "    counts = {}\n"
            "    best = None\n"
            "    best_n = 0\n"
            "    for x in items:\n"
            "        counts[x] = counts.get(x, 0) + 1\n"
            "        n = counts[x]\n"
            "        if n > best_n:\n"
            "            best = x\n"
            "            best_n = n\n"
            "    return best\n",
            lambda low: (
                bool(re.search(r"most[- ]common(?: element)?|mode of a list", low))
                and "even" not in low
                and "vowel" not in low
                and "consonant" not in low
            ),
            (
                (([1, 2, 2, 3],), 2),
                ((["a", "b", "a"],), "a"),
                (([],), None),
            ),
        ),
        T(
            "count_uppercase",
            "def count_uppercase(s):\n"
            '    """Count uppercase ASCII letters in a string."""\n'
            "    return sum(1 for ch in str(s) if 'A' <= ch <= 'Z')\n",
            lambda low: bool(
                re.search(r"count(?:s|ing)? uppercase|uppercase letters", low)
            ),
            (
                (("AbC",), 2),
                (("",), 0),
                (("xyz",), 0),
            ),
        ),
        T(
            "consecutive_diffs",
            "def consecutive_diffs(nums):\n"
            '    """Adjacent differences nums[i+1] - nums[i]."""\n'
            "    return [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]\n",
            lambda low: bool(
                re.search(r"consecutive[- ]diff(?:erence)?s?|adjacent[- ]diff", low)
            ),
            (
                (([1, 3, 6],), [2, 3]),
                (([4],), []),
                (([],), []),
            ),
        ),
    ]
