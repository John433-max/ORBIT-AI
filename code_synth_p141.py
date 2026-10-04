"""Cycle 419: graph asks still unmatched after p140.

Matchers stay phrase-specific so critical connections, connecting-cities MST,
and number of islands stay on earlier templates.
- count complete components (union-find edge quota; LC 2685)
- distance-limited path existence (offline union-find; LC 1697)
- critical and pseudo-critical MST edges (forced Kruskal; LC 1489)
- minimum score of a path between two cities (component min edge; LC 2492)
- minimum cost to make at least one valid path (0-1 BFS; LC 1368)
- restricted paths from first to last (Dijkstra + DAG DP; LC 1786)
"""
from __future__ import annotations

from code_synth import Template


def _complete(low: str) -> bool:
    return "complete component" in low


def _limited(low: str) -> bool:
    return "edge length limited" in low or "distance limited paths" in low


def _pseudo(low: str) -> bool:
    return "pseudo-critical" in low or "pseudo critical" in low


def _min_score(low: str) -> bool:
    return "minimum score of a path" in low


def _valid_path(low: str) -> bool:
    return "valid path" in low and "minimum cost" in low


def _restricted(low: str) -> bool:
    return "restricted path" in low


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_complete_components",
            "def countCompleteComponents(n, edges):\n"
            '    """Complete connected components (LeetCode 2685)."""\n'
            "    parent = list(range(n))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    nodes = [1] * n\n"
            "    ec = [0] * n\n"
            "    for a, b in edges:\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra == rb:\n"
            "            ec[ra] += 1\n"
            "        else:\n"
            "            parent[rb] = ra\n"
            "            nodes[ra] += nodes[rb]\n"
            "            ec[ra] += ec[rb] + 1\n"
            "    ans = 0\n"
            "    for i in range(n):\n"
            "        if find(i) == i and ec[i] == nodes[i] * (nodes[i] - 1) // 2:\n"
            "            ans += 1\n"
            "    return ans\n",
            _complete,
            (
                ((6, [[0, 1], [0, 2], [1, 2], [3, 4]]), 3),
                ((6, [[0, 1], [0, 2], [1, 2], [3, 4], [3, 5]]), 1),
            ),
        ),
        T(
            "distance_limited_paths",
            "def distanceLimitedPathsExist(n, edgeList, queries):\n"
            '    """Whether each query has a path using edges shorter than limit (LeetCode 1697)."""\n'
            "    parent = list(range(n))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[rb] = ra\n"
            "\n"
            "    edges = sorted(edgeList, key=lambda e: e[2])\n"
            "    qs = sorted(enumerate(queries), key=lambda it: it[1][2])\n"
            "    ans = [False] * len(queries)\n"
            "    j = 0\n"
            "    for idx, (u, v, limit) in qs:\n"
            "        while j < len(edges) and edges[j][2] < limit:\n"
            "            union(edges[j][0], edges[j][1])\n"
            "            j += 1\n"
            "        ans[idx] = find(u) == find(v)\n"
            "    return ans\n",
            _limited,
            (
                ((3, [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]], [[0, 1, 2], [0, 2, 5]]), [False, True]),
                ((5, [[0, 1, 10], [1, 2, 5], [2, 3, 9], [3, 4, 13]], [[0, 4, 14], [1, 4, 13]]), [True, False]),
            ),
        ),
        T(
            "critical_pseudo_critical_edges",
            "def findCriticalAndPseudoCriticalEdges(n, edges):\n"
            '    """Critical and pseudo-critical MST edge indices (LeetCode 1489)."""\n'
            "    indexed = [(w, a, b, i) for i, (a, b, w) in enumerate(edges)]\n"
            "\n"
            "    def mst(force=None, skip=None):\n"
            "        parent = list(range(n))\n"
            "\n"
            "        def find(x):\n"
            "            while parent[x] != x:\n"
            "                parent[x] = parent[parent[x]]\n"
            "                x = parent[x]\n"
            "            return x\n"
            "\n"
            "        cost = 0\n"
            "        used = 0\n"
            "\n"
            "        def link(a, b, w):\n"
            "            nonlocal cost, used\n"
            "            ra, rb = find(a), find(b)\n"
            "            if ra == rb:\n"
            "                return\n"
            "            parent[rb] = ra\n"
            "            cost += w\n"
            "            used += 1\n"
            "\n"
            "        if force is not None:\n"
            "            w, a, b, i = indexed[force]\n"
            "            link(a, b, w)\n"
            "        for w, a, b, i in sorted(indexed):\n"
            "            if i == skip or i == force:\n"
            "                continue\n"
            "            link(a, b, w)\n"
            "        if used != n - 1:\n"
            "            return 10 ** 18\n"
            "        return cost\n"
            "\n"
            "    base = mst()\n"
            "    crit, pseudo = [], []\n"
            "    for i in range(len(edges)):\n"
            "        if mst(skip=i) > base:\n"
            "            crit.append(i)\n"
            "        elif mst(force=i) == base:\n"
            "            pseudo.append(i)\n"
            "    return [crit, pseudo]\n",
            _pseudo,
            (
                ((5, [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]]), [[0, 1], [2, 3, 4, 5]]),
                ((4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]]), [[], [0, 1, 2, 3]]),
            ),
        ),
        T(
            "min_score_path",
            "def minScore(n, roads):\n"
            '    """Min edge on any walk between cities 1 and n (LeetCode 2492)."""\n'
            "    g = [[] for _ in range(n + 1)]\n"
            "    for a, b, d in roads:\n"
            "        g[a].append((b, d))\n"
            "        g[b].append((a, d))\n"
            "    seen = [False] * (n + 1)\n"
            "    stack = [1]\n"
            "    seen[1] = True\n"
            "    best = 10 ** 18\n"
            "    while stack:\n"
            "        u = stack.pop()\n"
            "        for v, d in g[u]:\n"
            "            if d < best:\n"
            "                best = d\n"
            "            if not seen[v]:\n"
            "                seen[v] = True\n"
            "                stack.append(v)\n"
            "    return best\n",
            _min_score,
            (
                ((4, [[1, 2, 9], [2, 3, 6], [2, 4, 5], [1, 4, 7]]), 5),
                ((4, [[1, 2, 2], [1, 3, 4], [3, 4, 7]]), 2),
            ),
        ),
        T(
            "min_cost_valid_path",
            "def minCost(grid):\n"
            '    """Min arrow changes for a path to the corner (LeetCode 1368)."""\n'
            "    from collections import deque\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    dirs = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}\n"
            "    dist = [[10 ** 9] * n for _ in range(m)]\n"
            "    dist[0][0] = 0\n"
            "    dq = deque([(0, 0)])\n"
            "    while dq:\n"
            "        r, c = dq.popleft()\n"
            "        for k, (dr, dc) in dirs.items():\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if not (0 <= nr < m and 0 <= nc < n):\n"
            "                continue\n"
            "            w = 0 if grid[r][c] == k else 1\n"
            "            if dist[r][c] + w < dist[nr][nc]:\n"
            "                dist[nr][nc] = dist[r][c] + w\n"
            "                if w == 0:\n"
            "                    dq.appendleft((nr, nc))\n"
            "                else:\n"
            "                    dq.append((nr, nc))\n"
            "    return dist[-1][-1]\n",
            _valid_path,
            (
                (([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]],), 3),
                (([[1, 1, 3], [3, 2, 2], [1, 1, 4]],), 0),
                (([[1, 2], [4, 3]],), 1),
            ),
        ),
        T(
            "count_restricted_paths",
            "def countRestrictedPaths(n, edges):\n"
            '    """Paths to n where distance-to-n strictly decreases (LeetCode 1786)."""\n'
            "    import heapq\n"
            "    g = [[] for _ in range(n + 1)]\n"
            "    for u, v, w in edges:\n"
            "        g[u].append((v, w))\n"
            "        g[v].append((u, w))\n"
            "    dist = [10 ** 18] * (n + 1)\n"
            "    dist[n] = 0\n"
            "    pq = [(0, n)]\n"
            "    while pq:\n"
            "        d, u = heapq.heappop(pq)\n"
            "        if d != dist[u]:\n"
            "            continue\n"
            "        for v, w in g[u]:\n"
            "            nd = d + w\n"
            "            if nd < dist[v]:\n"
            "                dist[v] = nd\n"
            "                heapq.heappush(pq, (nd, v))\n"
            "    mod = 10 ** 9 + 7\n"
            "    order = sorted(range(1, n + 1), key=lambda x: dist[x])\n"
            "    ways = [0] * (n + 1)\n"
            "    ways[n] = 1\n"
            "    for u in order:\n"
            "        for v, _w in g[u]:\n"
            "            if dist[v] < dist[u]:\n"
            "                ways[u] = (ways[u] + ways[v]) % mod\n"
            "    return ways[1]\n",
            _restricted,
            (
                ((5, [[1, 2, 3], [1, 3, 3], [2, 3, 1], [1, 4, 2], [5, 2, 2], [3, 5, 1], [5, 4, 10]]), 3),
            ),
        ),
    ]
