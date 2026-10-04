"""Cycle 412: graph asks that still returned NotImplemented drafts.

Official example checks (not copied solutions):
- 1254 closed islands: land (0) not touching the border
- 797 all paths: DFS order from 0 to n-1
- 802 eventual safe: nodes that only reach terminals
- 1376 inform time: tree depth weighted by informTime
- 2101 detonate bombs: directed reachability inside radius
- 1466 reorder routes: edges pointing away from city 0

Matchers require the problem phrase so island-count and ticket-buy stay put.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "closed_islands",
            "def closedIsland(grid):\n"
            '    """Count land islands (0) that do not touch the border."""\n'
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "\n"
            "    def flood(r, c):\n"
            "        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != 0:\n"
            "            return\n"
            "        grid[r][c] = 1\n"
            "        flood(r + 1, c)\n"
            "        flood(r - 1, c)\n"
            "        flood(r, c + 1)\n"
            "        flood(r, c - 1)\n"
            "\n"
            "    for r in range(rows):\n"
            "        flood(r, 0)\n"
            "        flood(r, cols - 1)\n"
            "    for c in range(cols):\n"
            "        flood(0, c)\n"
            "        flood(rows - 1, c)\n"
            "    count = 0\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 0:\n"
            "                count += 1\n"
            "                flood(r, c)\n"
            "    return count\n",
            lambda low: "closed" in low and "island" in low,
            (
                (
                    (
                        [
                            [1, 1, 1, 1, 1, 1, 1, 0],
                            [1, 0, 0, 0, 0, 1, 1, 0],
                            [1, 0, 1, 0, 1, 1, 1, 0],
                            [1, 0, 0, 0, 0, 1, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 0],
                        ],
                    ),
                    2,
                ),
                (([[0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0]],), 1),
                (([[1, 1, 1, 1, 1, 1, 1],
                   [1, 0, 0, 0, 0, 0, 1],
                   [1, 0, 1, 1, 1, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1],
                   [1, 0, 1, 1, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1]],), 2),
            ),
        ),
        T(
            "all_paths_source_target",
            "def allPathsSourceTarget(graph):\n"
            '    """Every path from node 0 to node n-1 in a DAG."""\n'
            "    n = len(graph)\n"
            "    out = []\n"
            "    path = [0]\n"
            "\n"
            "    def dfs(u):\n"
            "        if u == n - 1:\n"
            "            out.append(path[:])\n"
            "            return\n"
            "        for v in graph[u]:\n"
            "            path.append(v)\n"
            "            dfs(v)\n"
            "            path.pop()\n"
            "\n"
            "    dfs(0)\n"
            "    return out\n",
            lambda low: "all path" in low and ("source" in low or "target" in low),
            (
                (([[1, 2], [3], [3], []],), [[0, 1, 3], [0, 2, 3]]),
                (
                    ([[4, 3, 1], [3, 2, 4], [3], [4], []],),
                    [[0, 4], [0, 3, 4], [0, 1, 3, 4], [0, 1, 2, 3, 4], [0, 1, 4]],
                ),
            ),
        ),
        T(
            "eventual_safe_states",
            "def eventualSafeNodes(graph):\n"
            '    """Nodes that only lead to terminal nodes, in ascending order."""\n'
            "    from collections import deque\n"
            "    n = len(graph)\n"
            "    rev = [[] for _ in range(n)]\n"
            "    outdeg = [0] * n\n"
            "    for u, nbrs in enumerate(graph):\n"
            "        outdeg[u] = len(nbrs)\n"
            "        for v in nbrs:\n"
            "            rev[v].append(u)\n"
            "    queue = deque(i for i in range(n) if outdeg[i] == 0)\n"
            "    safe = [False] * n\n"
            "    while queue:\n"
            "        u = queue.popleft()\n"
            "        safe[u] = True\n"
            "        for parent in rev[u]:\n"
            "            outdeg[parent] -= 1\n"
            "            if outdeg[parent] == 0:\n"
            "                queue.append(parent)\n"
            "    return [i for i in range(n) if safe[i]]\n",
            lambda low: "eventual" in low and "safe" in low,
            (
                (([[1, 2], [2, 3], [5], [0], [5], [], []],), [2, 4, 5, 6]),
                (([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []],), [4]),
            ),
        ),
        T(
            "inform_employees",
            "def numOfMinutes(n, headID, manager, informTime):\n"
            '    """Minutes for news from the head to reach every employee."""\n'
            "    children = [[] for _ in range(n)]\n"
            "    for i, boss in enumerate(manager):\n"
            "        if boss >= 0:\n"
            "            children[boss].append(i)\n"
            "\n"
            "    def dfs(u):\n"
            "        extra = 0\n"
            "        for v in children[u]:\n"
            "            extra = max(extra, dfs(v))\n"
            "        return informTime[u] + extra\n"
            "\n"
            "    return dfs(headID)\n",
            lambda low: "inform" in low and "employee" in low,
            (
                ((1, 0, [-1], [0]), 0),
                ((6, 2, [2, 2, -1, 2, 2, 2], [0, 0, 1, 0, 0, 0]), 1),
                ((7, 6, [1, 2, 3, 4, 5, 6, -1], [0, 6, 5, 4, 3, 2, 1]), 21),
            ),
        ),
        T(
            "detonate_bombs",
            "def maximumDetonation(bombs):\n"
            '    """Most bombs detonated from one start, including the chain."""\n'
            "    n = len(bombs)\n"
            "    adj = [[] for _ in range(n)]\n"
            "    for i, (x, y, r) in enumerate(bombs):\n"
            "        r2 = r * r\n"
            "        for j, (xj, yj, _rj) in enumerate(bombs):\n"
            "            if i == j:\n"
            "                continue\n"
            "            dx, dy = xj - x, yj - y\n"
            "            if dx * dx + dy * dy <= r2:\n"
            "                adj[i].append(j)\n"
            "\n"
            "    def reach(start):\n"
            "        seen = {start}\n"
            "        stack = [start]\n"
            "        while stack:\n"
            "            u = stack.pop()\n"
            "            for v in adj[u]:\n"
            "                if v not in seen:\n"
            "                    seen.add(v)\n"
            "                    stack.append(v)\n"
            "        return len(seen)\n"
            "\n"
            "    return max(reach(i) for i in range(n)) if n else 0\n",
            lambda low: "detonat" in low or ("bomb" in low and "maximum" in low),
            (
                (([[2, 1, 3], [6, 1, 4]],), 2),
                (([[1, 1, 5], [10, 10, 5]],), 1),
                (([[1, 2, 3], [2, 3, 1], [3, 4, 2], [4, 5, 3], [5, 6, 4]],), 5),
            ),
        ),
        T(
            "reorder_routes",
            "def minReorder(n, connections):\n"
            '    """Flips so every route leads toward city 0."""\n'
            "    adj = [[] for _ in range(n)]\n"
            "    for a, b in connections:\n"
            "        adj[a].append((b, 1))\n"
            "        adj[b].append((a, 0))\n"
            "    seen = [False] * n\n"
            "    seen[0] = True\n"
            "    stack = [0]\n"
            "    flips = 0\n"
            "    while stack:\n"
            "        u = stack.pop()\n"
            "        for v, cost in adj[u]:\n"
            "            if not seen[v]:\n"
            "                seen[v] = True\n"
            "                flips += cost\n"
            "                stack.append(v)\n"
            "    return flips\n",
            lambda low: "reorder" in low and "route" in low,
            (
                ((6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]), 3),
                ((5, [[1, 0], [1, 2], [3, 2], [3, 4]]), 2),
                ((3, [[1, 0], [2, 0]]), 0),
            ),
        ),
    ]
