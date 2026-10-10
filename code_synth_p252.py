"""Cycle 554: Edmonds blossom, Mo's, sqrt decomposition, Euler tour, Dinic.

Fills remaining draft-stub gaps from agent routing probes.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "dinic_max_flow",
            "def dinic(n, edges, source, sink):\n"
            '    """Max flow with Dinic blocking flows.\n'
            '    edges: list of (u, v, capacity). Returns max flow value."""\n'
            "    graph = [[] for _ in range(n)]\n"
            "    for u, v, c in edges:\n"
            "        graph[u].append([v, c, len(graph[v])])\n"
            "        graph[v].append([u, 0, len(graph[u]) - 1])\n"
            "\n"
            "    def bfs(level):\n"
            "        from collections import deque\n"
            "        q = deque([source])\n"
            "        level[source] = 0\n"
            "        while q:\n"
            "            u = q.popleft()\n"
            "            for v, cap, _ in graph[u]:\n"
            "                if cap > 0 and level[v] < 0:\n"
            "                    level[v] = level[u] + 1\n"
            "                    q.append(v)\n"
            "        return level[sink] >= 0\n"
            "\n"
            "    def dfs(u, pushed, level, it):\n"
            "        if u == sink or pushed == 0:\n"
            "            return pushed\n"
            "        while it[u] < len(graph[u]):\n"
            "            v, cap, rev = graph[u][it[u]]\n"
            "            if cap > 0 and level[v] == level[u] + 1:\n"
            "                tr = dfs(v, min(pushed, cap), level, it)\n"
            "                if tr:\n"
            "                    graph[u][it[u]][1] -= tr\n"
            "                    graph[v][rev][1] += tr\n"
            "                    return tr\n"
            "            it[u] += 1\n"
            "        return 0\n"
            "\n"
            "    flow = 0\n"
            "    while True:\n"
            "        level = [-1] * n\n"
            "        if not bfs(level):\n"
            "            break\n"
            "        it = [0] * n\n"
            "        while True:\n"
            "            pushed = dfs(source, 10 ** 18, level, it)\n"
            "            if not pushed:\n"
            "                break\n"
            "            flow += pushed\n"
            "    return flow\n",
            lambda low: bool(
                re.search(
                    r"\bdinic(?:'s)?(?: algorithm)?\b|"
                    r"\bdinic max(?:imum)?[- ]?flow\b|"
                    r"\bblocking[- ]?flow\b",
                    low,
                )
            ),
            (
                ((4, [(0, 1, 3), (0, 2, 2), (1, 2, 1), (1, 3, 2), (2, 3, 4)], 0, 3), 5),
                ((2, [(0, 1, 7)], 0, 1), 7),
                ((3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)], 0, 2), 2),
            ),
        ),
        T(
            "edmonds_blossom",
            "def maximum_matching(n, edges):\n"
            '    """Maximum matching in general graphs (Edmonds blossom / Gabow style).\n'
            '    edges: undirected (u, v). Returns mate array (-1 if unmatched).\n'
            '    Correct for small graphs; uses blossom contraction."""\n'
            "    mate = [-1] * n\n"
            "    g = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        g[u].append(v)\n"
            "        g[v].append(u)\n"
            "\n"
            "    def get_aug_path(root):\n"
            "        from collections import deque\n"
            "        parent = [-1] * n\n"
            "        base = list(range(n))\n"
            "        used = [0] * n\n"
            "        q = deque([root])\n"
            "        used[root] = 1\n"
            "\n"
            "        def lca(a, b):\n"
            "            vis = [False] * n\n"
            "            while True:\n"
            "                a = base[a]\n"
            "                vis[a] = True\n"
            "                if mate[a] < 0:\n"
            "                    break\n"
            "                a = parent[mate[a]]\n"
            "            while True:\n"
            "                b = base[b]\n"
            "                if vis[b]:\n"
            "                    return b\n"
            "                b = parent[mate[b]]\n"
            "\n"
            "        def mark_blossom(v, b, child):\n"
            "            while base[v] != b:\n"
            "                bl, br = base[v], base[mate[v]]\n"
            "                used[bl] = used[br] = 1\n"
            "                parent[v] = child\n"
            "                child = mate[v]\n"
            "                v = parent[mate[v]]\n"
            "\n"
            "        while q:\n"
            "            v = q.popleft()\n"
            "            for to in g[v]:\n"
            "                if base[v] == base[to] or mate[v] == to:\n"
            "                    continue\n"
            "                if to == root or (mate[to] >= 0 and parent[mate[to]] >= 0):\n"
            "                    cur = lca(v, to)\n"
            "                    mark_blossom(v, cur, to)\n"
            "                    mark_blossom(to, cur, v)\n"
            "                    for i in range(n):\n"
            "                        if used[base[i]]:\n"
            "                            base[i] = cur\n"
            "                            if not used[i]:\n"
            "                                used[i] = 1\n"
            "                                q.append(i)\n"
            "                elif parent[to] < 0:\n"
            "                    parent[to] = v\n"
            "                    if mate[to] < 0:\n"
            "                        # reconstruct path and augment\n"
            "                        path = []\n"
            "                        x = to\n"
            "                        while x >= 0:\n"
            "                            path.append(x)\n"
            "                            p = parent[x]\n"
            "                            if p < 0:\n"
            "                                break\n"
            "                            path.append(p)\n"
            "                            x = mate[p]\n"
            "                        for i in range(0, len(path) - 1, 2):\n"
            "                            a, b = path[i], path[i + 1]\n"
            "                            mate[a] = b\n"
            "                            mate[b] = a\n"
            "                        return True\n"
            "                    used[mate[to]] = 1\n"
            "                    q.append(mate[to])\n"
            "        return False\n"
            "\n"
            "    for i in range(n):\n"
            "        if mate[i] < 0:\n"
            "            get_aug_path(i)\n"
            "    return mate\n",
            lambda low: bool(
                re.search(
                    r"\bblossom(?: algorithm)?\b|"
                    r"\bedmonds(?:'s)?(?: matching| blossom)?\b|"
                    r"\bmaximum matching(?: in)?(?: a)? general(?: graph)?\b|"
                    r"\bgeneral graph matching\b|"
                    r"\bnon[- ]?bipartite matching\b",
                    low,
                )
            )
            and "bipartite" not in low
            and "hungarian" not in low,
            (
                ((4, [(0, 1), (1, 2), (2, 3)]), [1, 0, 3, 2]),
                ((2, [(0, 1)]), [1, 0]),
                ((3, [(0, 1)]), [1, 0, -1]),
            ),
        ),
        T(
            "mos_algorithm",
            "def mos_algorithm(arr, queries):\n"
            '    """Offline range distinct-count queries with Mo\'s algorithm.\n'
            '    queries: list of (L, R) inclusive 0-based. Returns distinct counts."""\n'
            "    import math\n"
            "    n = len(arr)\n"
            "    qn = len(queries)\n"
            "    if qn == 0:\n"
            "        return []\n"
            "    bsize = max(1, int(n ** 0.5) or 1)\n"
            "    order = sorted(\n"
            "        range(qn),\n"
            "        key=lambda i: (\n"
            "            queries[i][0] // bsize,\n"
            "            queries[i][1] if (queries[i][0] // bsize) % 2 == 0 else -queries[i][1],\n"
            "        ),\n"
            "    )\n"
            "    freq = {}\n"
            "    distinct = [0]\n"
            "\n"
            "    def add(x):\n"
            "        freq[x] = freq.get(x, 0) + 1\n"
            "        if freq[x] == 1:\n"
            "            distinct[0] += 1\n"
            "\n"
            "    def remove(x):\n"
            "        freq[x] -= 1\n"
            "        if freq[x] == 0:\n"
            "            distinct[0] -= 1\n"
            "            del freq[x]\n"
            "\n"
            "    ans = [0] * qn\n"
            "    cur_l, cur_r = 0, -1\n"
            "    for qi in order:\n"
            "        L, R = queries[qi]\n"
            "        while cur_l > L:\n"
            "            cur_l -= 1\n"
            "            add(arr[cur_l])\n"
            "        while cur_r < R:\n"
            "            cur_r += 1\n"
            "            add(arr[cur_r])\n"
            "        while cur_l < L:\n"
            "            remove(arr[cur_l])\n"
            "            cur_l += 1\n"
            "        while cur_r > R:\n"
            "            remove(arr[cur_r])\n"
            "            cur_r -= 1\n"
            "        ans[qi] = distinct[0]\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bmo'?s(?: algorithm)?\b|"
                    r"\bmo algorithm\b",
                    low,
                )
            ),
            (
                (([1, 2, 1, 3, 2], [(0, 2), (1, 4), (0, 4)]), [2, 3, 3]),
                (([5, 5, 5], [(0, 0), (0, 2)]), [1, 1]),
                (([1, 2, 3], []), []),
            ),
        ),
        T(
            "sqrt_decomposition",
            "def sqrt_decomposition(arr, ops):\n"
            '    """Range sum + point update via sqrt decomposition.\n'
            '    ops: (\"sum\", L, R) or (\"update\", idx, val). Returns sum results."""\n'
            "    n = len(arr)\n"
            "    a = list(arr)\n"
            "    bsize = max(1, int(n ** 0.5) or 1)\n"
            "    nb = (n + bsize - 1) // bsize\n"
            "    blocks = [0] * nb\n"
            "    for i, v in enumerate(a):\n"
            "        blocks[i // bsize] += v\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        if op[0] == 'sum':\n"
            "            L, R = op[1], op[2]\n"
            "            s = 0\n"
            "            while L <= R and L % bsize:\n"
            "                s += a[L]\n"
            "                L += 1\n"
            "            while L + bsize - 1 <= R:\n"
            "                s += blocks[L // bsize]\n"
            "                L += bsize\n"
            "            while L <= R:\n"
            "                s += a[L]\n"
            "                L += 1\n"
            "            out.append(s)\n"
            "        else:\n"
            "            idx, val = op[1], op[2]\n"
            "            blocks[idx // bsize] += val - a[idx]\n"
            "            a[idx] = val\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsqrt[- ]?decomposition\b|"
                    r"\bsquare[- ]?root decomposition\b|"
                    r"\bblock(?:s)? decomposition\b",
                    low,
                )
            )
            and "mo" not in low,
            (
                (([1, 2, 3, 4, 5], [('sum', 0, 4), ('update', 2, 10), ('sum', 0, 4)]), [15, 22]),
                (([5], [('sum', 0, 0)]), [5]),
                (([1, 2, 3], [('sum', 1, 1)]), [2]),
            ),
        ),
        T(
            "euler_tour",
            "def euler_tour(n, edges, root=0):\n"
            '    """Euler tour of a tree: entry/exit times and flat tour.\n'
            '    edges: undirected tree edges. Returns (tin, tout, tour)."""\n'
            "    graph = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        graph[u].append(v)\n"
            "        graph[v].append(u)\n"
            "    tin = [-1] * n\n"
            "    tout = [-1] * n\n"
            "    tour = []\n"
            "    timer = [0]\n"
            "\n"
            "    def dfs(u, p):\n"
            "        tin[u] = timer[0]\n"
            "        timer[0] += 1\n"
            "        tour.append(u)\n"
            "        for v in graph[u]:\n"
            "            if v != p:\n"
            "                dfs(v, u)\n"
            "        tout[u] = timer[0] - 1\n"
            "\n"
            "    if n:\n"
            "        dfs(root, -1)\n"
            "    return tin, tout, tour\n",
            lambda low: bool(
                re.search(
                    r"\beuler[- ]?tour(?: tree)?\b|"
                    r"\beuler tour technique\b|"
                    r"\btree euler tour\b|"
                    r"\bin[- ]?out time(?:s)?(?: on )?tree\b",
                    low,
                )
            ),
            (
                ((4, [(0, 1), (0, 2), (1, 3)], 0), ([0, 1, 3, 2], [3, 2, 3, 2], [0, 1, 3, 2])),
                ((1, [], 0), ([0], [0], [0])),
                ((3, [(0, 1), (1, 2)], 0), ([0, 1, 2], [2, 2, 2], [0, 1, 2])),
            ),
        ),
    ]
