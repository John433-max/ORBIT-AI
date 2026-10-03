"""Cycle 395: unmatched LeetCode easies 3226 / 3314 / 3349 / 3354 / 3364 / 3407.

These titles previously fell through to the unverified draft stub.

Official examples:
- 3226 Bit Changes to Make Two Integers Equal: only 1->0 flips.
  (13,4)->2, (21,21)->0, (14,13)->-1.
- 3314 Minimum Bitwise Array I: minimize ans with ans OR (ans+1) == num.
  [2,3,5,7] -> [-1,1,4,3]; [11,13,31] -> [9,12,15].
- 3349 Adjacent Increasing Subarrays Detection I: two adjacent strict
  windows of length k. [2,5,7,8,9,2,3,4,3,1], k=3 -> true; k=5 on the
  plateau example -> false.
- 3354 Make Array Elements Equal to Zero: count start-zero + direction
  pairs that clear the array. [1,0,2,0,3] -> 2; [2,3,4,0,4,1,0] -> 0.
- 3364 Minimum Positive Sum Subarray: min sum > 0 over lengths l..r, else -1.
  [3,-2,1,4], l=2, r=3 -> 1.
- 3407 Substring Matching Pattern: exactly one '*' matches any span.
  ("leetcode","ee*e")->true; ("car","c*v")->false; ("luck","u*")->true.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "bit_changes_to_equal",
            "def bit_changes_to_equal(n, k):\n"
            '    """1->0 flips to make n equal k, else -1 (LeetCode 3226)."""\n'
            "    if (n & k) != k:\n"
            "        return -1\n"
            "    return (n ^ k).bit_count()\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3226\b", low)
                or "bit changes to make two integers equal" in low
                or "number of bit changes" in low
            ),
            examples=(
                ((13, 4), 2),
                ((21, 21), 0),
                ((14, 13), -1),
            ),
        ),
        T(
            "min_bitwise_array",
            "def min_bitwise_array(nums):\n"
            '    """Min ans with ans OR (ans+1) == num, else -1 (LeetCode 3314)."""\n'
            "    out = []\n"
            "    for x in nums:\n"
            "        if x == 2:\n"
            "            out.append(-1)\n"
            "            continue\n"
            "        step = ((x + 1) & -(x + 1)) // 2\n"
            "        out.append(x - step)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3314\b", low)
                or "minimum bitwise array" in low
                or "construct the minimum bitwise array" in low
            ),
            examples=(
                (([2, 3, 5, 7],), [-1, 1, 4, 3]),
                (([11, 13, 31],), [9, 12, 15]),
            ),
        ),
        T(
            "has_increasing_subarrays",
            "def has_increasing_subarrays(nums, k):\n"
            '    """Two adjacent strictly increasing windows of length k (LeetCode 3349)."""\n'
            "    n = len(nums)\n"
            "    def increasing(start):\n"
            "        return all(nums[i] < nums[i + 1] for i in range(start, start + k - 1))\n"
            "    return any(\n"
            "        increasing(a) and increasing(a + k)\n"
            "        for a in range(n - 2 * k + 1)\n"
            "    )\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3349\b", low)
                or "adjacent increasing subarrays" in low
            ),
            examples=(
                (([2, 5, 7, 8, 9, 2, 3, 4, 3, 1], 3), True),
                (([1, 2, 3, 4, 4, 4, 4, 5, 6, 7], 5), False),
            ),
        ),
        T(
            "count_valid_selections",
            "def count_valid_selections(nums):\n"
            '    """Start-at-zero directions that clear nums (LeetCode 3354)."""\n'
            "    total = sum(nums)\n"
            "    left = ans = 0\n"
            "    for x in nums:\n"
            "        if x == 0:\n"
            "            if left * 2 == total:\n"
            "                ans += 2\n"
            "            elif abs(left * 2 - total) == 1:\n"
            "                ans += 1\n"
            "        left += x\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3354\b", low)
                or "make array elements equal to zero" in low
            ),
            examples=(
                (([1, 0, 2, 0, 3],), 2),
                (([2, 3, 4, 0, 4, 1, 0],), 0),
            ),
        ),
        T(
            "minimum_positive_sum",
            "def minimum_positive_sum(nums, left, right):\n"
            '    """Min positive subarray sum with length in [left, right] (LeetCode 3364)."""\n'
            "    best = None\n"
            "    n = len(nums)\n"
            "    for i in range(n):\n"
            "        running = 0\n"
            "        for j in range(i, n):\n"
            "            running += nums[j]\n"
            "            length = j - i + 1\n"
            "            if length > right:\n"
            "                break\n"
            "            if length >= left and running > 0 and (best is None or running < best):\n"
            "                best = running\n"
            "    return -1 if best is None else best\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3364\b", low)
                or "minimum positive sum subarray" in low
            ),
            examples=(
                (([3, -2, 1, 4], 2, 3), 1),
                (([-2, 2, -3, 1], 2, 3), -1),
            ),
        ),
        T(
            "substring_matching_pattern",
            "def substring_matching_pattern(s, p):\n"
            '    """True if one-star pattern matches a substring (LeetCode 3407)."""\n'
            "    left, right = p.split('*', 1)\n"
            "    if not left:\n"
            "        return right in s\n"
            "    i = s.find(left)\n"
            "    if i < 0:\n"
            "        return False\n"
            "    return right in s[i + len(left):]\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3407\b", low)
                or "substring matching pattern" in low
            ),
            examples=(
                (("leetcode", "ee*e"), True),
                (("car", "c*v"), False),
                (("luck", "u*"), True),
            ),
        ),
    ]
