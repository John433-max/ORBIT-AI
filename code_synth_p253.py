"""Cycle 555: A* pathfinding, sparse-table RMQ, quickselect, Tarjan SCC,
LIS n log n, matrix-chain order.

Fills draft-stub gaps from agent routing probes.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "astar_path",
            "def astar(grid, start, goal):\n"
            '    """4-way A* on a 0/1 grid (1 = wall). Returns path length or -1."""\n'
            "    if not grid or not grid[0]:\n"
            "        return -1\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    sr, sc = start\n"
            "    gr, gc = goal\n"
            "    if not (0 <= sr < rows and 0 <= sc < cols and 0 <= gr < rows and 0 <= gc < cols):\n"
            "        return -1\n"
            "    if grid[sr][sc] or grid[gr][gc]:\n"
            "        return -1\n"
            "    import heapq\n"
            "    def h(r, c):\n"
            "        return abs(r - gr) + abs(c - gc)\n"
            "    pq = [(h(sr, sc), 0, sr, sc)]\n"
            "    best = {(sr, sc): 0}\n"
            "    while pq:\n"
            "        _, g, r, c = heapq.heappop(pq)\n"
            "        if g != best.get((r, c), -1):\n"
            "            continue\n"
            "        if (r, c) == (gr, gc):\n"
            "            return g\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:\n"
            "                ng = g + 1\n"
            "                if ng < best.get((nr, nc), 10 ** 18):\n"
            "                    best[(nr, nc)] = ng\n"
            "                    heapq.heappush(pq, (ng + h(nr, nc), ng, nr, nc))\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\ba\s*\*\s*(?:search|path(?:finding)?|algorithm)?\b|"
                    r"\ba[- ]star(?: search| path(?:finding)?| algorithm)?\b|"
                    r"\bastar(?: search| path(?:finding)?| algorithm)?\b",
                    low,
                )
            )
            and "dijkstra" not in low,
            (
                (([[0, 0, 0], [0, 1, 0], [0, 0, 0]], (0, 0), (2, 2)), 4),
                (([[0, 1, 0], [0, 1, 0], [0, 0, 0]], (0, 0), (0, 2)), 6),
                (([[0]], (0, 0), (0, 0)), 0),
                (([[0, 1], [1, 0]], (0, 0), (1, 1)), -1),
            ),
        ),
        T(
            "sparse_table_rmq",
            "def sparse_table_rmq(arr, queries):\n"
            '    """Range minimum queries via sparse table. queries are inclusive (l, r)."""\n'
            "    n = len(arr)\n"
            "    if n == 0:\n"
            "        return [None for _ in queries]\n"
            "    import math\n"
            "    log = [0] * (n + 1)\n"
            "    for i in range(2, n + 1):\n"
            "        log[i] = log[i // 2] + 1\n"
            "    kmax = log[n] + 1\n"
            "    st = [[0] * n for _ in range(kmax)]\n"
            "    for i in range(n):\n"
            "        st[0][i] = arr[i]\n"
            "    for k in range(1, kmax):\n"
            "        half = 1 << (k - 1)\n"
            "        for i in range(n - (1 << k) + 1):\n"
            "            st[k][i] = min(st[k - 1][i], st[k - 1][i + half])\n"
            "    out = []\n"
            "    for l, r in queries:\n"
            "        if l > r or l < 0 or r >= n:\n"
            "            out.append(None)\n"
            "            continue\n"
            "        k = log[r - l + 1]\n"
            "        out.append(min(st[k][l], st[k][r - (1 << k) + 1]))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsparse[- ]table\b|"
                    r"\brmq\b.{0,24}\bsparse\b|"
                    r"\bsparse\b.{0,24}\brmq\b|"
                    r"\brange minimum query\b",
                    low,
                )
            )
            and "segment" not in low,
            (
                (([2, 4, 3, 1, 6, 7, 8, 9, 1, 7], [(0, 9), (2, 5), (4, 4)]), [1, 1, 6]),
                (([5], [(0, 0)]), [5]),
                (([3, 1, 4], [(1, 2), (0, 0)]), [1, 3]),
            ),
        ),
        T(
            "quickselect",
            "def quickselect(arr, k):\n"
            '    """k-th smallest (0-based) via in-place quickselect. Returns None if k out of range."""\n'
            "    if not arr or k < 0 or k >= len(arr):\n"
            "        return None\n"
            "    a = list(arr)\n"
            "    lo, hi = 0, len(a) - 1\n"
            "    while lo <= hi:\n"
            "        pivot = a[hi]\n"
            "        i = lo\n"
            "        for j in range(lo, hi):\n"
            "            if a[j] <= pivot:\n"
            "                a[i], a[j] = a[j], a[i]\n"
            "                i += 1\n"
            "        a[i], a[hi] = a[hi], a[i]\n"
            "        if i == k:\n"
            "            return a[i]\n"
            "        if i < k:\n"
            "            lo = i + 1\n"
            "        else:\n"
            "            hi = i - 1\n"
            "    return None\n",
            lambda low: bool(
                re.search(
                    r"\bquick[- ]?select\b|"
                    r"\bquickselect\b",
                    low,
                )
            ),
            (
                (([3, 1, 4, 2, 5], 0), 1),
                (([3, 1, 4, 2, 5], 2), 3),
                (([3, 1, 4, 2, 5], 4), 5),
                (([7], 0), 7),
            ),
        ),
        T(
            "tarjan_scc",
            "def tarjan_scc(n, edges):\n"
            '    """Strongly connected components via Tarjan. Returns components sorted by min node."""\n'
            "    graph = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        graph[u].append(v)\n"
            "    index = 0\n"
            "    stack = []\n"
            "    onstack = [False] * n\n"
            "    indices = [-1] * n\n"
            "    lowlink = [0] * n\n"
            "    comps = []\n"
            "\n"
            "    def strongconnect(v):\n"
            "        nonlocal index\n"
            "        indices[v] = lowlink[v] = index\n"
            "        index += 1\n"
            "        stack.append(v)\n"
            "        onstack[v] = True\n"
            "        for w in graph[v]:\n"
            "            if indices[w] < 0:\n"
            "                strongconnect(w)\n"
            "                lowlink[v] = min(lowlink[v], lowlink[w])\n"
            "            elif onstack[w]:\n"
            "                lowlink[v] = min(lowlink[v], indices[w])\n"
            "        if lowlink[v] == indices[v]:\n"
            "            comp = []\n"
            "            while True:\n"
            "                w = stack.pop()\n"
            "                onstack[w] = False\n"
            "                comp.append(w)\n"
            "                if w == v:\n"
            "                    break\n"
            "            comps.append(sorted(comp))\n"
            "\n"
            "    for v in range(n):\n"
            "        if indices[v] < 0:\n"
            "            strongconnect(v)\n"
            "    comps.sort(key=lambda c: c[0] if c else -1)\n"
            "    return comps\n",
            lambda low: bool(
                re.search(
                    r"\btarjan(?:'s)?(?: algorithm)?\b|"
                    r"\btarjans\b|"
                    r"\btarjan scc\b|"
                    r"\bscc via tarjan\b",
                    low,
                )
            )
            and "bridge" not in low
            and "articulation" not in low,
            (
                ((5, [(1, 0), (0, 2), (2, 1), (0, 3), (3, 4)]), [[0, 1, 2], [3], [4]]),
                ((3, [(0, 1), (1, 2), (2, 0)]), [[0, 1, 2]]),
                ((2, []), [[0], [1]]),
            ),
        ),
        T(
            "lis_nlogn",
            "def lis_nlogn(arr):\n"
            '    """Length of the longest strictly increasing subsequence, O(n log n)."""\n'
            "    tails = []\n"
            "    import bisect\n"
            "    for x in arr:\n"
            "        i = bisect.bisect_left(tails, x)\n"
            "        if i == len(tails):\n"
            "            tails.append(x)\n"
            "        else:\n"
            "            tails[i] = x\n"
            "    return len(tails)\n",
            lambda low: bool(
                re.search(
                    r"\blis\b.{0,16}\bn\s*log\s*n\b|"
                    r"\bn\s*log\s*n\b.{0,16}\blis\b|"
                    r"\bnlogn\b.{0,24}\b(?:lis|increasing)\b|"
                    r"\bpatience sorting\b|"
                    r"\blongest increasing subsequence\b.{0,24}\bn\s*log\s*n\b",
                    low,
                )
            ),
            (
                (([10, 9, 2, 5, 3, 7, 101, 18],), 4),
                (([0, 1, 0, 3, 2, 3],), 4),
                (([7, 7, 7, 7],), 1),
                (([],), 0),
            ),
        ),
        T(
            "matrix_chain_order",
            "def matrix_chain_order(dims):\n"
            '    """Minimum scalar multiplications to multiply matrices with given dims."""\n'
            "    n = len(dims) - 1\n"
            "    if n <= 1:\n"
            "        return 0\n"
            "    dp = [[0] * n for _ in range(n)]\n"
            "    for length in range(2, n + 1):\n"
            "        for i in range(n - length + 1):\n"
            "            j = i + length - 1\n"
            "            best = 10 ** 18\n"
            "            for k in range(i, j):\n"
            "                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]\n"
            "                if cost < best:\n"
            "                    best = cost\n"
            "            dp[i][j] = best\n"
            "    return dp[0][n - 1]\n",
            lambda low: bool(
                re.search(
                    r"\bmatrix[- ]chain(?: order| multiplication| mult)?\b|"
                    r"\bmcm\b|"
                    r"\bmatrix chain order\b|"
                    r"\boptimal matrix chain\b",
                    low,
                )
            )
            and "multiply two" not in low
            and "matrix_multiply" not in low,
            (
                (([40, 20, 30, 10, 30],), 26000),
                (([10, 20, 30],), 6000),
                (([5, 5],), 0),
            ),
        ),
    ]
