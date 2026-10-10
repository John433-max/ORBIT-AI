"""Cycle 553: Hungarian (Kuhn-Munkres) min-cost assignment + Kasai LCP array.

Loaded first so classic algorithm phrases beat draft stubs and longest_common_prefix.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "hungarian_assignment",
            "def hungarian_assignment(cost):\n"
            '    """Min-cost assignment via Kuhn-Munkres / Hungarian.\n'
            '    cost: n x n matrix. Returns (total, list of column for each row)."""\n'
            "    n = len(cost)\n"
            "    if n == 0:\n"
            "        return 0, []\n"
            "    u = [0] * (n + 1)\n"
            "    v = [0] * (n + 1)\n"
            "    p = [0] * (n + 1)\n"
            "    way = [0] * (n + 1)\n"
            "    for i in range(1, n + 1):\n"
            "        p[0] = i\n"
            "        j0 = 0\n"
            "        minv = [float('inf')] * (n + 1)\n"
            "        used = [False] * (n + 1)\n"
            "        while True:\n"
            "            used[j0] = True\n"
            "            i0 = p[j0]\n"
            "            delta = float('inf')\n"
            "            j1 = 0\n"
            "            for j in range(1, n + 1):\n"
            "                if not used[j]:\n"
            "                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]\n"
            "                    if cur < minv[j]:\n"
            "                        minv[j] = cur\n"
            "                        way[j] = j0\n"
            "                    if minv[j] < delta:\n"
            "                        delta = minv[j]\n"
            "                        j1 = j\n"
            "            for j in range(n + 1):\n"
            "                if used[j]:\n"
            "                    u[p[j]] += delta\n"
            "                    v[j] -= delta\n"
            "                else:\n"
            "                    minv[j] -= delta\n"
            "            j0 = j1\n"
            "            if p[j0] == 0:\n"
            "                break\n"
            "        while j0:\n"
            "            j1 = way[j0]\n"
            "            p[j0] = p[j1]\n"
            "            j0 = j1\n"
            "    assignment = [0] * n\n"
            "    for j in range(1, n + 1):\n"
            "        if p[j] != 0:\n"
            "            assignment[p[j] - 1] = j - 1\n"
            "    total = sum(cost[i][assignment[i]] for i in range(n))\n"
            "    return total, assignment\n",
            lambda low: bool(
                re.search(
                    r"\bhungarian(?: algorithm)?\b|"
                    r"\bkuhn[- ]?munkres\b|"
                    r"\bassignment problem\b|"
                    r"\bmin(?:imum)?[- ]?cost assignment\b|"
                    r"\bminimum cost bipartite matching\b",
                    low,
                )
            ),
            (
                (([[4, 1, 3], [2, 0, 5], [3, 2, 2]],), (5, [1, 0, 2])),
                (([[10, 19, 8], [15, 15, 0], [3, 7, 6]],), (17, [0, 2, 1])),
                (([[1, 2], [3, 4]],), (5, [0, 1])),
            ),
        ),
        T(
            "longest_common_prefix_array",
            "def longest_common_prefix_array(s, sa=None):\n"
            '    """Kasai LCP array. lcp[i] = LCP of suffixes at sa[i-1] and sa[i].\n'
            '    Returns list of length n-1. Builds SA naively if sa is omitted."""\n'
            "    n = len(s)\n"
            "    if n == 0:\n"
            "        return []\n"
            "    if sa is None:\n"
            "        sa = sorted(range(n), key=lambda i: s[i:])\n"
            "    rank = [0] * n\n"
            "    for i, p in enumerate(sa):\n"
            "        rank[p] = i\n"
            "    lcp = [0] * n\n"
            "    k = 0\n"
            "    for i in range(n):\n"
            "        if rank[i] == 0:\n"
            "            k = 0\n"
            "            continue\n"
            "        j = sa[rank[i] - 1]\n"
            "        while i + k < n and j + k < n and s[i + k] == s[j + k]:\n"
            "            k += 1\n"
            "        lcp[rank[i]] = k\n"
            "        if k:\n"
            "            k -= 1\n"
            "    return lcp[1:]\n",
            lambda low: bool(
                re.search(
                    r"\blcp[- ]?array\b|"
                    r"\blongest common prefix array\b|"
                    r"\bkasai(?: algorithm)?\b|"
                    r"\bbuild lcp\b|"
                    r"\bconstruct (?:the )?lcp\b",
                    low,
                )
            )
            and "longest common prefix of" not in low,
            (
                (("banana",), [1, 3, 0, 0, 2]),
                (("banana", [5, 3, 1, 0, 4, 2]), [1, 3, 0, 0, 2]),
                (("",), []),
            ),
        ),
    ]
