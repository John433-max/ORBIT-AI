"""Cycle 575: Rod cutting, Chinese Remainder Theorem, s-t min-cut capacity.

Closes the educational gap documented in Cycle 574. Smoke rows and
test_p272_rod_cutting_crt_mincut already expect these names; the pack
was listed in the loader but never landed.

Rod cutting: bottom-up DP (CLRS 15.1). prices[i] is the price of length i+1.
CRT: constructive solution for pairwise-coprime moduli (product + modular inverse).
Min-cut capacity: Edmonds-Karp max-flow (equals min-cut by the max-flow min-cut theorem).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "rod_cutting",
            "def rod_cutting(n, prices):\n"
            '    """Maximum revenue from cutting a rod of length n.\n\n'
            "    prices[i] is the price of a piece of length i+1.\n"
            "    Bottom-up DP (CLRS 15.1).\n"
            '    """\n'
            "    n = int(n)\n"
            "    if n <= 0 or not prices:\n"
            "        return 0\n"
            "    p = list(prices)\n"
            "    dp = [0] * (n + 1)\n"
            "    for length in range(1, n + 1):\n"
            "        best = 0\n"
            "        for cut in range(1, length + 1):\n"
            "            if cut - 1 < len(p):\n"
            "                best = max(best, p[cut - 1] + dp[length - cut])\n"
            "        dp[length] = best\n"
            "    return dp[n]\n",
            lambda low: bool(
                re.search(
                    r"\brod[- ]cutting\b|"
                    r"\bcutting a rod\b|"
                    r"\bmaximum revenue from cutting\b|"
                    r"\brevenue from cutting a rod\b",
                    low,
                )
            )
            and "coin" not in low,
            (
                ((4, [1, 5, 8, 9]), 10),
                ((8, [1, 5, 8, 9, 10, 17, 17, 20]), 22),
                ((0, [1, 5]), 0),
            ),
        ),
        T(
            "chinese_remainder",
            "def chinese_remainder(residues, moduli):\n"
            '    """Solve x ≡ a_i (mod m_i) for pairwise-coprime moduli.\n\n'
            "    Returns the unique solution modulo the product of the moduli.\n"
            "    Constructive CRT: x = sum(a_i * (M/m_i) * inv(M/m_i, m_i)) mod M.\n"
            '    """\n'
            "    a = list(residues)\n"
            "    m = list(moduli)\n"
            "    if not a or len(a) != len(m):\n"
            "        return 0\n"
            "    M = 1\n"
            "    for mi in m:\n"
            "        M *= int(mi)\n"
            "    x = 0\n"
            "    for ai, mi in zip(a, m):\n"
            "        Mi = M // int(mi)\n"
            "        x = (x + int(ai) * Mi * pow(Mi, -1, int(mi))) % M\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bchinese[- ]remainder\b|"
                    r"\bcrt\b|"
                    r"\bsimultaneous congruences\b",
                    low,
                )
            )
            and "cart" not in low
            and "credit" not in low,
            (
                (([2, 3, 2], [3, 5, 7]), 23),
                (([0, 3], [3, 4]), 3),
                (([1], [5]), 1),
            ),
        ),
        T(
            "min_cut_capacity",
            "def min_cut_capacity(n, edges, source, sink):\n"
            '    """s-t minimum-cut capacity (equals max-flow by the max-flow min-cut theorem).\n\n'
            "    edges is a list of (u, v, cap). Returns the capacity of a minimum s-t cut.\n"
            '    """\n'
            "    from collections import defaultdict, deque\n"
            "    n = int(n)\n"
            "    source, sink = int(source), int(sink)\n"
            "    if source == sink or n <= 0:\n"
            "        return 0\n"
            "    graph = [defaultdict(int) for _ in range(n)]\n"
            "    for u, v, c in edges:\n"
            "        if 0 <= u < n and 0 <= v < n:\n"
            "            graph[u][v] += c\n"
            "\n"
            "    def bfs():\n"
            "        parent = [-1] * n\n"
            "        parent[source] = source\n"
            "        q = deque([source])\n"
            "        while q:\n"
            "            u = q.popleft()\n"
            "            for v, cap in graph[u].items():\n"
            "                if cap > 0 and parent[v] == -1:\n"
            "                    parent[v] = u\n"
            "                    if v == sink:\n"
            "                        return parent\n"
            "                    q.append(v)\n"
            "        return None\n"
            "\n"
            "    flow = 0\n"
            "    while True:\n"
            "        parent = bfs()\n"
            "        if parent is None:\n"
            "            break\n"
            "        bottle = float('inf')\n"
            "        v = sink\n"
            "        while v != source:\n"
            "            u = parent[v]\n"
            "            bottle = min(bottle, graph[u][v])\n"
            "            v = u\n"
            "        v = sink\n"
            "        while v != source:\n"
            "            u = parent[v]\n"
            "            graph[u][v] -= bottle\n"
            "            graph[v][u] += bottle\n"
            "            v = u\n"
            "        flow += bottle\n"
            "    return flow\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)?[- ]cut\b|"
                    r"\bs-t min[- ]cut\b|"
                    r"\bminimum cut capacity\b|"
                    r"\bmin-cut capacity\b",
                    low,
                )
            )
            and "max flow" not in low
            and "maximum flow" not in low,
            (
                ((4, [(0, 1, 10), (0, 2, 10), (1, 2, 1), (1, 3, 10), (2, 3, 10)], 0, 3), 20),
                ((2, [(0, 1, 7)], 0, 1), 7),
                ((3, [(0, 1, 1), (1, 2, 1)], 0, 2), 1),
            ),
        ),
    ]
