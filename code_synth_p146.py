"""Cycle 424: heap-greedy and all-shortest-ladder asks still unmatched after p145.

Matchers stay phrase-specific so word ladder (length), course schedule, and
trap-rain stay on earlier packs.
- word ladder II (all shortest sequences; LC 126)
- IPO maximized capital (LC 502)
- maximum performance of a team (LC 1383)
- furthest building you can reach (LC 1642)
- minimum cost to hire k workers (LC 857)
- minimum number of refueling stops (LC 871)
"""
from __future__ import annotations

from code_synth import Template


def _ladder_ii(low: str) -> bool:
    return "word ladder ii" in low or "word ladder 2" in low or "all shortest transformation" in low


def _ipo(low: str) -> bool:
    return "ipo" in low and ("capital" in low or "profit" in low or "502" in low or "leetcode" in low)


def _performance(low: str) -> bool:
    return "performance of a team" in low or "maximum performance" in low and "team" in low


def _furthest(low: str) -> bool:
    return "furthest building" in low or "farthest building" in low


def _hire(low: str) -> bool:
    return "hire k workers" in low or "cost to hire" in low


def _refuel(low: str) -> bool:
    return "refueling stop" in low or "refuel stops" in low


def templates() -> list[Template]:
    return [
        Template(
            "word_ladder_ii",
            "def findLadders(beginWord, endWord, wordList):\n"
            '    """All shortest word ladders (LeetCode 126). Paths sorted."""\n'
            "    from collections import defaultdict, deque\n"
            "    words = set(wordList)\n"
            "    if endWord not in words:\n"
            "        return []\n"
            "    parents = defaultdict(list)\n"
            "    q = deque([beginWord])\n"
            "    seen = {beginWord}\n"
            "    found = False\n"
            "    while q and not found:\n"
            "        level = set()\n"
            "        for _ in range(len(q)):\n"
            "            word = q.popleft()\n"
            "            for i in range(len(word)):\n"
            "                for ch in 'abcdefghijklmnopqrstuvwxyz':\n"
            "                    nxt = word[:i] + ch + word[i + 1:]\n"
            "                    if nxt not in words or nxt in seen:\n"
            "                        continue\n"
            "                    parents[nxt].append(word)\n"
            "                    level.add(nxt)\n"
            "                    if nxt == endWord:\n"
            "                        found = True\n"
            "        seen |= level\n"
            "        q.extend(level)\n"
            "    if not found:\n"
            "        return []\n"
            "    out = []\n"
            "    def dfs(word, path):\n"
            "        if word == beginWord:\n"
            "            out.append(path[::-1])\n"
            "            return\n"
            "        for parent in parents[word]:\n"
            "            dfs(parent, path + [parent])\n"
            "    dfs(endWord, [endWord])\n"
            "    out.sort()\n"
            "    return out\n",
            _ladder_ii,
            (
                (
                    ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),
                    [
                        ["hit", "hot", "dot", "dog", "cog"],
                        ["hit", "hot", "lot", "log", "cog"],
                    ],
                ),
                (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), []),
            ),
        ),
        Template(
            "ipo_capital",
            "def findMaximizedCapital(k, w, profits, capital):\n"
            '    """Max capital after at most k IPO projects (LeetCode 502)."""\n'
            "    import heapq\n"
            "    jobs = sorted(zip(capital, profits))\n"
            "    i = 0\n"
            "    ready = []\n"
            "    n = len(jobs)\n"
            "    for _ in range(k):\n"
            "        while i < n and jobs[i][0] <= w:\n"
            "            heapq.heappush(ready, -jobs[i][1])\n"
            "            i += 1\n"
            "        if not ready:\n"
            "            break\n"
            "        w += -heapq.heappop(ready)\n"
            "    return w\n",
            _ipo,
            (
                ((2, 0, [1, 2, 3], [0, 1, 1]), 4),
                ((3, 0, [1, 2, 3], [0, 1, 2]), 6),
            ),
        ),
        Template(
            "max_team_performance",
            "def maxPerformance(n, speed, efficiency, k):\n"
            '    """Max team performance mod 1e9+7 (LeetCode 1383)."""\n'
            "    import heapq\n"
            "    mod = 10 ** 9 + 7\n"
            "    people = sorted(zip(efficiency, speed), reverse=True)\n"
            "    slow = []\n"
            "    speed_sum = 0\n"
            "    best = 0\n"
            "    for eff, spd in people:\n"
            "        heapq.heappush(slow, spd)\n"
            "        speed_sum += spd\n"
            "        if len(slow) > k:\n"
            "            speed_sum -= heapq.heappop(slow)\n"
            "        best = max(best, speed_sum * eff)\n"
            "    return best % mod\n",
            _performance,
            (
                ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 2), 60),
                ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 3), 68),
                ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 4), 72),
            ),
        ),
        Template(
            "furthest_building",
            "def furthestBuilding(heights, bricks, ladders):\n"
            '    """Furthest building index using bricks and ladders (LeetCode 1642)."""\n'
            "    import heapq\n"
            "    used = []\n"
            "    for i in range(len(heights) - 1):\n"
            "        climb = heights[i + 1] - heights[i]\n"
            "        if climb <= 0:\n"
            "            continue\n"
            "        heapq.heappush(used, climb)\n"
            "        if len(used) > ladders:\n"
            "            bricks -= heapq.heappop(used)\n"
            "            if bricks < 0:\n"
            "                return i\n"
            "    return len(heights) - 1\n",
            _furthest,
            (
                (([4, 2, 7, 6, 9, 14, 12], 5, 1), 4),
                (([4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2), 7),
                (([14, 3, 19, 3], 17, 0), 3),
            ),
        ),
        Template(
            "min_cost_hire_workers",
            "def mincostToHireWorkers(quality, wage, k):\n"
            '    """Min wage to hire k workers at a fair ratio (LeetCode 857)."""\n'
            "    import heapq\n"
            "    workers = sorted((w / q, q) for q, w in zip(quality, wage))\n"
            "    heap = []\n"
            "    qsum = 0\n"
            "    best = float('inf')\n"
            "    for ratio, q in workers:\n"
            "        heapq.heappush(heap, -q)\n"
            "        qsum += q\n"
            "        if len(heap) > k:\n"
            "            qsum += heapq.heappop(heap)\n"
            "        if len(heap) == k:\n"
            "            best = min(best, qsum * ratio)\n"
            "    return round(best, 5)\n",
            _hire,
            (
                (([10, 20, 5], [70, 50, 30], 2), 105.0),
                (([3, 1, 10, 10, 1], [4, 8, 2, 2, 7], 3), 30.66667),
            ),
        ),
        Template(
            "min_refuel_stops",
            "def minRefuelStops(target, startFuel, stations):\n"
            '    """Fewest refueling stops to reach target, or -1 (LeetCode 871)."""\n'
            "    import heapq\n"
            "    fuel = startFuel\n"
            "    i = 0\n"
            "    ready = []\n"
            "    stops = 0\n"
            "    n = len(stations)\n"
            "    while fuel < target:\n"
            "        while i < n and stations[i][0] <= fuel:\n"
            "            heapq.heappush(ready, -stations[i][1])\n"
            "            i += 1\n"
            "        if not ready:\n"
            "            return -1\n"
            "        fuel += -heapq.heappop(ready)\n"
            "        stops += 1\n"
            "    return stops\n",
            _refuel,
            (
                ((1, 1, []), 0),
                ((100, 1, [[10, 100]]), -1),
                ((100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]), 2),
            ),
        ),
    ]
