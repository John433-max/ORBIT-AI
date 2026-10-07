"""Cycle 484: consonants, digit product, middle chars, strip digits, long words, zip pairs.

Matchers stay phrase-specific so vowel counts, list products, and interleave
templates keep their asks.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_consonants",
            "def count_consonants(s):\n"
            '    """Count ASCII consonants. Vowels and non-letters are ignored."""\n'
            "    vowels = set('aeiouAEIOU')\n"
            "    return sum(1 for ch in s if ch.isalpha() and ch not in vowels)\n",
            lambda low: "consonant" in low and "vowel" not in low,
            (
                (("orbit",), 3),
                (("aeiou",), 0),
                (("A1 b",), 1),
            ),
        ),
        T(
            "digit_product",
            "def digit_product(n):\n"
            '    """Product of decimal digits. 0 if any digit is 0."""\n'
            "    n = abs(int(n))\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    prod = 1\n"
            "    while n:\n"
            "        prod *= n % 10\n"
            "        n //= 10\n"
            "    return prod\n",
            lambda low: bool(re.search(r"product of (?:the )?digits", low))
            and "list" not in low
            and "array" not in low,
            (
                ((234,), 24),
                ((105,), 0),
                ((7,), 7),
            ),
        ),
        T(
            "middle_chars",
            "def middle_chars(s):\n"
            '    """Middle character, or the two middle characters if length is even."""\n'
            "    n = len(s)\n"
            "    if n == 0:\n"
            "        return ''\n"
            "    mid = n // 2\n"
            "    if n % 2:\n"
            "        return s[mid]\n"
            "    return s[mid - 1:mid + 1]\n",
            lambda low: "middle character" in low and "matrix" not in low,
            (
                (("abc",), "b"),
                (("abcd",), "bc"),
                (("",), ""),
            ),
        ),
        T(
            "strip_digits",
            "def strip_digits(s):\n"
            '    """Remove decimal digit characters; keep everything else."""\n'
            "    return ''.join(ch for ch in s if not ch.isdigit())\n",
            lambda low: bool(re.search(r"strip(?:s|ping)? digits|remove digits from", low))
            and "leading" not in low,
            (
                (("a1b2",), "ab"),
                (("orbit",), "orbit"),
                (("42",), ""),
            ),
        ),
        T(
            "words_longer_than",
            "def words_longer_than(s, n):\n"
            '    """Whitespace-separated words whose length is greater than n."""\n'
            "    return [w for w in s.split() if len(w) > n]\n",
            lambda low: "words longer than" in low and "path" not in low,
            (
                (("tiny orbit runtime", 4), ["orbit", "runtime"]),
                (("a bb", 1), ["bb"]),
                (("", 0), []),
            ),
        ),
        T(
            "zip_pairs",
            "def zip_pairs(a, b):\n"
            '    """Pair items from two lists up to the shorter length."""\n'
            "    return list(zip(a, b))\n",
            lambda low: bool(re.search(r"zip(?:s|ping)? two lists|pairs from two lists", low))
            and "interleav" not in low,
            (
                (([1, 2], ["a", "b"]), [(1, "a"), (2, "b")]),
                (([1], [9, 8]), [(1, 9)]),
                (([], [1]), []),
            ),
        ),
    ]
