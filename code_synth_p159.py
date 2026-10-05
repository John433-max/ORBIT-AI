"""Cycle 440: rotation check, word-frequency map, nested-dict flatten.

These asks either fell through to the NotImplemented draft (string rotation)
or were stolen by list flatten / whitespace word-count templates.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "is_rotation",
            "def is_rotation(a, b):\n"
            '    """True if b is a rotation of a (same length, b in a+a)."""\n'
            "    a, b = str(a), str(b)\n"
            "    if len(a) != len(b):\n"
            "        return False\n"
            "    return b in (a + a)\n",
            lambda low: bool(re.search(r"\brotat(?:e|es|ed|ion|ions)\b", low))
            and bool(re.search(r"\bstring|str\b", low))
            and "matrix" not in low
            and "image" not in low
            and "list" not in low,
            ((("abcde", "cdeab"), True), (("abc", "acb"), False)),
        ),
        T(
            "word_frequency",
            "def word_frequency(s):\n"
            '    """Count whitespace-separated word occurrences."""\n'
            "    counts = {}\n"
            "    for word in str(s).split():\n"
            "        counts[word] = counts.get(word, 0) + 1\n"
            "    return counts\n",
            lambda low: bool(
                re.search(r"\bfrequenc(?:y|ies)\b|\bfreq\b|\bhistogram\b", low)
                and re.search(r"\bwords?\b", low)
            )
            and "character" not in low
            and "letter" not in low,
            ((("a b a",), {"a": 2, "b": 1}), (("one",), {"one": 1})),
        ),
        T(
            "flatten_dict",
            "def flatten_dict(mapping, sep='.'):\n"
            '    """Flatten a nested dict; keys join with sep."""\n'
            "    out = {}\n"
            "\n"
            "    def walk(node, prefix):\n"
            "        if isinstance(node, dict):\n"
            "            for key, value in node.items():\n"
            "                nxt = f\"{prefix}{sep}{key}\" if prefix else str(key)\n"
            "                walk(value, nxt)\n"
            "        else:\n"
            "            out[prefix] = node\n"
            "\n"
            "    walk(mapping, \"\")\n"
            "    return out\n",
            lambda low: "flatten" in low
            and bool(re.search(r"\bdict(?:ionary|ionaries)?\b", low))
            and "list" not in low,
            (
                (({"a": {"b": 1}, "c": 2},), {"a.b": 1, "c": 2}),
                (({"x": 1},), {"x": 1}),
            ),
        ),
    ]
