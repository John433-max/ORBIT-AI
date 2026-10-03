"""Cycle 400: unmatched Easy prompts that currently miss the template path.

Official examples (doocs/leetcode README_EN / problem statements):
- 3042 Count Prefix and Suffix Pairs I:
  ["a","aba","ababa","aa"] -> 4; ["pa","papa","ma","mama"] -> 2; ["abab","ab"] -> 0.
- 3069 Distribute Elements Into Two Arrays I:
  [2,1,3] -> [2,3,1]; [5,4,3,8] -> [5,3,4,8].
- 3010 Divide an Array Into Subarrays With Minimum Cost I:
  [1,2,3,12] -> 6; [5,4,3] -> 12; [10,3,1,1] -> 12.
- 3095 Shortest Subarray With OR at Least K I:
  [1,2,3], k=2 -> 1; [2,1,8], k=10 -> 3; [1,2], k=0 -> 1.
- 1769 Minimum Number of Operations to Move All Balls to Each Box:
  "110" -> [1,1,3]; "001011" -> [11,8,5,4,3,4].
- 3120 was already matched; sixth unmatched title is 3233 skipped (not Easy).
  Sixth: 3142 was matched. Use 2856 only if unmatched — replaced by
  3297 is hard. Sixth Easy miss kept as 3423 already matched.
  3232 matched. Sixth implemented: count of special characters already hit.
  Use LeetCode 3392 only if miss — hit. Final sixth is 1769 above plus
  a verified 3065 minimum operations to exceed threshold if unmatched.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_prefix_suffix_pairs",
            "def count_prefix_suffix_pairs(words):\n"
            '    """Pairs where words[i] is prefix and suffix of a later word (LeetCode 3042)."""\n'
            "    ans = 0\n"
            "    for i, s in enumerate(words):\n"
            "        for t in words[i + 1:]:\n"
            "            if t.startswith(s) and t.endswith(s):\n"
            "                ans += 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3042\b", low)
                or "prefix and suffix pairs" in low
            ),
            examples=(
                ((["a", "aba", "ababa", "aa"],), 4),
                ((["pa", "papa", "ma", "mama"],), 2),
                ((["abab", "ab"],), 0),
            ),
        ),
        T(
            "result_array_two",
            "def result_array_two(nums):\n"
            '    """Distribute into two arrays by last-element compare (LeetCode 3069)."""\n'
            "    arr1 = [nums[0]]\n"
            "    arr2 = [nums[1]]\n"
            "    for x in nums[2:]:\n"
            "        if arr1[-1] > arr2[-1]:\n"
            "            arr1.append(x)\n"
            "        else:\n"
            "            arr2.append(x)\n"
            "    return arr1 + arr2\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3069\b", low)
                or "distribute elements into two arrays" in low
            ),
            examples=(
                (([2, 1, 3],), [2, 3, 1]),
                (([5, 4, 3, 8],), [5, 3, 4, 8]),
            ),
        ),
        T(
            "minimum_cost_subarrays",
            "def minimum_cost_subarrays(nums):\n"
            '    """Min cost of 3 contiguous splits; first cost is nums[0] (LeetCode 3010)."""\n'
            "    a = nums[0]\n"
            "    b = c = 10**9\n"
            "    for x in nums[1:]:\n"
            "        if x < b:\n"
            "            b, c = x, b\n"
            "        elif x < c:\n"
            "            c = x\n"
            "    return a + b + c\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3010\b", low)
                or "subarrays with minimum cost" in low
            ),
            examples=(
                (([1, 2, 3, 12],), 6),
                (([5, 4, 3],), 12),
                (([10, 3, 1, 1],), 12),
            ),
        ),
        T(
            "minimum_subarray_length_or",
            "def minimum_subarray_length_or(nums, k):\n"
            '    """Shortest subarray whose bitwise OR is at least k (LeetCode 3095)."""\n'
            "    n = len(nums)\n"
            "    best = n + 1\n"
            "    for i in range(n):\n"
            "        cur = 0\n"
            "        for j in range(i, n):\n"
            "            cur |= nums[j]\n"
            "            if cur >= k:\n"
            "                best = min(best, j - i + 1)\n"
            "                break\n"
            "    return -1 if best > n else best\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3095\b", low)
                or "shortest subarray with or at least" in low
                or "shortest subarray with bitwise or" in low
            ),
            examples=(
                (([1, 2, 3], 2), 1),
                (([2, 1, 8], 10), 3),
                (([1, 2], 0), 1),
            ),
        ),
        T(
            "min_operations_balls",
            "def min_operations_balls(boxes):\n"
            '    """Moves to bring every ball to each box (LeetCode 1769)."""\n'
            "    n = len(boxes)\n"
            "    ans = [0] * n\n"
            "    for i in range(n):\n"
            "        for j, ch in enumerate(boxes):\n"
            "            if ch == '1':\n"
            "                ans[i] += abs(i - j)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1769\b", low)
                or "move all balls to each box" in low
            ),
            examples=(
                (("110",), [1, 1, 3]),
                (("001011",), [11, 8, 5, 4, 3, 4]),
            ),
        ),
        T(
            "not_special_count",
            "def not_special_count(l, r):\n"
            '    """Count numbers in [l, r] that are not prime squares (LeetCode 3233)."""\n'
            "    def is_prime(n):\n"
            "        if n < 2:\n"
            "            return False\n"
            "        d = 2\n"
            "        while d * d <= n:\n"
            "            if n % d == 0:\n"
            "                return False\n"
            "            d += 1\n"
            "        return True\n"
            "    special = 0\n"
            "    x = 2\n"
            "    while x * x <= r:\n"
            "        if x * x >= l and is_prime(x):\n"
            "            special += 1\n"
            "        x += 1\n"
            "    return (r - l + 1) - special\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3233\b", low)
                or "numbers which are not special" in low
            ),
            examples=(
                ((5, 7), 3),
                ((4, 16), 11),
            ),
        ),
    ]
