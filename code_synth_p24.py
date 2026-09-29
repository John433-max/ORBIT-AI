"""Cycle 283: graph/array templates + tighter sibling matchers."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "max_area_of_island",
            "def max_area_of_island(grid):\n"
            '    """Largest 4-connected group of 1s in a grid."""\n'
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    seen = [[False] * n for _ in range(m)]\n"
            "\n"
            "    def dfs(r, c):\n"
            "        if r < 0 or c < 0 or r >= m or c >= n or seen[r][c] or grid[r][c] != 1:\n"
            "            return 0\n"
            "        seen[r][c] = True\n"
            "        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)\n"
            "\n"
            "    best = 0\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            if grid[i][j] == 1 and not seen[i][j]:\n"
            "                best = max(best, dfs(i, j))\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmax(imum)? area of (an )?island\b|"
                    r"\bmax_area_of_island\b|"
                    r"\blargest island area\b",
                    low,
                )
            ),
            (
                (([[0, 0, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 0]],), 4),
                (([[0, 0], [0, 0]],), 0),
            ),
        ),
        T(
            "keys_and_rooms",
            "def can_visit_all_rooms(rooms):\n"
            '    """True if every room is reachable from room 0 via keys."""\n'
            "    n = len(rooms)\n"
            "    seen = {0}\n"
            "    stack = [0]\n"
            "    while stack:\n"
            "        cur = stack.pop()\n"
            "        for key in rooms[cur]:\n"
            "            if key not in seen:\n"
            "                seen.add(key)\n"
            "                stack.append(key)\n"
            "    return len(seen) == n\n",
            lambda low: bool(
                re.search(
                    r"\bkeys and rooms\b|"
                    r"\bcan_visit_all_rooms\b|"
                    r"\bvisit all rooms\b",
                    low,
                )
            ),
            (
                (([[1], [2], [3], []],), True),
                (([[1, 3], [3, 0, 1], [2], [0]],), False),
            ),
        ),
        T(
            "open_lock",
            "def open_lock(deadends, target):\n"
            '    """Min turns to open a 4-digit lock, avoiding deadends."""\n'
            "    dead = set(deadends)\n"
            "    if '0000' in dead:\n"
            "        return -1\n"
            "    if target == '0000':\n"
            "        return 0\n"
            "    from collections import deque\n"
            "    q = deque([('0000', 0)])\n"
            "    seen = {'0000'}\n"
            "    while q:\n"
            "        cur, dist = q.popleft()\n"
            "        for i in range(4):\n"
            "            d = int(cur[i])\n"
            "            for nd in ((d + 1) % 10, (d - 1) % 10):\n"
            "                nxt = cur[:i] + str(nd) + cur[i + 1:]\n"
            "                if nxt in seen or nxt in dead:\n"
            "                    continue\n"
            "                if nxt == target:\n"
            "                    return dist + 1\n"
            "                seen.add(nxt)\n"
            "                q.append((nxt, dist + 1))\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bopen(?:s|ing)?(?: the)? lock\b|"
                    r"\bopen_lock\b|"
                    r"\bcombination lock\b",
                    low,
                )
            ),
            (
                ((["0201", "0101", "0102", "1212", "2002"], "0202"), 6),
                ((["8888"], "0009"), 1),
            ),
        ),
        T(
            "shortest_bridge",
            "def shortest_bridge(grid):\n"
            '    """Min 0s to flip to connect the two islands."""\n'
            "    n = len(grid)\n"
            "    seen = [[False] * n for _ in range(n)]\n"
            "    from collections import deque\n"
            "    q = deque()\n"
            "\n"
            "    def dfs(r, c):\n"
            "        if r < 0 or c < 0 or r >= n or c >= n or seen[r][c] or grid[r][c] != 1:\n"
            "            return\n"
            "        seen[r][c] = True\n"
            "        q.append((r, c, 0))\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            dfs(r + dr, c + dc)\n"
            "\n"
            "    found = False\n"
            "    for i in range(n):\n"
            "        for j in range(n):\n"
            "            if grid[i][j] == 1:\n"
            "                dfs(i, j)\n"
            "                found = True\n"
            "                break\n"
            "        if found:\n"
            "            break\n"
            "    while q:\n"
            "        r, c, d = q.popleft()\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if nr < 0 or nc < 0 or nr >= n or nc >= n or seen[nr][nc]:\n"
            "                continue\n"
            "            if grid[nr][nc] == 1:\n"
            "                return d\n"
            "            seen[nr][nc] = True\n"
            "            q.append((nr, nc, d + 1))\n"
            "    return 0\n",
            lambda low: bool(
                re.search(r"\bshortest bridge\b|\bshortest_bridge\b", low)
            ),
            (
                (([[0, 1], [1, 0]],), 1),
                (([[0, 1, 0], [0, 0, 0], [0, 0, 1]],), 2),
            ),
        ),
        T(
            "is_bipartite",
            "def is_bipartite(graph):\n"
            '    """True if the undirected graph is 2-colorable."""\n'
            "    n = len(graph)\n"
            "    color = [0] * n\n"
            "    for start in range(n):\n"
            "        if color[start]:\n"
            "            continue\n"
            "        color[start] = 1\n"
            "        stack = [start]\n"
            "        while stack:\n"
            "            u = stack.pop()\n"
            "            for v in graph[u]:\n"
            "                if color[v] == 0:\n"
            "                    color[v] = -color[u]\n"
            "                    stack.append(v)\n"
            "                elif color[v] == color[u]:\n"
            "                    return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(r"\bis( graph)? bipartite\b|\bis_bipartite\b|\b2-colorable\b", low)
            ),
            (
                (([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]],), False),
                (([[1, 3], [0, 2], [1, 3], [0, 2]],), True),
            ),
        ),
        T(
            "find_celebrity",
            "def find_celebrity(matrix):\n"
            '    """Find the celebrity in an n x n knows-matrix, or -1."""\n'
            "    n = len(matrix)\n"
            "    if n == 0:\n"
            "        return -1\n"
            "\n"
            "    def knows(a, b):\n"
            "        return bool(matrix[a][b])\n"
            "\n"
            "    cand = 0\n"
            "    for i in range(1, n):\n"
            "        if knows(cand, i):\n"
            "            cand = i\n"
            "    for i in range(n):\n"
            "        if i == cand:\n"
            "            continue\n"
            "        if knows(cand, i) or not knows(i, cand):\n"
            "            return -1\n"
            "    return cand\n",
            lambda low: bool(
                re.search(r"\bfinds?( the)? celebrity\b|\bfind_celebrity\b", low)
            ),
            (
                (([[1, 1, 0], [0, 1, 0], [1, 1, 1]],), 1),
                (([[1, 1], [1, 1]],), -1),
            ),
        ),
    ]
