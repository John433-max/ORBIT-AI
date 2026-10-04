"""Cycle 407: medium graph/DP asks that still drafted.

Official examples (problem statements only, not copied solutions):
- 778 Swim in Rising Water: [[0,2],[1,3]] -> 3.
- 1091 Shortest Path in Binary Matrix: [[0,1],[1,0]] -> 2; blocked start -> -1.
- 1631 Path With Minimum Effort: [[1,2,2],[3,8,2],[5,3,5]] -> 2.
- 741 Cherry Pickup: [[0,1,-1],[1,0,-1],[1,1,1]] -> 5.
- 975 Odd Even Jumps: [10,13,12,14,15] -> 2; [2,3,1,1,4] -> 3.
- 815 Bus Routes: routes [[1,2,7],[3,6,7]], 1->6 -> 2.
- 909 Snakes and Ladders: 6x6 board with 15/13/35 portals -> 4.
- 444 Sequence Reconstruction: [1,2,3] with [[1,2],[1,3],[2,3]] -> true.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "swim_rising_water_778",
            "def swimInWater(grid):\n"
            '    """Min time to swim to the corner (LeetCode 778)."""\n'
            "    import heapq\n"
            "    n = len(grid)\n"
            "    heap = [(grid[0][0], 0, 0)]\n"
            "    seen = {(0, 0)}\n"
            "    while heap:\n"
            "        t, r, c = heapq.heappop(heap)\n"
            "        if r == n - 1 and c == n - 1:\n"
            "            return t\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:\n"
            "                seen.add((nr, nc))\n"
            "                heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"\b778\b", low)
                or ("swim" in low and "rising" in low)
            ),
            (
                (([[0, 2], [1, 3]],), 3),
                (([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]],), 16),
            ),
        ),
        T(
            "binary_matrix_shortest_1091",
            "def shortestPathBinaryMatrix(grid):\n"
            '    """8-direction shortest path on a binary matrix (LeetCode 1091)."""\n'
            "    from collections import deque\n"
            "    n = len(grid)\n"
            "    if not grid or grid[0][0] or grid[-1][-1]:\n"
            "        return -1\n"
            "    grid = [row[:] for row in grid]\n"
            "    q = deque([(0, 0, 1)])\n"
            "    grid[0][0] = 1\n"
            "    while q:\n"
            "        r, c, d = q.popleft()\n"
            "        if r == n - 1 and c == n - 1:\n"
            "            return d\n"
            "        for dr in (-1, 0, 1):\n"
            "            for dc in (-1, 0, 1):\n"
            "                if dr == 0 and dc == 0:\n"
            "                    continue\n"
            "                nr, nc = r + dr, c + dc\n"
            "                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:\n"
            "                    grid[nr][nc] = 1\n"
            "                    q.append((nr, nc, d + 1))\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"\b1091\b", low)
                or ("binary matrix" in low and "shortest" in low)
            ),
            (
                (([[0, 1], [1, 0]],), 2),
                (([[0, 0, 0], [1, 1, 0], [1, 1, 0]],), 4),
                (([[1, 0, 0], [1, 1, 0], [1, 1, 0]],), -1),
            ),
        ),
        T(
            "min_effort_path_1631",
            "def minimumEffortPath(heights):\n"
            '    """Min max-edge path on a height map (LeetCode 1631)."""\n'
            "    import heapq\n"
            "    m, n = len(heights), len(heights[0])\n"
            "    dist = [[10 ** 9] * n for _ in range(m)]\n"
            "    dist[0][0] = 0\n"
            "    heap = [(0, 0, 0)]\n"
            "    while heap:\n"
            "        e, r, c = heapq.heappop(heap)\n"
            "        if e > dist[r][c]:\n"
            "            continue\n"
            "        if r == m - 1 and c == n - 1:\n"
            "            return e\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < m and 0 <= nc < n:\n"
            "                ne = max(e, abs(heights[nr][nc] - heights[r][c]))\n"
            "                if ne < dist[nr][nc]:\n"
            "                    dist[nr][nc] = ne\n"
            "                    heapq.heappush(heap, (ne, nr, nc))\n"
            "    return dist[-1][-1]\n",
            lambda low: bool(
                re.search(r"\b1631\b", low)
                or ("minimum effort" in low)
                or ("min effort" in low)
            ),
            (
                (([[1, 2, 2], [3, 8, 2], [5, 3, 5]],), 2),
                (([[1, 2, 3], [3, 8, 4], [5, 3, 5]],), 1),
                (([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]],), 0),
            ),
        ),
        T(
            "cherry_pickup_741",
            "def cherryPickup(grid):\n"
            '    """Max cherries on two paths (LeetCode 741)."""\n'
            "    n = len(grid)\n"
            "    neg = -10 ** 9\n"
            "    dp = [[neg] * n for _ in range(n)]\n"
            "    dp[0][0] = grid[0][0]\n"
            "    for k in range(1, 2 * n - 1):\n"
            "        ndp = [[neg] * n for _ in range(n)]\n"
            "        for r1 in range(max(0, k - (n - 1)), min(n, k + 1)):\n"
            "            c1 = k - r1\n"
            "            if grid[r1][c1] < 0:\n"
            "                continue\n"
            "            for r2 in range(max(0, k - (n - 1)), min(n, k + 1)):\n"
            "                c2 = k - r2\n"
            "                if grid[r2][c2] < 0:\n"
            "                    continue\n"
            "                best = neg\n"
            "                for pr1 in (r1 - 1, r1):\n"
            "                    for pr2 in (r2 - 1, r2):\n"
            "                        if 0 <= pr1 < n and 0 <= pr2 < n:\n"
            "                            best = max(best, dp[pr1][pr2])\n"
            "                if best < 0:\n"
            "                    continue\n"
            "                add = grid[r1][c1]\n"
            "                if (r1, c1) != (r2, c2):\n"
            "                    add += grid[r2][c2]\n"
            "                ndp[r1][r2] = best + add\n"
            "        dp = ndp\n"
            "    return max(0, dp[n - 1][n - 1])\n",
            lambda low: bool(
                re.search(r"\b741\b", low)
                or ("cherry" in low and "pickup" in low)
            ),
            (
                (([[0, 1, -1], [1, 0, -1], [1, 1, 1]],), 5),
                (([[1, 1, -1], [1, -1, 1], [-1, 1, 1]],), 0),
            ),
        ),
        T(
            "odd_even_jumps_975",
            "def oddEvenJumps(arr):\n"
            '    """Count indices that reach the end via odd/even jumps (LeetCode 975)."""\n'
            "    n = len(arr)\n"
            "    def nxt(higher):\n"
            "        order = sorted(range(n), key=(lambda i: (arr[i], i)) if higher else (lambda i: (-arr[i], i)))\n"
            "        stack = []\n"
            "        res = [-1] * n\n"
            "        for i in order:\n"
            "            while stack and stack[-1] < i:\n"
            "                res[stack.pop()] = i\n"
            "            stack.append(i)\n"
            "        return res\n"
            "    hi, lo = nxt(True), nxt(False)\n"
            "    odd = [False] * n\n"
            "    even = [False] * n\n"
            "    odd[-1] = even[-1] = True\n"
            "    for i in range(n - 2, -1, -1):\n"
            "        if hi[i] != -1:\n"
            "            odd[i] = even[hi[i]]\n"
            "        if lo[i] != -1:\n"
            "            even[i] = odd[lo[i]]\n"
            "    return sum(odd)\n",
            lambda low: bool(
                re.search(r"\b975\b", low)
                or ("odd" in low and "even" in low and "jump" in low)
            ),
            (
                (([10, 13, 12, 14, 15],), 2),
                (([2, 3, 1, 1, 4],), 3),
                (([5, 1, 3, 4, 2],), 3),
            ),
        ),
        T(
            "bus_routes_815",
            "def numBusesToDestination(routes, source, target):\n"
            '    """Fewest buses from source to target (LeetCode 815)."""\n'
            "    from collections import defaultdict, deque\n"
            "    if source == target:\n"
            "        return 0\n"
            "    stop = defaultdict(set)\n"
            "    for i, route in enumerate(routes):\n"
            "        for s in route:\n"
            "            stop[s].add(i)\n"
            "    q = deque([(source, 0)])\n"
            "    seen_stop = {source}\n"
            "    seen_bus = set()\n"
            "    while q:\n"
            "        s, d = q.popleft()\n"
            "        for b in list(stop[s]):\n"
            "            if b in seen_bus:\n"
            "                continue\n"
            "            seen_bus.add(b)\n"
            "            for nxt in routes[b]:\n"
            "                if nxt == target:\n"
            "                    return d + 1\n"
            "                if nxt not in seen_stop:\n"
            "                    seen_stop.add(nxt)\n"
            "                    q.append((nxt, d + 1))\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"\b815\b", low)
                or ("bus" in low and "route" in low)
            ),
            (
                (([[1, 2, 7], [3, 6, 7]], 1, 6), 2),
                (([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12), -1),
            ),
        ),
        T(
            "snakes_ladders_909",
            "def snakesAndLadders(board):\n"
            '    """Min dice rolls on a snakes-and-ladders board (LeetCode 909)."""\n'
            "    from collections import deque\n"
            "    n = len(board)\n"
            "    target = n * n\n"
            "    def loc(x):\n"
            "        r, c = divmod(x - 1, n)\n"
            "        row = n - 1 - r\n"
            "        col = c if r % 2 == 0 else n - 1 - c\n"
            "        return row, col\n"
            "    q = deque([(1, 0)])\n"
            "    seen = {1}\n"
            "    while q:\n"
            "        x, d = q.popleft()\n"
            "        if x == target:\n"
            "            return d\n"
            "        for y in range(x + 1, min(x + 6, target) + 1):\n"
            "            r, c = loc(y)\n"
            "            nxt = board[r][c] if board[r][c] != -1 else y\n"
            "            if nxt not in seen:\n"
            "                seen.add(nxt)\n"
            "                q.append((nxt, d + 1))\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"\b909\b", low)
                or ("snake" in low and "ladder" in low)
            ),
            (
                (([[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, 35, -1, -1, 13, -1], [-1, -1, -1, -1, -1, -1], [-1, 15, -1, -1, -1, -1]],), 4),
                (([[-1, -1], [-1, 3]],), 1),
            ),
        ),
        T(
            "sequence_reconstruction_444",
            "def sequenceReconstruction(org, seqs):\n"
            '    """True if seqs uniquely reconstruct org (LeetCode 444)."""\n'
            "    from collections import defaultdict, deque\n"
            "    if not seqs:\n"
            "        return False\n"
            "    adj = defaultdict(set)\n"
            "    indeg = {x: 0 for x in org}\n"
            "    nodes = set()\n"
            "    for seq in seqs:\n"
            "        if not seq:\n"
            "            continue\n"
            "        for x in seq:\n"
            "            if x not in indeg:\n"
            "                return False\n"
            "            nodes.add(x)\n"
            "        for a, b in zip(seq, seq[1:]):\n"
            "            if b not in adj[a]:\n"
            "                adj[a].add(b)\n"
            "                indeg[b] += 1\n"
            "    if nodes != set(org):\n"
            "        return False\n"
            "    q = deque([x for x in org if indeg[x] == 0])\n"
            "    built = []\n"
            "    while q:\n"
            "        if len(q) != 1:\n"
            "            return False\n"
            "        u = q.popleft()\n"
            "        built.append(u)\n"
            "        for v in adj[u]:\n"
            "            indeg[v] -= 1\n"
            "            if indeg[v] == 0:\n"
            "                q.append(v)\n"
            "    return built == list(org)\n",
            lambda low: bool(
                re.search(r"\b444\b", low)
                or ("sequence" in low and "reconstruct" in low)
            ),
            (
                (([1, 2, 3], [[1, 2], [1, 3], [2, 3]]), True),
                (([1, 2, 3], [[1, 2], [1, 3]]), False),
                (([4, 1, 5, 2, 6, 3], [[5, 2, 6, 3], [4, 1, 5, 2]]), True),
            ),
        ),
    ]
