"""Cycle 342: unused Easy — deci-binary partitions / leetcode bank /
positive step start / middle index / size-three distinct / one ones-segment."""

from __future__ import annotations

import re
from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "min_partitions",
            "def min_partitions(n):\n"
            '    """Min deci-binary numbers that sum to n (LeetCode 1689)."""\n'
            "    return max(int(ch) for ch in n)\n",
            lambda low: "deci-binary" in low,
            (
                (("32",), 3),
                (("82734",), 8),
                (("27346209830709182346",), 9),
            ),
        ),
        T(
            "total_money",
            "def total_money(n):\n"
            '    """Money saved over n days in the LeetCode bank (LeetCode 1716)."""\n'
            "    weeks, rem = divmod(n, 7)\n"
            "    return (\n"
            "        weeks * 28\n"
            "        + 7 * weeks * (weeks - 1) // 2\n"
            "        + rem * (rem + 1) // 2\n"
            "        + weeks * rem\n"
            "    )\n",
            lambda low: "leetcode bank" in low or "leet code bank" in low,
            (
                ((4,), 10),
                ((10,), 37),
                ((20,), 96),
            ),
        ),
        T(
            "min_start_value",
            "def min_start_value(nums):\n"
            '    """Smallest start so the step-by-step sum stays positive (LeetCode 1413)."""\n'
            "    running = lowest = 0\n"
            "    for value in nums:\n"
            "        running += value\n"
            "        if running < lowest:\n"
            "            lowest = running\n"
            "    return 1 - lowest\n",
            lambda low: "positive step by step" in low,
            (
                (([-3, 2, -3, 4, 2],), 5),
                (([1, 2],), 1),
                (([1, -2, -3],), 5),
            ),
        ),
        T(
            "find_middle_index",
            "def find_middle_index(nums):\n"
            '    """Index where the left sum equals the right sum (LeetCode 1991)."""\n'
            "    total = sum(nums)\n"
            "    left = 0\n"
            "    for i, value in enumerate(nums):\n"
            "        if left == total - left - value:\n"
            "            return i\n"
            "        left += value\n"
            "    return -1\n",
            lambda low: "middle index" in low,
            (
                (([2, 3, -1, 8, 4],), 3),
                (([1, -1, 4],), 2),
                (([2, 5],), -1),
            ),
        ),
        T(
            "count_good_substrings",
            "def count_good_substrings(s):\n"
            '    """Size-3 windows with three distinct characters (LeetCode 1876)."""\n'
            "    return sum(\n"
            "        len(set(s[i:i + 3])) == 3 for i in range(len(s) - 2)\n"
            "    )\n",
            lambda low: "size three with distinct" in low,
            (
                (("xyzzaz",), 1),
                (("aababcabc",), 4),
                (("aaa",), 0),
            ),
        ),
        T(
            "check_ones_segment",
            "def check_ones_segment(s):\n"
            '    """Binary string has at most one contiguous segment of ones (LeetCode 1784)."""\n'
            "    return '01' not in s\n",
            lambda low: "segment of ones" in low,
            (
                (("1001",), False),
                (("110",), True),
                (("1",), True),
            ),
        ),
    ]
