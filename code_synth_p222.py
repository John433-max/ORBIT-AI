"""Cycle 506: unmatched write-a-function asks.

LeetCode 3158, 3194, 3028, 2544, 2441, 3232.
Phrase gates stay narrow so xor/average/digit templates do not steal them.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "duplicate_numbers_xor",
            "def duplicate_numbers_xor(nums):\n"
            '    """XOR of values that appear exactly twice (LeetCode 3158)."""\n'
            "    from collections import Counter\n"
            "    acc = 0\n"
            "    for value, count in Counter(nums).items():\n"
            "        if count == 2:\n"
            "            acc ^= value\n"
            "    return acc\n",
            lambda low: (
                "xor" in low
                and "twice" in low
                and ("appear" in low or "duplicate" in low)
            ),
            (
                (([1, 2, 1, 3],), 1),
                (([1, 2, 3],), 0),
                (([1, 2, 2, 1],), 3),
            ),
        ),
        T(
            "maximum_odd_binary_number",
            "def maximum_odd_binary_number(s):\n"
            '    """Largest odd binary string with the same bits (LeetCode 2864)."""\n'
            "    ones = s.count('1')\n"
            "    zeros = len(s) - ones\n"
            "    if ones == 0:\n"
            "        return s\n"
            "    return '1' * (ones - 1) + '0' * zeros + '1'\n",
            lambda low: "odd binary" in low and "number" in low,
            (
                (("010",), "001"),
                (("0101",), "1001"),
            ),
        ),
        T(
            "return_to_boundary_count",
            "def return_to_boundary_count(nums):\n"
            '    """Times an ant on the boundary returns to 0 (LeetCode 3028)."""\n'
            "    pos = 0\n"
            "    hits = 0\n"
            "    for step in nums:\n"
            "        pos += step\n"
            "        if pos == 0:\n"
            "            hits += 1\n"
            "    return hits\n",
            lambda low: "boundary" in low and ("ant" in low or "return" in low),
            (
                (([2, 3, -5],), 1),
                (([3, 2, -3, -4],), 0),
            ),
        ),
        T(
            "alternate_digit_sum",
            "def alternate_digit_sum(n):\n"
            '    """Alternating digit sum; first digit is positive (LeetCode 2544)."""\n'
            "    total = 0\n"
            "    sign = 1\n"
            "    for ch in str(n):\n"
            "        total += sign * int(ch)\n"
            "        sign = -sign\n"
            "    return total\n",
            lambda low: "alternating" in low and "digit" in low and "sum" in low,
            (
                ((521,), 4),
                ((111,), 1),
                ((886996,), 0),
            ),
        ),
        T(
            "find_max_k",
            "def find_max_k(nums):\n"
            '    """Largest positive that also has its negative, else -1 (LeetCode 2441)."""\n'
            "    seen = set(nums)\n"
            "    best = -1\n"
            "    for value in nums:\n"
            "        if value > best and -value in seen:\n"
            "            best = value\n"
            "    return best\n",
            lambda low: (
                "negative" in low
                and ("positive" in low or "largest" in low)
                and ("exist" in low or "with its negative" in low)
            ),
            (
                (([-1, 2, -3, 3],), 3),
                (([-1, 10, 6, 7, -7, 1],), 7),
                (([-10, 8, 6, 7, -2, -3],), -1),
            ),
        ),
        T(
            "can_alice_win",
            "def can_alice_win(nums):\n"
            '    """Alice wins the digit game iff single-digit sum != double-digit sum (LeetCode 3232)."""\n'
            "    single = sum(x for x in nums if x < 10)\n"
            "    double = sum(x for x in nums if x >= 10)\n"
            "    return single != double\n",
            lambda low: (
                "digit game" in low
                or ("alice" in low and "win" in low and "digit" in low)
            ),
            (
                (([1, 2, 3, 4, 10],), False),
                (([1, 2, 3, 4, 5, 14],), True),
                (([5, 5, 5, 25],), True),
            ),
        ),
    ]
