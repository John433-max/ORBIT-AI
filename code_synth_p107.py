"""Cycle 385–386: Easy prompts still absent from the template index.

LeetCode 3432, 3438, 3477, 3507, and 3550 were not referenced by any pack.
Cycle 386 adds second-largest-in-a-list so that NL coding request returns
verified code instead of the NotImplemented draft stub. Matchers stay
ID- or phrase-specific so partition, fruits-I, digit-sum, and
second-largest-digit (1796) templates keep their existing prompts.
Loaded before p106.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_partitions_even_sum_diff",
            "def count_partitions_even_sum_diff(nums):\n"
            '    """Cuts where left-sum minus right-sum is even (LeetCode 3432)."""\n'
            "    left, right = 0, sum(nums)\n"
            "    ans = 0\n"
            "    for x in nums[:-1]:\n"
            "        left += x\n"
            "        right -= x\n"
            "        ans += (left - right) % 2 == 0\n"
            "    return ans\n"
            "\n"
            "def countPartitions(nums):\n"
            "    return count_partitions_even_sum_diff(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3432\b|\beven sum difference\b|"
                    r"\bpartitions with even sum\b",
                    low,
                )
            ),
            (
                (([10, 10, 3, 7, 6],), 4),
                (([1, 2, 2],), 0),
                (([2, 4, 6, 8],), 3),
            ),
        ),
        T(
            "find_valid_pair",
            "def find_valid_pair(s):\n"
            '    """First adjacent distinct digits whose counts equal themselves (LeetCode 3438)."""\n'
            "    cnt = [0] * 10\n"
            "    for ch in s:\n"
            "        cnt[int(ch)] += 1\n"
            "    for i in range(1, len(s)):\n"
            "        x, y = int(s[i - 1]), int(s[i])\n"
            "        if x != y and cnt[x] == x and cnt[y] == y:\n"
            "            return s[i - 1 : i + 1]\n"
            "    return \"\"\n"
            "\n"
            "def findValidPair(s):\n"
            "    return find_valid_pair(s)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3438\b|\bvalid pair of adjacent digits\b|"
                    r"\badjacent digits in string\b",
                    low,
                )
            ),
            (
                (("2523533",), "23"),
                (("221",), "21"),
                (("22",), ""),
            ),
        ),
        T(
            "num_of_unplaced_fruits",
            "def num_of_unplaced_fruits(fruits, baskets):\n"
            '    """Fruits left after leftmost fitting basket (LeetCode 3477)."""\n'
            "    vis = [False] * len(baskets)\n"
            "    ans = len(fruits)\n"
            "    for x in fruits:\n"
            "        for i, y in enumerate(baskets):\n"
            "            if y >= x and not vis[i]:\n"
            "                vis[i] = True\n"
            "                ans -= 1\n"
            "                break\n"
            "    return ans\n"
            "\n"
            "def numOfUnplacedFruits(fruits, baskets):\n"
            "    return num_of_unplaced_fruits(fruits, baskets)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3477\b|\bfruits into baskets ii\b|"
                    r"\bunplaced fruits\b",
                    low,
                )
            ),
            (
                (([4, 2, 5], [3, 5, 4]), 1),
                (([3, 6, 1], [6, 4, 7]), 0),
                (([1], [1]), 0),
            ),
        ),
        T(
            "minimum_pair_removal",
            "def minimum_pair_removal(nums):\n"
            '    """Merge leftmost min-sum adjacent pair until non-decreasing (LeetCode 3507)."""\n'
            "    arr = list(nums)\n"
            "    ans = 0\n"
            "    def non_decreasing(a):\n"
            "        return all(a[i] >= a[i - 1] for i in range(1, len(a)))\n"
            "    while len(arr) > 1 and not non_decreasing(arr):\n"
            "        k = 0\n"
            "        best = arr[0] + arr[1]\n"
            "        for i in range(1, len(arr) - 1):\n"
            "            t = arr[i] + arr[i + 1]\n"
            "            if t < best:\n"
            "                best = t\n"
            "                k = i\n"
            "        arr[k] = best\n"
            "        del arr[k + 1]\n"
            "        ans += 1\n"
            "    return ans\n"
            "\n"
            "def minimumPairRemoval(nums):\n"
            "    return minimum_pair_removal(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3507\b|\bminimum pair removal\b|"
                    r"\bpair removal to sort\b",
                    low,
                )
            ),
            (
                (([5, 2, 3, 1],), 2),
                (([1, 2, 2],), 0),
                (([3, 1],), 1),
            ),
        ),
        T(
            "smallest_index_digit_sum",
            "def smallest_index_digit_sum(nums):\n"
            '    """Smallest i whose digit sum equals i, else -1 (LeetCode 3550)."""\n'
            "    for i, x in enumerate(nums):\n"
            "        s = 0\n"
            "        while x:\n"
            "            s += x % 10\n"
            "            x //= 10\n"
            "        if s == i:\n"
            "            return i\n"
            "    return -1\n"
            "\n"
            "def smallestIndex(nums):\n"
            "    return smallest_index_digit_sum(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3550\b|\bdigit sum equal to index\b|"
                    r"\bsmallest index with digit sum\b",
                    low,
                )
            ),
            (
                (([1, 3, 2],), 2),
                (([1, 10, 11],), 1),
                (([1, 2, 3],), -1),
            ),
        ),
        T(
            "second_largest",
            "def second_largest(nums):\n"
            '    """Second-largest distinct value, or None if fewer than two."""\n'
            "    uniq = sorted(set(nums), reverse=True)\n"
            "    return uniq[1] if len(uniq) > 1 else None\n",
            lambda low: (
                "digit" not in low
                and "1796" not in low
                and bool(
                    re.search(
                        r"\bsecond[- ]largest (number|element|value|item)\b",
                        low,
                    )
                )
            ),
            (
                (([1, 2, 3, 4],), 3),
                (([9, 1, 9, 2],), 2),
                (([5, 5, 5],), None),
            ),
        ),
    ]
