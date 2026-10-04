"""Cycle 423: box-push, course DAG, and island-cut asks still unmatched after p144.

Matchers stay phrase-specific so num-islands, large-island, and closed-island
templates stay on earlier packs.
- minimum moves to move a box (player-reachable push BFS; LC 1263)
- parallel courses III (DAG finish time; LC 2050)
- minimum days to disconnect an island (at most 2; LC 1568)
- as far from land as possible (multi-source BFS; LC 1162)
- time needed to inform all employees (tree DP; LC 1376)
- minimum vertices to reach all nodes (indegree 0; LC 1557)
"""
from __future__ import annotations

from code_synth import Template


def _box(low: str) -> bool:
    return "move a box" in low or "push the box" in low


def _courses(low: str) -> bool:
    return "parallel courses" in low


def _disconnect(low: str) -> bool:
    return "disconnect" in low and "island" in low


def _far(low: str) -> bool:
    return "far from land" in low


def _inform(low: str) -> bool:
    return "inform all employees" in low or "inform employees" in low


def _vertices(low: str) -> bool:
    return "vertices to reach all" in low or "reach all nodes" in low


def templates() -> list[Template]:
    return [
        Template(
            "min_push_box",
            "def minPushBox(grid):\n"
            '    """Min pushes to move the box onto the target (LeetCode 1263)."""\n'
            "    from collections import deque\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    box = player = target = None\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            cell = grid[r][c]\n"
            "            if cell == 'B':\n"
            "                box = (r, c)\n"
            "            elif cell == 'S':\n"
            "                player = (r, c)\n"
            "            elif cell == 'T':\n"
            "                target = (r, c)\n"
            "    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))\n"
            "    def can_reach(start, end, boxpos):\n"
            "        if start == end:\n"
            "            return True\n"
            "        seen = {start}\n"
            "        stack = [start]\n"
            "        while stack:\n"
            "            x, y = stack.pop()\n"
            "            for dx, dy in dirs:\n"
            "                nx, ny = x + dx, y + dy\n"
            "                if (\n"
            "                    0 <= nx < rows and 0 <= ny < cols\n"
            "                    and grid[nx][ny] != '#'\n"
            "                    and (nx, ny) != boxpos\n"
            "                    and (nx, ny) not in seen\n"
            "                ):\n"
            "                    if (nx, ny) == end:\n"
            "                        return True\n"
            "                    seen.add((nx, ny))\n"
            "                    stack.append((nx, ny))\n"
            "        return False\n"
            "    q = deque([(box[0], box[1], player[0], player[1], 0)])\n"
            "    seen_state = {(box[0], box[1], player[0], player[1])}\n"
            "    while q:\n"
            "        br, bc, pr, pc, dist = q.popleft()\n"
            "        if (br, bc) == target:\n"
            "            return dist\n"
            "        for dx, dy in dirs:\n"
            "            nr, nc = br + dx, bc + dy\n"
            "            px, py = br - dx, bc - dy\n"
            "            if not (0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#'):\n"
            "                continue\n"
            "            if not (0 <= px < rows and 0 <= py < cols and grid[px][py] != '#'):\n"
            "                continue\n"
            "            state = (nr, nc, px, py)\n"
            "            if state in seen_state:\n"
            "                continue\n"
            "            if can_reach((pr, pc), (px, py), (br, bc)):\n"
            "                seen_state.add(state)\n"
            "                q.append((nr, nc, px, py, dist + 1))\n"
            "    return -1\n",
            _box,
            (
                (([
                    ["#", "#", "#", "#", "#", "#"],
                    ["#", "T", "#", "#", "#", "#"],
                    ["#", ".", ".", "B", ".", "#"],
                    ["#", ".", "#", "#", ".", "#"],
                    ["#", ".", ".", ".", "S", "#"],
                    ["#", "#", "#", "#", "#", "#"],
                ],), 3),
                (([
                    ["#", "#", "#", "#", "#", "#"],
                    ["#", "T", "#", "#", "#", "#"],
                    ["#", ".", ".", "B", ".", "#"],
                    ["#", "#", "#", "#", ".", "#"],
                    ["#", ".", ".", ".", "S", "#"],
                    ["#", "#", "#", "#", "#", "#"],
                ],), -1),
                (([
                    ["#", "#", "#", "#", "#", "#"],
                    ["#", "T", ".", ".", "#", "#"],
                    ["#", ".", "#", "B", ".", "#"],
                    ["#", ".", ".", ".", ".", "#"],
                    ["#", ".", ".", ".", "S", "#"],
                    ["#", "#", "#", "#", "#", "#"],
                ],), 5),
            ),
        ),
        Template(
            "parallel_courses_iii",
            "def minimumTime(n, relations, time):\n"
            '    """Earliest month every course finishes (LeetCode 2050)."""\n'
            "    from collections import defaultdict, deque\n"
            "    n = int(n)\n"
            "    time = [int(v) for v in time]\n"
            "    graph = defaultdict(list)\n"
            "    indeg = [0] * (n + 1)\n"
            "    for prev, nxt in relations:\n"
            "        graph[int(prev)].append(int(nxt))\n"
            "        indeg[int(nxt)] += 1\n"
            "    finish = [0] * (n + 1)\n"
            "    q = deque()\n"
            "    for course in range(1, n + 1):\n"
            "        if indeg[course] == 0:\n"
            "            finish[course] = time[course - 1]\n"
            "            q.append(course)\n"
            "    while q:\n"
            "        course = q.popleft()\n"
            "        for nxt in graph[course]:\n"
            "            finish[nxt] = max(finish[nxt], finish[course] + time[nxt - 1])\n"
            "            indeg[nxt] -= 1\n"
            "            if indeg[nxt] == 0:\n"
            "                q.append(nxt)\n"
            "    return max(finish)\n",
            _courses,
            (
                ((3, [[1, 3], [2, 3]], [3, 2, 5]), 8),
                ((5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]), 12),
            ),
        ),
        Template(
            "min_days_disconnect_island",
            "def minDays(grid):\n"
            '    """Days to disconnect the island; answer is 0, 1, or 2 (LeetCode 1568)."""\n'
            "    rows, cols = len(grid), len(grid[0])\n"
            "    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))\n"
            "    def count():\n"
            "        seen = [[False] * cols for _ in range(rows)]\n"
            "        def dfs(r, c):\n"
            "            seen[r][c] = True\n"
            "            for dr, dc in dirs:\n"
            "                nr, nc = r + dr, c + dc\n"
            "                if (\n"
            "                    0 <= nr < rows and 0 <= nc < cols\n"
            "                    and grid[nr][nc] == 1 and not seen[nr][nc]\n"
            "                ):\n"
            "                    dfs(nr, nc)\n"
            "        islands = 0\n"
            "        for r in range(rows):\n"
            "            for c in range(cols):\n"
            "                if grid[r][c] == 1 and not seen[r][c]:\n"
            "                    islands += 1\n"
            "                    dfs(r, c)\n"
            "        return islands\n"
            "    if count() != 1:\n"
            "        return 0\n"
            "    lands = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]\n"
            "    for r, c in lands:\n"
            "        grid[r][c] = 0\n"
            "        broken = count() != 1\n"
            "        grid[r][c] = 1\n"
            "        if broken:\n"
            "            return 1\n"
            "    return 2\n",
            _disconnect,
            (
                (([[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],), 2),
                (([[1, 1]],), 2),
                (([[1, 0, 1, 0]],), 0),
            ),
        ),
        Template(
            "as_far_from_land",
            "def maxDistance(grid):\n"
            '    """Max Manhattan distance from water to the nearest land (LeetCode 1162)."""\n'
            "    from collections import deque\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    q = deque()\n"
            "    seen = [[False] * cols for _ in range(rows)]\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 1:\n"
            "                q.append((r, c))\n"
            "                seen[r][c] = True\n"
            "    if not q or len(q) == rows * cols:\n"
            "        return -1\n"
            "    dist = -1\n"
            "    while q:\n"
            "        for _ in range(len(q)):\n"
            "            r, c = q.popleft()\n"
            "            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nr, nc = r + dr, c + dc\n"
            "                if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc]:\n"
            "                    seen[nr][nc] = True\n"
            "                    q.append((nr, nc))\n"
            "        dist += 1\n"
            "    return dist\n",
            _far,
            (
                (([[1, 0, 1], [0, 0, 0], [1, 0, 1]],), 2),
                (([[1, 0, 0], [0, 0, 0], [0, 0, 0]],), 4),
                (([[1, 1], [1, 1]],), -1),
            ),
        ),
        Template(
            "inform_employees",
            "def numOfMinutes(n, headID, manager, informTime):\n"
            '    """Minutes for a head to inform every employee (LeetCode 1376)."""\n'
            "    from collections import defaultdict\n"
            "    children = defaultdict(list)\n"
            "    for emp, mgr in enumerate(manager):\n"
            "        if int(mgr) >= 0:\n"
            "            children[int(mgr)].append(emp)\n"
            "    def dfs(emp):\n"
            "        return int(informTime[emp]) + max((dfs(child) for child in children[emp]), default=0)\n"
            "    return dfs(int(headID))\n",
            _inform,
            (
                ((1, 0, [-1], [0]), 0),
                ((6, 2, [2, 2, -1, 2, 2, 2], [0, 0, 1, 0, 0, 0]), 1),
                ((7, 6, [1, 2, 3, 4, 5, 6, -1], [0, 6, 5, 4, 3, 2, 1]), 21),
            ),
        ),
        Template(
            "min_vertices_reach_all",
            "def findSmallestSetOfVertices(n, edges):\n"
            '    """Nodes with indegree 0 reach every node (LeetCode 1557)."""\n'
            "    incoming = [False] * int(n)\n"
            "    for _src, dst in edges:\n"
            "        incoming[int(dst)] = True\n"
            "    return [node for node, has_in in enumerate(incoming) if not has_in]\n",
            _vertices,
            (
                ((6, [[0, 1], [0, 2], [2, 5], [3, 4], [4, 2]]), [0, 3]),
                ((5, [[0, 1], [2, 1], [3, 1], [1, 4], [2, 4]]), [0, 2, 3]),
            ),
        ),
    ]
