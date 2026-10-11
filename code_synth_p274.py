"""Cycle 576: Classic greedy/DP algorithm templates.

Closes educational gaps for:
- Activity selection (greedy interval scheduling, CLRS 16.1)
- Fractional knapsack (greedy by value/weight, CLRS 16.2)
- Job sequencing with deadlines (greedy profit)
- Optimal BST (DP, CLRS 15.5)
- Find bridges (Tarjan low-link)
- Min-cost max-flow (successive shortest paths, educational)

Matchers are phrase-specific so existing max_flow / knapsack_01 / critical_connections
are not stolen. Self-checking examples keep CodeAgent verification deterministic.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "activity_selection",
            "def activity_selection(starts, finishes):\n"
            '    """Select maximum non-overlapping activities (CLRS 16.1 greedy).\n\n'
            "    starts[i], finishes[i] are the start/finish of activity i.\n"
            "    Returns list of selected activity indices in order.\n"
            '    """\n'
            "    n = min(len(starts), len(finishes))\n"
            "    if n == 0:\n"
            "        return []\n"
            "    order = sorted(range(n), key=lambda i: (int(finishes[i]), int(starts[i])))\n"
            "    chosen = []\n"
            "    last_finish = -10**18\n"
            "    for i in order:\n"
            "        if int(starts[i]) >= last_finish:\n"
            "            chosen.append(i)\n"
            "            last_finish = int(finishes[i])\n"
            "    return chosen\n",
            lambda low: bool(
                re.search(r"\bactivity[- ]?selection\b", low)
                or re.search(r"\binterval[- ]?scheduling\b", low)
                or (
                    "select" in low
                    and "activit" in low
                    and ("non-overlap" in low or "compatible" in low or "maximum" in low)
                )
            ),
            examples=(
                (([1, 3, 0, 5, 8, 5], [2, 4, 6, 7, 9, 9]), [0, 1, 3, 4]),
                (([1, 2], [3, 4]), [0]),
                (([], []), []),
            ),
        ),
        T(
            "fractional_knapsack",
            "def fractional_knapsack(weights, values, capacity):\n"
            '    """Maximum value with fractional items allowed (CLRS 16.2).\n\n'
            "    Greedy by value/weight density. Returns total value (float).\n"
            '    """\n'
            "    n = min(len(weights), len(values))\n"
            "    cap = float(capacity)\n"
            "    if n == 0 or cap <= 0:\n"
            "        return 0.0\n"
            "    items = []\n"
            "    for i in range(n):\n"
            "        w = float(weights[i])\n"
            "        v = float(values[i])\n"
            "        if w > 0:\n"
            "            items.append((v / w, w, v))\n"
            "    items.sort(reverse=True)\n"
            "    total = 0.0\n"
            "    for density, w, v in items:\n"
            "        if cap <= 0:\n"
            "            break\n"
            "        take = min(w, cap)\n"
            "        total += density * take\n"
            "        cap -= take\n"
            "    return total\n",
            lambda low: bool(
                re.search(r"\bfractional[- ]?knapsack\b", low)
                or (
                    "knapsack" in low
                    and "fraction" in low
                    and "0/1" not in low
                    and "01" not in low
                )
            ),
            examples=(
                (([10, 20, 30], [60, 100, 120], 50), 240.0),
                (([10, 20], [60, 100], 15), 85.0),
                (([], [], 10), 0.0),
            ),
        ),
        T(
            "job_sequencing",
            "def job_sequencing(deadlines, profits):\n"
            '    """Schedule unit-time jobs for maximum profit under deadlines.\n\n'
            "    deadlines[i], profits[i] for job i (1-based deadline).\n"
            "    Returns (total_profit, list of chosen job indices).\n"
            '    """\n'
            "    n = min(len(deadlines), len(profits))\n"
            "    if n == 0:\n"
            "        return (0, [])\n"
            "    jobs = sorted(range(n), key=lambda i: -int(profits[i]))\n"
            "    max_d = max(int(deadlines[i]) for i in range(n))\n"
            "    slot = [-1] * (max_d + 1)\n"
            "    total = 0\n"
            "    chosen = []\n"
            "    for i in jobs:\n"
            "        d = int(deadlines[i])\n"
            "        for t in range(min(d, max_d), 0, -1):\n"
            "            if slot[t] == -1:\n"
            "                slot[t] = i\n"
            "                total += int(profits[i])\n"
            "                chosen.append(i)\n"
            "                break\n"
            "    chosen.sort()\n"
            "    return (total, chosen)\n",
            lambda low: bool(
                re.search(r"\bjob[- ]?sequenc", low)
                or re.search(r"\bjob[- ]?scheduling\b", low)
                or (
                    "deadline" in low
                    and "profit" in low
                    and ("job" in low or "schedule" in low)
                )
            ),
            examples=(
                (([4, 1, 1, 1], [20, 10, 40, 30]), (60, [0, 2])),
                (([2, 1, 2, 1], [100, 19, 27, 25]), (127, [0, 2])),
                (([], []), (0, [])),
            ),
        ),
        T(
            "optimal_bst",
            "def optimal_bst(freqs):\n"
            '    """Minimum expected search cost for optimal BST (CLRS 15.5).\n\n'
            "    freqs[i] is the probability/frequency of key i.\n"
            "    Returns the minimum expected cost (float).\n"
            '    """\n'
            "    n = len(freqs)\n"
            "    if n == 0:\n"
            "        return 0.0\n"
            "    p = [float(x) for x in freqs]\n"
            "    # cost[i][j] = min cost for keys i..j inclusive\n"
            "    cost = [[0.0] * n for _ in range(n)]\n"
            "    # prefix sums for range frequency\n"
            "    pref = [0.0] * (n + 1)\n"
            "    for i in range(n):\n"
            "        pref[i + 1] = pref[i] + p[i]\n"
            "        cost[i][i] = p[i]\n"
            "    for length in range(2, n + 1):\n"
            "        for i in range(0, n - length + 1):\n"
            "            j = i + length - 1\n"
            "            w = pref[j + 1] - pref[i]\n"
            "            best = float('inf')\n"
            "            for r in range(i, j + 1):\n"
            "                left = cost[i][r - 1] if r > i else 0.0\n"
            "                right = cost[r + 1][j] if r < j else 0.0\n"
            "                best = min(best, left + right)\n"
            "            cost[i][j] = best + w\n"
            "    return cost[0][n - 1]\n",
            lambda low: bool(
                re.search(r"\boptimal[- ]?bst\b", low)
                or re.search(r"\boptimal[- ]?binary[- ]?search[- ]?tree\b", low)
                or (
                    "optimal" in low
                    and "binary search tree" in low
                )
            ),
            examples=(
                (([0.25, 0.25, 0.25, 0.25],), 2.0),
                (([0.2, 0.3, 0.5],), 1.7),
                (([],), 0.0),
            ),
        ),
        T(
            "find_bridges",
            "def find_bridges(n, edges):\n"
            '    """Find all bridges in an undirected graph (Tarjan low-link).\n\n'
            "    n = number of nodes 0..n-1; edges = list of [u,v] pairs.\n"
            "    Returns list of bridge edges [u,v] with u < v.\n"
            '    """\n'
            "    g = [[] for _ in range(n)]\n"
            "    for e in edges:\n"
            "        u, v = int(e[0]), int(e[1])\n"
            "        g[u].append(v)\n"
            "        g[v].append(u)\n"
            "    disc = [-1] * n\n"
            "    low = [-1] * n\n"
            "    parent = [-1] * n\n"
            "    bridges = []\n"
            "    time = [0]\n"
            "\n"
            "    def dfs(u):\n"
            "        disc[u] = low[u] = time[0]\n"
            "        time[0] += 1\n"
            "        for v in g[u]:\n"
            "            if disc[v] == -1:\n"
            "                parent[v] = u\n"
            "                dfs(v)\n"
            "                low[u] = min(low[u], low[v])\n"
            "                if low[v] > disc[u]:\n"
            "                    bridges.append([min(u, v), max(u, v)])\n"
            "            elif v != parent[u]:\n"
            "                low[u] = min(low[u], disc[v])\n"
            "\n"
            "    for i in range(n):\n"
            "        if disc[i] == -1:\n"
            "            dfs(i)\n"
            "    bridges.sort()\n"
            "    return bridges\n"
            "\n"
            "def criticalConnections(n, connections):\n"
            "    return find_bridges(n, connections)\n",
            lambda low: bool(
                re.search(r"\bfind[- ]?bridges?\b", low)
                or re.search(r"\bbridge[- ]?find", low)
                or re.search(r"\bbridges? in (?:an? )?(?:undirected )?graph\b", low)
                or (
                    "bridge" in low
                    and "graph" in low
                    and "critical" not in low
                )
            ),
            examples=(
                ((4, [[0, 1], [1, 2], [2, 0], [1, 3]]), [[1, 3]]),
                ((2, [[0, 1]]), [[0, 1]]),
                ((3, [[0, 1], [1, 2], [2, 0]]), []),
            ),
        ),
        T(
            "min_cost_flow",
            "def min_cost_flow(n, edges, source, sink, demand):\n"
            '    """Min-cost max-flow up to `demand` via successive shortest paths.\n\n'
            "    edges: list of (u, v, capacity, cost).\n"
            "    Returns (flow_sent, total_cost). Educational O(F * V * E) implementation.\n"
            '    """\n'
            "    INF = 10**18\n"
            "    # residual: list of [to, rev, cap, cost]\n"
            "    g = [[] for _ in range(n)]\n"
            "\n"
            "    def add_edge(u, v, cap, cost):\n"
            "        g[u].append([v, len(g[v]), cap, cost])\n"
            "        g[v].append([u, len(g[u]) - 1, 0, -cost])\n"
            "\n"
            "    for e in edges:\n"
            "        u, v, cap, cost = int(e[0]), int(e[1]), int(e[2]), int(e[3])\n"
            "        add_edge(u, v, cap, cost)\n"
            "\n"
            "    flow = 0\n"
            "    cost_sum = 0\n"
            "    demand = int(demand)\n"
            "    source, sink = int(source), int(sink)\n"
            "\n"
            "    while flow < demand:\n"
            "        dist = [INF] * n\n"
            "        prev_v = [-1] * n\n"
            "        prev_e = [-1] * n\n"
            "        dist[source] = 0\n"
            "        updated = True\n"
            "        for _ in range(n):\n"
            "            if not updated:\n"
            "                break\n"
            "            updated = False\n"
            "            for v in range(n):\n"
            "                if dist[v] == INF:\n"
            "                    continue\n"
            "                for i, (to, rev, cap, c) in enumerate(g[v]):\n"
            "                    if cap > 0 and dist[to] > dist[v] + c:\n"
            "                        dist[to] = dist[v] + c\n"
            "                        prev_v[to] = v\n"
            "                        prev_e[to] = i\n"
            "                        updated = True\n"
            "        if dist[sink] == INF:\n"
            "            break\n"
            "        # augment\n"
            "        aug = demand - flow\n"
            "        v = sink\n"
            "        while v != source:\n"
            "            pv = prev_v[v]\n"
            "            pe = prev_e[v]\n"
            "            aug = min(aug, g[pv][pe][2])\n"
            "            v = pv\n"
            "        v = sink\n"
            "        while v != source:\n"
            "            pv = prev_v[v]\n"
            "            pe = prev_e[v]\n"
            "            g[pv][pe][2] -= aug\n"
            "            rev = g[pv][pe][1]\n"
            "            g[v][rev][2] += aug\n"
            "            v = pv\n"
            "        flow += aug\n"
            "        cost_sum += aug * dist[sink]\n"
            "    return (flow, cost_sum)\n",
            lambda low: bool(
                re.search(r"\bmin(?:imum)?[- ]?cost[- ]?(?:max[- ]?)?flow\b", low)
                or re.search(r"\bmin[- ]?cost[- ]?max[- ]?flow\b", low)
                or (
                    "min" in low
                    and "cost" in low
                    and "flow" in low
                    and "cut" not in low
                )
            ),
            examples=(
                (
                    (
                        4,
                        [[0, 1, 2, 2], [0, 2, 2, 5], [1, 2, 1, 1], [1, 3, 2, 4], [2, 3, 2, 3]],
                        0,
                        3,
                        3,
                    ),
                    (3, 20),
                ),
                ((2, [[0, 1, 5, 1]], 0, 1, 3), (3, 3)),
                ((2, [], 0, 1, 1), (0, 0)),
            ),
        ),
    ]
