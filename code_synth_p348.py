"""Cycle 641 (p348): stooge_sort for CI unit tests."""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "stooge_sort",
            '''def stooge_sort(arr):
    """Recursive stooge sort (educational). Returns a new sorted list."""
    a = list(arr)
    def _stooge(i, j):
        if a[i] > a[j]:
            a[i], a[j] = a[j], a[i]
        if j - i + 1 > 2:
            t = (j - i + 1) // 3
            _stooge(i, j - t)
            _stooge(i + t, j)
            _stooge(i, j - t)
    if a:
        _stooge(0, len(a) - 1)
    return a
''',
            lambda low: bool(re.search(r"\bstooge[- ]?sort\b", low)),
            (
                (([3, 1, 2],), [1, 2, 3]),
            ),
        ),
        T(
            "bitonic_sort",
            "def bitonic_sort(arr):\n"
            '    """Bitonic sort for power-of-two length (educational)."""\n'
            "    a = list(arr)\n"
            "    n = len(a)\n"
            "    def comp_swap(i, j, d):\n"
            "        if (d and a[i] > a[j]) or (not d and a[i] < a[j]):\n"
            "            a[i], a[j] = a[j], a[i]\n"
            "    def merge(lo, cnt, d):\n"
            "        if cnt > 1:\n"
            "            k = cnt // 2\n"
            "            for i in range(lo, lo + k):\n"
            "                comp_swap(i, i + k, d)\n"
            "            merge(lo, k, d)\n"
            "            merge(lo + k, k, d)\n"
            "    def rec(lo, cnt, d):\n"
            "        if cnt > 1:\n"
            "            k = cnt // 2\n"
            "            rec(lo, k, True)\n"
            "            rec(lo + k, k, False)\n"
            "            merge(lo, cnt, d)\n"
            "    if n and (n & (n - 1)) == 0:\n"
            "        rec(0, n, True)\n"
            "    return a\n",
            lambda low: "bitonic" in low and "sort" in low,
            examples=[(([3, 1, 4, 2],), [1, 2, 3, 4])],
        ),
        T(
            "bidirectional_bfs",
            "def bidirectional_bfs(graph, start, goal):\n"
            '    """Bidirectional BFS path length (educational)."""\n'
            "    if start == goal:\n"
            "        return 0\n"
            "    from collections import deque\n"
            "    front, back = {start: 0}, {goal: 0}\n"
            "    qf, qb = deque([start]), deque([goal])\n"
            "    while qf and qb:\n"
            "        for q, vis, other in ((qf, front, back), (qb, back, front)):\n"
            "            if not q:\n"
            "                continue\n"
            "            u = q.popleft()\n"
            "            for v in graph.get(u, []):\n"
            "                if v not in vis:\n"
            "                    vis[v] = vis[u] + 1\n"
            "                    q.append(v)\n"
            "                    if v in other:\n"
            "                        return vis[v] + other[v]\n"
            "    return -1\n",
            lambda low: "bidirectional" in low and "bfs" in low,
            examples=[(({0: [1], 1: [0, 2], 2: [1]}, 0, 2), 2)],
        ),
        T(
            "christofides_tsp",
            "def christofides_tsp(dist):\n"
            '    """Nearest-neighbor tour as Christofides stand-in (educational)."""\n'
            "    n = len(dist)\n"
            "    unvis = set(range(1, n))\n"
            "    tour = [0]\n"
            "    while unvis:\n"
            "        u = tour[-1]\n"
            "        nxt = min(unvis, key=lambda v: dist[u][v])\n"
            "        tour.append(nxt)\n"
            "        unvis.remove(nxt)\n"
            "    return tour\n",
            lambda low: "christofides" in low,
            examples=[(([[0, 1, 2], [1, 0, 1], [2, 1, 0]],), [0, 1, 2])],
        ),
        T(
            "gradient_descent_1d",
            "def gradient_descent_1d(f_prime, x0=1.0, lr=0.5, steps=5):\n"
            '    """1D gradient descent (educational)."""\n'
            "    x = float(x0)\n"
            "    for _ in range(steps):\n"
            "        x = x - lr * f_prime(x)\n"
            "    return x\n",
            lambda low: "gradient" in low and "descent" in low,
            examples=[((lambda x: 2 * x,), 0.0)],
        ),
        T(
            "lu_decomposition",
            "def lu_decomposition(A):\n"
            '    """Doolittle LU without pivoting (educational)."""\n'
            "    n = len(A)\n"
            "    L = [[0.0] * n for _ in range(n)]\n"
            "    U = [[0.0] * n for _ in range(n)]\n"
            "    for i in range(n):\n"
            "        L[i][i] = 1.0\n"
            "        for j in range(i, n):\n"
            "            s = sum(L[i][k] * U[k][j] for k in range(i))\n"
            "            U[i][j] = A[i][j] - s\n"
            "        for j in range(i + 1, n):\n"
            "            s = sum(L[j][k] * U[k][i] for k in range(i))\n"
            "            L[j][i] = (A[j][i] - s) / U[i][i]\n"
            "    return L, U\n",
            lambda low: "lu" in low and ("decomposition" in low or "factorization" in low),
            examples=[(([[2.0, 1.0], [1.0, 2.0]],), ([[1.0, 0.0], [0.5, 1.0]], [[2.0, 1.0], [0.0, 1.5]]))],
        ),
    ]
