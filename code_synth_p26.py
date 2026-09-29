"""Cycle 286: two-sum II / segments / unsorted window / averages / LCIS / LHS."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "two_sum_ii",
            "def two_sum_ii(numbers, target):\n"
            '    """1-indexed two-sum on a nondecreasing array (two pointers)."""\n'
            "    i, j = 0, len(numbers) - 1\n"
            "    while i < j:\n"
            "        s = numbers[i] + numbers[j]\n"
            "        if s == target:\n"
            "            return (i + 1, j + 1)\n"
            "        if s < target:\n"
            "            i += 1\n"
            "        else:\n"
            "            j -= 1\n"
            "    return (-1, -1)\n",
            lambda low: bool(
                re.search(
                    r"\btwo[_ ]sum[_ ]ii\b|"
                    r"\btwo[- ]sum (?:ii|2)\b|"
                    r"\btwo sum (?:on |of )?a sorted array\b|"
                    r"\btwo pointers? two[- ]sum\b|"
                    r"\b1[- ]indexed two[- ]sum\b",
                    low,
                )
            ),
            (
                (([2, 7, 11, 15], 9), (1, 2)),
                (([2, 3, 4], 6), (1, 3)),
                (([-1, 0], -1), (1, 2)),
            ),
        ),
        T(
            "count_segments",
            "def count_segments(s):\n"
            '    """Count space-separated segments in s."""\n'
            "    return len(s.split())\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]segments\b|"
                    r"\bnumber of segments in (?:a |the )?string\b|"
                    r"\bcount (?:the )?segments\b",
                    low,
                )
            ),
            (
                (("Hello, my name is John",), 5),
                (("Hello",), 1),
                (("   ",), 0),
            ),
        ),
        T(
            "find_unsorted_subarray",
            "def find_unsorted_subarray(nums):\n"
            '    """Length of the shortest subarray that must be sorted."""\n'
            "    n = len(nums)\n"
            "    if n <= 1:\n"
            "        return 0\n"
            "    ordered = sorted(nums)\n"
            "    lo, hi = 0, n - 1\n"
            "    while lo < n and nums[lo] == ordered[lo]:\n"
            "        lo += 1\n"
            "    while hi >= 0 and nums[hi] == ordered[hi]:\n"
            "        hi -= 1\n"
            "    return 0 if lo > hi else hi - lo + 1\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]unsorted[_ ]subarray\b|"
                    r"\bshortest unsorted (?:continuous )?subarray\b|"
                    r"\bunsorted continuous subarray\b",
                    low,
                )
            ),
            (
                (([2, 6, 4, 8, 10, 9, 15],), 5),
                (([1, 2, 3, 4],), 0),
                (([1],), 0),
            ),
        ),
        T(
            "find_max_average",
            "def find_max_average(nums, k):\n"
            '    """Maximum average of any contiguous subarray of length k."""\n'
            "    window = sum(nums[:k])\n"
            "    best = window\n"
            "    for i in range(k, len(nums)):\n"
            "        window += nums[i] - nums[i - k]\n"
            "        if window > best:\n"
            "            best = window\n"
            "    return best / float(k)\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]max[_ ]average\b|"
                    r"\bmaximum average subarray\b|"
                    r"\bmax average of (?:any |a )?subarray\b",
                    low,
                )
                and "moving" not in low
            ),
            (
                (([1, 12, -5, -6, 50, 3], 4), 12.75),
                (([5], 1), 5.0),
            ),
        ),
        T(
            "find_length_of_lcis",
            "def find_length_of_lcis(nums):\n"
            '    """Length of the longest continuous increasing subsequence."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    best = cur = 1\n"
            "    for i in range(1, len(nums)):\n"
            "        if nums[i] > nums[i - 1]:\n"
            "            cur += 1\n"
            "            if cur > best:\n"
            "                best = cur\n"
            "        else:\n"
            "            cur = 1\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]length[_ ]of[_ ]lcis\b|"
                    r"\blongest continuous increasing\b|"
                    r"\blcis\b",
                    low,
                )
                and "path" not in low
                and "subsequence that is not continuous" not in low
            ),
            (
                (([1, 3, 5, 4, 7],), 3),
                (([2, 2, 2, 2, 2],), 1),
            ),
        ),
        T(
            "find_lhs",
            "def find_lhs(nums):\n"
            '    """Longest harmonious subsequence (max-min == 1)."""\n'
            "    from collections import Counter\n"
            "    c = Counter(nums)\n"
            "    best = 0\n"
            "    for x, n in c.items():\n"
            "        if x + 1 in c:\n"
            "            s = n + c[x + 1]\n"
            "            if s > best:\n"
            "                best = s\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]lhs\b|"
                    r"\blongest harmonious subsequence\b|"
                    r"\bharmonious subsequence\b",
                    low,
                )
            ),
            (
                (([1, 3, 2, 2, 5, 2, 3, 7],), 5),
                (([1, 2, 3, 4],), 2),
                (([1, 1, 1, 1],), 0),
            ),
        ),
    ]
