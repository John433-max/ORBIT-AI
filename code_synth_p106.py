"""Cycle 384: Easy prompts still absent from the template index.

LeetCode 1979 / 1984 / 2164 / 2273 / 2287 / 3014 were not referenced by any
pack. Matchers stay ID- or phrase-specific so gcd, sort, anagram, and
character-count templates keep their existing prompts. Loaded before p1.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "find_gcd_array",
            "def find_gcd_array(nums):\n"
            '    """GCD of the smallest and largest values (LeetCode 1979)."""\n'
            "    from math import gcd\n"
            "    return gcd(min(nums), max(nums))\n"
            "\n"
            "def findGCD(nums):\n"
            "    return find_gcd_array(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1979\b|\bgcd of an array\b|"
                    r"\bgreatest common divisor of an array\b",
                    low,
                )
            ),
            (
                (([2, 5, 6, 9, 10],), 2),
                (([7, 5, 6, 8, 3],), 1),
                (([3, 3],), 3),
            ),
        ),
        T(
            "min_diff_k_scores",
            "def min_diff_k_scores(nums, k):\n"
            '    """Min highest-lowest gap over any k scores (LeetCode 1984)."""\n'
            "    if k <= 1:\n"
            "        return 0\n"
            "    s = sorted(nums)\n"
            "    return min(s[i + k - 1] - s[i] for i in range(len(s) - k + 1))\n"
            "\n"
            "def minimumDifference(nums, k):\n"
            "    return min_diff_k_scores(nums, k)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1984\b|\bk scores\b|"
                    r"\bminimum difference between highest and lowest\b",
                    low,
                )
            ),
            (
                (([90], 1), 0),
                (([9, 4, 1, 7], 2), 2),
                (([9, 4, 1, 7], 3), 5),
            ),
        ),
        T(
            "sort_even_odd_indices",
            "def sort_even_odd_indices(nums):\n"
            '    """Even indices ascending, odd indices descending (LeetCode 2164)."""\n'
            "    even = sorted(nums[0::2])\n"
            "    odd = sorted(nums[1::2], reverse=True)\n"
            "    out = []\n"
            "    for i in range(len(nums)):\n"
            "        out.append(even[i // 2] if i % 2 == 0 else odd[i // 2])\n"
            "    return out\n"
            "\n"
            "def sortEvenOdd(nums):\n"
            "    return sort_even_odd_indices(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2164\b|\bsort even and odd indices\b|"
                    r"\beven and odd indices independently\b",
                    low,
                )
            ),
            (
                (([4, 1, 2, 3],), [2, 3, 4, 1]),
                (([2, 1],), [2, 1]),
            ),
        ),
        T(
            "remove_anagrams",
            "def remove_anagrams(words):\n"
            '    """Drop words that are anagrams of the previous keep (LeetCode 2273)."""\n'
            "    out = []\n"
            "    prev = None\n"
            "    for w in words:\n"
            "        sig = tuple(sorted(w))\n"
            "        if sig != prev:\n"
            "            out.append(w)\n"
            "            prev = sig\n"
            "    return out\n"
            "\n"
            "def removeAnagrams(words):\n"
            "    return remove_anagrams(words)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2273\b|\bremoving anagrams\b|\bremove anagrams\b",
                    low,
                )
            ),
            (
                ((["abba", "baba", "bbaa", "cd", "cd"],), ["abba", "cd"]),
                ((["a", "b", "c", "d", "e"],), ["a", "b", "c", "d", "e"]),
            ),
        ),
        T(
            "rearrange_characters",
            "def rearrange_characters(s, target):\n"
            '    """How many copies of target fit in s (LeetCode 2287)."""\n'
            "    from collections import Counter\n"
            "    have, need = Counter(s), Counter(target)\n"
            "    return min(have[ch] // need[ch] for ch in need)\n"
            "\n"
            "def rearrangeCharacters(s, target):\n"
            "    return rearrange_characters(s, target)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2287\b|"
                    r"\brearrange characters to make target\b",
                    low,
                )
            ),
            (
                (("ilovecodingonleetcode", "code"), 2),
                (("abcba", "abc"), 1),
                (("abbaccaddaeea", "aaaaa"), 1),
            ),
        ),
        T(
            "minimum_pushes",
            "def minimum_pushes(word):\n"
            '    """Min key pushes for a distinct-letter word on 8 keys (LeetCode 3014)."""\n'
            "    n = len(word)\n"
            "    return sum(i // 8 + 1 for i in range(n))\n"
            "\n"
            "def minimumPushes(word):\n"
            "    return minimum_pushes(word)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3014\b|\bminimum pushes to type word\b|"
                    r"\bminimum number of pushes\b",
                    low,
                )
            ),
            (
                (("abcde",), 5),
                (("xycdefghij",), 12),
            ),
        ),
    ]
