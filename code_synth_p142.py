"""Cycle 420: shortest-path counting and meeting graphs still unmatched after p141.

Matchers stay phrase-specific so cheapest flights, network delay, and
maximum-probability paths stay on earlier templates.
- number of ways to arrive at destination (Dijkstra counts; LC 1976)
- minimum fuel cost to report to the capital (tree ceil; LC 2477)
- minimum cost to reach destination in time (time-indexed Dijkstra; LC 1928)
- reachable nodes in subdivided graph (Dijkstra + edge quota; LC 882)
- second minimum time to reach destination (two-best + signals; LC 2045)
- find all people with secret (time-grouped spread; LC 2092)
"""
from __future__ import annotations

from code_synth import Template


def _ways(low: str) -> bool:
    return "ways to arrive" in low or ("arrive at destination" in low and "way" in low)


def _fuel(low: str) -> bool:
    return "fuel" in low and "capital" in low


def _in_time(low: str) -> bool:
    return "destination in time" in low or "reach destination in time" in low


def _subdivided(low: str) -> bool:
    return "subdivided" in low


def _second_min(low: str) -> bool:
    return "second minimum time" in low


def _secret(low: str) -> bool:
    return "people with secret" in low or "with the secret" in low


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_paths_arrive",
            "def countPaths(n, roads):\n"
            '    """Ways to arrive at n-1 on a shortest path (LeetCode 1976)."""\n'
            "    import heapq\n"
            "    MOD = 10 ** 9 + 7\n"
            "    g = [[] for _ in range(n)]\n"
            "    for u, v, w in roads:\n"
            "        g[u].append((v, w))\n"
            "        g[v].append((u, w))\n"
            "    dist = [10 ** 18] * n\n"
            "    ways = [0] * n\n"
            "    dist[0] = 0\n"
            "    ways[0] = 1\n"
            "    heap = [(0, 0)]\n"
            "    while heap:\n"
            "        d, u = heapq.heappop(heap)\n"
            "        if d != dist[u]:\n"
            "            continue\n"
            "        for v, w in g[u]:\n"
            "            nd = d + w\n"
            "            if nd < dist[v]:\n"
            "                dist[v] = nd\n"
            "                ways[v] = ways[u]\n"
            "                heapq.heappush(heap, (nd, v))\n"
            "            elif nd == dist[v]:\n"
            "                ways[v] = (ways[v] + ways[u]) % MOD\n"
            "    return ways[n - 1] % MOD\n",
            _ways,
            (
                (
                    (
                        7,
                        [
                            [0, 6, 7],
                            [0, 1, 2],
                            [1, 2, 3],
                            [1, 3, 3],
                            [6, 3, 3],
                            [3, 5, 1],
                            [6, 5, 1],
                            [2, 5, 1],
                            [0, 4, 5],
                            [4, 6, 2],
                        ],
                    ),
                    4,
                ),
                ((2, [[1, 0, 10]]), 1),
            ),
        ),
        T(
            "minimum_fuel_capital",
            "def minimumFuelCost(roads, seats):\n"
            '    """Fuel to bring everyone to capital 0 (LeetCode 2477)."""\n'
            "    n = len(roads) + 1\n"
            "    g = [[] for _ in range(n)]\n"
            "    for a, b in roads:\n"
            "        g[a].append(b)\n"
            "        g[b].append(a)\n"
            "    ans = 0\n"
            "\n"
            "    def dfs(u, parent):\n"
            "        nonlocal ans\n"
            "        size = 1\n"
            "        for v in g[u]:\n"
            "            if v != parent:\n"
            "                size += dfs(v, u)\n"
            "        if u:\n"
            "            ans += (size + seats - 1) // seats\n"
            "        return size\n"
            "\n"
            "    dfs(0, -1)\n"
            "    return ans\n",
            _fuel,
            (
                (([[0, 1], [0, 2], [0, 3]], 5), 3),
                (([[3, 1], [3, 2], [1, 0], [0, 4], [0, 5], [4, 6]], 2), 7),
                (([], 1), 0),
            ),
        ),
        T(
            "min_cost_destination_time",
            "def minCost(maxTime, edges, passingFees):\n"
            '    """Min passing-fee cost with total time <= maxTime (LeetCode 1928)."""\n'
            "    import heapq\n"
            "    n = len(passingFees)\n"
            "    g = [[] for _ in range(n)]\n"
            "    for u, v, t in edges:\n"
            "        g[u].append((v, t))\n"
            "        g[v].append((u, t))\n"
            "    INF = 10 ** 18\n"
            "    dist = [[INF] * (maxTime + 1) for _ in range(n)]\n"
            "    dist[0][0] = passingFees[0]\n"
            "    heap = [(passingFees[0], 0, 0)]\n"
            "    while heap:\n"
            "        cost, t, u = heapq.heappop(heap)\n"
            "        if cost != dist[u][t]:\n"
            "            continue\n"
            "        if u == n - 1:\n"
            "            return cost\n"
            "        for v, w in g[u]:\n"
            "            nt = t + w\n"
            "            if nt > maxTime:\n"
            "                continue\n"
            "            nc = cost + passingFees[v]\n"
            "            if nc < dist[v][nt]:\n"
            "                dist[v][nt] = nc\n"
            "                heapq.heappush(heap, (nc, nt, v))\n"
            "    return -1\n",
            _in_time,
            (
                (
                    (
                        30,
                        [[0, 1, 10], [1, 2, 10], [2, 5, 10], [0, 3, 1], [3, 4, 10], [4, 5, 15]],
                        [5, 1, 2, 20, 20, 3],
                    ),
                    11,
                ),
                (
                    (
                        29,
                        [[0, 1, 10], [1, 2, 10], [2, 5, 10], [0, 3, 1], [3, 4, 10], [4, 5, 15]],
                        [5, 1, 2, 20, 20, 3],
                    ),
                    48,
                ),
                (
                    (
                        25,
                        [[0, 1, 10], [1, 2, 10], [2, 5, 10], [0, 3, 1], [3, 4, 10], [4, 5, 15]],
                        [5, 1, 2, 20, 20, 3],
                    ),
                    -1,
                ),
            ),
        ),
        T(
            "reachable_nodes_subdivided",
            "def reachableNodes(edges, maxMoves, n):\n"
            '    """Reachable nodes after subdividing edges (LeetCode 882)."""\n'
            "    import heapq\n"
            "    g = [[] for _ in range(n)]\n"
            "    for u, v, cnt in edges:\n"
            "        g[u].append((v, cnt + 1))\n"
            "        g[v].append((u, cnt + 1))\n"
            "    dist = [10 ** 18] * n\n"
            "    dist[0] = 0\n"
            "    heap = [(0, 0)]\n"
            "    while heap:\n"
            "        d, u = heapq.heappop(heap)\n"
            "        if d != dist[u]:\n"
            "            continue\n"
            "        for v, w in g[u]:\n"
            "            nd = d + w\n"
            "            if nd < dist[v] and nd <= maxMoves:\n"
            "                dist[v] = nd\n"
            "                heapq.heappush(heap, (nd, v))\n"
            "    ans = sum(d <= maxMoves for d in dist)\n"
            "    for u, v, cnt in edges:\n"
            "        a = maxMoves - dist[u] if dist[u] <= maxMoves else 0\n"
            "        b = maxMoves - dist[v] if dist[v] <= maxMoves else 0\n"
            "        ans += min(cnt, a + b)\n"
            "    return ans\n",
            _subdivided,
            (
                (([[0, 1, 10], [0, 2, 1], [1, 2, 2]], 6, 3), 13),
                (([[0, 1, 4], [1, 2, 6], [0, 2, 8], [1, 3, 1]], 10, 4), 23),
                (([[1, 2, 4], [1, 4, 5], [1, 3, 1], [2, 3, 4], [3, 4, 5]], 17, 5), 1),
            ),
        ),
        T(
            "second_minimum_time",
            "def secondMinimum(n, edges, time, change):\n"
            '    """Second-minimum time with traffic signals (LeetCode 2045)."""\n'
            "    import heapq\n"
            "    g = [[] for _ in range(n + 1)]\n"
            "    for u, v in edges:\n"
            "        g[u].append(v)\n"
            "        g[v].append(u)\n"
            "    best = [[10 ** 18, 10 ** 18] for _ in range(n + 1)]\n"
            "    best[1][0] = 0\n"
            "    heap = [(0, 1)]\n"
            "    while heap:\n"
            "        d, u = heapq.heappop(heap)\n"
            "        if d > best[u][1]:\n"
            "            continue\n"
            "        turns = d // change\n"
            "        leave = d if turns % 2 == 0 else (turns + 1) * change\n"
            "        nd = leave + time\n"
            "        for v in g[u]:\n"
            "            if nd < best[v][0]:\n"
            "                best[v][1] = best[v][0]\n"
            "                best[v][0] = nd\n"
            "                heapq.heappush(heap, (nd, v))\n"
            "            elif best[v][0] < nd < best[v][1]:\n"
            "                best[v][1] = nd\n"
            "                heapq.heappush(heap, (nd, v))\n"
            "    return best[n][1]\n",
            _second_min,
            (
                ((5, [[1, 2], [1, 3], [1, 4], [3, 4], [4, 5]], 3, 5), 13),
                ((2, [[1, 2]], 3, 2), 11),
            ),
        ),
        T(
            "find_all_people_secret",
            "def findAllPeople(n, meetings, firstPerson):\n"
            '    """People who learn the secret (LeetCode 2092)."""\n'
            "    meetings = sorted(meetings, key=lambda row: row[2])\n"
            "    know = {0, firstPerson}\n"
            "    i = 0\n"
            "    m = len(meetings)\n"
            "    while i < m:\n"
            "        t = meetings[i][2]\n"
            "        j = i\n"
            "        g = {}\n"
            "        while j < m and meetings[j][2] == t:\n"
            "            a, b, _ = meetings[j]\n"
            "            g.setdefault(a, []).append(b)\n"
            "            g.setdefault(b, []).append(a)\n"
            "            j += 1\n"
            "        stack = [x for x in g if x in know]\n"
            "        seen = set(stack)\n"
            "        while stack:\n"
            "            u = stack.pop()\n"
            "            know.add(u)\n"
            "            for v in g[u]:\n"
            "                if v not in seen:\n"
            "                    seen.add(v)\n"
            "                    stack.append(v)\n"
            "        i = j\n"
            "    return sorted(know)\n",
            _secret,
            (
                ((6, [[1, 2, 5], [2, 3, 8], [1, 5, 10]], 1), [0, 1, 2, 3, 5]),
                ((4, [[3, 1, 3], [1, 2, 2], [0, 3, 3]], 3), [0, 1, 3]),
                ((5, [[3, 4, 2], [1, 2, 1], [2, 3, 1]], 1), [0, 1, 2, 3, 4]),
            ),
        ),
    ]
