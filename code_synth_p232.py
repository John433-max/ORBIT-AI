"""Cycle 518: sentence count, leading-zero strip, list range, positive filter, dict keys, ASCII sum.

Matchers stay narrower than count-words, zero-pad, min-of-list, and digit-sum.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_sentences",
            "def count_sentences(s):\n"
            '    """Count sentence-ending marks (. ! ?)."""\n'
            "    return sum(1 for ch in str(s) if ch in '.!?')\n",
            lambda low: (
                "sentence" in low
                and "count" in low
                and "word" not in low
                and "letter" not in low
            ),
            (
                (("Hi. Go!",), 2),
                (("no end",), 0),
                (("A? B. C!",), 3),
            ),
        ),
        T(
            "strip_leading_zeros",
            "def strip_leading_zeros(s):\n"
            '    """Drop leading zeros; keep a single zero and a leading minus."""\n'
            "    text = str(s)\n"
            "    sign = ''\n"
            "    if text.startswith('-'):\n"
            "        sign, text = '-', text[1:]\n"
            "    body = text.lstrip('0') or '0'\n"
            "    if body == '0':\n"
            "        return '0'\n"
            "    return sign + body\n",
            lambda low: (
                "leading" in low
                and "zero" in low
                and "pad" not in low
                and "count" not in low
            ),
            (
                (("007",), "7"),
                (("-0042",), "-42"),
                (("000",), "0"),
            ),
        ),
        T(
            "list_range",
            "def list_range(nums):\n"
            '    """Return max(nums) - min(nums); empty list is 0."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    return max(nums) - min(nums)\n",
            lambda low: (
                "range" in low
                and "list" in low
                and "missing" not in low
                and "python" not in low
                and "span" not in low
                and "index" not in low
                and "interquartile" not in low
                and "iqr" not in low
                and "statistical" not in low
            ),
            (
                (([3, 1, 9],), 8),
                (([4],), 0),
                (([],), 0),
            ),
        ),
        T(
            "filter_positive",
            "def filter_positive(nums):\n"
            '    """Keep values strictly greater than zero, preserving order."""\n'
            "    return [x for x in nums if x > 0]\n",
            lambda low: (
                "positive" in low
                and ("filter" in low or "keep" in low)
                and "count" not in low
                and "sum" not in low
                and "product" not in low
                and "matrix" not in low
            ),
            (
                (([1, -2, 0, 3],), [1, 3]),
                (([-1, -4],), []),
                (([],), []),
            ),
        ),
        T(
            "dict_keys",
            "def dict_keys(d):\n"
            '    """Return dictionary keys in insertion order."""\n'
            "    return list(d.keys())\n",
            lambda low: (
                "key" in low
                and ("dictionary" in low or "dict" in low)
                and "value" not in low
                and "sort" not in low
                and "invert" not in low
                and "missing" not in low
            ),
            (
                (({"a": 1, "b": 2},), ["a", "b"]),
                (({},), []),
                (({"z": 0},), ["z"]),
            ),
        ),
        T(
            "sum_ascii",
            "def sum_ascii(s):\n"
            '    """Sum Unicode code points of each character."""\n'
            "    return sum(ord(ch) for ch in str(s))\n",
            lambda low: "ascii" in low and "sum" in low and "count" not in low,
            (
                (("A",), 65),
                (("ab",), 195),
                (("",), 0),
            ),
        ),
    ]
