"""Cycle 488: blank lines, adjacent swap, distinct count, wrap, join, digits.

Matchers are phrase-specific so chunk, last-n, digit-count, and pad-left
templates keep their asks.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "remove_blank_lines",
            "def remove_blank_lines(s):\n"
            '    """Drop lines that are empty or whitespace-only."""\n'
            "    s = str(s)\n"
            "    lines = s.splitlines()\n"
            "    return '\\n'.join(line for line in lines if line.strip())\n",
            lambda low: "blank" in low and "line" in low and "string" in low,
            (
                (("a\n\n b\n",), "a\n b"),
                (("\n\n",), ""),
                (("keep",), "keep"),
            ),
        ),
        T(
            "swap_adjacent",
            "def swap_adjacent(items):\n"
            '    """Swap each adjacent pair; leave a trailing odd item in place."""\n'
            "    items = list(items)\n"
            "    out = items[:]\n"
            "    for i in range(0, len(out) - 1, 2):\n"
            "        out[i], out[i + 1] = out[i + 1], out[i]\n"
            "    return out\n",
            lambda low: "adjacent" in low and "pair" in low and "list" in low,
            (
                (([1, 2, 3, 4],), [2, 1, 4, 3]),
                (([1],), [1]),
                (([],), []),
            ),
        ),
        T(
            "count_distinct",
            "def count_distinct(items):\n"
            '    """Count unique values, preserving hashable equality."""\n'
            "    return len(set(items))\n",
            lambda low: "distinct" in low and ("count" in low or "number" in low) and "list" in low,
            (
                (([1, 1, 2, 3],), 3),
                (([],), 0),
                (("aba",), 2),
            ),
        ),
        T(
            "wrap_text",
            "def wrap_text(s, width):\n"
            '    """Hard-wrap a string into lines of at most width characters."""\n'
            "    s = str(s)\n"
            "    width = int(width)\n"
            "    if width <= 0:\n"
            "        return s\n"
            "    return '\\n'.join(s[i:i + width] for i in range(0, len(s), width))\n",
            lambda low: "wrap" in low and "width" in low and "string" in low and "word" not in low,
            (
                (("abcdef", 2), "ab\ncd\nef"),
                (("hi", 10), "hi"),
                (("", 3), ""),
            ),
        ),
        T(
            "join_with",
            "def join_with(items, sep):\n"
            '    """Join items with a separator after stringifying each item."""\n'
            "    return str(sep).join(str(x) for x in items)\n",
            lambda low: "separator" in low and "between" in low and "list" in low,
            (
                ((["a", "b", "c"], "-"), "a-b-c"),
                (([], ","), ""),
                (([1, 2], ":"), "1:2"),
            ),
        ),
        T(
            "extract_digits",
            "def extract_digits(s):\n"
            '    """Return only the digit characters, in order."""\n'
            "    return ''.join(ch for ch in str(s) if ch.isdigit())\n",
            lambda low: "extract" in low and "digit" in low and "string" in low,
            (
                (("a1b22",), "122"),
                (("none",), ""),
                (("09",), "09"),
            ),
        ),
    ]
