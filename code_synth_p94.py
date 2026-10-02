"""Cycle 369: furthest houses, candy discount, obtain zero, k-beauty, greatest letter, fill cups.

2085 / 2124 / 2176 phrases already matched earlier packs, so those slots use
fallthrough Easy problems instead.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "max_distance_colors",
            "def max_distance_colors(colors):\n"
            '    """Max |i-j| with colors[i] != colors[j] (LeetCode 2078)."""\n'
            "    n = len(colors)\n"
            "    if n < 2:\n"
            "        return 0\n"
            "    left = 0\n"
            "    while left < n and colors[left] == colors[-1]:\n"
            "        left += 1\n"
            "    right = n - 1\n"
            "    while right >= 0 and colors[right] == colors[0]:\n"
            "        right -= 1\n"
            "    return max(n - 1 - left, right)\n"
            "\n"
            "def maxDistance(colors):\n"
            "    return max_distance_colors(colors)\n",
            lambda low: bool(
                re.search(
                    r"\btwo furthest houses with different colors\b|"
                    r"\bfurthest houses with different colors\b|"
                    r"\bleetcode 2078\b",
                    low,
                )
            ),
            (
                (([1, 1, 1, 6, 1, 1, 1],), 3),
                (([1, 8, 3, 8, 3],), 4),
                (([0, 1],), 1),
            ),
        ),
        T(
            "minimum_cost_candies",
            "def minimum_cost_candies(cost):\n"
            '    """Min cost buying candies; every third (desc) is free (LeetCode 2144)."""\n'
            "    ordered = sorted(cost, reverse=True)\n"
            "    return sum(value for i, value in enumerate(ordered) if (i + 1) % 3 != 0)\n"
            "\n"
            "def minimumCost(cost):\n"
            "    return minimum_cost_candies(cost)\n",
            lambda low: bool(
                re.search(
                    r"\bminimum cost of buying candies\b|"
                    r"\bbuying candies with a discount\b|"
                    r"\bleetcode 2144\b",
                    low,
                )
            ),
            (
                (([1, 2, 3],), 5),
                (([6, 5, 7, 9, 2, 2],), 23),
                (([5, 5],), 10),
            ),
        ),
        T(
            "count_operations_zero",
            "def count_operations_zero(num1, num2):\n"
            '    """Subtraction steps until one number is zero (LeetCode 2169)."""\n'
            "    steps = 0\n"
            "    a, b = num1, num2\n"
            "    while a and b:\n"
            "        if a < b:\n"
            "            a, b = b, a\n"
            "        steps += a // b\n"
            "        a %= b\n"
            "    return steps\n"
            "\n"
            "def countOperations(num1, num2):\n"
            "    return count_operations_zero(num1, num2)\n",
            lambda low: bool(
                re.search(
                    r"\bcount operations to obtain zero\b|"
                    r"\boperations to obtain zero\b|"
                    r"\bleetcode 2169\b",
                    low,
                )
            ),
            (
                ((2, 3), 3),
                ((10, 10), 1),
            ),
        ),
        T(
            "k_beauty",
            "def k_beauty(num, k):\n"
            '    """Count length-k substrings that divide num (LeetCode 2269)."""\n'
            "    s = str(num)\n"
            "    total = 0\n"
            "    for i in range(len(s) - k + 1):\n"
            "        value = int(s[i:i + k])\n"
            "        if value and num % value == 0:\n"
            "            total += 1\n"
            "    return total\n"
            "\n"
            "def divisorSubstrings(num, k):\n"
            "    return k_beauty(num, k)\n",
            lambda low: bool(
                re.search(
                    r"\bk[- ]beauty of a number\b|"
                    r"\bfind the k beauty\b|"
                    r"\bleetcode 2269\b",
                    low,
                )
            ),
            (
                ((240, 2), 2),
                ((430043, 2), 2),
            ),
        ),
        T(
            "greatest_letter",
            "def greatest_letter(s):\n"
            '    """Greatest letter present in both cases, else empty (LeetCode 2309)."""\n'
            "    letters = set(s)\n"
            "    best = \"\"\n"
            "    for ch in \"ABCDEFGHIJKLMNOPQRSTUVWXYZ\":\n"
            "        if ch in letters and ch.lower() in letters:\n"
            "            best = ch\n"
            "    return best\n"
            "\n"
            "def greatestLetter(s):\n"
            "    return greatest_letter(s)\n",
            lambda low: bool(
                re.search(
                    r"\bgreatest english letter\b|"
                    r"\bletter in upper and lower case\b|"
                    r"\bleetcode 2309\b",
                    low,
                )
            ),
            (
                (("lEeTcOdE",), "E"),
                (("arRAzFif",), "R"),
                (("AbCdEfGhIjK",), ""),
            ),
        ),
        T(
            "fill_cups",
            "def fill_cups(amount):\n"
            '    """Seconds to fill cups, two different types per second (LeetCode 2335)."""\n'
            "    total = sum(amount)\n"
            "    peak = max(amount) if amount else 0\n"
            "    return max(peak, (total + 1) // 2)\n"
            "\n"
            "def fillCups(amount):\n"
            "    return fill_cups(amount)\n",
            lambda low: bool(
                re.search(
                    r"\bminimum amount of time to fill cups\b|"
                    r"\btime to fill cups\b|"
                    r"\bleetcode 2335\b",
                    low,
                )
            ),
            (
                (([1, 4, 2],), 4),
                (([5, 4, 4],), 7),
                (([5, 0, 0],), 5),
            ),
        ),
    ]
