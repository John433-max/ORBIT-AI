"""Cycle 377: split-array, two-occurrence substring, valid word, prefix min cost, distinct length-3, ops to k.

3046 / 3090 / 3136 / 3502 / 3258 / 3375 were unmatched stubs.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "is_possible_to_split",
            "def is_possible_to_split(nums):\n"
            '    """True if even array can be split into two equal distinct halves (LeetCode 3046)."""\n'
            "    from collections import Counter\n"
            "    return all(v <= 2 for v in Counter(nums).values())\n"
            "\n"
            "def isPossibleToSplit(nums):\n"
            "    return is_possible_to_split(nums)\n",
            lambda low: bool(
                re.search(r"\bleetcode 3046\b|\bsplit the array\b", low)
            )
            and "split array largest" not in low
            and "split linked" not in low,
            (
                (([1, 1, 2, 2, 3, 4],), True),
                (([1, 1, 1, 1],), False),
                (([1, 1, 2, 2],), True),
            ),
        ),
        T(
            "maximum_length_substring_two_occurrences",
            "def maximum_length_substring_two_occurrences(s):\n"
            '    """Longest substring with each char at most twice (LeetCode 3090)."""\n'
            "    from collections import Counter\n"
            "    cnt = Counter()\n"
            "    left = ans = 0\n"
            "    for right, ch in enumerate(s):\n"
            "        cnt[ch] += 1\n"
            "        while cnt[ch] > 2:\n"
            "            cnt[s[left]] -= 1\n"
            "            left += 1\n"
            "        ans = max(ans, right - left + 1)\n"
            "    return ans\n"
            "\n"
            "def maximumLengthSubstring(s):\n"
            "    return maximum_length_substring_two_occurrences(s)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3090\b|\btwo occurrences\b",
                    low,
                )
            ),
            (
                (("bcbbbcba",), 4),
                (("aaaa",), 2),
                (("abcabc",), 6),
            ),
        ),
        T(
            "is_valid_word",
            "def is_valid_word(word):\n"
            '    """Valid word: len>=3, alnum, at least one vowel and consonant (LeetCode 3136)."""\n'
            "    if len(word) < 3:\n"
            "        return False\n"
            "    vowels = set('aeiouAEIOU')\n"
            "    has_v = has_c = False\n"
            "    for ch in word:\n"
            "        if not ch.isalnum():\n"
            "            return False\n"
            "        if ch.isalpha():\n"
            "            if ch in vowels:\n"
            "                has_v = True\n"
            "            else:\n"
            "                has_c = True\n"
            "    return has_v and has_c\n"
            "\n"
            "def isValid(word):\n"
            "    return is_valid_word(word)\n",
            lambda low: bool(
                re.search(r"\bleetcode 3136\b|\bvalid word\b", low)
            )
            and "word break" not in low
            and "word pattern" not in low
            and "word search" not in low,
            (
                (("234Adas",), True),
                (("b3",), False),
                (("a3$e",), False),
            ),
        ),
        T(
            "min_cost_to_reach_position",
            "def min_cost_to_reach_position(cost):\n"
            '    """Prefix minimum cost to reach each index (LeetCode 3502)."""\n'
            "    out = []\n"
            "    best = None\n"
            "    for x in cost:\n"
            "        best = x if best is None else min(best, x)\n"
            "        out.append(best)\n"
            "    return out\n"
            "\n"
            "def minCosts(cost):\n"
            "    return min_cost_to_reach_position(cost)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3502\b|\bminimum cost to reach every position\b",
                    low,
                )
            ),
            (
                (([5, 3, 4, 1, 3, 2],), [5, 3, 3, 1, 1, 1]),
                (([1, 2, 4, 6, 7],), [1, 1, 1, 1, 1]),
                (([4],), [4]),
            ),
        ),
        T(
            "count_distinct_length_three",
            "def count_distinct_length_three(s):\n"
            '    """Count length-3 substrings with all distinct chars (LeetCode 3258)."""\n'
            "    ans = 0\n"
            "    for i in range(len(s) - 2):\n"
            "        window = s[i:i + 3]\n"
            "        if len(set(window)) == 3:\n"
            "            ans += 1\n"
            "    return ans\n"
            "\n"
            "def numberOfSubstrings(s):\n"
            "    return count_distinct_length_three(s)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3258\b|\blength three with all distinct\b",
                    low,
                )
            ),
            (
                (("xyzzaz",), 1),
                (("aababcabc",), 4),
                (("aaa",), 0),
            ),
        ),
        T(
            "min_operations_equal_k",
            "def min_operations_equal_k(nums, k):\n"
            '    """Ops to make every value equal k, or -1 if any value is below k (LeetCode 3375)."""\n'
            "    if any(x < k for x in nums):\n"
            "        return -1\n"
            "    return len({x for x in nums if x > k})\n"
            "\n"
            "def minOperations(nums, k):\n"
            "    return min_operations_equal_k(nums, k)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3375\b|\barray values equal to k\b",
                    low,
                )
            ),
            (
                (([5, 2, 5, 4, 5], 2), 2),
                (([2, 1, 2], 2), -1),
                (([9, 7, 5, 3], 1), 4),
            ),
        ),
    ]
