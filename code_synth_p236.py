"""Cycle 524: zip-three, three-way interleave, all-digits, comma split, pair transpose, windows.

These asks returned NotImplemented drafts or were stolen by two-list interleave.
This pack loads before p230/p161. Two-list interleave matchers also decline "three".
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "zip_three",
            "def zip_three(a, b, c):\n"
            '    """Zip three sequences; stop at the shortest."""\n'
            "    return list(zip(a, b, c))\n",
            lambda low: (
                "zip" in low
                and "three" in low
                and "list" in low
                and "unzip" not in low
            ),
            (
                (([1, 2], [3, 4], [5, 6]), [(1, 3, 5), (2, 4, 6)]),
                (([1], [2, 9], [3]), [(1, 2, 3)]),
                (([], [1], [2]), []),
            ),
        ),
        T(
            "interleave_three",
            "def interleave_three(a, b, c):\n"
            '    """Alternate items from three sequences; leftover tails are appended in order."""\n'
            "    out = []\n"
            "    n = max(len(a), len(b), len(c))\n"
            "    for i in range(n):\n"
            "        if i < len(a):\n"
            "            out.append(a[i])\n"
            "        if i < len(b):\n"
            "            out.append(b[i])\n"
            "        if i < len(c):\n"
            "            out.append(c[i])\n"
            "    return out\n",
            lambda low: "interleav" in low and "three" in low and "linked" not in low,
            (
                (([1, 2], [3, 4], [5, 6]), [1, 3, 5, 2, 4, 6]),
                (([1], [], [2, 3]), [1, 2, 3]),
                (([], [], []), []),
            ),
        ),
        T(
            "is_all_digits",
            "def is_all_digits(s):\n"
            '    """True when s is non-empty and every character is a digit."""\n'
            "    return bool(s) and s.isdigit()\n",
            lambda low: bool(re.search(r"all (characters are |chars are )?digits|string is all digits", low))
            and "count" not in low
            and "remove" not in low
            and "only" not in low,
            (
                (("123",), True),
                (("12a",), False),
                (("",), False),
            ),
        ),
        T(
            "split_commas",
            "def split_commas(s):\n"
            '    """Split on commas and strip whitespace around each field."""\n'
            "    if s == \"\":\n"
            "        return []\n"
            "    return [part.strip() for part in s.split(\",\")]\n",
            lambda low: "comma" in low and "split" in low and "csv" not in low,
            (
                (("a, b,c",), ["a", "b", "c"]),
                (("",), []),
                (("only",), ["only"]),
            ),
        ),
        T(
            "transpose_pairs",
            "def transpose_pairs(pairs):\n"
            '    """Turn a list of pairs into a pair of lists."""\n'
            "    if not pairs:\n"
            "        return [], []\n"
            "    left, right = zip(*pairs)\n"
            "    return list(left), list(right)\n",
            lambda low: "transpose" in low and "pair" in low and "matrix" not in low,
            (
                (([(1, "a"), (2, "b")],), ([1, 2], ["a", "b"])),
                (([],), ([], [])),
            ),
        ),
        T(
            "sliding_windows",
            "def sliding_windows(items, k):\n"
            '    """Contiguous windows of length k; empty when k is invalid."""\n'
            "    if k <= 0 or k > len(items):\n"
            "        return []\n"
            "    return [list(items[i:i + k]) for i in range(len(items) - k + 1)]\n",
            lambda low: (
                (
                    "sliding window" in low
                    or "sliding windows" in low
                    or (
                        ("window" in low or "windows" in low)
                        and ("list" in low or "size" in low or "size k" in low)
                    )
                )
                and "maximum" not in low
                and "minimum" not in low
            ),
            (
                (([1, 2, 3, 4], 2), [[1, 2], [2, 3], [3, 4]]),
                (([1, 2], 3), []),
                (([1], 1), [[1]]),
            ),
        ),
    ]
