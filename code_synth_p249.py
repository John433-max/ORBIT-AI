"""Cycle 552: Hopcroft-Karp maximum bipartite matching + suffix-array construction.

Loaded first so classic algorithm phrases beat draft stubs and ensure_suffix.
"""
from __future__ import annotations

import re
from collections import deque

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "hopcroft_karp",
            "def hopcroft_karp(graph):\n"
            '    """Maximum bipartite matching via Hopcroft-Karp. graph: left -> list of right.\n'
            '    Returns (size, dict left->right). O(E * sqrt(V))."""\n'
            "    from collections import deque\n"
            "    lefts = list(graph.keys())\n"
            "    pair_u = {u: None for u in lefts}\n"
            "    pair_v = {}\n"
            "    for nbrs in graph.values():\n"
            "        for v in nbrs:\n"
            "            pair_v.setdefault(v, None)\n"
            "    dist = {}\n"
            "    INF = float('inf')\n"
            "\n"
            "    def bfs():\n"
            "        q = deque()\n"
            "        for u in lefts:\n"
            "            if pair_u[u] is None:\n"
            "                dist[u] = 0\n"
            "                q.append(u)\n"
            "            else:\n"
            "                dist[u] = INF\n"
            "        found = False\n"
            "        while q:\n"
            "            u = q.popleft()\n"
            "            if dist[u] >= INF:\n"
            "                continue\n"
            "            for v in graph.get(u, ()):\n"
            "                nxt = pair_v.get(v)\n"
            "                if nxt is None:\n"
            "                    found = True\n"
            "                elif dist.get(nxt, INF) == INF:\n"
            "                    dist[nxt] = dist[u] + 1\n"
            "                    q.append(nxt)\n"
            "        return found\n"
            "\n"
            "    def dfs(u):\n"
            "        for v in graph.get(u, ()):\n"
            "            nxt = pair_v.get(v)\n"
            "            if nxt is None or (dist.get(nxt, INF) == dist.get(u, INF) + 1 and dfs(nxt)):\n"
            "                pair_u[u] = v\n"
            "                pair_v[v] = u\n"
            "                return True\n"
            "        dist[u] = INF\n"
            "        return False\n"
            "\n"
            "    matching = 0\n"
            "    while bfs():\n"
            "        for u in lefts:\n"
            "            if pair_u[u] is None and dfs(u):\n"
            "                matching += 1\n"
            "    return matching, {u: v for u, v in pair_u.items() if v is not None}\n",
            lambda low: bool(
                re.search(
                    r"\bhopcroft[- ]?karp\b|"
                    r"\bmaximum bipartite matching\b|"
                    r"\bbipartite matching\b|"
                    r"\bmaximum matching in (?:a )?bipartite\b",
                    low,
                )
            ),
            (
                (
                    ({1: ["a", "b"], 2: ["a"], 3: ["b", "c"]},),
                    (3, {1: "b", 2: "a", 3: "c"}),
                ),
                (
                    ({"L0": [0, 1], "L1": [1, 2], "L2": [0]},),
                    (3, {"L0": 1, "L1": 2, "L2": 0}),
                ),
            ),
        ),
        T(
            "build_suffix_array",
            "def build_suffix_array(s):\n"
            '    """Suffix array: starting indices of sorted suffixes of s (naive sort)."""\n'
            "    s = str(s)\n"
            "    n = len(s)\n"
            "    return sorted(range(n), key=lambda i: s[i:])\n",
            lambda low: bool(
                re.search(
                    r"\bsuffix[- ]?array\b|"
                    r"\bbuild (?:a )?sa\b|"
                    r"\bconstruct suffix array\b|"
                    r"\bsuffix array construction\b",
                    low,
                )
            )
            and "ensure" not in low
            and "append" not in low,
            (
                (("banana",), [5, 3, 1, 0, 4, 2]),
                (("mississippi",), [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]),
            ),
        ),
    ]
