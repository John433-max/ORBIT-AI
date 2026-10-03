"""Cycle 388: Easy prompts still absent from the template index.

LeetCode 3487, 3560, 3602, 3633, 3658, and 3663 were not referenced by any
pack. Matchers stay ID- or phrase-specific so unique-subarray, gcd, digit,
and cost templates keep their prompts.
Loaded before p108.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "max_unique_subarray_sum",
            "def max_unique_subarray_sum(nums):\n"
            '    """Max sum of a unique subarray after deletions (LeetCode 3487)."""\n'
            "    positives = {x for x in nums if x > 0}\n"
            "    if positives:\n"
            "        return sum(positives)\n"
            "    return max(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3487\b|"
                    r"\bunique subarray sum after deletion\b|"
                    r"\bmaximum unique subarray sum\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4, 5],), 15),
                (([1, 1, 0, 1, 1],), 1),
                (([1, 2, -1, -2, 1, 0, -1],), 3),
                (([-2, -1, -3],), -1),
            ),
        ),
        T(
            "min_log_transport_cost",
            "def min_log_transport_cost(n, m, k):\n"
            '    """Min cut cost to fit two logs on three trucks of cap k (LeetCode 3560)."""\n'
            "    n, m, k = int(n), int(m), int(k)\n"
            "    if n <= k and m <= k:\n"
            "        return 0\n"
            "    long = n if n > k else m\n"
            "    return k * (long - k)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3560\b|"
                    r"\blog transportation cost\b|"
                    r"\bminimum log transportation\b",
                    low,
                )
            ),
            (
                ((6, 5, 5), 5),
                ((4, 4, 6), 0),
                ((8, 3, 5), 15),
            ),
        ),
        T(
            "concat_hex36",
            "def concat_hex36(n):\n"
            '    """Concat hex(n^2) and base-36(n^3), uppercase (LeetCode 3602)."""\n'
            "    def to_base(x, base):\n"
            "        digits = []\n"
            "        while x:\n"
            "            x, v = divmod(x, base)\n"
            "            digits.append(str(v) if v <= 9 else chr(ord('A') + v - 10))\n"
            "        return ''.join(reversed(digits)) or '0'\n"
            "    n = int(n)\n"
            "    return to_base(n * n, 16) + to_base(n * n * n, 36)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3602\b|"
                    r"\bhexatrigesimal\b|"
                    r"\bhexadecimal and hexatrigesimal\b",
                    low,
                )
            ),
            (
                ((13,), "A91P1"),
                ((36,), "5101000"),
                ((1,), "11"),
            ),
        ),
        T(
            "earliest_finish_rides",
            "def earliest_finish_rides(land_start, land_dur, water_start, water_dur):\n"
            '    """Earliest finish of one land and one water ride, either order (LeetCode 3633)."""\n'
            "    def best(starts, durs, other_starts, other_durs):\n"
            "        min_end = min(s + d for s, d in zip(starts, durs))\n"
            "        return min(max(min_end, os) + od for os, od in zip(other_starts, other_durs))\n"
            "    return min(\n"
            "        best(land_start, land_dur, water_start, water_dur),\n"
            "        best(water_start, water_dur, land_start, land_dur),\n"
            "    )\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3633\b|"
                    r"\bland and water rides\b|"
                    r"\bearliest finish time for land\b",
                    low,
                )
            ),
            (
                (([2, 8], [4, 1], [6], [3]), 9),
                (([5], [3], [1, 4], [2, 6]), 8),
            ),
        ),
        T(
            "gcd_odd_even_sums",
            "def gcd_odd_even_sums(n):\n"
            '    """GCD of the first n odd sums and first n even sums (LeetCode 3658)."""\n'
            "    return int(n)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3658\b|"
                    r"\bgcd of odd and even sums\b|"
                    r"\bodd and even sums\b",
                    low,
                )
            ),
            (
                ((4,), 4),
                ((5,), 5),
                ((1,), 1),
            ),
        ),
        T(
            "least_frequent_digit",
            "def least_frequent_digit(n):\n"
            '    """Smallest digit with the lowest positive frequency in n (LeetCode 3663)."""\n'
            "    counts = [0] * 10\n"
            "    x = int(n)\n"
            "    if x == 0:\n"
            "        return 0\n"
            "    while x:\n"
            "        x, digit = divmod(x, 10)\n"
            "        counts[digit] += 1\n"
            "    best, freq = 0, 10 ** 9\n"
            "    for digit, seen in enumerate(counts):\n"
            "        if 0 < seen < freq:\n"
            "            freq = seen\n"
            "            best = digit\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3663\b|"
                    r"\bleast frequent digit\b|"
                    r"\bthe least frequent digit\b",
                    low,
                )
            ),
            (
                ((1553322,), 1),
                ((723344511,), 2),
                ((7,), 7),
            ),
        ),
    ]
