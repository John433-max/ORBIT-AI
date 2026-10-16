"""Cycle 594: cocktail sort, cycle sort, LZW, move-to-front, 2-opt TSP, binary GA.

Educational pure-Python classics that previously returned None on match_template.
Matchers kept narrow so they do not steal existing sort / TSP / search templates.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "cocktail_sort",
            "def cocktail_sort(arr):\n"
            '    """Sort with cocktail (shaker) sort. Returns a new list."""\n'
            "    a = list(arr)\n"
            "    n = len(a)\n"
            "    swapped = True\n"
            "    start, end = 0, n - 1\n"
            "    while swapped:\n"
            "        swapped = False\n"
            "        for i in range(start, end):\n"
            "            if a[i] > a[i + 1]:\n"
            "                a[i], a[i + 1] = a[i + 1], a[i]\n"
            "                swapped = True\n"
            "        if not swapped:\n"
            "            break\n"
            "        swapped = False\n"
            "        end -= 1\n"
            "        for i in range(end - 1, start - 1, -1):\n"
            "            if a[i] > a[i + 1]:\n"
            "                a[i], a[i + 1] = a[i + 1], a[i]\n"
            "                swapped = True\n"
            "        start += 1\n"
            "    return a\n",
            lambda q: bool(re.search(r"cocktail\\s+sort|shaker\\s+sort", q, re.I)),
            examples=(([3, 1, 2],), [1, 2, 3]),
        ),
    ]
