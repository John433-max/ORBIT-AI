"""Cycle 408: graph/DP asks that returned drafts or the stock max-profit template.

Official examples (not copied solutions):
- 1326 taps: n=5 ranges=[3,4,1,1,0,0] -> 1; n=3 ranges=[0,0,0,0] -> -1
- 847 visit-all: star graph -> 4; second graph -> 4
- 1235 jobs: profits 120 / 150 / 6; adjacent jobs may touch at the endpoint
- 773 sliding puzzle: one move -> 1; unsolvable -> -1; five moves -> 5
- 1368 valid path: cost 3 / 0 / 1
- 818 race car: target 3 -> 2; target 6 -> 5

Matchers require the problem phrase so stock max-profit and open-lock stay put.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "min_taps",
            "def minTaps(n, ranges):\n"
            '    """Minimum taps to water [0, n] (jump-game cover)."""\n'
            "    far = [0] * (n + 1)\n"
            "    for i, reach in enumerate(ranges):\n"
            "        left = 0 if i - reach < 0 else i - reach\n"
            "        right = n if i + reach > n else i + reach\n"
            "        if right > far[left]:\n"
            "            far[left] = right\n"
            "    taps = 0\n"
            "    end = 0\n"
            "    next_end = 0\n"
            "    for i in range(n + 1):\n"
            "        if i > next_end:\n"
            "            return -1\n"
            "        if far[i] > next_end:\n"
            "            next_end = far[i]\n"
            "        if i == end:\n"
            "            if end >= n:\n"
            "                break\n"
            "            taps += 1\n"
            "            end = next_end\n"
            "            if end >= n:\n"
            "                break\n"
            "    return taps\n",
            lambda low: "tap" in low and ("garden" in low or "water" in low),
            (
                ((5, [3, 4, 1, 1, 0, 0]), 1),
                ((3, [0, 0, 0, 0]), -1),
                ((1, [1, 1]), 1),
            ),
        ),
        T(
            "shortest_path_visiting_all",
            "def shortestPathLength(graph):\n"
            '    """Shortest walk that visits every node (state BFS)."""\n'
            "    from collections import deque\n"
            "    n = len(graph)\n"
            "    if n <= 1:\n"
            "        return 0\n"
            "    full = (1 << n) - 1\n"
            "    queue = deque((i, 1 << i, 0) for i in range(n))\n"
            "    seen = {(i, 1 << i) for i in range(n)}\n"
            "    while queue:\n"
            "        node, mask, dist = queue.popleft()\n"
            "        for nxt in graph[node]:\n"
            "            nmask = mask | (1 << nxt)\n"
            "            if nmask == full:\n"
            "                return dist + 1\n"
            "            state = (nxt, nmask)\n"
            "            if state not in seen:\n"
            "                seen.add(state)\n"
            "                queue.append((nxt, nmask, dist + 1))\n"
            "    return -1\n",
            lambda low: (
                "visiting all" in low
                or "visit all nodes" in low
                or "shortest path visiting" in low
            ),
            (
                (([[1, 2, 3], [0], [0], [0]],), 4),
                (([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]],), 4),
                (([[]],), 0),
            ),
        ),
        T(
            "job_scheduling",
            "def jobScheduling(startTime, endTime, profit):\n"
            '    """Max profit of non-overlapping jobs (end-time DP)."""\n'
            "    import bisect\n"
            "    jobs = sorted(zip(startTime, endTime, profit), key=lambda job: job[1])\n"
            "    ends = [0]\n"
            "    best = [0]\n"
            "    for start, end, gain in jobs:\n"
            "        idx = bisect.bisect_right(ends, start) - 1\n"
            "        cand = best[idx] + gain\n"
            "        if cand > best[-1]:\n"
            "            ends.append(end)\n"
            "            best.append(cand)\n"
            "    return best[-1]\n",
            lambda low: "job" in low and "schedul" in low,
            (
                (([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]), 120),
                (([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]), 150),
                (([1, 1, 1], [2, 3, 4], [5, 6, 4]), 6),
            ),
        ),
        T(
            "sliding_puzzle",
            "def slidingPuzzle(board):\n"
            '    """Minimum moves to solve the 2x3 sliding puzzle."""\n'
            "    from collections import deque\n"
            "    start = tuple(board[0] + board[1])\n"
            "    goal = (1, 2, 3, 4, 5, 0)\n"
            "    if start == goal:\n"
            "        return 0\n"
            "    moves = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}\n"
            "    zero = start.index(0)\n"
            "    queue = deque([(start, zero, 0)])\n"
            "    seen = {start}\n"
            "    while queue:\n"
            "        state, z, dist = queue.popleft()\n"
            "        for nxt in moves[z]:\n"
            "            cells = list(state)\n"
            "            cells[z], cells[nxt] = cells[nxt], cells[z]\n"
            "            ns = tuple(cells)\n"
            "            if ns == goal:\n"
            "                return dist + 1\n"
            "            if ns not in seen:\n"
            "                seen.add(ns)\n"
            "                queue.append((ns, nxt, dist + 1))\n"
            "    return -1\n",
            lambda low: "sliding puzzle" in low,
            (
                (([[1, 2, 3], [4, 0, 5]],), 1),
                (([[1, 2, 3], [5, 4, 0]],), -1),
                (([[4, 1, 2], [5, 0, 3]],), 5),
            ),
        ),
        T(
            "min_cost_valid_path",
            "def minCost(grid):\n"
            '    """Min sign changes for a valid path (0-1 BFS)."""\n'
            "    from collections import deque\n"
            "    rows = len(grid)\n"
            "    cols = len(grid[0])\n"
            "    dirs = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}\n"
            "    inf = rows * cols\n"
            "    dist = [[inf] * cols for _ in range(rows)]\n"
            "    dist[0][0] = 0\n"
            "    queue = deque([(0, 0)])\n"
            "    while queue:\n"
            "        r, c = queue.popleft()\n"
            "        for sign, (dr, dc) in dirs.items():\n"
            "            nr = r + dr\n"
            "            nc = c + dc\n"
            "            if nr < 0 or nc < 0 or nr >= rows or nc >= cols:\n"
            "                continue\n"
            "            cost = 0 if grid[r][c] == sign else 1\n"
            "            nd = dist[r][c] + cost\n"
            "            if nd < dist[nr][nc]:\n"
            "                dist[nr][nc] = nd\n"
            "                if cost == 0:\n"
            "                    queue.appendleft((nr, nc))\n"
            "                else:\n"
            "                    queue.append((nr, nc))\n"
            "    return dist[rows - 1][cols - 1]\n",
            lambda low: "valid path" in low and ("cost" in low or "minimum" in low or "min " in low),
            (
                (([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]],), 3),
                (([[1, 1, 3], [3, 2, 2], [1, 1, 4]],), 0),
                (([[1, 2], [4, 3]],), 1),
            ),
        ),
        T(
            "race_car",
            "def racecar(target):\n"
            '    """Minimum instructions to reach target (A accelerate, R reverse)."""\n'
            "    from collections import deque\n"
            "    queue = deque([(0, 1, 0)])\n"
            "    seen = {(0, 1)}\n"
            "    limit = target * 2\n"
            "    while queue:\n"
            "        pos, speed, steps = queue.popleft()\n"
            "        npos = pos + speed\n"
            "        nspeed = speed * 2\n"
            "        if npos == target:\n"
            "            return steps + 1\n"
            "        if abs(npos) < limit and (npos, nspeed) not in seen:\n"
            "            seen.add((npos, nspeed))\n"
            "            queue.append((npos, nspeed, steps + 1))\n"
            "        rspeed = -1 if speed > 0 else 1\n"
            "        if (pos, rspeed) not in seen:\n"
            "            seen.add((pos, rspeed))\n"
            "            queue.append((pos, rspeed, steps + 1))\n"
            "    return -1\n",
            lambda low: bool(re.search(r"\brace\s*car\b", low) or "racecar" in low),
            (
                ((3,), 2),
                ((6,), 5),
                ((1,), 1),
            ),
        ),
    ]
