"""Cycle 442: interleave, digit sum, unique characters, swap, strip punctuation, pairs to dict.

These asks returned no template (NotImplemented draft). Matchers are phrase-gated
so list-unique, zip-to-dict, and vowel counts keep their existing names.

Cycle 443: digit_sum must not steal LeetCode siblings that also say "sum of digits"
(get_lucky / count_even / sum_base). Those live in earlier packs and win only if
this broad matcher declines.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "interleave",
            "def interleave(a, b):\n"
            '    """Alternate items from a and b; leftover tail is appended."""\n'
            "    out = []\n"
            "    n = min(len(a), len(b))\n"
            "    for i in range(n):\n"
            "        out.append(a[i])\n"
            "        out.append(b[i])\n"
            "    out.extend(a[n:])\n"
            "    out.extend(b[n:])\n"
            "    return out\n",
            lambda low: "interleav" in low and "linked" not in low and "string" not in low,
            (
                (([1, 2, 3], ["a", "b"]), [1, "a", 2, "b", 3]),
                (([1], [2, 3]), [1, 2, 3]),
            ),
        ),
        T(
            "digit_sum",
            "def digit_sum(n):\n"
            '    """Return the sum of decimal digits (sign ignored)."""\n'
            "    total = 0\n"
            "    for ch in str(abs(int(n))):\n"
            "        total += int(ch)\n"
            "    return total\n",
            lambda low: bool(re.search(r"\bdigit[- ]?sum\b|\bsum of (?:the )?digits\b", low))
            and "divide" not in low
            and "alternat" not in low
            and "leetcode" not in low
            and "base" not in low
            and "string" not in low
            and "even" not in low
            and "count" not in low
            and "convert" not in low
            and "product" not in low
            and "element" not in low
            and "index" not in low
            and "divisib" not in low,
            (((123,), 6), ((0,), 0)),
        ),
        T(
            "unique_chars",
            "def unique_chars(s):\n"
            '    """Return unique characters in first-seen order."""\n'
            "    seen = set()\n"
            "    out = []\n"
            "    for ch in str(s):\n"
            "        if ch in seen:\n"
            "            continue\n"
            "        seen.add(ch)\n"
            "        out.append(ch)\n"
            "    return \"\".join(out)\n",
            lambda low: bool(re.search(r"\bunique\b", low))
            and bool(re.search(r"\bcharacters?\b|\bchars?\b", low))
            and "list" not in low,
            ((("abca",), "abc"), (("",), "")),
        ),
        T(
            "swap_values",
            "def swap_values(a, b):\n"
            '    """Return a and b exchanged."""\n'
            "    return b, a\n",
            lambda low: bool(re.search(r"\bswaps?\b", low))
            and bool(re.search(r"\b(variables?|values?|two)\b", low))
            and "dict" not in low
            and "key" not in low
            and "node" not in low,
            (((1, 2), (2, 1)), (("x", "y"), ("y", "x"))),
        ),
        T(
            "remove_punctuation",
            "def remove_punctuation(s):\n"
            '    """Drop punctuation; keep letters, digits, and spaces."""\n'
            "    return \"\".join(ch for ch in str(s) if ch.isalnum() or ch.isspace())\n",
            lambda low: "punctuation" in low
            and bool(re.search(r"\b(remov\w*|strip|drop|without)\b", low))
            and "palindrome" not in low,
            ((("hi, world!",), "hi world"), (("a.b",), "ab")),
        ),
        T(
            "pairs_to_dict",
            "def pairs_to_dict(pairs):\n"
            '    """Build a dict from (key, value) pairs; later keys win."""\n'
            "    return {k: v for k, v in pairs}\n",
            lambda low: bool(re.search(r"\bpairs?\b", low))
            and bool(re.search(r"\bdicts?\b|\bdictionary\b", low))
            and "linked" not in low
            and "zip" not in low,
            (
                ((("a", 1), ("b", 2)],), {"a": 1, "b": 2}),
                ((("a", 1), ("a", 3)],), {"a": 3}),
            ),
        ),
    ]
