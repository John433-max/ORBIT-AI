"""Cycle 483: swap-case, list GCD, shortest word, word lengths, initials, prefix mins.

Matchers stay phrase-specific so two-argument gcd, swap-values, running maximum,
and shortest-path templates keep their asks.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "swap_case",
            "def swap_case(s):\n"
            '    """Swap uppercase and lowercase letters; leave other chars."""\n'
            "    return ''.join(\n"
            "        ch.lower() if ch.isupper() else ch.upper() if ch.islower() else ch\n"
            "        for ch in s\n"
            "    )\n",
            lambda low: bool(re.search(r"swaps?(?: the)?[- ]case", low))
            and "node" not in low
            and "value" not in low,
            (
                (("AbC",), "aBc"),
                (("",), ""),
                (("Hello!",), "hELLO!"),
            ),
        ),
        T(
            "gcd_of_list",
            "def gcd_of_list(nums):\n"
            '    """Greatest common divisor of a list of integers. Empty -> 0."""\n'
            "    def _gcd(a, b):\n"
            "        a, b = abs(int(a)), abs(int(b))\n"
            "        while b:\n"
            "            a, b = b, a % b\n"
            "        return a\n"
            "    acc = 0\n"
            "    for x in nums:\n"
            "        acc = _gcd(acc, x)\n"
            "    return acc\n",
            lambda low: bool(
                re.search(r"gcd of (?:a |the )?list|gcd of numbers|greatest common divisor of (?:a |the )?list", low)
            )
            and "string" not in low,
            (
                (([48, 18, 30],), 6),
                (([7, 13],), 1),
                (([],), 0),
            ),
        ),
        T(
            "shortest_word",
            "def shortest_word(s):\n"
            '    """Shortest whitespace-separated word, or empty string if none."""\n'
            "    words = s.split()\n"
            "    if not words:\n"
            "        return ''\n"
            "    return min(words, key=len)\n",
            lambda low: "shortest word" in low
            and "ladder" not in low
            and "path" not in low
            and "completing" not in low
            and "matrix" not in low,
            (
                (("tiny orbit runtime",), "tiny"),
                (("a bb",), "a"),
                (("",), ""),
            ),
        ),
        T(
            "word_lengths",
            "def word_lengths(s):\n"
            '    """Length of each whitespace-separated word."""\n'
            "    return [len(w) for w in s.split()]\n",
            lambda low: bool(
                re.search(r"word lengths|length of each word|lengths of each word", low)
            )
            and "longest" not in low
            and "shortest" not in low,
            (
                (("ab c",), [2, 1]),
                (("",), []),
                (("one",), [3]),
            ),
        ),
        T(
            "initials",
            "def initials(s):\n"
            '    """First letter of each whitespace-separated word, uppercased."""\n'
            "    return ''.join(w[0].upper() for w in s.split() if w)\n",
            lambda low: bool(
                re.search(r"initials of|first letters of each word", low)
            )
            and "acronym" not in low,
            (
                (("orbit ai runtime",), "OAR"),
                (("a",), "A"),
                (("",), ""),
            ),
        ),
        T(
            "cumulative_min",
            "def cumulative_min(nums):\n"
            '    """Prefix minima: each position is the min seen so far."""\n'
            "    out = []\n"
            "    best = None\n"
            "    for x in nums:\n"
            "        best = x if best is None else min(best, x)\n"
            "        out.append(best)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"cumulative[- ]min(?:imum|ima)?|prefix[- ]min(?:imum|ima)?|running[- ]min(?:imum)?", low)
            ),
            (
                (([3, 1, 2, 0],), [3, 1, 1, 0]),
                (([],), []),
                (([4],), [4]),
            ),
        ),
    ]
