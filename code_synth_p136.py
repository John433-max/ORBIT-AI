"""Cycle 413: graph asks missing from smoke (official example checks).

Matchers are phrase-specific so bipartite / place-flowers / accounts-merge stay put.
- clone graph (adjacency-list educational form)
- graph valid tree
- possible bipartition
- flower planting (4 colors, gardens)
- nearest exit in a maze
- max area of island
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "clone_graph",
            "def clone_graph(graph):\n"
            '    """Deep-copy an adjacency map {node: [neighbors]}."""\n'
            "    if not graph:\n"
            "        return {}\n"
            "    cloned = {node: [] for node in graph}\n"
            "    for node, nbrs in graph.items():\n"
            "        cloned[node] = list(nbrs)\n"
            "        for nbr in nbrs:\n"
            "            cloned.setdefault(nbr, [])\n"
            "    return cloned\n",
            lambda low: "clone" in low and "graph" in low,
            (
                (({0: [1, 2], 1: [0, 2], 2: [0, 1]},), {0: [1, 2], 1: [0, 2], 2: [0, 1]}),
                (({1: []},), {1: []}),
            ),
        ),
        T(
            "graph_valid_tree",
            "def valid_tree(n, edges):\n"
            '    """True if the undirected graph is a tree (connected, n-1 edges)."""\n'
            "    if len(edges) != n - 1:\n"
            "        return False\n"
            "    adj = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        adj[u].append(v)\n"
            "        adj[v].append(u)\n"
            "    seen = {0}\n"
            "    stack = [0]\n"
            "    while stack:\n"
            "        u = stack.pop()\n"
            "        for v in adj[u]:\n"
            "            if v not in seen:\n"
            "                seen.add(v)\n"
            "                stack.append(v)\n"
            "    return len(seen) == n\n",
            lambda low: "valid tree" in low and "graph" in low,
            (
                ((5, [[0, 1], [0, 2], [0, 3], [1, 4]]), True),
                ((5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]), False),
            ),
        ),
        T(
            "possible_bipartition",
            "def possibleBipartition(n, dislikes):\n"
            '    """True if people 1..n can be split so dislikes are across groups."""\n'
            "    adj = [[] for _ in range(n + 1)]\n"
            "    for a, b in dislikes:\n"
            "        adj[a].append(b)\n"
            "        adj[b].append(a)\n"
            "    color = [0] * (n + 1)\n\n"
            "    def dfs(u, c):\n"
            "        color[u] = c\n"
            "        for v in adj[u]:\n"
            "            if color[v] == c:\n"
            "                return False\n"
            "            if color[v] == 0 and not dfs(v, -c):\n"
            "                return False\n"
            "        return True\n\n"
            "    for i in range(1, n + 1):\n"
            "        if color[i] == 0 and not dfs(i, 1):\n"
            "            return False\n"
            "    return True\n",
            lambda low: "bipartition" in low and "bipartite" not in low,
            (
                ((4, [[1, 2], [1, 3], [1, 4]]), True),
                ((3, [[1, 2], [1, 3], [2, 3]]), False),
            ),
        ),
        T(
            "flower_planting",
            "def gardenNoAdj(n, paths):\n"
            '    """Plant 1..4 flower types so adjacent gardens differ."""\n'
            "    adj = [[] for _ in range(n + 1)]\n"
            "    for u, v in paths:\n"
            "        adj[u].append(v)\n"
            "        adj[v].append(u)\n"
            "    ans = [0] * (n + 1)\n"
            "    for g in range(1, n + 1):\n"
            "        used = {ans[nei] for nei in adj[g] if ans[nei]}\n"
            "        for color in (1, 2, 3, 4):\n"
            "            if color not in used:\n"
            "                ans[g] = color\n"
            "                break\n"
            "    return ans[1:]\n",
            lambda low: "flower planting" in low or ("gardens" in low and "flower" in low),
            (
                ((3, [[1, 2], [2, 3], [3, 1]]), [1, 2, 3]),
                ((4, [[1, 2], [3, 4]]), [1, 2, 1, 2]),
            ),
        ),
        T(
            "nearest_exit",
            "def nearestExit(maze, entrance):\n"
            '    """Steps to the nearest border exit, or -1."""\n'
            "    from collections import deque\n"
            "    rows, cols = len(maze), len(maze[0])\n"
            "    sr, sc = entrance\n"
            "    q = deque([(sr, sc, 0)])\n"
            "    seen = {(sr, sc)}\n"
            "    while q:\n"
            "        r, c, d = q.popleft()\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if not (0 <= nr < rows and 0 <= nc < cols):\n"
            "                continue\n"
            "            if maze[nr][nc] == '+' or (nr, nc) in seen:\n"
            "                continue\n"
            "            if nr in (0, rows - 1) or nc in (0, cols - 1):\n"
            "                return d + 1\n"
            "            seen.add((nr, nc))\n"
            "            q.append((nr, nc, d + 1))\n"
            "    return -1\n",
            lambda low: "nearest exit" in low,
            (
                (
                    (
                        [["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]],
                        [1, 2],
                    ),
                    1,
                ),
                (([["+", "+", "+"], [".", ".", "."], ["+", "+", "+"]], [1, 0]), 2),
            ),
        ),
        T(
            "max_area_of_island",
            "def max_area_of_island(grid):\n"
            '    """Largest 4-connected island of 1s."""\n'
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    seen = [[False] * cols for _ in range(rows)]\n\n"
            "    def dfs(r, c):\n"
            "        if r < 0 or c < 0 or r >= rows or c >= cols or seen[r][c] or grid[r][c] != 1:\n"
            "            return 0\n"
            "        seen[r][c] = True\n"
            "        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)\n\n"
            "    best = 0\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 1 and not seen[r][c]:\n"
            "                best = max(best, dfs(r, c))\n"
            "    return best\n"
            "\n"
            "def maxAreaOfIsland(grid):\n"
            "    return max_area_of_island(grid)\n",
            lambda low: "max area" in low and "island" in low,
            (
                (([[1, 1, 0], [1, 0, 0], [0, 0, 1]],), 3),
                (([[0, 0], [0, 0]],), 0),
            ),
        ),
    ]
