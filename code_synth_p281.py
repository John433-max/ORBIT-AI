"""Cycle 584: unmatched textbook algorithms (push-relabel, SPFA, Borůvka MST,
linear recurrence, maximum clique / Bron-Kerbosch, chromatic number).

Natural-language probes for these still returned None after packs through p280.
Matchers are phrase-specific so dinic/max_flow, bellman_ford, kruskal,
berlekamp_massey stay put.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "push_relabel",
            "def push_relabel(n, edges, source, sink):\n"
            '    """Max flow via the highest-label push-relabel algorithm.\n'
            "\n"
            "    edges: list of (u, v, capacity). Returns the max-flow value.\n"
            "    Educational pure-Python implementation (Goldberg-Tarjan style).\n"
            '    """\n'
            "    if not (0 <= source < n and 0 <= sink < n) or source == sink:\n"
            "        return 0\n"
            "    graph = [[] for _ in range(n)]\n"
            "    for u, v, c in edges:\n"
            "        if c <= 0:\n"
            "            continue\n"
            "        graph[u].append([v, c, len(graph[v])])\n"
            "        graph[v].append([u, 0, len(graph[u]) - 1])\n"
            "    height = [0] * n\n"
            "    excess = [0] * n\n"
            "    height[source] = n\n"
            "    for i, edge in enumerate(graph[source]):\n"
            "        v, cap, rev = edge\n"
            "        if cap > 0:\n"
            "            edge[1] = 0\n"
            "            graph[v][rev][1] += cap\n"
            "            excess[v] += cap\n"
            "            excess[source] -= cap\n"
            "\n"
            "    def push(u, i):\n"
            "        v, cap, rev = graph[u][i]\n"
            "        delta = min(excess[u], cap)\n"
            "        if delta <= 0 or height[u] != height[v] + 1:\n"
            "            return False\n"
            "        graph[u][i][1] -= delta\n"
            "        graph[v][rev][1] += delta\n"
            "        excess[u] -= delta\n"
            "        excess[v] += delta\n"
            "        return True\n"
            "\n"
            "    def relabel(u):\n"
            "        mh = n * 2\n"
            "        for v, cap, _ in graph[u]:\n"
            "            if cap > 0:\n"
            "                mh = min(mh, height[v])\n"
            "        if mh < n * 2:\n"
            "            height[u] = mh + 1\n"
            "\n"
            "    active = [i for i in range(n) if i != source and i != sink and excess[i] > 0]\n"
            "    while active:\n"
            "        u = active.pop()\n"
            "        if excess[u] <= 0:\n"
            "            continue\n"
            "        pushed = False\n"
            "        for i in range(len(graph[u])):\n"
            "            if excess[u] <= 0:\n"
            "                break\n"
            "            if push(u, i):\n"
            "                pushed = True\n"
            "                v = graph[u][i][0]\n"
            "                if v != source and v != sink and excess[v] > 0 and v not in active:\n"
            "                    active.append(v)\n"
            "        if excess[u] > 0:\n"
            "            relabel(u)\n"
            "            active.append(u)\n"
            "    return excess[sink]\n",
            lambda low: bool(
                re.search(r"\bpush[- ]relabel\b|\bpreflow[- ]push\b", low)
            ),
            (
                ((4, [(0, 1, 10), (0, 2, 10), (1, 2, 1), (1, 3, 10), (2, 3, 10)], 0, 3), 20),
                ((2, [(0, 1, 7)], 0, 1), 7),
                ((3, [(0, 1, 1), (1, 2, 1)], 0, 2), 1),
            ),
        ),
        T(
            "spfa",
            "def spfa(n, edges, source):\n"
            '    """Shortest paths from source using SPFA (queue-based Bellman-Ford).\n'
            "\n"
            "    edges: list of (u, v, w). Returns distances (None = unreachable).\n"
            "    Detects negative cycles reachable from source (returns None list).\n"
            '    """\n'
            "    from collections import deque\n"
            "    INF = float('inf')\n"
            "    dist = [INF] * n\n"
            "    if not (0 <= source < n):\n"
            "        return [None] * n\n"
            "    dist[source] = 0\n"
            "    q = deque([source])\n"
            "    inq = [False] * n\n"
            "    inq[source] = True\n"
            "    count = [0] * n\n"
            "    while q:\n"
            "        u = q.popleft()\n"
            "        inq[u] = False\n"
            "        for a, b, w in edges:\n"
            "            if a != u:\n"
            "                continue\n"
            "            if 0 <= b < n and dist[u] < INF and dist[u] + w < dist[b]:\n"
            "                dist[b] = dist[u] + w\n"
            "                if not inq[b]:\n"
            "                    q.append(b)\n"
            "                    inq[b] = True\n"
            "                    count[b] += 1\n"
            "                    if count[b] > n:\n"
            "                        return [None] * n\n"
            "    return [None if d == INF else d for d in dist]\n",
            lambda low: bool(re.search(r"\bspfa\b", low)),
            (
                ((3, [(0, 1, 1), (1, 2, 2), (0, 2, 4)], 0), [0, 1, 3]),
                ((3, [(0, 1, 5), (1, 2, -2)], 0), [0, 5, 3]),
                ((2, [(1, 0, 1)], 0), [0, None]),
            ),
        ),
        T(
            "boruvka",
            "def boruvka(n, edges):\n"
            '    """Borůvka MST total weight.\n'
            "\n"
            "    edges: list of (u, v, w). Returns the MST weight (or partial forest weight).\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    parent = list(range(n))\n"
            "    rank = [0] * n\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra == rb:\n"
            "            return False\n"
            "        if rank[ra] < rank[rb]:\n"
            "            ra, rb = rb, ra\n"
            "        parent[rb] = ra\n"
            "        if rank[ra] == rank[rb]:\n"
            "            rank[ra] += 1\n"
            "        return True\n"
            "\n"
            "    total = 0\n"
            "    components = n\n"
            "    while components > 1:\n"
            "        cheapest = [-1] * n\n"
            "        for i, (u, v, w) in enumerate(edges):\n"
            "            if not (0 <= u < n and 0 <= v < n):\n"
            "                continue\n"
            "            ru, rv = find(u), find(v)\n"
            "            if ru == rv:\n"
            "                continue\n"
            "            if cheapest[ru] == -1 or edges[cheapest[ru]][2] > w:\n"
            "                cheapest[ru] = i\n"
            "            if cheapest[rv] == -1 or edges[cheapest[rv]][2] > w:\n"
            "                cheapest[rv] = i\n"
            "        merged = False\n"
            "        for i in cheapest:\n"
            "            if i == -1:\n"
            "                continue\n"
            "            u, v, w = edges[i]\n"
            "            if union(u, v):\n"
            "                total += w\n"
            "                components -= 1\n"
            "                merged = True\n"
            "        if not merged:\n"
            "            break\n"
            "    return total\n",
            lambda low: bool(re.search(r"\bbor[uů]vka\b|\bboruvka\b", low)),
            (
                ((4, [(0, 1, 1), (1, 2, 2), (0, 2, 4), (2, 3, 3)]), 6),
                ((3, [(0, 1, 5), (1, 2, 1), (0, 2, 2)]), 3),
                ((2, [(0, 1, 9)]), 9),
            ),
        ),
        T(
            "linear_recurrence",
            "def linear_recurrence(coeffs, init, n):\n"
            '    """Compute the n-th term of a linear recurrence.\n'
            "\n"
            "    a[k] = sum(coeffs[i] * a[k-1-i] for i in range(len(coeffs)))\n"
            "    for k >= len(init). init holds a[0..order-1]. Returns a[n].\n"
            "    Educational O(order * n) implementation.\n"
            '    """\n'
            "    order = len(coeffs)\n"
            "    if order == 0:\n"
            "        return 0 if n >= 0 else None\n"
            "    if n < 0:\n"
            "        return None\n"
            "    if n < len(init):\n"
            "        return init[n]\n"
            "    seq = list(init[:order])\n"
            "    while len(seq) <= n:\n"
            "        nxt = 0\n"
            "        for i, c in enumerate(coeffs):\n"
            "            nxt += c * seq[-(i + 1)]\n"
            "        seq.append(nxt)\n"
            "    return seq[n]\n",
            lambda low: bool(
                re.search(
                    r"\blinear[- ]recurrence\b|\bnext term.*recurrence\b|\brecurrence sequence\b",
                    low,
                )
            ),
            (
                (([1, 1], [0, 1], 10), 55),  # Fibonacci-like: F10=55 if F0=0,F1=1
                (([1, 1], [1, 1], 5), 8),
                (([2], [3], 4), 48),  # a[k]=2*a[k-1], a0=3 → 3,6,12,24,48
            ),
        ),
        T(
            "maximum_clique",
            "def maximum_clique(n, edges):\n"
            '    """Size of a maximum clique in an undirected graph.\n'
            "\n"
            "    edges: list of (u, v) undirected edges. Uses Bron-Kerbosch with pivoting.\n"
            "    Educational pure-Python; exponential — suitable for small n.\n"
            '    """\n'
            "    adj = [set() for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        if 0 <= u < n and 0 <= v < n and u != v:\n"
            "            adj[u].add(v)\n"
            "            adj[v].add(u)\n"
            "    best = [0]\n"
            "\n"
            "    def bronk(r, p, x):\n"
            "        if not p and not x:\n"
            "            best[0] = max(best[0], len(r))\n"
            "            return\n"
            "        u = next(iter(p | x), None)\n"
            "        pivot_nbrs = adj[u] if u is not None else set()\n"
            "        for v in list(p - pivot_nbrs):\n"
            "            bronk(r | {v}, p & adj[v], x & adj[v])\n"
            "            p = p - {v}\n"
            "            x = x | {v}\n"
            "\n"
            "    bronk(set(), set(range(n)), set())\n"
            "    return best[0]\n",
            lambda low: bool(
                re.search(r"\bmaximum[- ]clique\b|\bbron[- ]kerbosch\b|\bmax clique\b", low)
            ),
            (
                ((4, [(0, 1), (1, 2), (0, 2), (2, 3)]), 3),
                ((3, [(0, 1), (1, 2), (0, 2)]), 3),
                ((3, [(0, 1)]), 2),
                ((2, []), 1),
            ),
        ),
        T(
            "chromatic_number",
            "def chromatic_number(n, edges):\n"
            '    """Chromatic number of an undirected graph (minimum colors).\n'
            "\n"
            "    edges: list of (u, v). Backtracking with greedy upper bound.\n"
            "    Educational pure-Python; exponential — suitable for small n.\n"
            '    """\n'
            "    adj = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        if 0 <= u < n and 0 <= v < n and u != v:\n"
            "            adj[u].append(v)\n"
            "            adj[v].append(u)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    color = [-1] * n\n"
            "\n"
            "    def ok(v, c):\n"
            "        for u in adj[v]:\n"
            "            if color[u] == c:\n"
            "                return False\n"
            "        return True\n"
            "\n"
            "    def solve(v, k):\n"
            "        if v == n:\n"
            "            return True\n"
            "        for c in range(k):\n"
            "            if ok(v, c):\n"
            "                color[v] = c\n"
            "                if solve(v + 1, k):\n"
            "                    return True\n"
            "                color[v] = -1\n"
            "        return False\n"
            "\n"
            "    for k in range(1, n + 1):\n"
            "        color[:] = [-1] * n\n"
            "        if solve(0, k):\n"
            "            return k\n"
            "    return n\n",
            lambda low: bool(
                re.search(r"\bchromatic[- ]number\b|\bgraph[- ]coloring\b|\bminimum colors?\b", low)
            ),
            (
                ((3, [(0, 1), (1, 2), (0, 2)]), 3),  # triangle
                ((4, [(0, 1), (1, 2), (2, 3), (3, 0)]), 2),  # even cycle
                ((2, [(0, 1)]), 2),
                ((1, []), 1),
            ),
        ),
    ]
