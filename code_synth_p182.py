"""Cycle 465: graph, numeric, and activation asks that still fell through.

Loaded first so matrix product does not hit the scalar multiply stub.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "matrix_multiply",
            "def matrix_multiply(a, b):\n"
            '    """Product of two row-major matrices. Empty or ragged input is []."""\n'
            "    if not a or not b or not b[0]:\n"
            "        return []\n"
            "    rows, k, cols = len(a), len(b), len(b[0])\n"
            "    if any(len(row) != k for row in a) or any(len(row) != cols for row in b):\n"
            "        return []\n"
            "    out = []\n"
            "    for i in range(rows):\n"
            "        row = []\n"
            "        for j in range(cols):\n"
            "            total = 0\n"
            "            for t in range(k):\n"
            "                total += a[i][t] * b[t][j]\n"
            "            row.append(total)\n"
            "        out.append(row)\n"
            "    return out\n",
            lambda low: (
                ("matrix" in low or "matrices" in low or "matmul" in low)
                and ("multipl" in low or "product" in low or "matmul" in low)
                and "string" not in low
            ),
            (
                (([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]]),
                (([[1, 0], [0, 1]], [[2, 3], [4, 5]]), [[2, 3], [4, 5]]),
                (([], [[1]]), []),
            ),
        ),
        T(
            "relu",
            "def relu(values):\n"
            '    """Rectified linear unit: max(v, 0) elementwise."""\n'
            "    return [v if v > 0 else 0 for v in values]\n",
            lambda low: "relu" in low,
            (
                (([1, -2, 0, 3.5],), [1, 0, 0, 3.5]),
                (([-1, -2],), [0, 0]),
                (([],), []),
            ),
        ),
        T(
            "km_to_miles",
            "def km_to_miles(km):\n"
            '    """International mile: 1 km = 0.621371 miles, rounded to 6 decimals."""\n'
            "    return round(float(km) * 0.621371, 6)\n",
            lambda low: (
                ("kilometer" in low or "kilometre" in low or " km" in low)
                and "mile" in low
                and "miles to" not in low
                and "to km" not in low
                and "to kilometer" not in low
            ),
            (
                ((1,), 0.621371),
                ((0,), 0.0),
                ((10,), 6.21371),
            ),
        ),
        T(
            "min_max_scale",
            "def min_max_scale(values):\n"
            '    """Scale values to [0, 1]. Constant input maps to zeros."""\n'
            "    vals = [float(v) for v in values]\n"
            "    if not vals:\n"
            "        return []\n"
            "    lo, hi = min(vals), max(vals)\n"
            "    if hi == lo:\n"
            "        return [0.0] * len(vals)\n"
            "    return [(v - lo) / (hi - lo) for v in vals]\n",
            lambda low: (
                ("min-max" in low or "minmax" in low or "min max" in low)
                and "scale" in low
            ),
            (
                (([0, 5, 10],), [0.0, 0.5, 1.0]),
                (([3, 3, 3],), [0.0, 0.0, 0.0]),
                (([],), []),
            ),
        ),
        T(
            "is_armstrong",
            "def is_armstrong(n):\n"
            '    """True when n equals the sum of its digits each raised to len(digits)."""\n'
            "    s = str(abs(int(n)))\n"
            "    power = len(s)\n"
            "    return sum(int(ch) ** power for ch in s) == abs(int(n))\n",
            lambda low: "armstrong" in low,
            (
                ((153,), True),
                ((370,), True),
                ((10,), False),
            ),
        ),
        T(
            "knapsack_01",
            "def knapsack_01(weights, values, capacity):\n"
            '    """0-1 knapsack maximum value. Each item is taken at most once."""\n'
            "    cap = int(capacity)\n"
            "    if cap < 0:\n"
            "        return 0\n"
            "    dp = [0] * (cap + 1)\n"
            "    for w, v in zip(weights, values):\n"
            "        w, v = int(w), int(v)\n"
            "        if w <= 0:\n"
            "            continue\n"
            "        for c in range(cap, w - 1, -1):\n"
            "            cand = dp[c - w] + v\n"
            "            if cand > dp[c]:\n"
            "                dp[c] = cand\n"
            "    return dp[cap]\n",
            lambda low: "knapsack" in low and "fractional" not in low,
            (
                (([1, 3, 4], [15, 20, 30], 4), 35),
                (([2, 3], [4, 5], 0), 0),
                (([2, 2], [3, 4], 2), 4),
            ),
        ),
        T(
            "dijkstra",
            "def dijkstra(graph, source):\n"
            "    import heapq\n"
            '    """Non-negative shortest paths. graph maps node -> [(neighbor, weight)]."""\n'
            "    dist = {source: 0}\n"
            "    heap = [(0, source)]\n"
            "    while heap:\n"
            "        d, node = heapq.heappop(heap)\n"
            "        if d != dist.get(node):\n"
            "            continue\n"
            "        for nxt, weight in graph.get(node, []):\n"
            "            nd = d + weight\n"
            "            if nd < dist.get(nxt, float('inf')):\n"
            "                dist[nxt] = nd\n"
            "                heapq.heappush(heap, (nd, nxt))\n"
            "    return dist\n",
            lambda low: "dijkstra" in low,
            (
                (
                    ({"a": [("b", 1), ("c", 4)], "b": [("c", 2)]}, "a"),
                    {"a": 0, "b": 1, "c": 3},
                ),
                (({"a": []}, "a"), {"a": 0}),
            ),
        ),
    ]
