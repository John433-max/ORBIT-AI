"""Cycle 411: grid/graph asks that still returned NotImplemented drafts.

Official examples (not copied solutions):
- 286 walls and gates: INF room next to a gate becomes 1
- 1162 farthest land: center of a plus is 2; single land is 4
- 1514 max probability: 0.5*0.5 = 0.25 beats the direct 0.2 edge
- 1020 enclaves: interior land that cannot reach the border
- 827 large island: flipping one 0 joins two islands
- 433 genetic mutation: one-letter bank BFS

Matchers require the problem phrase so island-count and knight-probability stay put.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "walls_and_gates",
            "def wallsAndGates(rooms):\n"
            '    """Fill each empty room with distance to the nearest gate."""\n'
            "    from collections import deque\n"
            "    if not rooms or not rooms[0]:\n"
            "        return rooms\n"
            "    rows, cols = len(rooms), len(rooms[0])\n"
            "    queue = deque()\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if rooms[r][c] == 0:\n"
            "                queue.append((r, c))\n"
            "    while queue:\n"
            "        r, c = queue.popleft()\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if (\n"
            "                0 <= nr < rows\n"
            "                and 0 <= nc < cols\n"
            "                and rooms[nr][nc] == 2147483647\n"
            "            ):\n"
            "                rooms[nr][nc] = rooms[r][c] + 1\n"
            "                queue.append((nr, nc))\n"
            "    return rooms\n",
            lambda low: "wall" in low and "gate" in low,
            (
                (
                    (
                        [
                            [2147483647, -1, 0, 2147483647],
                            [2147483647, 2147483647, 2147483647, -1],
                            [2147483647, -1, 2147483647, -1],
                            [0, -1, 2147483647, 2147483647],
                        ],
                    ),
                    [
                        [3, -1, 0, 1],
                        [2, 2, 1, -1],
                        [1, -1, 2, -1],
                        [0, -1, 3, 4],
                    ],
                ),
                (([[0, -1], [2147483647, 2147483647]],), [[0, -1], [1, 2]]),
            ),
        ),
        T(
            "as_far_from_land",
            "def maxDistance(grid):\n"
            '    """Max distance from a water cell to the nearest land, or -1."""\n'
            "    from collections import deque\n"
            "    if not grid or not grid[0]:\n"
            "        return -1\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    queue = deque()\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 1:\n"
            "                queue.append((r, c))\n"
            "    if not queue or len(queue) == rows * cols:\n"
            "        return -1\n"
            "    dist = -1\n"
            "    while queue:\n"
            "        for _ in range(len(queue)):\n"
            "            r, c = queue.popleft()\n"
            "            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nr, nc = r + dr, c + dc\n"
            "                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:\n"
            "                    grid[nr][nc] = 1\n"
            "                    queue.append((nr, nc))\n"
            "        dist += 1\n"
            "    return dist\n",
            lambda low: "far" in low and "land" in low,
            (
                (([[1, 0, 1], [0, 0, 0], [1, 0, 1]],), 2),
                (([[1, 0, 0], [0, 0, 0], [0, 0, 0]],), 4),
                (([[1, 1], [1, 1]],), -1),
            ),
        ),
        T(
            "maximum_probability_path",
            "def maxProbability(n, edges, succProb, start, end):\n"
            '    """Highest-probability path from start to end (LeetCode 1514)."""\n'
            "    import heapq\n"
            "    graph = [[] for _ in range(n)]\n"
            "    for (a, b), prob in zip(edges, succProb):\n"
            "        graph[a].append((b, prob))\n"
            "        graph[b].append((a, prob))\n"
            "    best = [0.0] * n\n"
            "    best[start] = 1.0\n"
            "    heap = [(-1.0, start)]\n"
            "    while heap:\n"
            "        neg, node = heapq.heappop(heap)\n"
            "        prob = -neg\n"
            "        if node == end:\n"
            "            return prob\n"
            "        if prob < best[node]:\n"
            "            continue\n"
            "        for nxt, edge in graph[node]:\n"
            "            cand = prob * edge\n"
            "            if cand > best[nxt]:\n"
            "                best[nxt] = cand\n"
            "                heapq.heappush(heap, (-cand, nxt))\n"
            "    return 0.0\n",
            lambda low: "maximum probability" in low or "max probability" in low,
            (
                ((3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.2], 0, 2), 0.25),
                ((3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.3], 0, 2), 0.3),
                ((3, [[0, 1]], [0.5], 0, 2), 0.0),
            ),
        ),
        T(
            "number_of_enclaves",
            "def numEnclaves(grid):\n"
            '    """Land cells that cannot walk to the border (LeetCode 1020)."""\n'
            "    rows, cols = len(grid), len(grid[0])\n"
            "\n"
            "    def sink(r, c):\n"
            "        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != 1:\n"
            "            return\n"
            "        grid[r][c] = 0\n"
            "        sink(r + 1, c)\n"
            "        sink(r - 1, c)\n"
            "        sink(r, c + 1)\n"
            "        sink(r, c - 1)\n"
            "\n"
            "    for r in range(rows):\n"
            "        sink(r, 0)\n"
            "        sink(r, cols - 1)\n"
            "    for c in range(cols):\n"
            "        sink(0, c)\n"
            "        sink(rows - 1, c)\n"
            "    return sum(sum(row) for row in grid)\n",
            lambda low: "enclave" in low,
            (
                (([[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],), 3),
                (([[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],), 0),
                (([[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],), 3),
            ),
        ),
        T(
            "making_a_large_island",
            "def largestIsland(grid):\n"
            '    """Largest island after changing at most one 0 to 1."""\n'
            "    rows, cols = len(grid), len(grid[0])\n"
            "    ids = [[0] * cols for _ in range(rows)]\n"
            "    size = {}\n"
            "    cur = 2\n"
            "\n"
            "    def paint(r, c):\n"
            "        stack = [(r, c)]\n"
            "        ids[r][c] = cur\n"
            "        count = 0\n"
            "        while stack:\n"
            "            x, y = stack.pop()\n"
            "            count += 1\n"
            "            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nx, ny = x + dx, y + dy\n"
            "                if (\n"
            "                    0 <= nx < rows\n"
            "                    and 0 <= ny < cols\n"
            "                    and grid[nx][ny] == 1\n"
            "                    and ids[nx][ny] == 0\n"
            "                ):\n"
            "                    ids[nx][ny] = cur\n"
            "                    stack.append((nx, ny))\n"
            "        return count\n"
            "\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 1 and ids[r][c] == 0:\n"
            "                size[cur] = paint(r, c)\n"
            "                cur += 1\n"
            "    best = max(size.values(), default=0)\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 0:\n"
            "                seen = set()\n"
            "                total = 1\n"
            "                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                    nr, nc = r + dx, c + dy\n"
            "                    ident = ids[nr][nc] if 0 <= nr < rows and 0 <= nc < cols else 0\n"
            "                    if ident > 1 and ident not in seen:\n"
            "                        seen.add(ident)\n"
            "                        total += size[ident]\n"
            "                if total > best:\n"
            "                    best = total\n"
            "    return best\n",
            lambda low: "large island" in low or ("making" in low and "island" in low),
            (
                (([[1, 0], [0, 1]],), 3),
                (([[1, 1], [1, 0]],), 4),
                (([[1, 1], [1, 1]],), 4),
            ),
        ),
        T(
            "minimum_genetic_mutation",
            "def minMutation(startGene, endGene, bank):\n"
            '    """Minimum one-letter mutations through the bank, or -1."""\n'
            "    from collections import deque\n"
            "    bank = set(bank)\n"
            "    if endGene not in bank:\n"
            "        return -1\n"
            "    queue = deque([(startGene, 0)])\n"
            "    seen = {startGene}\n"
            "    while queue:\n"
            "        gene, dist = queue.popleft()\n"
            "        if gene == endGene:\n"
            "            return dist\n"
            "        for i in range(len(gene)):\n"
            "            for ch in \"ACGT\":\n"
            "                nxt = gene[:i] + ch + gene[i + 1 :]\n"
            "                if nxt in bank and nxt not in seen:\n"
            "                    seen.add(nxt)\n"
            "                    queue.append((nxt, dist + 1))\n"
            "    return -1\n",
            lambda low: "genetic" in low and "mutation" in low,
            (
                (("AACCGGTT", "AACCGGTA", ["AACCGGTA"]), 1),
                (("AACCGGTT", "AAACGGTA", ["AACCGGTA", "AACCGCTA", "AAACGGTA"]), 2),
                (("AAAAACCC", "AACCCCCC", ["AAAACCCC", "AAACCCCC", "AACCCCCC"]), 3),
            ),
        ),
    ]
