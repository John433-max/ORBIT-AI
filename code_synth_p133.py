"""Cycle 410: hard grid/graph asks that still returned drafts.

Official examples (not copied solutions):
- 675 cut trees: [[1,2,3],[0,0,4],[7,6,5]] -> 6; blocked -> -1; start tree -> 6
- 864 all keys: ["@.a..","###.#","b.A.B"] -> 8; second grid -> 6; ["@Aa"] -> -1
- 1293 obstacles: k=1 on the 5x3 grid -> 6; blocked k=1 -> -1
- 174 dungeon: [[-2,-3,3],[-5,-10,1],[10,30,-5]] -> 7
- 688 knight probability: n=3 k=2 origin -> 0.0625; n=1 k=0 -> 1.0
- 1197 knight moves: (2,1) -> 1; (5,5) -> 4

Matchers require the problem phrase so stock max-profit and open-lock stay put.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "cut_off_trees",
            "def cutOffTree(forest):\n"
            '    """Minimum steps to cut trees shortest-to-tallest."""\n'
            "    from collections import deque\n"
            "    m, n = len(forest), len(forest[0])\n"
            "    trees = sorted(\n"
            "        (forest[r][c], r, c)\n"
            "        for r in range(m)\n"
            "        for c in range(n)\n"
            "        if forest[r][c] > 1\n"
            "    )\n"
            "    def bfs(sr, sc, tr, tc):\n"
            "        if sr == tr and sc == tc:\n"
            "            return 0\n"
            "        queue = deque([(sr, sc, 0)])\n"
            "        seen = {(sr, sc)}\n"
            "        while queue:\n"
            "            r, c, dist = queue.popleft()\n"
            "            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nr, nc = r + dr, c + dc\n"
            "                if (\n"
            "                    0 <= nr < m\n"
            "                    and 0 <= nc < n\n"
            "                    and forest[nr][nc]\n"
            "                    and (nr, nc) not in seen\n"
            "                ):\n"
            "                    if nr == tr and nc == tc:\n"
            "                        return dist + 1\n"
            "                    seen.add((nr, nc))\n"
            "                    queue.append((nr, nc, dist + 1))\n"
            "        return -1\n"
            "    steps = 0\n"
            "    r = c = 0\n"
            "    for _, tr, tc in trees:\n"
            "        dist = bfs(r, c, tr, tc)\n"
            "        if dist < 0:\n"
            "            return -1\n"
            "        steps += dist\n"
            "        r, c = tr, tc\n"
            "    return steps\n",
            lambda low: "cut off" in low and "tree" in low,
            (
                (([[1, 2, 3], [0, 0, 4], [7, 6, 5]],), 6),
                (([[1, 2, 3], [0, 0, 0], [7, 6, 5]],), -1),
                (([[2, 3, 4], [0, 0, 5], [8, 7, 6]],), 6),
            ),
        ),
        T(
            "shortest_path_all_keys",
            "def shortestPathAllKeys(grid):\n"
            '    """Shortest walk that collects every key (state BFS)."""\n'
            "    from collections import deque\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    keys = 0\n"
            "    sr = sc = 0\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            ch = grid[i][j]\n"
            "            if ch == '@':\n"
            "                sr, sc = i, j\n"
            "            elif 'a' <= ch <= 'f':\n"
            "                keys += 1\n"
            "    full = (1 << keys) - 1\n"
            "    queue = deque([(sr, sc, 0, 0)])\n"
            "    seen = {(sr, sc, 0)}\n"
            "    while queue:\n"
            "        r, c, mask, dist = queue.popleft()\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if not (0 <= nr < m and 0 <= nc < n):\n"
            "                continue\n"
            "            ch = grid[nr][nc]\n"
            "            if ch == '#':\n"
            "                continue\n"
            "            nmask = mask\n"
            "            if 'a' <= ch <= 'f':\n"
            "                nmask |= 1 << (ord(ch) - ord('a'))\n"
            "            elif 'A' <= ch <= 'F' and (nmask & (1 << (ord(ch) - ord('A')))) == 0:\n"
            "                continue\n"
            "            if nmask == full:\n"
            "                return dist + 1\n"
            "            state = (nr, nc, nmask)\n"
            "            if state not in seen:\n"
            "                seen.add(state)\n"
            "                queue.append((nr, nc, nmask, dist + 1))\n"
            "    return -1\n",
            lambda low: "all keys" in low or ("keys" in low and "shortest path" in low and "lock" not in low),
            (
                ((["@.a..", "###.#", "b.A.B"],), 8),
                ((["@..aA", "..B#.", "....b"],), 6),
                ((["@Aa"],), -1),
            ),
        ),
        T(
            "shortest_path_obstacles",
            "def shortestPath(grid, k):\n"
            '    """Shortest path allowing at most k obstacle eliminations."""\n'
            "    from collections import deque\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    if m == 1 and n == 1:\n"
            "        return 0\n"
            "    queue = deque([(0, 0, k, 0)])\n"
            "    seen = {(0, 0, k)}\n"
            "    while queue:\n"
            "        r, c, rem, dist = queue.popleft()\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if not (0 <= nr < m and 0 <= nc < n):\n"
            "                continue\n"
            "            nrem = rem - grid[nr][nc]\n"
            "            if nrem < 0:\n"
            "                continue\n"
            "            if nr == m - 1 and nc == n - 1:\n"
            "                return dist + 1\n"
            "            state = (nr, nc, nrem)\n"
            "            if state not in seen:\n"
            "                seen.add(state)\n"
            "                queue.append((nr, nc, nrem, dist + 1))\n"
            "    return -1\n",
            lambda low: "obstacles elimination" in low or ("obstacle" in low and "elimination" in low),
            (
                (([[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]], 1), 6),
                (([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 1), -1),
            ),
        ),
        T(
            "dungeon_game",
            "def calculateMinimumHP(dungeon):\n"
            '    """Minimum initial health to reach the princess."""\n'
            "    m, n = len(dungeon), len(dungeon[0])\n"
            "    need = [[10 ** 9] * (n + 1) for _ in range(m + 1)]\n"
            "    need[m][n - 1] = need[m - 1][n] = 1\n"
            "    for i in range(m - 1, -1, -1):\n"
            "        for j in range(n - 1, -1, -1):\n"
            "            nxt = min(need[i + 1][j], need[i][j + 1]) - dungeon[i][j]\n"
            "            need[i][j] = nxt if nxt > 1 else 1\n"
            "    return need[0][0]\n",
            lambda low: "dungeon" in low,
            (
                (([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]],), 7),
                (([[0]],), 1),
            ),
        ),
        T(
            "knight_probability",
            "def knightProbability(n, k, row, column):\n"
            '    """Probability a knight remains on the board after k moves."""\n'
            "    moves = (\n"
            "        (1, 2), (1, -2), (-1, 2), (-1, -2),\n"
            "        (2, 1), (2, -1), (-2, 1), (-2, -1),\n"
            "    )\n"
            "    dp = [[0.0] * n for _ in range(n)]\n"
            "    dp[row][column] = 1.0\n"
            "    for _ in range(k):\n"
            "        nxt = [[0.0] * n for _ in range(n)]\n"
            "        for r in range(n):\n"
            "            for c in range(n):\n"
            "                if dp[r][c] == 0.0:\n"
            "                    continue\n"
            "                share = dp[r][c] / 8.0\n"
            "                for dr, dc in moves:\n"
            "                    nr, nc = r + dr, c + dc\n"
            "                    if 0 <= nr < n and 0 <= nc < n:\n"
            "                        nxt[nr][nc] += share\n"
            "        dp = nxt\n"
            "    return sum(sum(line) for line in dp)\n",
            lambda low: "knight" in low and "probab" in low,
            (
                ((3, 2, 0, 0), 0.0625),
                ((1, 0, 0, 0), 1.0),
            ),
        ),
        T(
            "minimum_knight_moves",
            "def minKnightMoves(x, y):\n"
            '    """Minimum knight moves from origin to (x, y)."""\n'
            "    from collections import deque\n"
            "    x, y = abs(x), abs(y)\n"
            "    queue = deque([(0, 0, 0)])\n"
            "    seen = {(0, 0)}\n"
            "    moves = (\n"
            "        (1, 2), (1, -2), (-1, 2), (-1, -2),\n"
            "        (2, 1), (2, -1), (-2, 1), (-2, -1),\n"
            "    )\n"
            "    while queue:\n"
            "        r, c, dist = queue.popleft()\n"
            "        if r == x and c == y:\n"
            "            return dist\n"
            "        for dr, dc in moves:\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if abs(nr) > x + 2 or abs(nc) > y + 2:\n"
            "                continue\n"
            "            if (nr, nc) not in seen:\n"
            "                seen.add((nr, nc))\n"
            "                queue.append((nr, nc, dist + 1))\n"
            "    return -1\n",
            lambda low: "knight" in low and "move" in low and "probab" not in low,
            (
                ((2, 1), 1),
                ((5, 5), 4),
                ((1, 1), 2),
            ),
        ),
    ]
