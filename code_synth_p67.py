"""Cycle 329: unused Easy — days together / four-digit min sum /
pivot integer / pairs sum < target / div vs non-div / odd binary."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_days_together",
            "def count_days_together(arriveAlice, leaveAlice, arriveBob, leaveBob):\n"
            '    """Inclusive overlap of Alice/Bob stays in a non-leap year (LeetCode 2409)."""\n'
            "    md = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]\n"
            "    def day(s):\n"
            "        m, d = map(int, s.split('-'))\n"
            "        return sum(md[: m - 1]) + d\n"
            "    a1, a2 = day(arriveAlice), day(leaveAlice)\n"
            "    b1, b2 = day(arriveBob), day(leaveBob)\n"
            "    return max(0, min(a2, b2) - max(a1, b1) + 1)\n",
            lambda low: bool(
                re.search(
                    r"\bcount_days_together\b|"
                    r"\bcount[_ ]days[_ ]spent[_ ]together\b|"
                    r"\bdays[_ ]spent[_ ]together\b|"
                    r"\bleetcode[_ ]2409\b",
                    low,
                )
            ),
            (
                (("08-15", "08-18", "08-16", "08-19"), 3),
                (("10-01", "10-31", "11-01", "12-31"), 0),
            ),
        ),
        T(
            "minimum_sum_four_digit",
            "def minimum_sum_four_digit(num):\n"
            '    """Split four digits into two 2-digit numbers with minimum sum (LeetCode 2160)."""\n'
            "    d = sorted(int(c) for c in f'{num:04d}')\n"
            "    return 10 * d[0] + 10 * d[1] + d[2] + d[3]\n",
            lambda low: bool(
                re.search(
                    r"\bminimum_sum_four_digit\b|"
                    r"\bminimum[_ ]sum[_ ]of[_ ]four[_ ]digit\b|"
                    r"\bminimum[_ ]sum[_ ]of[_ ]a[_ ]four[_ ]digit[_ ]number\b|"
                    r"\bleetcode[_ ]2160\b",
                    low,
                )
            ),
            (
                ((2932,), 52),
                ((4009,), 13),
            ),
        ),
        T(
            "find_the_pivot_integer",
            "def find_the_pivot_integer(n):\n"
            '    """x in 1..n with sum(1..x)==sum(x..n), else -1 (LeetCode 2485)."""\n'
            "    total = n * (n + 1) // 2\n"
            "    acc = 0\n"
            "    for x in range(1, n + 1):\n"
            "        acc += x\n"
            "        if acc == total - acc + x:\n"
            "            return x\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bfind_the_pivot_integer\b|"
                    r"\bleetcode[_ ]2485\b",
                    low,
                )
            )
            and "index" not in low
            and "array" not in low,
            (
                ((8,), 6),
                ((1,), 1),
                ((4,), -1),
            ),
        ),
        T(
            "find_minimum_average",
            "def find_minimum_average(nums):\n"
            '    """Repeatedly pair min+max; return smallest average of those pairs (LeetCode 3194)."""\n'
            "    a = sorted(nums)\n"
            "    i, j = 0, len(a) - 1\n"
            "    best = float('inf')\n"
            "    while i < j:\n"
            "        best = min(best, (a[i] + a[j]) / 2)\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return best\n"
            "\n"
            "def minimum_average(nums):\n"
            "    return find_minimum_average(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bfind_minimum_average\b|"
                    r"\bminimum[_ ]average[_ ]of[_ ]smallest[_ ]and[_ ]largest\b|"
                    r"\bminimum[_ ]average\b|"
                    r"\bleetcode[_ ]3194\b",
                    low,
                )
            )
            and "sliding" not in low
            and "subarray" not in low,
            (
                (([7, 8, 3, 4, 15, 13, 4, 1],), 5.5),
                (([1, 9, 8, 3, 10, 5],), 5.5),
            ),
        ),
        T(
            "divisible_and_non_divisible",
            "def divisible_and_non_divisible(n, m):\n"
            '    """Sum of [1..n] not div by m minus sum of those div by m (LeetCode 2894)."""\n'
            "    num1 = num2 = 0\n"
            "    for i in range(1, n + 1):\n"
            "        if i % m == 0:\n"
            "            num2 += i\n"
            "        else:\n"
            "            num1 += i\n"
            "    return num1 - num2\n",
            lambda low: bool(
                re.search(
                    r"\bdivisible_and_non_divisible\b|"
                    r"\bdivisible[_ ]and[_ ]non[_ ]divisible\b|"
                    r"\bdifference[_ ]of[_ ]sums\b|"
                    r"\bleetcode[_ ]2894\b",
                    low,
                )
            )
            and "divisible by three" not in low,
            (
                ((10, 3), 19),
                ((5, 6), 15),
                ((5, 1), -15),
            ),
        ),
        T(
            "maximum_odd_binary",
            "def maximum_odd_binary(s):\n"
            '    """Rearrange bits so the binary value is odd and maximum (LeetCode 2864)."""\n'
            "    ones = s.count('1')\n"
            "    zeros = len(s) - ones\n"
            "    return '1' * (ones - 1) + '0' * zeros + '1'\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum_odd_binary\b|"
                    r"\bmaximum[_ ]odd[_ ]binary[_ ]number\b|"
                    r"\bleetcode[_ ]2864\b",
                    low,
                )
            ),
            (
                (("010",), "001"),
                (("0101",), "1001"),
            ),
        ),
    ]
