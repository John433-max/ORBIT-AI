"""Cycle 334: unused Easy — distance value / divisor game / tribonacci /
rectangle overlap / long pressed name / last stone weight."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "find_the_distance_value",
            "def find_the_distance_value(arr1, arr2, d):\n"
            '    """Count arr1[i] with no arr2[j] within d (LeetCode 1385)."""\n'
            "    return sum(\n"
            "        1 for a in arr1 if all(abs(a - b) > d for b in arr2)\n"
            "    )\n",
            lambda low: bool(
                re.search(
                    r"\bfind_the_distance_value\b|"
                    r"\bfind[_ ]the[_ ]distance[_ ]value\b|"
                    r"\bdistance[_ ]value[_ ]between[_ ]two[_ ]arrays\b|"
                    r"\bleetcode[_ ]1385\b",
                    low,
                )
            )
            and "bus stop" not in low,
            (
                (([4, 5, 8], [10, 9, 1, 8], 2), 2),
                (([1, 4, 2, 3], [-4, -3, 6, 10, 20, 30], 3), 2),
                (([2, 1, 3], [3], 3), 0),
            ),
        ),
        T(
            "divisor_game",
            "def divisor_game(n):\n"
            '    """Alice wins the divisor game iff n is even (LeetCode 1025)."""\n'
            "    return n % 2 == 0\n",
            lambda low: bool(
                re.search(
                    r"\bdivisor_game\b|"
                    r"\bdivisor[_ ]game\b|"
                    r"\bleetcode[_ ]1025\b",
                    low,
                )
            )
            and "alice win" not in low
            and "digit game" not in low,
            (
                ((2,), True),
                ((3,), False),
                ((4,), True),
            ),
        ),
        T(
            "tribonacci",
            "def tribonacci(n):\n"
            '    """Nth Tribonacci number T0=0 T1=1 T2=1 (LeetCode 1137)."""\n'
            "    if n == 0:\n"
            "        return 0\n"
            "    if n <= 2:\n"
            "        return 1\n"
            "    a, b, c = 0, 1, 1\n"
            "    for _ in range(3, n + 1):\n"
            "        a, b, c = b, c, a + b + c\n"
            "    return c\n",
            lambda low: bool(
                re.search(
                    r"\btribonacci\b|"
                    r"\bn[_ -]?th[_ ]tribonacci\b|"
                    r"\bleetcode[_ ]1137\b",
                    low,
                )
            )
            and "fibonacci" not in low,
            (
                ((4,), 4),
                ((25,), 1389537),
                ((0,), 0),
            ),
        ),
        T(
            "prefixes_div_by_5",
            "def prefixes_div_by_5(nums):\n"
            '    """Which binary prefixes form numbers divisible by 5 (LeetCode 1018)."""\n'
            "    out = []\n"
            "    val = 0\n"
            "    for bit in nums:\n"
            "        val = ((val << 1) + bit) % 5\n"
            "        out.append(val == 0)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bprefixes_div_by_5\b|"
                    r"\bbinary[_ ]prefix(es)?[_ ]divisible[_ ]by[_ ]5\b|"
                    r"\bleetcode[_ ]1018\b",
                    low,
                )
            ),
            (
                (([0, 1, 1],), [True, False, False]),
                (([1, 1, 1],), [False, False, False]),
            ),
        ),
        T(
            "is_long_pressed_name",
            "def is_long_pressed_name(name, typed):\n"
            '    """True if typed is name with optional long-press (LeetCode 925)."""\n'
            "    i = 0\n"
            "    for j, ch in enumerate(typed):\n"
            "        if i < len(name) and name[i] == ch:\n"
            "            i += 1\n"
            "        elif j == 0 or ch != typed[j - 1]:\n"
            "            return False\n"
            "    return i == len(name)\n",
            lambda low: bool(
                re.search(
                    r"\bis_long_pressed_name\b|"
                    r"\blong[_ ]pressed[_ ]name\b|"
                    r"\bleetcode[_ ]925\b",
                    low,
                )
            ),
            (
                (("alex", "aaleex"), True),
                (("saeed", "ssaaedd"), False),
                (("leelee", "lleeelee"), True),
            ),
        ),
        T(
            "last_stone_weight",
            "def last_stone_weight(stones):\n"
            '    """Smash heaviest pair until one or zero stones (LeetCode 1046)."""\n'
            "    import heapq\n"
            "    h = [-s for s in stones]\n"
            "    heapq.heapify(h)\n"
            "    while len(h) > 1:\n"
            "        y = -heapq.heappop(h)\n"
            "        x = -heapq.heappop(h)\n"
            "        if y != x:\n"
            "            heapq.heappush(h, -(y - x))\n"
            "    return -h[0] if h else 0\n",
            lambda low: bool(
                re.search(
                    r"\blast_stone_weight\b|"
                    r"\blast[_ ]stone[_ ]weight\b|"
                    r"\bleetcode[_ ]1046\b",
                    low,
                )
            )
            and "ii" not in low,
            (
                (([2, 7, 4, 1, 8, 1],), 1),
                (([1],), 1),
            ),
        ),
    ]
