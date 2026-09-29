"""Cycle 300: tested devices / employees target / difference of sums / L-R diffs / min number game / k-set-bit indices."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_tested_devices",
            "def count_tested_devices(batteryPercentages):\n"
            '    """Count devices tested after decrementing later batteries (LeetCode 2960)."""\n'
            "    tested = 0\n"
            "    for b in batteryPercentages:\n"
            "        if b - tested > 0:\n"
            "            tested += 1\n"
            "    return tested\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]tested[_ ]devices\b|"
                    r"\bcount tested devices after test operations\b|"
                    r"\bcount (?:the )?tested devices\b",
                    low,
                )
            ),
            (
                (([1, 1, 2, 1, 3],), 3),
                (([0, 1, 2],), 2),
                (([0, 0, 0],), 0),
            ),
        ),
        T(
            "number_of_employees_who_met_target",
            "def number_of_employees_who_met_target(hours, target):\n"
            '    """Employees with hours >= target (LeetCode 2798)."""\n'
            "    return sum(1 for h in hours if h >= target)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]of[_ ]employees[_ ]who[_ ]met[_ ]target\b|"
                    r"\bemployees who met (?:the )?target\b|"
                    r"\bnumber of employees who met target\b",
                    low,
                )
            ),
            (
                (([0, 1, 2, 3, 4], 2), 3),
                (([5, 1, 4, 2, 2], 6), 0),
                (([1, 2], 1), 2),
            ),
        ),
        T(
            "difference_of_sums",
            "def difference_of_sums(n, m):\n"
            '    """Sum of [1..n] not divisible by m minus those that are (LeetCode 2535/2894)."""\n'
            "    total = n * (n + 1) // 2\n"
            "    k = n // m\n"
            "    div = m * k * (k + 1) // 2\n"
            "    return total - 2 * div\n",
            lambda low: bool(
                re.search(
                    r"\bdifference[_ ]of[_ ]sums\b|"
                    r"\bdifference between element sum and digit sum\b|"
                    r"\bdifference of sums divisible by\b|"
                    r"\bdivisible and non-divisible sums difference\b",
                    low,
                )
            )
            and "two arrays" not in low,
            (
                ((10, 3), 19),
                ((5, 6), 15),
                ((5, 1), -15),
            ),
        ),
        T(
            "left_right_difference",
            "def left_right_difference(nums):\n"
            '    """|leftSum[i] - rightSum[i]| for each index (LeetCode 2574)."""\n'
            "    total = sum(nums)\n"
            "    left = 0\n"
            "    out = []\n"
            "    for x in nums:\n"
            "        right = total - left - x\n"
            "        out.append(abs(left - right))\n"
            "        left += x\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bleft[_ ]right[_ ]difference\b|"
                    r"\bleft and right sum differences\b|"
                    r"\bleft right difference\b",
                    low,
                )
            ),
            (
                (([10, 4, 8, 3],), [15, 1, 11, 22]),
                (([1],), [0]),
                (([1, 2, 3],), [5, 2, 3]),
            ),
        ),
        T(
            "number_game",
            "def number_game(nums):\n"
            '    """Alice/Bob min-pair swap game (LeetCode 2974)."""\n'
            "    a = sorted(nums)\n"
            "    for i in range(0, len(a) - 1, 2):\n"
            "        a[i], a[i + 1] = a[i + 1], a[i]\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]game\b|"
                    r"\bminimum number game\b|"
                    r"\balice and bob number game\b",
                    low,
                )
            ),
            (
                (([5, 4, 2, 3],), [3, 2, 5, 4]),
                (([2, 5],), [5, 2]),
                (([1, 2, 3, 4],), [2, 1, 4, 3]),
            ),
        ),
        T(
            "sum_indices_with_k_set_bits",
            "def sum_indices_with_k_set_bits(nums, k):\n"
            '    """Sum nums[i] where i has k set bits (LeetCode 2859)."""\n'
            "    return sum(v for i, v in enumerate(nums) if bin(i).count('1') == k)\n",
            lambda low: bool(
                re.search(
                    r"\bsum[_ ]indices[_ ]with[_ ]k[_ ]set[_ ]bits\b|"
                    r"\bsum of values at indices with k set bits\b|"
                    r"\bindices with k set bits\b",
                    low,
                )
            ),
            (
                (([5, 10, 1, 5, 2], 1), 13),
                (([4, 3, 2, 1], 2), 1),
                (([1, 2], 0), 1),
            ),
        ),
    ]
