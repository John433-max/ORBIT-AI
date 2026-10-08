"""Cycle 523: line count, tabs-to-spaces, leading vowel, value indices, list rotation, inclusive range sum.

These asks fell through to the NotImplemented draft. Matchers stay narrower than
rotate_string, index-of, and generic range/sum templates.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "line_count",
            "def line_count(text):\n"
            '    """Number of lines; empty text is 0; a trailing newline does not add an extra line."""\n'
            "    if text == \"\":\n"
            "        return 0\n"
            "    return len(text.splitlines())\n",
            lambda low: bool(re.search(r"\b(number of|count) lines\b", low))
            and "online" not in low,
            (
                (("a\nb",), 2),
                (("",), 0),
                (("a\n",), 1),
            ),
        ),
        T(
            "tabs_to_spaces",
            "def tabs_to_spaces(text, width=4):\n"
            '    """Replace each tab with width spaces."""\n'
            "    return text.replace(\"\\t\", \" \" * width)\n",
            lambda low: "tab" in low and "space" in low and "replac" in low,
            (
                (("a\tb",), "a    b"),
                (("a\tb", 2), "a  b"),
                (("",), ""),
            ),
        ),
        T(
            "starts_with_vowel",
            "def starts_with_vowel(text):\n"
            '    """True if the first non-space character is a vowel (aeiou)."""\n'
            "    s = text.lstrip()\n"
            "    return bool(s) and s[0].lower() in \"aeiou\"\n",
            lambda low: "vowel" in low and "start" in low and "count" not in low,
            (
                (("apple",), True),
                (("  Orange",), True),
                (("sky",), False),
                (("",), False),
            ),
        ),
        T(
            "indices_of",
            "def indices_of(items, value):\n"
            '    """Every index where items equals value."""\n'
            "    return [i for i, x in enumerate(items) if x == value]\n",
            lambda low: "indices of" in low and "matrix" not in low,
            (
                (([1, 2, 1, 3], 1), [0, 2]),
                ((["a", "b"], "z"), []),
                (([], 0), []),
            ),
        ),
        T(
            "is_list_rotation",
            "def is_list_rotation(a, b):\n"
            '    """True if b is a rotation of a (same length, same cyclic order)."""\n'
            "    a = list(a)\n"
            "    b = list(b)\n"
            "    if len(a) != len(b):\n"
            "        return False\n"
            "    if not a:\n"
            "        return True\n"
            "    return any(a[i:] + a[:i] == b for i in range(len(a)))\n",
            lambda low: "rotation" in low
            and ("each other" in low or "are rotations" in low)
            and "string" not in low
            and "matrix" not in low,
            (
                (([1, 2, 3], [3, 1, 2]), True),
                (([1, 2, 3], [1, 3, 2]), False),
                (([], []), True),
            ),
        ),
        T(
            "inclusive_range_sum",
            "def inclusive_range_sum(start, end):\n"
            '    """Sum of integers from start through end, inclusive."""\n'
            "    if end < start:\n"
            "        start, end = end, start\n"
            "    return (end - start + 1) * (start + end) // 2\n",
            lambda low: "inclusive" in low and "range" in low and "sum" in low,
            (
                ((1, 3), 6),
                ((3, 1), 6),
                ((5, 5), 5),
            ),
        ),
    ]
