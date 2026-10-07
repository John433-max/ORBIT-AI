"""Cycle 503: unmatched write-a-function asks.

LeetCode 2221 / 1910 / 2441 / 2500 / 2553 / 2578.
The nth-triangular template must not steal "triangular sum".
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "triangular_sum",
            "def triangular_sum(nums):\n"
            '    """Repeated adjacent sums mod 10 until one value remains (LeetCode 2221)."""\n'
            "    a = [int(x) for x in nums]\n"
            "    while len(a) > 1:\n"
            "        a = [(a[i] + a[i + 1]) % 10 for i in range(len(a) - 1)]\n"
            "    return a[0] if a else 0\n",
            lambda low: "triangular sum" in low or "triangular_sum" in low,
            (
                (([1, 2, 3, 4, 5],), 8),
                (([5],), 5),
                (([1, 2, 3],), 8),
            ),
        ),
        T(
            "remove_occurrences",
            "def remove_occurrences(s, part):\n"
            '    """Remove every leftmost occurrence of part (LeetCode 1910)."""\n'
            "    s = str(s)\n"
            "    part = str(part)\n"
            "    if not part:\n"
            "        return s\n"
            "    while part in s:\n"
            "        s = s.replace(part, '', 1)\n"
            "    return s\n",
            lambda low: (
                "occurrences of a substring" in low
                or "remove_occurrences" in low
                or ("remove all occurrences" in low and "substring" in low)
            ),
            (
                (("daabcbaabcbc", "abc"), "dab"),
                (("axxxxyyyyb", "xy"), "ab"),
                (("abc", "abc"), ""),
            ),
        ),
        T(
            "find_max_k",
            "def find_max_k(nums):\n"
            '    """Largest k > 0 such that -k is also present, else -1 (LeetCode 2441)."""\n'
            "    seen = set(int(x) for x in nums)\n"
            "    best = -1\n"
            "    for x in seen:\n"
            "        if x > best and -x in seen:\n"
            "            best = x\n"
            "    return best\n",
            lambda low: (
                "exists with its negative" in low
                or "find_max_k" in low
                or ("largest" in low and "its negative" in low)
            ),
            (
                (([-1, 2, -3, 3],), 3),
                (([-1, 10, 6, 7, -7, 1],), 7),
                (([-10, 8, 6, 7, -2, -3],), -1),
            ),
        ),
        T(
            "delete_greatest_value",
            "def delete_greatest_value(grid):\n"
            '    """Sum of row-maxes after sorting each row (LeetCode 2500)."""\n'
            "    rows = [sorted(int(x) for x in row) for row in grid]\n"
            "    if not rows or not rows[0]:\n"
            "        return 0\n"
            "    total = 0\n"
            "    for col in range(len(rows[0])):\n"
            "        total += max(row[col] for row in rows)\n"
            "    return total\n",
            lambda low: (
                "greatest value in each row" in low
                or "delete_greatest_value" in low
            ),
            (
                (([[1, 2, 4], [3, 3, 1]],), 8),
                (([[10]],), 10),
                (([[1, 2], [3, 4]],), 7),
            ),
        ),
        T(
            "separate_digits",
            "def separate_digits(nums):\n"
            '    """Split each integer into its decimal digits (LeetCode 2553)."""\n'
            "    out = []\n"
            "    for n in nums:\n"
            "        out.extend(int(ch) for ch in str(abs(int(n))))\n"
            "    return out\n",
            lambda low: (
                "separate_digits" in low
                or "separates the digits" in low
                or "separate the digits" in low
            )
            and "digit sum" not in low,
            (
                (([13, 25, 83, 77],), [1, 3, 2, 5, 8, 3, 7, 7]),
                (([7, 1, 3, 9],), [7, 1, 3, 9]),
                (([100],), [1, 0, 0]),
            ),
        ),
        T(
            "split_num",
            "def split_num(num):\n"
            '    """Split digits into two numbers with minimum sum (LeetCode 2578)."""\n'
            "    digits = sorted(str(abs(int(num))))\n"
            "    a = b = 0\n"
            "    for i, ch in enumerate(digits):\n"
            "        if i % 2 == 0:\n"
            "            a = a * 10 + int(ch)\n"
            "        else:\n"
            "            b = b * 10 + int(ch)\n"
            "    return a + b\n",
            lambda low: (
                "split_num" in low
                or "minimum sum" in low and "split" in low
            )
            and "subarray" not in low,
            (
                ((4325,), 59),
                ((687,), 75),
                ((10,), 1),
            ),
        ),
    ]
