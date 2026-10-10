"""Cycle 548: Kruskal / Prim MST. Loaded first so 'spanning tree' beats list_span."""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "kruskal",
            "def kruskal(n, edges):\n"
            '    """Kruskal MST weight. edges is a list of (u, v, w). n is the vertex count."""\n'
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
            "    used = 0\n"
            "    for u, v, w in sorted(edges, key=lambda e: e[2]):\n"
            "        if 0 <= u < n and 0 <= v < n and union(u, v):\n"
            "            total += w\n"
            "            used += 1\n"
            "            if used == n - 1:\n"
            "                break\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bkruskal(?:'s)?(?: algorithm)?\b|"
                    r"\bminimum spanning tree\b|"
                    r"\bminimum spanning-tree\b|"
                    r"\bmst\b|"
                    r"\bspanning tree\b",
                    low,
                )
            )
            and "prim" not in low
            and "list" not in low
            and "statistical" not in low
            and "cidr" not in low,
            (
                ((4, [(0, 1, 1), (1, 2, 2), (0, 2, 4), (2, 3, 3)]), 6),
                ((3, [(0, 1, 5), (1, 2, 1), (0, 2, 2)]), 3),
            ),
        ),
        T(
            "prim",
            "def prim(n, edges):\n"
            '    """Prim MST weight. edges is a list of (u, v, w). n is the vertex count."""\n'
            "    import heapq\n"
            "    adj = [[] for _ in range(n)]\n"
            "    for u, v, w in edges:\n"
            "        if 0 <= u < n and 0 <= v < n:\n"
            "            adj[u].append((w, v))\n"
            "            adj[v].append((w, u))\n"
            "    seen = [False] * n\n"
            "    heap = [(0, 0)]\n"
            "    total = 0\n"
            "    taken = 0\n"
            "    while heap and taken < n:\n"
            "        w, node = heapq.heappop(heap)\n"
            "        if seen[node]:\n"
            "            continue\n"
            "        seen[node] = True\n"
            "        total += w\n"
            "        taken += 1\n"
            "        for nw, nxt in adj[node]:\n"
            "            if not seen[nxt]:\n"
            "                heapq.heappush(heap, (nw, nxt))\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bprim(?:'s)?(?: algorithm)?\b|"
                    r"\bprims algorithm\b",
                    low,
                )
            )
            and "number" not in low
            and "prime" not in low
            and "primitive" not in low,
            (
                ((4, [(0, 1, 1), (1, 2, 2), (0, 2, 4), (2, 3, 3)]), 6),
                ((3, [(0, 1, 5), (1, 2, 1), (0, 2, 2)]), 3),
            ),
        ),
    ]
