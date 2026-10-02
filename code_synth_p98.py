"""Cycle 374: two-out-of-three, strict mid counts, reverse-equal, nearest point, even-odd subarray, diagonal prime.

2032 / 2148 / 1460 / 1779 / 2760 / 2614 were unmatched stubs.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "two_out_of_three",
            "def two_out_of_three(nums1, nums2, nums3):\n"
            '    """Sorted values present in at least two of three arrays (LeetCode 2032)."""\n'
            "    sets = (set(nums1), set(nums2), set(nums3))\n"
            "    vals = set().union(*sets)\n"
            "    return sorted(v for v in vals if sum(v in s for s in sets) >= 2)\n"
            "\n"
            "def twoOutOfThree(nums1, nums2, nums3):\n"
            "    return two_out_of_three(nums1, nums2, nums3)\n",
            lambda low: bool(
                re.search(r"\btwo out of three\b|\bleetcode 2032\b", low)
            ),
            (
                (([1, 1, 3, 2], [2, 3], [3]), [2, 3]),
                (([3, 1], [2, 3], [1, 2]), [1, 2, 3]),
                (([1, 2, 2], [4, 3, 3], [5]), []),
            ),
        ),
        T(
            "count_elements_strict",
            "def count_elements_strict(nums):\n"
            '    """Count values with both a strictly smaller and greater element (LeetCode 2148)."""\n'
            "    lo, hi = min(nums), max(nums)\n"
            "    return sum(1 for x in nums if lo < x < hi)\n"
            "\n"
            "def countElements(nums):\n"
            "    return count_elements_strict(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bstrictly smaller and greater\b|\bleetcode 2148\b",
                    low,
                )
            ),
            (
                (([11, 7, 2, 15],), 2),
                (([-3, 3, 3, 90],), 2),
                (([1],), 0),
            ),
        ),
        T(
            "can_be_equal_reverse",
            "def can_be_equal_reverse(target, arr):\n"
            '    """Equal after subarray reversals iff same multiset (LeetCode 1460)."""\n'
            "    return sorted(target) == sorted(arr)\n"
            "\n"
            "def canBeEqual(target, arr):\n"
            "    return can_be_equal_reverse(target, arr)\n",
            lambda low: bool(
                re.search(
                    r"\breversing subarrays\b|\bleetcode 1460\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4], [2, 4, 1, 3]), True),
                (([7], [7]), True),
                (([3, 7, 9], [3, 7, 11]), False),
            ),
        ),
        T(
            "nearest_valid_point",
            "def nearest_valid_point(x, y, points):\n"
            '    """Index of nearest same-x or same-y point, else -1 (LeetCode 1779)."""\n'
            "    best = -1\n"
            "    dist = None\n"
            "    for i, (px, py) in enumerate(points):\n"
            "        if px != x and py != y:\n"
            "            continue\n"
            "        d = abs(px - x) + abs(py - y)\n"
            "        if dist is None or d < dist:\n"
            "            dist = d\n"
            "            best = i\n"
            "    return best\n"
            "\n"
            "def nearestValidPoint(x, y, points):\n"
            "    return nearest_valid_point(x, y, points)\n",
            lambda low: bool(
                re.search(
                    r"\bnearest point\b|\bleetcode 1779\b",
                    low,
                )
            ),
            (
                ((3, 4, [[1, 2], [3, 1], [2, 4], [2, 3], [4, 4]]), 2),
                ((3, 4, [[3, 4]]), 0),
                ((3, 4, [[2, 3]]), -1),
            ),
        ),
        T(
            "longest_even_odd_subarray",
            "def longest_even_odd_subarray(nums, threshold):\n"
            '    """Longest even-start alternating subarray under threshold (LeetCode 2760)."""\n'
            "    best = i = 0\n"
            "    n = len(nums)\n"
            "    while i < n:\n"
            "        if nums[i] % 2 == 0 and nums[i] <= threshold:\n"
            "            j = i\n"
            "            while (\n"
            "                j + 1 < n\n"
            "                and nums[j + 1] <= threshold\n"
            "                and nums[j] % 2 != nums[j + 1] % 2\n"
            "            ):\n"
            "                j += 1\n"
            "            best = max(best, j - i + 1)\n"
            "            i = j + 1 if j > i else i + 1\n"
            "        else:\n"
            "            i += 1\n"
            "    return best\n"
            "\n"
            "def longestAlternatingSubarray(nums, threshold):\n"
            "    return longest_even_odd_subarray(nums, threshold)\n",
            lambda low: bool(
                re.search(
                    r"\blongest even odd subarray\b|"
                    r"\beven odd subarray with threshold\b|"
                    r"\bleetcode 2760\b",
                    low,
                )
            ),
            (
                (([3, 2, 5, 4], 5), 3),
                (([1, 2], 2), 1),
                (([2, 3, 4, 5], 4), 3),
            ),
        ),
        T(
            "diagonal_prime",
            "def diagonal_prime(nums):\n"
            '    """Largest prime on either diagonal, else 0 (LeetCode 2614)."""\n'
            "    def is_prime(n):\n"
            "        if n < 2:\n"
            "            return False\n"
            "        d = 2\n"
            "        while d * d <= n:\n"
            "            if n % d == 0:\n"
            "                return False\n"
            "            d += 1\n"
            "        return True\n"
            "\n"
            "    n = len(nums)\n"
            "    best = 0\n"
            "    for i in range(n):\n"
            "        for v in (nums[i][i], nums[i][n - 1 - i]):\n"
            "            if v > best and is_prime(v):\n"
            "                best = v\n"
            "    return best\n"
            "\n"
            "def diagonalPrime(nums):\n"
            "    return diagonal_prime(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bprime in diagonal\b|"
                    r"\bprime on diagonal\b|"
                    r"\bleetcode 2614\b",
                    low,
                )
            ),
            (
                (([[1, 2, 3], [5, 6, 7], [9, 10, 11]],), 11),
                (([[1, 2, 3], [5, 17, 7], [9, 11, 10]],), 17),
                (([[1, 1], [1, 1]],), 0),
            ),
        ),
    ]
