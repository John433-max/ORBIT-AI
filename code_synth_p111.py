"""Cycle 390: Easy prompts still absent from the template index.

LeetCode 3783, 3794, 3798, 3803, 3813, and 3827 were not referenced by any
pack. Matchers stay ID- or title-specific so reverse-prefix-of-word (2000),
count-vowels, and reverse-vowels keep their prompts.
Loaded before p110.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "mirror_distance",
            "def mirror_distance(n):\n"
            '    """Absolute difference between n and its digit reverse (LeetCode 3783)."""\n'
            "    rev = int(str(int(n))[::-1])\n"
            "    return abs(int(n) - rev)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3783\b|"
                    r"\bmirror distance\b",
                    low,
                )
            ),
            (
                ((25,), 27),
                ((10,), 9),
                ((7,), 0),
            ),
        ),
        T(
            "reverse_string_prefix",
            "def reverse_string_prefix(s, k):\n"
            '    """Reverse the first k characters of s (LeetCode 3794)."""\n'
            "    k = int(k)\n"
            "    return s[:k][::-1] + s[k:]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3794\b|"
                    r"\breverse string prefix\b|"
                    r"\breverse the first k characters\b",
                    low,
                )
            ),
            (
                (("abcd", 2), "bacd"),
                (("xyz", 3), "zyx"),
                (("hey", 1), "hey"),
            ),
        ),
        T(
            "largest_even_number",
            "def largest_even_number(s):\n"
            '    """Largest even integer by deleting chars from a 1/2 string (LeetCode 3798)."""\n'
            "    return s.rstrip('1')\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3798\b|"
                    r"\blargest even number\b|"
                    r"\blargest possible even\b",
                    low,
                )
            ),
            (
                (("1112",), "1112"),
                (("221",), "22"),
                (("1",), ""),
            ),
        ),
        T(
            "count_residue_prefixes",
            "def count_residue_prefixes(s):\n"
            '    """Prefixes whose distinct count equals length mod 3 (LeetCode 3803)."""\n'
            "    seen = set()\n"
            "    ans = 0\n"
            "    for i, ch in enumerate(s, 1):\n"
            "        seen.add(ch)\n"
            "        if len(seen) == i % 3:\n"
            "            ans += 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3803\b|"
                    r"\bresidue prefixes\b|"
                    r"\bcount residue prefix",
                    low,
                )
            ),
            (
                (("abc",), 2),
                (("dd",), 1),
                (("bob",), 2),
            ),
        ),
        T(
            "vowel_consonant_score",
            "def vowel_consonant_score(s):\n"
            '    """floor(vowels/consonants), ignoring spaces and digits (LeetCode 3813)."""\n'
            "    vowels = set('aeiou')\n"
            "    v = c = 0\n"
            "    for ch in s:\n"
            "        if ch.isalpha():\n"
            "            if ch in vowels:\n"
            "                v += 1\n"
            "            else:\n"
            "                c += 1\n"
            "    return 0 if c == 0 else v // c\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3813\b|"
                    r"\bvowel[- ]consonant score\b",
                    low,
                )
            ),
            (
                (("cooear",), 2),
                (("axeyizou",), 1),
                (("au 123",), 0),
            ),
        ),
        T(
            "count_monobit",
            "def count_monobit(n):\n"
            '    """Count 0 and all-ones binaries in [0, n] (LeetCode 3827)."""\n'
            "    n = int(n)\n"
            "    ans = x = 1\n"
            "    i = 1\n"
            "    while x <= n:\n"
            "        ans += 1\n"
            "        x += 1 << i\n"
            "        i += 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3827\b|"
                    r"\bmonobit integers?\b|"
                    r"\bcount monobit\b",
                    low,
                )
            ),
            (
                ((1,), 2),
                ((4,), 3),
                ((0,), 1),
            ),
        ),
    ]
