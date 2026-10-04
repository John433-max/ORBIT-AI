"""Cycle 421: union-find supply graphs and time-bounded grids still unmatched after p142.

Matchers stay phrase-specific so second-minimum time, word break, and maze
templates stay on earlier packs.
- earliest moment everyone become friends (union-find; LC 1101)
- optimize water distribution in a village (virtual-well MST; LC 1168)
- minimum time to visit a cell in a grid (parity Dijkstra; LC 2577)
- shortest path visiting all nodes (state BFS; LC 847)
- last day you can still cross (binary search + flood; LC 1970)
- word ladder (one-letter BFS; LC 127)
"""
from __future__ import annotations

from code_synth import Template


def _friends(low: str) -> bool:
    return "become friends" in low or "earliest moment when everyone" in low


def _water(low: str) -> bool:
    return "water distribution" in low or "supply water" in low


def _visit_cell(low: str) -> bool:
    return "visit a cell" in low


def _visit_all(low: str) -> bool:
    return "visiting all nodes" in low


def _cross(low: str) -> bool:
    return "still cross" in low or "latest day to cross" in low


def _ladder(low: str) -> bool:
    return "word ladder" in low and "word break" not in low and " ii" not in low


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "earliest_friends",
            "def earliestAcq(logs, n):\n"
            '    """Earliest time everyone is connected (LeetCode 1101)."""\n'
            "    parent = list(range(n))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    comps = n\n"
            "    for t, a, b in sorted(logs):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[ra] = rb\n"
            "            comps -= 1\n"
            "            if comps == 1:\n"
            "                return t\n"
            "    return -1\n",
            _friends,
            (
                (
                    (
                        [
                            [20190101, 0, 1],
                            [20190104, 3, 4],
                            [20190107, 2, 3],
                            [20190211, 1, 5],
                            [20190224, 2, 4],
                            [20190301, 0, 3],
                            [20190312, 1, 2],
                            [20190322, 4, 5],
                        ],
                        6,
                    ),
                    20190301,
                ),
                (([[0, 2, 0], [1, 0, 1], [3, 0, 3], [4, 1, 2], [7, 3, 1]], 4), 3),
            ),
        ),
        T(
            "optimize_water_distribution",
            "def minCostToSupplyWater(n, wells, pipes):\n"
            '    """Min cost to water every house (LeetCode 1168)."""\n'
            "    edges = [(w, 0, i + 1) for i, w in enumerate(wells)]\n"
            "    edges.extend((c, a, b) for a, b, c in pipes)\n"
            "    edges.sort()\n"
            "    parent = list(range(n + 1))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    cost = used = 0\n"
            "    for c, a, b in edges:\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[ra] = rb\n"
            "            cost += c\n"
            "            used += 1\n"
            "            if used == n:\n"
            "                return cost\n"
            "    return cost\n",
            _water,
            (
                ((3, [1, 2, 2], [[1, 2, 1], [2, 3, 1]]), 3),
                ((2, [1, 1], [[1, 2, 1], [1, 2, 2]]), 2),
            ),
        ),
        T(
            "min_time_visit_cell",
            "def minimumTime(grid):\n"
            '    """Min time to reach the bottom-right cell (LeetCode 2577)."""\n'
            "    import heapq\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    if (m == 1 or grid[1][0] > 1) and (n == 1 or grid[0][1] > 1):\n"
            "        return -1 if m * n > 1 else 0\n"
            "    dist = [[10 ** 18] * n for _ in range(m)]\n"
            "    dist[0][0] = 0\n"
            "    heap = [(0, 0, 0)]\n"
            "    while heap:\n"
            "        t, r, c = heapq.heappop(heap)\n"
            "        if t != dist[r][c]:\n"
            "            continue\n"
            "        if r == m - 1 and c == n - 1:\n"
            "            return t\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if not (0 <= nr < m and 0 <= nc < n):\n"
            "                continue\n"
            "            nt = t + 1\n"
            "            need = grid[nr][nc]\n"
            "            if need > nt:\n"
            "                nt = need + ((need - nt) & 1)\n"
            "            if nt < dist[nr][nc]:\n"
            "                dist[nr][nc] = nt\n"
            "                heapq.heappush(heap, (nt, nr, nc))\n"
            "    return -1\n",
            _visit_cell,
            (
                (([[0, 1, 3, 2], [5, 1, 2, 5], [4, 3, 8, 6]],), 7),
                (([[0, 2, 4], [3, 2, 1], [1, 0, 4]],), -1),
            ),
        ),
        T(
            "shortest_path_visiting_all",
            "def shortestPathLength(graph):\n"
            '    """Shortest walk that visits every node (LeetCode 847)."""\n'
            "    from collections import deque\n"
            "    n = len(graph)\n"
            "    full = (1 << n) - 1\n"
            "    q = deque((i, 1 << i, 0) for i in range(n))\n"
            "    seen = {(i, 1 << i) for i in range(n)}\n"
            "    while q:\n"
            "        u, mask, dist = q.popleft()\n"
            "        if mask == full:\n"
            "            return dist\n"
            "        for v in graph[u]:\n"
            "            nmask = mask | (1 << v)\n"
            "            state = (v, nmask)\n"
            "            if state not in seen:\n"
            "                seen.add(state)\n"
            "                q.append((v, nmask, dist + 1))\n"
            "    return 0\n",
            _visit_all,
            (
                (([[1, 2, 3], [0], [0], [0]],), 4),
                (([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]],), 4),
            ),
        ),
        T(
            "last_day_to_cross",
            "def latestDayToCross(row, col, cells):\n"
            '    """Last day a top-bottom path remains (LeetCode 1970)."""\n'
            "    from collections import deque\n"
            "\n"
            "    def can(day):\n"
            "        flooded = [[False] * col for _ in range(row)]\n"
            "        for i in range(day):\n"
            "            r, c = cells[i]\n"
            "            flooded[r - 1][c - 1] = True\n"
            "        q = deque()\n"
            "        seen = [[False] * col for _ in range(row)]\n"
            "        for c in range(col):\n"
            "            if not flooded[0][c]:\n"
            "                seen[0][c] = True\n"
            "                q.append((0, c))\n"
            "        while q:\n"
            "            r, c = q.popleft()\n"
            "            if r == row - 1:\n"
            "                return True\n"
            "            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nr, nc = r + dr, c + dc\n"
            "                if 0 <= nr < row and 0 <= nc < col and not seen[nr][nc] and not flooded[nr][nc]:\n"
            "                    seen[nr][nc] = True\n"
            "                    q.append((nr, nc))\n"
            "        return False\n"
            "\n"
            "    lo, hi, ans = 0, len(cells), 0\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if can(mid):\n"
            "            ans = mid\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return ans\n",
            _cross,
            (
                ((2, 2, [[1, 1], [2, 1], [1, 2], [2, 2]]), 2),
                ((2, 2, [[1, 1], [1, 2], [2, 1], [2, 2]]), 1),
                (
                    (
                        3,
                        3,
                        [
                            [1, 2],
                            [2, 1],
                            [3, 3],
                            [2, 2],
                            [1, 1],
                            [1, 3],
                            [2, 3],
                            [3, 2],
                            [3, 1],
                        ],
                    ),
                    3,
                ),
            ),
        ),
        T(
            "word_ladder",
            "def ladderLength(beginWord, endWord, wordList):\n"
            '    """Shortest word ladder length, or 0 (LeetCode 127)."""\n'
            "    from collections import deque\n"
            "    bank = set(wordList)\n"
            "    if endWord not in bank:\n"
            "        return 0\n"
            "    q = deque([(beginWord, 1)])\n"
            "    seen = {beginWord}\n"
            "    alpha = 'abcdefghijklmnopqrstuvwxyz'\n"
            "    while q:\n"
            "        word, dist = q.popleft()\n"
            "        if word == endWord:\n"
            "            return dist\n"
            "        chars = list(word)\n"
            "        for i in range(len(chars)):\n"
            "            orig = chars[i]\n"
            "            for ch in alpha:\n"
            "                chars[i] = ch\n"
            "                nxt = ''.join(chars)\n"
            "                if nxt in bank and nxt not in seen:\n"
            "                    seen.add(nxt)\n"
            "                    q.append((nxt, dist + 1))\n"
            "            chars[i] = orig\n"
            "    return 0\n"
            "\n"
            "def word_ladder(begin_word, end_word, word_list):\n"
            "    return ladderLength(begin_word, end_word, word_list)\n",
            _ladder,
            (
                (("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
                (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0),
            ),
        ),
    ]
