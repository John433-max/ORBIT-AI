"""Cycle 558: Jarvis march, 2-SAT, minimax, alpha-beta, line-sweep overlaps, gift wrapping.

Fills remaining draft-stub gaps for classic algorithms.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "jarvis_march",
            "def jarvis_march(points):\n"
            '    """Gift wrapping / Jarvis march convex hull. Returns hull points in order."""\n'
            "    if len(points) < 3:\n"
            "        return list(points)\n"
            "    start = min(points, key=lambda p: (p[0], p[1]))\n"
            "    hull = []\n"
            "    current = start\n"
            "    while True:\n"
            "        hull.append(current)\n"
            "        nxt = points[0] if points[0] != current else points[1]\n"
            "        for p in points:\n"
            "            if p == current:\n"
            "                continue\n"
            "            cross = (nxt[0] - current[0]) * (p[1] - current[1]) - (nxt[1] - current[1]) * (p[0] - current[0])\n"
            "            if cross < 0 or (cross == 0 and (p[0] - current[0])**2 + (p[1] - current[1])**2 > (nxt[0] - current[0])**2 + (nxt[1] - current[1])**2):\n"
            "                nxt = p\n"
            "        current = nxt\n"
            "        if current == start:\n"
            "            break\n"
            "    return hull\n",
            lambda low: bool(
                re.search(r"\bjarvis[- ]?march\b|\bgift[- ]wrapping\b", low)
            )
            and "graham" not in low,
            (
                ((((0, 0), (1, 1), (2, 0), (1, 0.5)),), [(0, 0), (2, 0), (1, 1)]),
                ((((0, 0), (1, 0), (0, 1)),), [(0, 0), (1, 0), (0, 1)]),
            ),
        ),
        T(
            "two_sat",
            "def two_sat(n, clauses):\n"
            '    """2-SAT via implication graph + Kosaraju SCC. Returns assignment or None if unsat."""\n'
            "    def idx(x):\n"
            "        return 2 * (abs(x) - 1) + (1 if x < 0 else 0)\n"
            "    g = [[] for _ in range(2 * n)]\n"
            "    gr = [[] for _ in range(2 * n)]\n"
            "    for a, b in clauses:\n"
            "        g[idx(-a)].append(idx(b))\n"
            "        g[idx(-b)].append(idx(a))\n"
            "        gr[idx(b)].append(idx(-a))\n"
            "        gr[idx(a)].append(idx(-b))\n"
            "    order = []\n"
            "    seen = [False] * (2 * n)\n"
            "    def dfs1(u):\n"
            "        seen[u] = True\n"
            "        for v in g[u]:\n"
            "            if not seen[v]:\n"
            "                dfs1(v)\n"
            "        order.append(u)\n"
            "    for i in range(2 * n):\n"
            "        if not seen[i]:\n"
            "            dfs1(i)\n"
            "    comp = [-1] * (2 * n)\n"
            "    def dfs2(u, c):\n"
            "        comp[u] = c\n"
            "        for v in gr[u]:\n"
            "            if comp[v] < 0:\n"
            "                dfs2(v, c)\n"
            "    c = 0\n"
            "    for u in reversed(order):\n"
            "        if comp[u] < 0:\n"
            "            dfs2(u, c)\n"
            "            c += 1\n"
            "    assign = []\n"
            "    for i in range(n):\n"
            "        if comp[2 * i] == comp[2 * i + 1]:\n"
            "            return None\n"
            "        assign.append(comp[2 * i] > comp[2 * i + 1])\n"
            "    return assign\n",
            lambda low: bool(
                re.search(r"\b2[- ]?sat\b|\btwo[- ]sat\b|\btwo satisfiability\b", low)
            ),
            (
                ((2, [(1, 2), (-1, 2)]), [True, True]),
                ((1, [(1, 1), (-1, -1)]), None),
            ),
        ),
        T(
            "minimax",
            "def minimax(node, depth, maximizing):\n"
            '    """Simple minimax on a tree of lists: leaf is int, internal is list of children."""\n'
            "    if depth == 0 or not isinstance(node, list):\n"
            "        return node if isinstance(node, int) else 0\n"
            "    if maximizing:\n"
            "        return max(minimax(c, depth - 1, False) for c in node)\n"
            "    return min(minimax(c, depth - 1, True) for c in node)\n",
            lambda low: bool(
                re.search(r"\bminimax\b", low)
            )
            and "alpha" not in low
            and "beta" not in low,
            (
                (([3, 5, 2], 1, True), 5),
                (([[1, 3], [2, 4]], 2, True), 2),
            ),
        ),
        T(
            "alpha_beta",
            "def alpha_beta(node, depth, alpha, beta, maximizing):\n"
            '    """Alpha-beta pruning minimax. node is int leaf or list of children."""\n'
            "    if depth == 0 or not isinstance(node, list):\n"
            "        return node if isinstance(node, int) else 0\n"
            "    if maximizing:\n"
            "        v = float('-inf')\n"
            "        for c in node:\n"
            "            v = max(v, alpha_beta(c, depth - 1, alpha, beta, False))\n"
            "            alpha = max(alpha, v)\n"
            "            if alpha >= beta:\n"
            "                break\n"
            "        return v\n"
            "    v = float('inf')\n"
            "    for c in node:\n"
            "        v = min(v, alpha_beta(c, depth - 1, alpha, beta, True))\n"
            "        beta = min(beta, v)\n"
            "        if beta <= alpha:\n"
            "            break\n"
            "    return v\n",
            lambda low: bool(
                re.search(r"\balpha[- ]?beta\b|\balphabeta\b", low)
            ),
            (
                (([3, 5, 2], 1, float("-inf"), float("inf"), True), 5),
                (([[1, 3], [2, 4]], 2, float("-inf"), float("inf"), True), 2),
            ),
        ),
        T(
            "line_sweep_overlaps",
            "def line_sweep_overlaps(intervals):\n"
            '    """Count number of overlapping interval pairs via sweep line. intervals: list of (start, end)."""\n'
            "    events = []\n"
            "    for s, e in intervals:\n"
            "        events.append((s, 1))\n"
            "        events.append((e, -1))\n"
            "    events.sort()\n"
            "    active = 0\n"
            "    overlaps = 0\n"
            "    for _, delta in events:\n"
            "        if delta == 1:\n"
            "            overlaps += active\n"
            "            active += 1\n"
            "        else:\n"
            "            active -= 1\n"
            "    return overlaps\n",
            lambda low: bool(
                re.search(r"\bline[- ]sweep\b|\bsweep[- ]line\b", low)
            )
            and "closest" not in low,
            (
                ((((1, 3), (2, 4), (5, 6)),), 1),
                ((((1, 5), (2, 3), (4, 6)),), 2),
            ),
        ),
        T(
            "gift_wrapping",
            "def gift_wrapping(points):\n"
            '    """Gift wrapping / Jarvis march convex hull. Returns hull points in order."""\n'
            "    if len(points) < 3:\n"
            "        return list(points)\n"
            "    start = min(points, key=lambda p: (p[0], p[1]))\n"
            "    hull = []\n"
            "    current = start\n"
            "    while True:\n"
            "        hull.append(current)\n"
            "        nxt = points[0] if points[0] != current else points[1]\n"
            "        for p in points:\n"
            "            if p == current:\n"
            "                continue\n"
            "            cross = (nxt[0] - current[0]) * (p[1] - current[1]) - (nxt[1] - current[1]) * (p[0] - current[0])\n"
            "            if cross < 0 or (cross == 0 and (p[0] - current[0])**2 + (p[1] - current[1])**2 > (nxt[0] - current[0])**2 + (nxt[1] - current[1])**2):\n"
            "                nxt = p\n"
            "        current = nxt\n"
            "        if current == start:\n"
            "            break\n"
            "    return hull\n",
            lambda low: bool(
                re.search(r"\bgift[- ]wrapping\b", low)
            )
            and "jarvis" not in low,
            (
                ((((0, 0), (1, 1), (2, 0)),), [(0, 0), (2, 0), (1, 1)]),
            ),
        ),
    ]
