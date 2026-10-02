"""Cycle 366: remove-zeros, missing elements, equal-moves III, reverse-binary flips, balanced removals, k-extreme difference."""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "remove_zeros_decimal",
            "def remove_zeros_decimal(n):\n"
            '    """Drop zero digits from the decimal form of n (LeetCode 3726)."""\n'
            "    x = int(n)\n"
            "    k = 1\n"
            "    ans = 0\n"
            "    while x:\n"
            "        digit = x % 10\n"
            "        if digit:\n"
            "            ans += digit * k\n"
            "            k *= 10\n"
            "        x //= 10\n"
            "    return ans\n"
            "\n"
            "def removeZeros(n):\n"
            "    return remove_zeros_decimal(n)\n",
            lambda low: bool(
                re.search(
                    r"\bremove zeros in decimal\b|"
                    r"\bleetcode 3726\b",
                    low,
                )
            ),
            (
                ((1020030,), 123),
                ((1,), 1),
                ((10,), 1),
            ),
        ),
        T(
            "find_missing_elements",
            "def find_missing_elements(nums):\n"
            '    """Sorted integers missing between min and max (LeetCode 3731)."""\n'
            "    have = set(nums)\n"
            "    lo, hi = min(have), max(have)\n"
            "    return [x for x in range(lo, hi + 1) if x not in have]\n"
            "\n"
            "def findMissingElements(nums):\n"
            "    return find_missing_elements(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bfind missing elements\b|"
                    r"\bleetcode 3731\b",
                    low,
                )
            ),
            (
                (((1, 4, 2, 5),), [3]),
                (((7, 8, 6, 9),), []),
                (((5, 1),), [2, 3, 4]),
            ),
        ),
        T(
            "min_moves_equal_array_iii",
            "def min_moves_equal_array_iii(nums):\n"
            '    """Increments to raise every value to the max (LeetCode 3736)."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    return max(nums) * len(nums) - sum(nums)\n"
            "\n"
            "def minMoves(nums):\n"
            "    return min_moves_equal_array_iii(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bequal array elements iii\b|"
                    r"\bleetcode 3736\b",
                    low,
                )
            ),
            (
                (((2, 1, 3),), 3),
                (((4, 4, 5),), 2),
                (((7,),), 0),
            ),
        ),
        T(
            "min_flips_reverse_binary",
            "def min_flips_reverse_binary(n):\n"
            '    """Flips so binary(n) equals its reverse (LeetCode 3750)."""\n'
            "    s = bin(int(n))[2:]\n"
            "    half = len(s) // 2\n"
            "    return 2 * sum(s[i] != s[-1 - i] for i in range(half))\n"
            "\n"
            "def minimumNumberOfFlips(n):\n"
            "    return min_flips_reverse_binary(n)\n",
            lambda low: bool(
                re.search(
                    r"\bflips to reverse binary\b|"
                    r"\breverse binary string\b|"
                    r"\bleetcode 3750\b",
                    low,
                )
            ),
            (
                ((7,), 0),
                ((10,), 4),
                ((1,), 0),
            ),
        ),
        T(
            "min_length_balanced_removals",
            "def min_length_balanced_removals(s):\n"
            '    """Length left after deleting equal-count a/b substrings (LeetCode 3746)."""\n'
            "    a = s.count('a')\n"
            "    return abs(a - (len(s) - a))\n"
            "\n"
            "def minLengthAfterRemovals(s):\n"
            "    return min_length_balanced_removals(s)\n",
            lambda low: bool(
                re.search(
                    r"\bbalanced removals\b|"
                    r"\bleetcode 3746\b",
                    low,
                )
            ),
            (
                (("aabbab",), 0),
                (("aaaa",), 4),
                (("aaabb",), 1),
            ),
        ),
        T(
            "abs_diff_k_extremes",
            "def abs_diff_k_extremes(nums, k):\n"
            '    """Sum of k largest minus sum of k smallest (LeetCode 3774)."""\n'
            "    ordered = sorted(nums)\n"
            "    return sum(ordered[-k:]) - sum(ordered[:k])\n"
            "\n"
            "def absDifference(nums, k):\n"
            "    return abs_diff_k_extremes(nums, k)\n",
            lambda low: bool(
                re.search(
                    r"\babsolute difference between maximum and minimum k\b|"
                    r"\bk largest and k smallest\b|"
                    r"\bleetcode 3774\b",
                    low,
                )
            ),
            (
                (((5, 2, 2, 4), 2), 5),
                (((100,), 1), 0),
            ),
        ),
    ]
