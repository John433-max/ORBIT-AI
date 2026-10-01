"""Cycle 315: buy two chocolates / typewriter time / merge similar items /
min-max game / pass the pillow / excel cells in a range."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "buy_choco",
            "def buy_choco(prices, money):\n"
            '    """Leftover money after buying the two cheapest chocolates (LeetCode 2706)."""\n'
            "    a = b = 10**9\n"
            "    for p in prices:\n"
            "        if p < a:\n"
            "            b = a\n"
            "            a = p\n"
            "        elif p < b:\n"
            "            b = p\n"
            "    cost = a + b\n"
            "    return money - cost if cost <= money else money\n",
            lambda low: bool(
                re.search(
                    r"\bbuy[_ ](?:two[_ ])?choco(?:lates?)?\b|"
                    r"\bbuy_choco\b",
                    low,
                )
            ),
            (
                (([1, 2, 2], 3), 0),
                (([3, 2, 3], 3), 3),
                (([98, 54, 6, 34, 66], 60), 20),
            ),
        ),
        T(
            "min_time_to_type",
            "def min_time_to_type(word):\n"
            '    """Seconds to type word on a circular a-z typewriter (LeetCode 1974)."""\n'
            "    t = 0\n"
            "    prev = 0\n"
            "    for ch in word:\n"
            "        cur = ord(ch) - 97\n"
            "        d = abs(cur - prev)\n"
            "        t += min(d, 26 - d) + 1\n"
            "        prev = cur\n"
            "    return t\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)?[_ ]time[_ ]to[_ ]type\b|"
                    r"\bmin_time_to_type\b|"
                    r"\bspecial[_ ]typewriter\b",
                    low,
                )
            ),
            (
                (("abc",), 5),
                (("bza",), 7),
                (("zjpc",), 34),
            ),
        ),
        T(
            "merge_similar_items",
            "def merge_similar_items(items1, items2):\n"
            '    """Merge two [value, weight] lists by value (LeetCode 2363)."""\n'
            "    w = {}\n"
            "    for v, wt in items1 + items2:\n"
            "        w[v] = w.get(v, 0) + wt\n"
            "    return [[v, w[v]] for v in sorted(w)]\n",
            lambda low: bool(
                re.search(
                    r"\bmerge[_ ]similar[_ ]items\b|"
                    r"\bmerge_similar_items\b",
                    low,
                )
            ),
            (
                (([[1, 1], [4, 5], [3, 8]], [[3, 1], [1, 5]]), [[1, 6], [3, 9], [4, 5]]),
                (([[1, 1], [3, 2], [2, 3]], [[2, 1], [3, 2], [1, 3]]), [[1, 4], [2, 4], [3, 4]]),
                (([[1, 3], [2, 2]], [[7, 1], [2, 2], [1, 4]]), [[1, 7], [2, 4], [7, 1]]),
            ),
        ),
        T(
            "min_max_game",
            "def min_max_game(nums):\n"
            '    """Alternate min/max until one value remains (LeetCode 2293)."""\n'
            "    while len(nums) > 1:\n"
            "        nxt = []\n"
            "        for i in range(0, len(nums), 2):\n"
            "            a, b = nums[i], nums[i + 1]\n"
            "            nxt.append(min(a, b) if (i // 2) % 2 == 0 else max(a, b))\n"
            "        nums = nxt\n"
            "    return nums[0]\n",
            lambda low: bool(
                re.search(
                    r"\bmin[_ ]max[_ ]game\b|"
                    r"\bminmax[_ ]game\b|"
                    r"\bmin_max_game\b",
                    low,
                )
            ),
            (
                (([1, 3, 5, 2, 4, 8, 2, 2],), 1),
                (([3],), 3),
                (([1, 2],), 1),
            ),
        ),
        T(
            "pass_the_pillow",
            "def pass_the_pillow(n, time):\n"
            '    """Who holds the pillow after `time` passes along 1..n..1 (LeetCode 2582)."""\n'
            "    cycle = 2 * (n - 1)\n"
            "    t = time % cycle\n"
            "    if t < n:\n"
            "        return 1 + t\n"
            "    return n - (t - (n - 1))\n",
            lambda low: bool(
                re.search(
                    r"\bpass[_ ]the[_ ]pillow\b|"
                    r"\bpass_the_pillow\b",
                    low,
                )
            ),
            (
                ((4, 5), 2),
                ((3, 2), 3),
                ((2, 1), 2),
            ),
        ),
        T(
            "cells_in_range",
            "def cells_in_range(s):\n"
            '    """Excel cells in inclusive range like A1:C2 (LeetCode 2194)."""\n'
            "    a, b = s.split(':')\n"
            "    c1, r1 = a[0], int(a[1:])\n"
            "    c2, r2 = b[0], int(b[1:])\n"
            "    out = []\n"
            "    for c in range(ord(c1), ord(c2) + 1):\n"
            "        for r in range(r1, r2 + 1):\n"
            "            out.append(chr(c) + str(r))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bcells[_ ]in[_ ](?:a[_ ])?range\b|"
                    r"\bcells_in_range\b|"
                    r"\bexcel[_ ]cells[_ ]in[_ ](?:a[_ ])?range\b",
                    low,
                )
            ),
            (
                (("K1:L2",), ["K1", "K2", "L1", "L2"]),
                (("A1:F1",), ["A1", "B1", "C1", "D1", "E1", "F1"]),
                (("A1:A3",), ["A1", "A2", "A3"]),
            ),
        ),
    ]
