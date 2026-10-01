"""Cycle 311: subset XOR sum / digit lucky / three divisors / |diff|=k pairs / seat moves / ticket time."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "subset_xor_sum",
            "def subset_xor_sum(nums):\n"
            '    """Sum of XOR totals of every subset (LeetCode 1863)."""\n'
            "    total = 0\n"
            "    n = len(nums)\n"
            "    for mask in range(1 << n):\n"
            "        x = 0\n"
            "        for i in range(n):\n"
            "            if mask & (1 << i):\n"
            "                x ^= nums[i]\n"
            "        total += x\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bsum[_ ]of[_ ]all[_ ]subset[_ ]xor[_ ]totals\b|"
                    r"\bsubset[_ ]xor[_ ]sum\b|"
                    r"\bsubset_xor_sum\b",
                    low,
                )
            ),
            (
                (([1, 3],), 6),
                (([5, 1, 6],), 28),
                (([3, 4, 5, 6, 7, 8],), 480),
            ),
        ),
        T(
            "get_lucky",
            "def get_lucky(s, k):\n"
            '    """Convert letters to 1-26 then sum digits k times (LeetCode 1945)."""\n'
            "    cur = \"\".join(str(ord(ch) - 96) for ch in s)\n"
            "    for _ in range(k):\n"
            "        cur = str(sum(int(d) for d in cur))\n"
            "    return int(cur)\n",
            lambda low: bool(
                re.search(
                    r"\bsum[_ ]of[_ ]digits[_ ]of[_ ]string[_ ]after[_ ]convert\b|"
                    r"\bget[_ ]lucky\b|"
                    r"\bget_lucky\b",
                    low,
                )
            ),
            (
                (("iiii", 1), 36),
                (("leetcode", 2), 6),
                (("zbax", 2), 8),
            ),
        ),
        T(
            "is_three",
            "def is_three(n):\n"
            '    """True iff n has exactly three positive divisors (LeetCode 1952)."""\n'
            "    if n < 4:\n"
            "        return False\n"
            "    root = int(n ** 0.5)\n"
            "    if root * root != n:\n"
            "        return False\n"
            "    if root < 2:\n"
            "        return False\n"
            "    i = 2\n"
            "    while i * i <= root:\n"
            "        if root % i == 0:\n"
            "            return False\n"
            "        i += 1\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bthree[_ ]divisors\b|"
                    r"\bexactly[_ ]three[_ ](positive[_ ])?divisors\b|"
                    r"\bis_three\b",
                    low,
                )
            ),
            (
                ((2,), False),
                ((4,), True),
                ((12,), False),
            ),
        ),
        T(
            "count_k_difference",
            "def count_k_difference(nums, k):\n"
            '    """Count pairs whose absolute difference is k (LeetCode 2006)."""\n'
            "    count = 0\n"
            "    n = len(nums)\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            if abs(nums[i] - nums[j]) == k:\n"
            "                count += 1\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\bpairs[_ ]with[_ ]absolute[_ ]difference[_ ]k\b|"
                    r"\bcount[_ ]k[_ ]difference\b|"
                    r"\bcount_k_difference\b",
                    low,
                )
            ),
            (
                (([1, 2, 2, 1], 1), 4),
                (([1, 3], 3), 0),
                (([3, 2, 1, 5, 4], 2), 3),
            ),
        ),
        T(
            "min_moves_to_seat",
            "def min_moves_to_seat(seats, students):\n"
            '    """Min moves to seat every student (LeetCode 2037)."""\n'
            "    seats = sorted(seats)\n"
            "    students = sorted(students)\n"
            "    return sum(abs(a - b) for a, b in zip(seats, students))\n",
            lambda low: bool(
                re.search(
                    r"\bminimum[_ ]number[_ ]of[_ ]moves[_ ]to[_ ]seat[_ ]everyone\b|"
                    r"\bmin[_ ]moves[_ ]to[_ ]seat\b|"
                    r"\bmin_moves_to_seat\b",
                    low,
                )
            ),
            (
                (([3, 1, 5], [2, 7, 4]), 4),
                (([4, 1, 5, 9], [1, 3, 2, 6]), 7),
                (([2, 2, 6, 6], [1, 3, 2, 6]), 4),
            ),
        ),
        T(
            "time_required_to_buy",
            "def time_required_to_buy(tickets, k):\n"
            '    """Seconds for person k to finish buying tickets (LeetCode 2073)."""\n'
            "    t = 0\n"
            "    need = tickets[k]\n"
            "    for i, x in enumerate(tickets):\n"
            "        if i <= k:\n"
            "            t += min(x, need)\n"
            "        else:\n"
            "            t += min(x, need - 1)\n"
            "    return t\n",
            lambda low: bool(
                re.search(
                    r"\btime[_ ]needed[_ ]to[_ ]buy[_ ]tickets\b|"
                    r"\btime[_ ]required[_ ]to[_ ]buy\b|"
                    r"\btime_required_to_buy\b",
                    low,
                )
            ),
            (
                (([2, 3, 2], 2), 6),
                (([5, 1, 1, 1], 0), 8),
                (([1], 0), 1),
            ),
        ),
    ]
