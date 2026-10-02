"""Cycle 367: second-largest digit, nice substring, sorted-rotated, one swap, population year, alternating binary flips."""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "second_largest_digit",
            "def second_largest_digit(s):\n"
            '    """Second-largest digit in s, or -1 (LeetCode 1796)."""\n'
            "    digits = sorted({int(c) for c in s if c.isdigit()})\n"
            "    return digits[-2] if len(digits) >= 2 else -1\n"
            "\n"
            "def secondHighest(s):\n"
            "    return second_largest_digit(s)\n"
            "\n"
            "def second_highest(s):\n"
            "    return second_largest_digit(s)\n",
            lambda low: bool(
                re.search(
                    r"\bsecond largest digit\b|"
                    r"\bleetcode 1796\b",
                    low,
                )
            ),
            (
                (("dfa12321afd",), 2),
                (("abc1111",), -1),
                (("sjhtz8344",), 4),
            ),
        ),
        T(
            "longest_nice_substring",
            "def longest_nice_substring(s):\n"
            '    """Longest substring with both cases of each letter (LeetCode 1763)."""\n'
            "    best = \"\"\n"
            "    n = len(s)\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n + 1):\n"
            "            if j - i <= len(best):\n"
            "                continue\n"
            "            sub = s[i:j]\n"
            "            letters = set(sub)\n"
            "            if all(ch.swapcase() in letters for ch in letters):\n"
            "                best = sub\n"
            "    return best\n"
            "\n"
            "def longestNiceSubstring(s):\n"
            "    return longest_nice_substring(s)\n",
            lambda low: bool(
                re.search(
                    r"\blongest nice substring\b|"
                    r"\bleetcode 1763\b",
                    low,
                )
            ),
            (
                (("YazaAay",), "aAa"),
                (("Bb",), "Bb"),
                (("c",), ""),
            ),
        ),
        T(
            "check_sorted_rotated",
            "def check_sorted_rotated(nums):\n"
            '    """True if nums is a rotation of a non-decreasing array (LeetCode 1752)."""\n'
            "    if not nums:\n"
            "        return True\n"
            "    drops = 0\n"
            "    n = len(nums)\n"
            "    for i in range(n):\n"
            "        if nums[i] > nums[(i + 1) % n]:\n"
            "            drops += 1\n"
            "            if drops > 1:\n"
            "                return False\n"
            "    return True\n"
            "\n"
            "def check(nums):\n"
            "    return check_sorted_rotated(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bsorted and rotated\b|"
                    r"\bleetcode 1752\b",
                    low,
                )
            ),
            (
                (((3, 4, 5, 1, 2),), True),
                (((2, 1, 3, 4),), False),
                (((1, 2, 3),), True),
            ),
        ),
        T(
            "one_string_swap",
            "def one_string_swap(s1, s2):\n"
            '    """True if s1 equals s2 after at most one swap (LeetCode 1790)."""\n'
            "    if len(s1) != len(s2):\n"
            "        return False\n"
            "    diff = [(a, b) for a, b in zip(s1, s2) if a != b]\n"
            "    return not diff or (len(diff) == 2 and diff[0] == diff[1][::-1])\n"
            "\n"
            "def areAlmostEqual(s1, s2):\n"
            "    return one_string_swap(s1, s2)\n",
            lambda low: bool(
                re.search(
                    r"\bone string swap\b|"
                    r"\balmost equal\b|"
                    r"\bleetcode 1790\b",
                    low,
                )
            ),
            (
                (("bank", "kanb"), True),
                (("attack", "defend"), False),
                (("kelb", "kelb"), True),
            ),
        ),
        T(
            "maximum_population_year",
            "def maximum_population_year(logs):\n"
            '    """Earliest year with the highest population (LeetCode 1854)."""\n'
            "    delta = [0] * 101\n"
            "    for birth, death in logs:\n"
            "        delta[birth - 1950] += 1\n"
            "        delta[death - 1950] -= 1\n"
            "    best = cur = 0\n"
            "    year = 1950\n"
            "    for i, change in enumerate(delta):\n"
            "        cur += change\n"
            "        if cur > best:\n"
            "            best = cur\n"
            "            year = 1950 + i\n"
            "    return year\n"
            "\n"
            "def maximumPopulation(logs):\n"
            "    return maximum_population_year(logs)\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum population year\b|"
                    r"\bleetcode 1854\b",
                    low,
                )
            ),
            (
                ((((1993, 1999), (2000, 2010)),), 1993),
                ((((1950, 1961), (1960, 1971), (1970, 1981)),), 1960),
                ((((1980, 1990), (1985, 1995)),), 1985),
            ),
        ),
        T(
            "min_changes_alternating",
            "def min_changes_alternating(s):\n"
            '    """Min flips so a binary string alternates (LeetCode 1758)."""\n'
            "    start0 = start1 = 0\n"
            "    for i, ch in enumerate(s):\n"
            "        expect0 = '0' if i % 2 == 0 else '1'\n"
            "        if ch != expect0:\n"
            "            start0 += 1\n"
            "        else:\n"
            "            start1 += 1\n"
            "    return min(start0, start1)\n"
            "\n"
            "def minOperations(s):\n"
            "    return min_changes_alternating(s)\n",
            lambda low: bool(
                re.search(
                    r"\balternating binary\b|"
                    r"\bleetcode 1758\b",
                    low,
                )
            ),
            (
                (("0100",), 1),
                (("10",), 0),
                (("1111",), 2),
            ),
        ),
    ]
