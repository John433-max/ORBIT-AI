"""Cycle 556: Boyer-Moore/Horspool, Kahn topo, binary-lifting LCA,
closest pair, Huffman cost, subset sum.

Fills remaining draft-stub gaps for classic CS algorithms.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "boyer_moore",
            "def boyer_moore(text, pattern):\n"
            '    """Horspool variant of Boyer-Moore. First index of pattern in text, or -1."""\n'
            "    text, pattern = str(text), str(pattern)\n"
            "    if not pattern:\n"
            "        return 0\n"
            "    n, m = len(text), len(pattern)\n"
            "    if m > n:\n"
            "        return -1\n"
            "    shift = {c: m for c in set(text)}\n"
            "    for i in range(m - 1):\n"
            "        shift[pattern[i]] = m - 1 - i\n"
            "    i = 0\n"
            "    while i <= n - m:\n"
            "        j = m - 1\n"
            "        while j >= 0 and text[i + j] == pattern[j]:\n"
            "            j -= 1\n"
            "        if j < 0:\n"
            "            return i\n"
            "        i += shift.get(text[i + m - 1], m)\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"\bboyer[- ]?moore\b", low)
                and ("string" in low or "search" in low or "pattern" in low or "horspool" in low or "substring" in low)
                and "majority" not in low
            ),
            (
                (("abcde", "cde"), 2),
                (("hello world", "xyz"), -1),
                (("aaaa", "aa"), 0),
            ),
        ),
        T(
            "kahn_topo",
            "def kahn_topo(n, edges):\n"
            '    """Kahn topological order. edges are (u, v) for u -> v. [] if a cycle."""\n'
            "    from collections import defaultdict, deque\n"
            "    n = int(n)\n"
            "    indeg = [0] * n\n"
            "    adj = defaultdict(list)\n"
            "    for u, v in edges:\n"
            "        adj[int(u)].append(int(v))\n"
            "        indeg[int(v)] += 1\n"
            "    q = deque(i for i in range(n) if indeg[i] == 0)\n"
            "    order = []\n"
            "    while q:\n"
            "        u = q.popleft()\n"
            "        order.append(u)\n"
            "        for v in adj[u]:\n"
            "            indeg[v] -= 1\n"
            "            if indeg[v] == 0:\n"
            "                q.append(v)\n"
            "    return order if len(order) == n else []\n",
            lambda low: bool(re.search(r"\bkahn(?:'s|s)?\b", low)) and "majority" not in low,
            (
                ((3, [(0, 1), (1, 2)]), [0, 1, 2]),
                ((2, [(0, 1), (1, 0)]), []),
                ((1, []), [0]),
            ),
        ),
        T(
            "binary_lifting_lca",
            "def binary_lifting_lca(parent, depth, u, v):\n"
            '    """LCA with binary lifting. parent[root]=-1, depth[root]=0."""\n'
            "    parent = [int(x) for x in parent]\n"
            "    depth = [int(x) for x in depth]\n"
            "    u, v = int(u), int(v)\n"
            "    n = len(parent)\n"
            "    if n == 0:\n"
            "        return -1\n"
            "    log = 1\n"
            "    while (1 << log) <= n:\n"
            "        log += 1\n"
            "    up = [[-1] * n for _ in range(log)]\n"
            "    for i in range(n):\n"
            "        up[0][i] = parent[i]\n"
            "    for k in range(1, log):\n"
            "        for i in range(n):\n"
            "            if up[k - 1][i] != -1:\n"
            "                up[k][i] = up[k - 1][up[k - 1][i]]\n"
            "    if depth[u] < depth[v]:\n"
            "        u, v = v, u\n"
            "    diff = depth[u] - depth[v]\n"
            "    for k in range(log):\n"
            "        if diff & (1 << k):\n"
            "            u = up[k][u]\n"
            "    if u == v:\n"
            "        return u\n"
            "    for k in range(log - 1, -1, -1):\n"
            "        if up[k][u] != -1 and up[k][u] != up[k][v]:\n"
            "            u = up[k][u]\n"
            "            v = up[k][v]\n"
            "    return up[0][u]\n",
            lambda low: bool(
                re.search(r"\bbinary[- ]lifting\b|\bjump[- ]pointers?\b", low)
                or (re.search(r"\blca\b", low) and "binary" in low)
            ),
            (
                (([-1, 0, 0, 1, 1], [0, 1, 1, 2, 2], 3, 4), 1),
                (([-1, 0, 0, 1, 1], [0, 1, 1, 2, 2], 3, 1), 1),
                (([-1, 0], [0, 1], 1, 0), 0),
            ),
        ),
        T(
            "closest_pair",
            "def closest_pair(points):\n"
            '    """Divide-and-conquer closest-pair squared distance."""\n'
            "    pts = sorted((float(x), float(y)) for x, y in points)\n"
            "    if len(pts) < 2:\n"
            "        return float('inf')\n"
            "    def d2(a, b):\n"
            "        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2\n"
            "    def rec(ps):\n"
            "        n = len(ps)\n"
            "        if n <= 3:\n"
            "            best = float('inf')\n"
            "            for i in range(n):\n"
            "                for j in range(i + 1, n):\n"
            "                    best = min(best, d2(ps[i], ps[j]))\n"
            "            return best\n"
            "        mid = n // 2\n"
            "        midx = ps[mid][0]\n"
            "        d = min(rec(ps[:mid]), rec(ps[mid:]))\n"
            "        strip = [p for p in ps if (p[0] - midx) ** 2 < d]\n"
            "        strip.sort(key=lambda p: p[1])\n"
            "        for i in range(len(strip)):\n"
            "            for j in range(i + 1, min(i + 8, len(strip))):\n"
            "                if (strip[j][1] - strip[i][1]) ** 2 >= d:\n"
            "                    break\n"
            "                d = min(d, d2(strip[i], strip[j]))\n"
            "        return d\n"
            "    return rec(pts)\n",
            lambda low: bool(re.search(r"\bclosest[- ]pair\b", low)),
            (
                (([(0, 0), (1, 1), (3, 4)],), 2.0),
                (([(0, 0), (5, 0), (0, 5)],), 25.0),
                (([(1, 1), (1, 1)],), 0.0),
            ),
        ),
        T(
            "huffman_total_cost",
            "def huffman_total_cost(freqs):\n"
            '    """Weighted external path length of a Huffman tree."""\n'
            "    import heapq\n"
            "    items = list(freqs.values()) if isinstance(freqs, dict) else list(freqs)\n"
            "    items = [int(x) for x in items if int(x) > 0]\n"
            "    if len(items) <= 1:\n"
            "        return 0\n"
            "    heapq.heapify(items)\n"
            "    cost = 0\n"
            "    while len(items) > 1:\n"
            "        a = heapq.heappop(items)\n"
            "        b = heapq.heappop(items)\n"
            "        cost += a + b\n"
            "        heapq.heappush(items, a + b)\n"
            "    return cost\n",
            lambda low: bool(re.search(r"\bhuffman\b", low)),
            (
                (([5, 9, 12, 13, 16, 45],), 224),
                (({"a": 1, "b": 1, "c": 1, "d": 1},), 8),
                (([3],), 0),
            ),
        ),
        T(
            "subset_sum",
            "def subset_sum(nums, target):\n"
            '    """True if a subset of nums sums to target."""\n'
            "    target = int(target)\n"
            "    possible = {0}\n"
            "    for x in nums:\n"
            "        x = int(x)\n"
            "        possible |= {s + x for s in possible}\n"
            "        if target in possible:\n"
            "            return True\n"
            "    return target in possible\n",
            # Exclude partition-equal / can_partition prompts (LeetCode 416).
            lambda low: bool(re.search(r"\bsubset[- ]sum\b", low))
            and "partition" not in low
            and "equal subset" not in low
            and "can_partition" not in low,
            (
                (([1, 2, 3], 5), True),
                (([1, 2, 3], 7), False),
                (([], 0), True),
            ),
        ),
    ]
