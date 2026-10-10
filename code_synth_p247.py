"""Cycle 550: KMP, segment-tree range sum, Edmonds-Karp, Kosaraju, articulation points, Z-algorithm.

Loaded first so specific phrases beat generic string-matching and component counters.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "kmp_search",
            "def kmp_search(text, pattern):\n"
            '    """First index of pattern in text via Knuth-Morris-Pratt, or -1."""\n'
            "    if pattern == \"\":\n"
            "        return 0\n"
            "    if text == \"\":\n"
            "        return -1\n"
            "    pi = [0] * len(pattern)\n"
            "    k = 0\n"
            "    for i in range(1, len(pattern)):\n"
            "        while k and pattern[k] != pattern[i]:\n"
            "            k = pi[k - 1]\n"
            "        if pattern[k] == pattern[i]:\n"
            "            k += 1\n"
            "        pi[i] = k\n"
            "    q = 0\n"
            "    for i, ch in enumerate(text):\n"
            "        while q and pattern[q] != ch:\n"
            "            q = pi[q - 1]\n"
            "        if pattern[q] == ch:\n"
            "            q += 1\n"
            "        if q == len(pattern):\n"
            "            return i - q + 1\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bkmp\b|\bknuth[- ]morris[- ]pratt\b|\bmorris[- ]pratt\b",
                    low,
                )
            )
            and "tree" not in low,
            (
                (("ababcababa", "ababa"), 5),
                (("hello", "ll"), 2),
                (("abc", "d"), -1),
                (("", "a"), -1),
            ),
        ),
        T(
            "segment_tree_sum",
            "def segment_tree_sum(nums, ops):\n"
            '    """Range-sum segment tree. ops are (\'sum\', l, r) or (\'set\', i, v)."""\n'
            "    n = len(nums)\n"
            "    if n == 0:\n"
            "        return [0 for op in ops if op[0] == \"sum\"]\n"
            "    tree = [0] * (4 * n)\n"
            "\n"
            "    def build(node, start, end):\n"
            "        if start == end:\n"
            "            tree[node] = nums[start]\n"
            "            return\n"
            "        mid = (start + end) // 2\n"
            "        build(2 * node, start, mid)\n"
            "        build(2 * node + 1, mid + 1, end)\n"
            "        tree[node] = tree[2 * node] + tree[2 * node + 1]\n"
            "\n"
            "    def update(node, start, end, idx, val):\n"
            "        if start == end:\n"
            "            tree[node] = val\n"
            "            nums[idx] = val\n"
            "            return\n"
            "        mid = (start + end) // 2\n"
            "        if idx <= mid:\n"
            "            update(2 * node, start, mid, idx, val)\n"
            "        else:\n"
            "            update(2 * node + 1, mid + 1, end, idx, val)\n"
            "        tree[node] = tree[2 * node] + tree[2 * node + 1]\n"
            "\n"
            "    def query(node, start, end, l, r):\n"
            "        if r < start or end < l:\n"
            "            return 0\n"
            "        if l <= start and end <= r:\n"
            "            return tree[node]\n"
            "        mid = (start + end) // 2\n"
            "        return query(2 * node, start, mid, l, r) + query(2 * node + 1, mid + 1, end, l, r)\n"
            "\n"
            "    build(1, 0, n - 1)\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        if op[0] == \"sum\":\n"
            "            out.append(query(1, 0, n - 1, op[1], op[2]))\n"
            "        elif op[0] == \"set\":\n"
            "            update(1, 0, n - 1, op[1], op[2])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsegment[- ]tree\b|\brange[- ]sum segment\b|\bsegment tree range sum\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4], [("sum", 0, 2), ("set", 1, 10), ("sum", 0, 2)]), [6, 14]),
                (([5], [("sum", 0, 0)]), [5]),
                (([], []), []),
            ),
        ),
        T(
            "max_flow",
            "def max_flow(n, edges, source, sink):\n"
            '    """Edmonds-Karp max flow. edges is a list of (u, v, cap)."""\n'
            "    from collections import defaultdict, deque\n"
            "    if source == sink:\n"
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
            "        bottle = float(\"inf\")\n"
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
                    r"\bmax(?:imum)?[- ]flow\b|\bedmonds[- ]karp\b|\bford[- ]fulkerson\b",
                    low,
                )
            )
            and "min cut" not in low
            and "min-cut" not in low,
            (
                ((4, [(0, 1, 10), (0, 2, 10), (1, 2, 1), (1, 3, 10), (2, 3, 10)], 0, 3), 20),
                ((2, [(0, 1, 7)], 0, 1), 7),
                ((3, [(0, 1, 1), (1, 2, 1)], 0, 2), 1),
            ),
        ),
        T(
            "kosaraju_scc",
            "def kosaraju_scc(n, edges):\n"
            '    """Number of strongly connected components (Kosaraju). edges are directed (u, v)."""\n'
            "    g = [[] for _ in range(n)]\n"
            "    gr = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        if 0 <= u < n and 0 <= v < n:\n"
            "            g[u].append(v)\n"
            "            gr[v].append(u)\n"
            "    order = []\n"
            "    seen = [False] * n\n"
            "\n"
            "    def dfs1(u):\n"
            "        seen[u] = True\n"
            "        for v in g[u]:\n"
            "            if not seen[v]:\n"
            "                dfs1(v)\n"
            "        order.append(u)\n"
            "\n"
            "    for i in range(n):\n"
            "        if not seen[i]:\n"
            "            dfs1(i)\n"
            "    seen = [False] * n\n"
            "\n"
            "    def dfs2(u):\n"
            "        seen[u] = True\n"
            "        for v in gr[u]:\n"
            "            if not seen[v]:\n"
            "                dfs2(v)\n"
            "\n"
            "    count = 0\n"
            "    for u in reversed(order):\n"
            "        if not seen[u]:\n"
            "            dfs2(u)\n"
            "            count += 1\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\bkosaraju\b|\bstrongly[- ]connected(?: components?)?\b|\bsccs?\b",
                    low,
                )
            )
            and "weakly" not in low,
            (
                ((5, [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]), 3),
                ((3, [(0, 1), (1, 0), (1, 2)]), 2),
                ((1, []), 1),
            ),
        ),
        T(
            "articulation_points",
            "def articulation_points(n, edges):\n"
            '    """Sorted articulation points (cut vertices) of an undirected graph."""\n'
            "    g = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        if u == v or not (0 <= u < n and 0 <= v < n):\n"
            "            continue\n"
            "        g[u].append(v)\n"
            "        g[v].append(u)\n"
            "    for i in range(n):\n"
            "        g[i] = list(dict.fromkeys(g[i]))\n"
            "    disc = [-1] * n\n"
            "    low = [-1] * n\n"
            "    parent = [-1] * n\n"
            "    ap = [False] * n\n"
            "    timer = [0]\n"
            "\n"
            "    def dfs(u):\n"
            "        children = 0\n"
            "        disc[u] = low[u] = timer[0]\n"
            "        timer[0] += 1\n"
            "        for v in g[u]:\n"
            "            if disc[v] == -1:\n"
            "                parent[v] = u\n"
            "                children += 1\n"
            "                dfs(v)\n"
            "                low[u] = min(low[u], low[v])\n"
            "                if parent[u] == -1 and children > 1:\n"
            "                    ap[u] = True\n"
            "                if parent[u] != -1 and low[v] >= disc[u]:\n"
            "                    ap[u] = True\n"
            "            elif v != parent[u]:\n"
            "                low[u] = min(low[u], disc[v])\n"
            "\n"
            "    for i in range(n):\n"
            "        if disc[i] == -1:\n"
            "            dfs(i)\n"
            "    return [i for i in range(n) if ap[i]]\n",
            lambda low: bool(
                re.search(
                    r"\barticulation[- ]points?\b|\bcut[- ]vertices\b|\bcut[- ]vertex\b",
                    low,
                )
            ),
            (
                ((5, [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]), [1, 3]),
                ((4, [(0, 1), (1, 2), (2, 3)]), [1, 2]),
                ((3, [(0, 1), (1, 2), (2, 0)]), []),
            ),
        ),
        T(
            "z_algorithm",
            "def z_algorithm(s):\n"
            '    """Z-array of s. Z[0] is 0 by convention."""\n'
            "    n = len(s)\n"
            "    z = [0] * n\n"
            "    l = r = 0\n"
            "    for i in range(1, n):\n"
            "        if i < r:\n"
            "            z[i] = min(r - i, z[i - l])\n"
            "        while i + z[i] < n and s[z[i]] == s[i + z[i]]:\n"
            "            z[i] += 1\n"
            "        if i + z[i] > r:\n"
            "            l, r = i, i + z[i]\n"
            "    return z\n",
            lambda low: bool(
                re.search(
                    r"\bz[- ]algorithm\b|\bz[- ]array\b|\bz algorithm\b",
                    low,
                )
            ),
            (
                (("aaaa",), [0, 3, 2, 1]),
                (("ababab",), [0, 0, 4, 0, 2, 0]),
                (("abc",), [0, 0, 0]),
            ),
        ),
    ]
