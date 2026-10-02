"""Cycle 375: knight tour, alternating subarray, divisibility score, good array, semi-ordered perm, substring reverse.

2596 / 2765 / 2644 / 2784 were unmatched stubs. 2717 was stolen by permute;
3083 was stolen by reverse_string.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "check_knight_tour_configuration",
            "def check_knight_tour_configuration(grid):\n"
            '    """True if grid is a knight tour starting at 0 (LeetCode 2596)."""\n'
            "    n = len(grid)\n"
            "    if not grid or grid[0][0] != 0:\n"
            "        return False\n"
            "    pos = {}\n"
            "    for r in range(n):\n"
            "        for c in range(n):\n"
            "            pos[grid[r][c]] = (r, c)\n"
            "    if len(pos) != n * n:\n"
            "        return False\n"
            "    deltas = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))\n"
            "    r, c = 0, 0\n"
            "    for step in range(1, n * n):\n"
            "        nr, nc = pos.get(step, (-1, -1))\n"
            "        if (nr - r, nc - c) not in deltas:\n"
            "            return False\n"
            "        r, c = nr, nc\n"
            "    return True\n"
            "\n"
            "def checkValidGrid(grid):\n"
            "    return check_knight_tour_configuration(grid)\n",
            lambda low: bool(
                re.search(r"\bknight tour\b|\bleetcode 2596\b", low)
            ),
            (
                (([[0, 11, 16, 5, 20], [17, 4, 19, 10, 15], [12, 1, 8, 21, 6], [3, 18, 23, 14, 9], [24, 13, 2, 7, 22]],), True),
                (([[0, 3, 6], [5, 8, 1], [2, 7, 4]],), False),
                (([[1, 0], [2, 3]],), False),
            ),
        ),
        T(
            "longest_alternating_subarray",
            "def longest_alternating_subarray(nums):\n"
            '    """Longest subarray with diffs +1,-1,+1,... else -1 (LeetCode 2765)."""\n'
            "    ans = 1\n"
            "    dp = 1\n"
            "    for i in range(1, len(nums)):\n"
            "        target = -1 if dp % 2 == 0 else 1\n"
            "        if nums[i] - nums[i - 1] == target:\n"
            "            dp += 1\n"
            "        elif nums[i] - nums[i - 1] == 1:\n"
            "            dp = 2\n"
            "        else:\n"
            "            dp = 1\n"
            "        if dp > ans:\n"
            "            ans = dp\n"
            "    return ans if ans > 1 else -1\n"
            "\n"
            "def alternatingSubarray(nums):\n"
            "    return longest_alternating_subarray(nums)\n",
            lambda low: bool(
                re.search(r"\balternating subarray\b|\bleetcode 2765\b", low)
            ),
            (
                (([2, 3, 4, 3, 4],), 4),
                (([4, 5, 6],), 2),
                (([21, 9, 5],), -1),
            ),
        ),
        T(
            "maximum_divisibility_score",
            "def maximum_divisibility_score(nums, divisors):\n"
            '    """Divisor with the most hits; ties take the smaller value (LeetCode 2644)."""\n'
            "    best = None\n"
            "    best_score = -1\n"
            "    for d in divisors:\n"
            "        score = sum(1 for x in nums if d and x % d == 0)\n"
            "        if score > best_score or (score == best_score and (best is None or d < best)):\n"
            "            best_score = score\n"
            "            best = d\n"
            "    return best\n"
            "\n"
            "def maxDivScore(nums, divisors):\n"
            "    return maximum_divisibility_score(nums, divisors)\n",
            lambda low: bool(
                re.search(r"\bdivisibility score\b|\bleetcode 2644\b", low)
            ),
            (
                (([2, 9, 15, 50], [5, 3, 7, 2]), 2),
                (([4, 7, 9, 3, 9], [5, 2, 3]), 3),
                (([20, 14, 21, 10], [10, 16, 20]), 10),
            ),
        ),
        T(
            "check_array_is_good",
            "def check_array_is_good(nums):\n"
            '    """Permutation of base[n] = [1..n-1, n, n] (LeetCode 2784)."""\n'
            "    n = len(nums) - 1\n"
            "    if n < 1:\n"
            "        return False\n"
            "    seen = [0] * (n + 1)\n"
            "    for x in nums:\n"
            "        if x < 1 or x > n:\n"
            "            return False\n"
            "        seen[x] += 1\n"
            "    if seen[n] != 2:\n"
            "        return False\n"
            "    return all(seen[i] == 1 for i in range(1, n))\n"
            "\n"
            "def isGood(nums):\n"
            "    return check_array_is_good(nums)\n",
            lambda low: bool(
                re.search(r"\barray is good\b|\bleetcode 2784\b", low)
            )
            and "good pair" not in low,
            (
                (([2, 1, 3],), False),
                (([1, 3, 3, 2],), True),
                (([1, 1],), True),
                (([3, 4, 4, 1, 2, 1],), False),
            ),
        ),
        T(
            "semi_ordered_permutation",
            "def semi_ordered_permutation(nums):\n"
            '    """Min adjacent swaps so 1 is first and n is last (LeetCode 2717)."""\n'
            "    n = len(nums)\n"
            "    i = nums.index(1)\n"
            "    j = nums.index(n)\n"
            "    return i + (n - 1 - j) - (1 if i > j else 0)\n"
            "\n"
            "def semiOrderedPermutation(nums):\n"
            "    return semi_ordered_permutation(nums)\n",
            lambda low: bool(
                re.search(r"\bsemi-ordered permutation\b|\bsemi ordered permutation\b|\bleetcode 2717\b", low)
            ),
            (
                (([2, 1, 4, 3],), 2),
                (([2, 4, 1, 3],), 3),
                (([1, 3, 4, 2, 5],), 0),
            ),
        ),
        T(
            "existence_of_substring_reverse",
            "def existence_of_substring_reverse(s):\n"
            '    """Length-2 substring also present in reverse(s) (LeetCode 3083)."""\n'
            "    rev = s[::-1]\n"
            "    pairs = {s[i:i + 2] for i in range(len(s) - 1)}\n"
            "    return any(p in rev for p in pairs)\n"
            "\n"
            "def isSubstringPresent(s):\n"
            "    return existence_of_substring_reverse(s)\n",
            lambda low: bool(
                re.search(
                    r"\bsubstring\b.*\breverse\b|\bleetcode 3083\b",
                    low,
                )
            )
            and "reverse a string" not in low
            and "reverses a string" not in low,
            (
                (("leetcode",), True),
                (("abcba",), True),
                (("abcd",), False),
            ),
        ),
    ]
