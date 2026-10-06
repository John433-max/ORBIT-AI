"""Cycle 478: running max, second smallest, char frequency, list product, strictly increasing, left pad.

These full-sentence asks previously fell through to the NotImplemented slug stub.
Matchers require the specific phrase so product-of-numbers, second-largest, and
Adler checksum stay on their existing templates.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "running_maximum",
            "def running_maximum(nums):\n"
            '    """Prefix maxima: each position is the max seen so far."""\n'
            "    out = []\n"
            "    best = None\n"
            "    for x in nums:\n"
            "        best = x if best is None else max(best, x)\n"
            "        out.append(best)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"running[- ]max(?:imum)?|prefix[- ]max(?:imum|ima)?", low)
            ),
            (
                (([1, 3, 2, 5],), [1, 3, 3, 5]),
                (([],), []),
                (([4],), [4]),
            ),
        ),
        T(
            "second_smallest",
            "def second_smallest(nums):\n"
            '    """Second-smallest distinct value, or None if fewer than two."""\n'
            "    vals = sorted(set(nums))\n"
            "    return vals[1] if len(vals) >= 2 else None\n",
            lambda low: (
                "second" in low
                and "smallest" in low
                and "largest" not in low
                and "highest" not in low
            ),
            (
                (([4, 1, 4, 2],), 2),
                (([7, 7],), None),
                (([3, 1],), 3),
            ),
        ),
        T(
            "char_frequency",
            "def char_frequency(s):\n"
            '    """Count each character, preserving first-seen order."""\n'
            "    counts = {}\n"
            "    for ch in s:\n"
            "        counts[ch] = counts.get(ch, 0) + 1\n"
            "    return counts\n",
            lambda low: bool(
                re.search(
                    r"character[- ]frequenc|char[- ]frequenc|count character|character count",
                    low,
                )
            )
            and "word" not in low,
            (
                (("aab",), {"a": 2, "b": 1}),
                (("",), {}),
                (("aba",), {"a": 2, "b": 1}),
            ),
        ),
        T(
            "list_product",
            "def list_product(nums):\n"
            '    """Product of numbers in a list. Empty product is 1."""\n'
            "    acc = 1\n"
            "    for x in nums:\n"
            "        acc *= x\n"
            "    return acc\n",
            lambda low: (
                "product" in low
                and "list" in low
                and "except self" not in low
                and "difference" not in low
            ),
            (
                (([2, 3, 4],), 24),
                (([],), 1),
                (([5],), 5),
            ),
        ),
        T(
            "is_strictly_increasing",
            "def is_strictly_increasing(nums):\n"
            '    """True when each value is strictly greater than the previous."""\n'
            "    return all(nums[i] < nums[i + 1] for i in range(len(nums) - 1))\n",
            lambda low: (
                "strictly" in low
                and "increasing" in low
                and "non-decreasing" not in low
                and "subsequence" not in low
            ),
            (
                (([1, 2, 4],), True),
                (([1, 1, 2],), False),
                (([],), True),
            ),
        ),
        T(
            "left_pad",
            "def left_pad(s, width, fill=\"0\"):\n"
            '    """Pad s on the left with fill until len(s) >= width."""\n'
            "    s = str(s)\n"
            "    fill = str(fill) or \" \"\n"
            "    if len(s) >= int(width):\n"
            "        return s\n"
            "    return (fill[0] * (int(width) - len(s))) + s\n",
            lambda low: bool(re.search(r"left[- ]?pad|pad(?:s|ding)? (?:a |the )?string on the left", low)),
            (
                (("7", 3, "0"), "007"),
                (("abc", 2, "0"), "abc"),
                (("", 2, "x"), "xx"),
            ),
        ),
    ]
