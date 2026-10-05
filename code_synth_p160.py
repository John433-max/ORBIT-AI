"""Cycle 441: deep copy, longest word, filter even, query parse, order-free equality, drop None.

These asks fell through to the NotImplemented draft. filter_even loads before
is_even so "filter even numbers" is not classified as a boolean even-check.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "deep_copy",
            "def deep_copy(obj):\n"
            '    """Return a recursive copy so nested lists/dicts are independent."""\n'
            "    import copy\n"
            "    return copy.deepcopy(obj)\n",
            lambda low: bool(re.search(r"\bdeep[- ]?cop(?:y|ies|ied)\b|\bdeepcopy\b", low)),
            (
                (([[1, 2], [3]],), [[1, 2], [3]]),
                (({"a": [1]},), {"a": [1]}),
            ),
        ),
        T(
            "longest_word",
            "def longest_word(s):\n"
            '    """Return the longest whitespace-separated word (first on ties)."""\n'
            "    best = \"\"\n"
            "    for word in str(s).split():\n"
            "        if len(word) > len(best):\n"
            "            best = word\n"
            "    return best\n",
            lambda low: "longest" in low and bool(re.search(r"\bwords?\b", low))
            and "substring" not in low
            and "palindrom" not in low
            and "increasing" not in low
            and "common" not in low,
            ((("a bb ccc",), "ccc"), (("hi",), "hi"), (("",), "")),
        ),
        T(
            "filter_even",
            "def filter_even(nums):\n"
            '    """Keep even integers, preserving order."""\n'
            "    return [x for x in nums if x % 2 == 0]\n",
            lambda low: bool(re.search(r"\b(filters?|filtering|keep|select)\b", low))
            and bool(re.search(r"\beven\b", low))
            and "odd" not in low,
            (
                (([1, 2, 3, 4],), [2, 4]),
                (([1, 3],), []),
            ),
        ),
        T(
            "parse_query",
            "def parse_query(qs):\n"
            '    """Parse a query string (optional ?url) into a dict of strings."""\n'
            "    from urllib.parse import parse_qsl\n"
            "    text = str(qs)\n"
            "    if \"?\" in text:\n"
            "        text = text.split(\"?\", 1)[1]\n"
            "    return dict(parse_qsl(text, keep_blank_values=True))\n",
            lambda low: bool(re.search(r"\bquery[- ]?string\b|\burl query\b|\bparse query\b", low)),
            (
                (("a=1&b=2",), {"a": "1", "b": "2"}),
                (("https://x.test/p?q=hi",), {"q": "hi"}),
            ),
        ),
        T(
            "equal_ignore_order",
            "def equal_ignore_order(a, b):\n"
            '    """True if sequences contain the same items with the same counts."""\n'
            "    return sorted(a) == sorted(b)\n",
            lambda low: bool(
                re.search(r"ignor(?:e|ing) order|regardless of order|same elements|as multisets?", low)
            )
            and bool(re.search(r"\blists?\b|\bsequences?\b", low)),
            (
                (([1, 2, 2], [2, 1, 2]), True),
                (([1, 2], [1, 2, 2]), False),
            ),
        ),
        T(
            "drop_none",
            "def drop_none(items):\n"
            '    """Drop None values, keeping other falsy items."""\n'
            "    return [x for x in items if x is not None]\n",
            lambda low: bool(re.search(r"\b(drop|remove|filter|strip)\b", low))
            and "none" in low
            and "linked" not in low,
            (
                (([1, None, 0, None, 2],), [1, 0, 2]),
                (([None],), []),
            ),
        ),
    ]
