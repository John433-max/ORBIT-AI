"""Cycle 418: graph asks still unmatched after p139.

Matchers stay phrase-specific so number of islands, min-cost-to-connect-points,
shortest-path-with-obstacles, and connected-components stay on earlier templates.
- make network connected (union-find spare edges; LC 1319)
- most stones removed with same row or column (row/col union; LC 947)
- city with smallest neighbor count within threshold (Floyd; LC 1334)
- minimum obstacle removal to reach corner (0-1 BFS; LC 2290)
- number of distinct islands (shape signature; LC 694)
- connecting cities with minimum cost (Kruskal MST; LC 1135)
"""
from __future__ import annotations

from code_synth import Template


def _make_network(low: str) -> bool:
    return "make network connected" in low or "operations to make network connected" in low


def _stones(low: str) -> bool:
    return "stones removed" in low and "row" in low


def _city(low: str) -> bool:
    return "smallest number of neighbors" in low or ("find the city" in low and "threshold" in low)


def _obstacles(low: str) -> bool:
    return "obstacle removal" in low and "corner" in low


def _distinct(low: str) -> bool:
    return "distinct islands" in low


def _cities(low: str) -> bool:
    return "connecting cities" in low and "minimum cost" in low


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "make_network_connected",
            "def makeConnected(n, connections):\n"
            '    """Min cables to reconnect a network, or -1 (LeetCode 1319)."""\n'
            "    if len(connections) < n - 1:\n"
            "        return -1\n"
            "    parent = list(range(n))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    comps = n\n"
            "    for a, b in connections:\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[ra] = rb\n"
            "            comps -= 1\n"
            "    return comps - 1\n",
            _make_network,
            (
                ((4, [[0, 1], [0, 2], [1, 2]]), 1),
                ((6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]), 2),
                ((6, [[0, 1], [0, 2], [0, 3], [1, 2]]), -1),
            ),
        ),
        T(
            "most_stones_removed",
            "def removeStones(stones):\n"
            '    """Stones removed until no two share a row or column (LeetCode 947)."""\n'
            "    parent = {}\n"
            "\n"
            "    def find(x):\n"
            "        parent.setdefault(x, x)\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[ra] = rb\n"
            "\n"
            "    for r, c in stones:\n"
            "        union(r, ~c)\n"
            "    return len(stones) - len({find(r) for r, _ in stones})\n",
            _stones,
            (
                (([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]],), 5),
                (([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]],), 3),
                (([[0, 0]],), 0),
            ),
        ),
        T(
            "find_the_city",
            "def findTheCity(n, edges, distanceThreshold):\n"
            '    """City with fewest neighbors within a distance (LeetCode 1334)."""\n'
            "    inf = 10 ** 9\n"
            "    dist = [[inf] * n for _ in range(n)]\n"
            "    for i in range(n):\n"
            "        dist[i][i] = 0\n"
            "    for u, v, w in edges:\n"
            "        dist[u][v] = dist[v][u] = w\n"
            "    for k in range(n):\n"
            "        for i in range(n):\n"
            "            dik = dist[i][k]\n"
            "            if dik >= inf:\n"
            "                continue\n"
            "            for j in range(n):\n"
            "                alt = dik + dist[k][j]\n"
            "                if alt < dist[i][j]:\n"
            "                    dist[i][j] = alt\n"
            "    best, best_cnt = -1, n\n"
            "    for i in range(n):\n"
            "        cnt = sum(dist[i][j] <= distanceThreshold for j in range(n) if j != i)\n"
            "        if cnt <= best_cnt:\n"
            "            best_cnt = cnt\n"
            "            best = i\n"
            "    return best\n",
            _city,
            (
                ((4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4), 3),
                ((5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2), 0),
            ),
        ),
        T(
            "min_obstacle_removal",
            "def minimumObstacles(grid):\n"
            '    """Min obstacles removed to reach the opposite corner (LeetCode 2290)."""\n'
            "    from collections import deque\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    dist = [[10 ** 9] * n for _ in range(m)]\n"
            "    dist[0][0] = 0\n"
            "    dq = deque([(0, 0)])\n"
            "    while dq:\n"
            "        r, c = dq.popleft()\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < m and 0 <= nc < n:\n"
            "                nd = dist[r][c] + grid[nr][nc]\n"
            "                if nd < dist[nr][nc]:\n"
            "                    dist[nr][nc] = nd\n"
            "                    if grid[nr][nc]:\n"
            "                        dq.append((nr, nc))\n"
            "                    else:\n"
            "                        dq.appendleft((nr, nc))\n"
            "    return dist[m - 1][n - 1]\n",
            _obstacles,
            (
                (([[0, 1, 1], [1, 1, 0], [1, 1, 0]],), 2),
                (([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]],), 0),
            ),
        ),
        T(
            "distinct_islands",
            "def numDistinctIslands(grid):\n"
            '    """Count unique island shapes up to translation (LeetCode 694)."""\n'
            "    m, n = len(grid), len(grid[0])\n"
            "    seen = set()\n"
            "    shapes = set()\n"
            "\n"
            "    def harvest(sr, sc):\n"
            "        stack = [(sr, sc)]\n"
            "        seen.add((sr, sc))\n"
            "        cells = []\n"
            "        while stack:\n"
            "            x, y = stack.pop()\n"
            "            cells.append((x - sr, y - sc))\n"
            "            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nx, ny = x + dx, y + dy\n"
            "                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1 and (nx, ny) not in seen:\n"
            "                    seen.add((nx, ny))\n"
            "                    stack.append((nx, ny))\n"
            "        return tuple(sorted(cells))\n"
            "\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            if grid[i][j] == 1 and (i, j) not in seen:\n"
            "                shapes.add(harvest(i, j))\n"
            "    return len(shapes)\n",
            _distinct,
            (
                (([[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]],), 1),
                (([[1, 1, 0, 1, 1], [1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [1, 1, 0, 1, 1]],), 3),
            ),
        ),
        T(
            "connecting_cities_min_cost",
            "def minimumCost(n, connections):\n"
            '    """Min cost to connect n cities, or -1 (LeetCode 1135)."""\n'
            "    parent = list(range(n + 1))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    cost = used = 0\n"
            "    for u, v, w in sorted(connections, key=lambda e: e[2]):\n"
            "        ru, rv = find(u), find(v)\n"
            "        if ru != rv:\n"
            "            parent[ru] = rv\n"
            "            cost += w\n"
            "            used += 1\n"
            "            if used == n - 1:\n"
            "                return cost\n"
            "    return -1\n",
            _cities,
            (
                ((3, [[1, 2, 5], [1, 3, 6], [2, 3, 1]]), 6),
                ((4, [[1, 2, 3], [3, 4, 4]]), -1),
            ),
        ),
    ]
