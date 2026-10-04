"""Cycle 422: bounded BFS and street-grid asks still unmatched after p143.

Matchers stay phrase-specific so jump-game II, valid-path cost, and maze-II
templates stay on earlier packs.
- minimum operations to convert number (range BFS; LC 2059)
- escape the ghosts (manhattan race; LC 789)
- escape a large maze (bounded flood; LC 1036)
- shortest path to get food (grid BFS; LC 1730)
- check valid street path (connector DFS; LC 1391)
- minimum jumps to reach home (forward/back BFS; LC 1654)
"""
from __future__ import annotations

from code_synth import Template


def _ops(low: str) -> bool:
    return "convert number" in low and "operation" in low


def _ghosts(low: str) -> bool:
    return "escape the ghosts" in low or "escape ghosts" in low


def _large_maze(low: str) -> bool:
    return "large maze" in low or "escape a large" in low


def _food(low: str) -> bool:
    return "path to get food" in low or "get food" in low


def _street(low: str) -> bool:
    return "valid path in a grid" in low or ("valid path" in low and "street" in low)


def _home(low: str) -> bool:
    return "reach home" in low or ("minimum jumps" in low and "forbidden" in low)


def templates() -> list[Template]:
    return [
        Template(
            "minimum_operations_convert",
            "def minimumOperations(nums, start, goal):\n"
            '    """Min + / - / xor ops to reach goal, staying in [0, 1000] (LC 2059)."""\n'
            "    from collections import deque\n"
            "    nums = [int(v) for v in nums]\n"
            "    start, goal = int(start), int(goal)\n"
            "    if start == goal:\n"
            "        return 0\n"
            "    seen = {start}\n"
            "    q = deque([(start, 0)])\n"
            "    while q:\n"
            "        cur, steps = q.popleft()\n"
            "        for val in nums:\n"
            "            for nxt in (cur + val, cur - val, cur ^ val):\n"
            "                if nxt == goal:\n"
            "                    return steps + 1\n"
            "                if 0 <= nxt <= 1000 and nxt not in seen:\n"
            "                    seen.add(nxt)\n"
            "                    q.append((nxt, steps + 1))\n"
            "    return -1\n",
            _ops,
            (
                (([2, 4, 12], 2, 12), 2),
                (([3, 5, 7], 0, -4), 2),
                (([2, 8, 16], 0, 1), -1),
            ),
        ),
        Template(
            "escape_ghosts",
            "def escapeGhosts(ghosts, target):\n"
            '    """Escape if you reach the target strictly before every ghost (LC 789)."""\n'
            "    tx, ty = int(target[0]), int(target[1])\n"
            "    mine = abs(tx) + abs(ty)\n"
            "    for ghost in ghosts:\n"
            "        if abs(int(ghost[0]) - tx) + abs(int(ghost[1]) - ty) <= mine:\n"
            "            return False\n"
            "    return True\n",
            _ghosts,
            (
                (([[1, 0], [0, 3]], [0, 1]), True),
                (([[1, 0]], [2, 0]), False),
                (([[2, 0]], [1, 0]), False),
            ),
        ),
        Template(
            "escape_large_maze",
            "def isEscapePossible(blocked, source, target):\n"
            '    """Escape a 1e6 maze if neither side is enclosed by blocked cells (LC 1036)."""\n'
            "    blocked = {tuple(cell) for cell in blocked}\n"
            "    limit = len(blocked)\n"
            "    def reachable(start, end):\n"
            "        start, end = tuple(start), tuple(end)\n"
            "        if start == end:\n"
            "            return True\n"
            "        seen = {start}\n"
            "        stack = [start]\n"
            "        while stack and len(seen) <= limit:\n"
            "            x, y = stack.pop()\n"
            "            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nxt = (x + dx, y + dy)\n"
            "                if nxt == end:\n"
            "                    return True\n"
            "                if (\n"
            "                    0 <= nxt[0] < 10**6\n"
            "                    and 0 <= nxt[1] < 10**6\n"
            "                    and nxt not in blocked\n"
            "                    and nxt not in seen\n"
            "                ):\n"
            "                    seen.add(nxt)\n"
            "                    stack.append(nxt)\n"
            "        return len(seen) > limit\n"
            "    return reachable(source, target) and reachable(target, source)\n",
            _large_maze,
            (
                (([[0, 1], [1, 0]], [0, 0], [0, 2]), False),
                (([], [0, 0], [999999, 999999]), True),
            ),
        ),
        Template(
            "shortest_path_food",
            "def getFood(grid):\n"
            '    """BFS from X to the nearest * ; # is blocked (LC 1730)."""\n'
            "    from collections import deque\n"
            "    grid = [list(row) for row in grid]\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    start = None\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            if grid[i][j] == 'X':\n"
            "                start = (i, j)\n"
            "    if start is None:\n"
            "        return -1\n"
            "    q = deque([(start[0], start[1], 0)])\n"
            "    seen = {start}\n"
            "    while q:\n"
            "        i, j, dist = q.popleft()\n"
            "        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            ni, nj = i + di, j + dj\n"
            "            if not (0 <= ni < m and 0 <= nj < n) or (ni, nj) in seen:\n"
            "                continue\n"
            "            cell = grid[ni][nj]\n"
            "            if cell == '#':\n"
            "                continue\n"
            "            if cell == '*':\n"
            "                return dist + 1\n"
            "            seen.add((ni, nj))\n"
            "            q.append((ni, nj, dist + 1))\n"
            "    return -1\n",
            _food,
            (
                (([["X", "O", "*"]],), 2),
                (([["X", "#", "*"]],), -1),
                (([["X", "O"], ["O", "*"]],), 2),
            ),
        ),
        Template(
            "valid_street_path",
            "def hasValidPath(grid):\n"
            '    """Street cells 1-6 connect only if both ends open toward each other (LC 1391)."""\n'
            "    dirs = {\n"
            "        1: ((0, -1), (0, 1)),\n"
            "        2: ((-1, 0), (1, 0)),\n"
            "        3: ((0, -1), (1, 0)),\n"
            "        4: ((0, 1), (1, 0)),\n"
            "        5: ((0, -1), (-1, 0)),\n"
            "        6: ((0, 1), (-1, 0)),\n"
            "    }\n"
            "    grid = [list(row) for row in grid]\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    seen = {(0, 0)}\n"
            "    stack = [(0, 0)]\n"
            "    while stack:\n"
            "        r, c = stack.pop()\n"
            "        if (r, c) == (m - 1, n - 1):\n"
            "            return True\n"
            "        for dr, dc in dirs[int(grid[r][c])]:\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if not (0 <= nr < m and 0 <= nc < n) or (nr, nc) in seen:\n"
            "                continue\n"
            "            if (-dr, -dc) in dirs[int(grid[nr][nc])]:\n"
            "                seen.add((nr, nc))\n"
            "                stack.append((nr, nc))\n"
            "    return False\n",
            _street,
            (
                (([[2, 4, 3], [6, 5, 2]],), True),
                (([[1, 2, 1], [1, 2, 1]],), False),
                (([[1, 1, 2]],), False),
            ),
        ),
        Template(
            "minimum_jumps_home",
            "def minimumJumps(forbidden, a, b, x):\n"
            '    """Forward a, optional single backward b, avoid forbidden (LC 1654)."""\n'
            "    from collections import deque\n"
            "    forbidden = {int(v) for v in forbidden}\n"
            "    a, b, x = int(a), int(b), int(x)\n"
            "    if x == 0:\n"
            "        return 0\n"
            "    limit = max([x, *forbidden, 0]) + a + b\n"
            "    seen = {(0, 0)}\n"
            "    q = deque([(0, 0, 0)])\n"
            "    while q:\n"
            "        pos, steps, backed = q.popleft()\n"
            "        nxt = pos + a\n"
            "        if nxt == x:\n"
            "            return steps + 1\n"
            "        if nxt <= limit and nxt not in forbidden and (nxt, 0) not in seen:\n"
            "            seen.add((nxt, 0))\n"
            "            q.append((nxt, steps + 1, 0))\n"
            "        if not backed:\n"
            "            nxt = pos - b\n"
            "            if nxt == x:\n"
            "                return steps + 1\n"
            "            if nxt >= 0 and nxt not in forbidden and (nxt, 1) not in seen:\n"
            "                seen.add((nxt, 1))\n"
            "                q.append((nxt, steps + 1, 1))\n"
            "    return -1\n",
            _home,
            (
                (([14, 4, 18, 1, 15], 3, 15, 9), 3),
                (([8, 3, 16, 6, 12, 20], 15, 13, 11), -1),
                (([1, 6, 2, 14, 5, 17, 4], 16, 9, 7), 2),
            ),
        ),
    ]
