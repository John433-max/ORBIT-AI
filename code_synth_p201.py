"""Cycle 485: vowel indices, collapse spaces, strip punctuation, keep digits, argmin, extract ints.

Matchers stay phrase-specific so vowel counts, strip-digits, and argmax keep their asks.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    punct_src = (
        "def strip_punctuation(s):\n"
        '    """Drop ASCII punctuation; keep letters, digits, and other chars."""\n'
        "    import string\n"
        "    punct = set(string.punctuation)\n"
        "    return ''.join(ch for ch in s if ch not in punct)\n"
    )
    extract_src = (
        "def extract_integers(s):\n"
        '    """Signed integers in left-to-right order. A leading minus binds."""\n'
        "    out = []\n"
        "    i = 0\n"
        "    n = len(s)\n"
        "    while i < n:\n"
        "        if s[i] == '-' and i + 1 < n and s[i + 1].isdigit():\n"
        "            j = i + 1\n"
        "            while j < n and s[j].isdigit():\n"
        "                j += 1\n"
        "            out.append(int(s[i:j]))\n"
        "            i = j\n"
        "        elif s[i].isdigit():\n"
        "            j = i\n"
        "            while j < n and s[j].isdigit():\n"
        "                j += 1\n"
        "            out.append(int(s[i:j]))\n"
        "            i = j\n"
        "        else:\n"
        "            i += 1\n"
        "    return out\n"
    )
    return [
        T(
            "vowel_indices",
            "def vowel_indices(s):\n"
            '    """Indices of ASCII vowels in s, left to right."""\n'
            "    vowels = set('aeiouAEIOU')\n"
            "    return [i for i, ch in enumerate(s) if ch in vowels]\n",
            lambda low: "vowel" in low
            and ("index" in low or "indices" in low or "positions" in low)
            and "count" not in low,
            (
                (("orbit",), [0, 3]),
                (("aeiou",), [0, 1, 2, 3, 4]),
                (("xyz",), []),
            ),
        ),
        T(
            "collapse_spaces",
            "def collapse_spaces(s):\n"
            '    """Collapse runs of whitespace to a single space and strip ends."""\n'
            "    return ' '.join(s.split())\n",
            lambda low: bool(
                re.search(
                    r"collaps(?:e|es|ing) (?:repeated )?(?:white)?spaces|collaps(?:e|es|ing) whitespace",
                    low,
                )
            ),
            (
                (("a  b\tc",), "a b c"),
                (("  orbit  ",), "orbit"),
                (("",), ""),
            ),
        ),
        T(
            "strip_punctuation",
            punct_src,
            lambda low: bool(
                re.search(r"strip(?:s|ping)? punctuation|remove punctuation", low)
            )
            and "digit" not in low,
            (
                (("hi, orbit!",), "hi orbit"),
                (("a.b",), "ab"),
                (("plain",), "plain"),
            ),
        ),
        T(
            "only_digits",
            "def only_digits(s):\n"
            '    """Keep decimal digit characters; drop everything else."""\n'
            "    return ''.join(ch for ch in s if ch.isdigit())\n",
            lambda low: bool(
                re.search(r"keep only digits|only digits|extract digits", low)
            )
            and "integer" not in low
            and "strip" not in low,
            (
                (("a1b2",), "12"),
                (("orbit",), ""),
                (("42",), "42"),
            ),
        ),
        T(
            "argmin_list",
            "def argmin_list(nums):\n"
            '    """Index of the first minimum. Empty list returns -1."""\n'
            "    if not nums:\n"
            "        return -1\n"
            "    best_i = 0\n"
            "    for i, v in enumerate(nums):\n"
            "        if v < nums[best_i]:\n"
            "            best_i = i\n"
            "    return best_i\n",
            lambda low: (
                "argmin" in low
                or "index of the minimum" in low
                or "index of min" in low
            )
            and "max" not in low,
            (
                (([3, 1, 2],), 1),
                (([5, 5, 1],), 2),
                (([],), -1),
            ),
        ),
        T(
            "extract_integers",
            extract_src,
            lambda low: bool(re.search(r"extract(?:s|ing)? integers?", low))
            and "digit" not in low,
            (
                (("a 12 b -3",), [12, -3]),
                (("none",), []),
                (("-7x8",), [-7, 8]),
            ),
        ),
    ]
