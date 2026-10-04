"""Cycle 417: directed / weighted graph asks still unmatched after p138.

Matchers stay phrase-specific so redundant connection (LC 684), alternating
sum, and minimum-effort path stay on earlier templates.
- redundant connection ii (double parent or cycle; LC 685)
- shortest path with alternating colors (color-state BFS; LC 1129)
- network delay time (Dijkstra; LC 743)
- cheapest flights within k stops (Bellman k+1; LC 787)
- open the lock (4-dial BFS; LC 752)
- critical connections (Tarjan bridges; LC 1192)
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "redundant_connection_ii",
            "def findRedundantDirectedConnection(edges):\n"
            '    """Edge to drop so a directed rooted tree remains (LeetCode 685)."""\n'
            "    n = len(edges)\n"
            "    parent = [0] * (n + 1)\n"
            "    cand1 = cand2 = None\n"
            "    for u, v in edges:\n"
            "        if parent[v]:\n"
            "            cand1 = [parent[v], v]\n"
            "            cand2 = [u, v]\n"
            "        else:\n"
            "            parent[v] = u\n"
            "\n"
            "    def find(x, p):\n"
            "        while p[x] != x:\n"
            "            p[x] = p[p[x]]\n"
            "            x = p[x]\n"
            "        return x\n"
            "\n"
            "    def cycle_edge(skip):\n"
            "        p = list(range(n + 1))\n"
            "        for u, v in edges:\n"
            "            if skip is not None and [u, v] == skip:\n"
            "                continue\n"
            "            ru, rv = find(u, p), find(v, p)\n"
            "            if ru == rv:\n"
            "                return [u, v]\n"
            "            p[rv] = ru\n"
            "        return None\n"
            "\n"
            "    if cand1 is None:\n"
            "        return cycle_edge(None)\n"
            "    if cycle_edge(cand2) is not None:\n"
            "        return cand1\n"
            "    return cand2\n",
            lambda low: "redundant connection ii" in low,
            (
                (([[1, 2], [1, 3], [2, 3]],), [2, 3]),
                (([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]],), [4, 1]),
            ),
        ),
        T(
            "shortest_alternating_paths",
            "def shortestAlternatingPaths(n, redEdges, blueEdges):\n"
            '    """Shortest alternating-color path from 0 (LeetCode 1129)."""\n'
            "    from collections import defaultdict, deque\n"
            "    red = defaultdict(list)\n"
            "    blue = defaultdict(list)\n"
            "    for u, v in redEdges:\n"
            "        red[u].append(v)\n"
            "    for u, v in blueEdges:\n"
            "        blue[u].append(v)\n"
            "    ans = [-1] * n\n"
            "    q = deque([(0, 0, 0), (0, 1, 0)])\n"
            "    seen = {(0, 0), (0, 1)}\n"
            "    while q:\n"
            "        node, color, dist = q.popleft()\n"
            "        if ans[node] == -1 or dist < ans[node]:\n"
            "            ans[node] = dist\n"
            "        nxt = blue if color == 0 else red\n"
            "        for v in nxt[node]:\n"
            "            state = (v, 1 - color)\n"
            "            if state not in seen:\n"
            "                seen.add(state)\n"
            "                q.append((v, 1 - color, dist + 1))\n"
            "    return ans\n",
            lambda low: "alternating color" in low or "alternating colours" in low,
            (
                ((3, [[0, 1], [1, 2]], []), [0, 1, -1]),
                ((3, [[0, 1]], [[1, 2]]), [0, 1, 2]),
                ((3, [[0, 1], [0, 2]], [[1, 0]]), [0, 1, 1]),
            ),
        ),
        T(
            "network_delay_time",
            "def networkDelayTime(times, n, k):\n"
            '    """Time for a signal from k to reach every node (LeetCode 743)."""\n'
            "    import heapq\n"
            "    from collections import defaultdict\n"
            "    graph = defaultdict(list)\n"
            "    for u, v, w in times:\n"
            "        graph[u].append((v, w))\n"
            "    dist = {k: 0}\n"
            "    heap = [(0, k)]\n"
            "    while heap:\n"
            "        d, u = heapq.heappop(heap)\n"
            "        if d != dist.get(u):\n"
            "            continue\n"
            "        for v, w in graph[u]:\n"
            "            nd = d + w\n"
            "            if nd < dist.get(v, 10 ** 18):\n"
            "                dist[v] = nd\n"
            "                heapq.heappush(heap, (nd, v))\n"
            "    if len(dist) < n:\n"
            "        return -1\n"
            "    return max(dist.values())\n"
            "\n"
            "def network_delay_time(times, n, k):\n"
            "    return networkDelayTime(times, n, k)\n",
            lambda low: "network delay" in low,
            (
                (([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), 2),
                (([[1, 2, 1]], 2, 1), 1),
                (([[1, 2, 1]], 2, 2), -1),
            ),
        ),
        T(
            "cheapest_flights",
            "def findCheapestPrice(n, flights, src, dst, k):\n"
            '    """Cheapest price with at most k stops (LeetCode 787)."""\n'
            "    inf = 10 ** 18\n"
            "    dist = [inf] * n\n"
            "    dist[src] = 0\n"
            "    for _ in range(k + 1):\n"
            "        nxt = dist[:]\n"
            "        for u, v, w in flights:\n"
            "            if dist[u] < inf and dist[u] + w < nxt[v]:\n"
            "                nxt[v] = dist[u] + w\n"
            "        dist = nxt\n"
            "    return dist[dst] if dist[dst] < inf else -1\n"
            "\n"
            "def cheapest_flights(n, flights, src, dst, k):\n"
            "    return findCheapestPrice(n, flights, src, dst, k)\n",
            lambda low: "cheapest flight" in low,
            (
                (
                    (
                        4,
                        [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]],
                        0,
                        3,
                        1,
                    ),
                    700,
                ),
                ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1), 200),
                ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0), 500),
            ),
        ),
        T(
            "open_the_lock",
            "def openLock(deadends, target):\n"
            '    """Minimum turns to open a 4-dial lock (LeetCode 752)."""\n'
            "    from collections import deque\n"
            "    dead = set(deadends)\n"
            "    if '0000' in dead:\n"
            "        return -1\n"
            "    if target == '0000':\n"
            "        return 0\n"
            "    q = deque([('0000', 0)])\n"
            "    seen = {'0000'}\n"
            "    while q:\n"
            "        state, dist = q.popleft()\n"
            "        for i in range(4):\n"
            "            d = int(state[i])\n"
            "            for nd in ((d + 1) % 10, (d - 1) % 10):\n"
            "                nxt = state[:i] + str(nd) + state[i + 1:]\n"
            "                if nxt in seen or nxt in dead:\n"
            "                    continue\n"
            "                if nxt == target:\n"
            "                    return dist + 1\n"
            "                seen.add(nxt)\n"
            "                q.append((nxt, dist + 1))\n"
            "    return -1\n"
            "\n"
            "def open_lock(deadends, target):\n"
            "    return openLock(deadends, target)\n",
            lambda low: "open the lock" in low or "open lock" in low,
            (
                ((["0201", "0101", "0102", "1212", "2002"], "0202"), 6),
                ((["8888"], "0009"), 1),
                ((["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888"), -1),
            ),
        ),
        T(
            "critical_connections",
            "def criticalConnections(n, connections):\n"
            '    """Bridges of an undirected graph (LeetCode 1192)."""\n'
            "    from collections import defaultdict\n"
            "    graph = defaultdict(list)\n"
            "    for u, v in connections:\n"
            "        graph[u].append(v)\n"
            "        graph[v].append(u)\n"
            "    tin = [-1] * n\n"
            "    low = [0] * n\n"
            "    timer = 0\n"
            "    ans = []\n"
            "\n"
            "    def dfs(u, parent):\n"
            "        nonlocal timer\n"
            "        tin[u] = low[u] = timer\n"
            "        timer += 1\n"
            "        for v in graph[u]:\n"
            "            if v == parent:\n"
            "                continue\n"
            "            if tin[v] == -1:\n"
            "                dfs(v, u)\n"
            "                low[u] = min(low[u], low[v])\n"
            "                if low[v] > tin[u]:\n"
            "                    ans.append([u, v])\n"
            "            else:\n"
            "                low[u] = min(low[u], tin[v])\n"
            "\n"
            "    for i in range(n):\n"
            "        if tin[i] == -1:\n"
            "            dfs(i, -1)\n"
            "    return ans\n"
            "\n"
            "def critical_connections(n, connections):\n"
            "    return criticalConnections(n, connections)\n",
            lambda low: "critical connection" in low,
            (
                ((4, [[0, 1], [1, 2], [2, 0], [1, 3]]), [[1, 3]]),
                ((2, [[0, 1]]), [[0, 1]]),
            ),
        ),
    ]
