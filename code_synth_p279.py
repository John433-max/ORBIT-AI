"""Cycle 582: textbook algorithms missing from smoke (strassen, gaussian, newton, simhash, johnson).

Bare titles in evals/datasets/smoke.jsonl fell through to NotImplemented drafts
or were stolen by matrix_multiply / science_math.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "strassen_mul",
            "def strassen_mul(a, b):\n"
            '    """Strassen matrix product for square power-of-two matrices.\n'
            "\n"
            "    Educational exact implementation. 1x1 is the base case;\n"
            "    larger n splits into quadrants and uses the 7-multiplication recurrence.\n"
            '    """\n'
            "    n = len(a)\n"
            "    if n == 1:\n"
            "        return [[a[0][0] * b[0][0]]]\n"
            "    mid = n // 2\n"
            "\n"
            "    def split(m):\n"
            "        return (\n"
            "            [row[:mid] for row in m[:mid]],\n"
            "            [row[mid:] for row in m[:mid]],\n"
            "            [row[:mid] for row in m[mid:]],\n"
            "            [row[mid:] for row in m[mid:]],\n"
            "        )\n"
            "\n"
            "    def add(x, y):\n"
            "        return [[x[i][j] + y[i][j] for j in range(len(x))] for i in range(len(x))]\n"
            "\n"
            "    def sub(x, y):\n"
            "        return [[x[i][j] - y[i][j] for j in range(len(x))] for i in range(len(x))]\n"
            "\n"
            "    A11, A12, A21, A22 = split(a)\n"
            "    B11, B12, B21, B22 = split(b)\n"
            "    M1 = strassen_mul(add(A11, A22), add(B11, B22))\n"
            "    M2 = strassen_mul(add(A21, A22), B11)\n"
            "    M3 = strassen_mul(A11, sub(B12, B22))\n"
            "    M4 = strassen_mul(A22, sub(B21, B11))\n"
            "    M5 = strassen_mul(add(A11, A12), B22)\n"
            "    M6 = strassen_mul(sub(A21, A11), add(B11, B12))\n"
            "    M7 = strassen_mul(sub(A12, A22), add(B21, B22))\n"
            "    C11 = add(sub(add(M1, M4), M5), M7)\n"
            "    C12 = add(M3, M5)\n"
            "    C21 = add(M2, M4)\n"
            "    C22 = add(sub(add(M1, M3), M2), M6)\n"
            "    out = []\n"
            "    for i in range(mid):\n"
            "        out.append(C11[i] + C12[i])\n"
            "    for i in range(mid):\n"
            "        out.append(C21[i] + C22[i])\n"
            "    return out\n",
            lambda low: bool(re.search(r"\bstrassen\b", low)),
            (
                (([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]]),
                (([[1, 0], [0, 1]], [[2, 3], [4, 5]]), [[2, 3], [4, 5]]),
            ),
        ),
        T(
            "gaussian_elimination",
            "def gaussian_elimination(a, b):\n"
            '    """Solve Ax = b by Gaussian elimination with partial pivoting.\n'
            "\n"
            "    a is an n x n matrix, b a length-n vector. Returns the solution\n"
            "    as a list of floats rounded to 10 decimals. Raises ValueError if singular.\n"
            '    """\n'
            "    n = len(a)\n"
            "    m = [row[:] + [b[i]] for i, row in enumerate(a)]\n"
            "    for col in range(n):\n"
            "        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))\n"
            "        m[col], m[pivot] = m[pivot], m[col]\n"
            "        piv = m[col][col]\n"
            "        if abs(piv) < 1e-12:\n"
            '            raise ValueError("singular")\n'
            "        for j in range(col, n + 1):\n"
            "            m[col][j] /= piv\n"
            "        for r in range(n):\n"
            "            if r == col:\n"
            "                continue\n"
            "            factor = m[r][col]\n"
            "            for j in range(col, n + 1):\n"
            "                m[r][j] -= factor * m[col][j]\n"
            "    return [round(m[i][n], 10) for i in range(n)]\n",
            lambda low: bool(
                re.search(r"\bgaussian[- ]elimination\b", low)
                or re.search(r"\bgauss[- ]jordan\b", low)
            ),
            (
                (([[2, 1], [1, 3]], [5, 10]), [1.0, 3.0]),
                (([[1, 0], [0, 1]], [4, 7]), [4.0, 7.0]),
            ),
        ),
        T(
            "newton_raphson",
            "def newton_raphson(f, fprime, x0, tol=1e-12, max_iter=50):\n"
            '    """Newton-Raphson root finder.\n'
            "\n"
            "    f and fprime are callables. Starts at x0 and iterates\n"
            "    x := x - f(x)/f'(x) until the step is below tol.\n"
            "    Returns the estimate rounded to 10 decimals.\n"
            '    """\n'
            "    x = float(x0)\n"
            "    for _ in range(max_iter):\n"
            "        fx = f(x)\n"
            "        df = fprime(x)\n"
            "        if df == 0:\n"
            "            break\n"
            "        nxt = x - fx / df\n"
            "        if abs(nxt - x) < tol:\n"
            "            return round(nxt, 10)\n"
            "        x = nxt\n"
            "    return round(x, 10)\n",
            lambda low: bool(
                re.search(r"\bnewton[- ]?raphson\b", low)
                or re.search(r"\bnewton'?s? method\b", low)
            )
            and "cooling" not in low,
            (
                ((lambda x: x * x - 4, lambda x: 2 * x, 1.0), 2.0),
                ((lambda x: x * x - 9, lambda x: 2 * x, 1.0), 3.0),
            ),
        ),
        T(
            "simhash",
            "def simhash(tokens, bits=16):\n"
            '    """SimHash fingerprint of tokens (or a whitespace-split string).\n'
            "\n"
            "    Returns an integer of `bits` width. Identical token multisets\n"
            "    produce the same fingerprint.\n"
            '    """\n'
            "    if isinstance(tokens, str):\n"
            "        tokens = tokens.split()\n"
            "    v = [0] * bits\n"
            "    for tok in tokens:\n"
            "        h = 2166136261\n"
            "        for ch in str(tok):\n"
            "            h ^= ord(ch)\n"
            "            h = (h * 16777619) & 0xFFFFFFFF\n"
            "        for i in range(bits):\n"
            "            bit = (h >> (i % 32)) & 1\n"
            "            v[i] += 1 if bit else -1\n"
            "    out = 0\n"
            "    for i, val in enumerate(v):\n"
            "        if val > 0:\n"
            "            out |= 1 << i\n"
            "    return out\n",
            lambda low: bool(re.search(r"\bsimhash\b", low)),
            (
                ((["cat", "sat", "on", "mat"],), 5333),
                ((["cat", "sat", "on", "mat", "cat"],), 23767),
                (([],), 0),
            ),
        ),
        T(
            "johnson_apsp",
            "def johnson_apsp(n, edges):\n"
            '    """Johnson all-pairs shortest paths.\n'
            "\n"
            "    n: node count (nodes 0..n-1). edges: list of (u, v, w).\n"
            "    Returns an n x n matrix of distances (None if unreachable),\n"
            "    or None if a negative cycle is reachable from the dummy source.\n"
            '    """\n'
            "    import heapq\n"
            "    import math\n"
            "\n"
            "    h = [0.0] * (n + 1)\n"
            "    ext = list(edges) + [(n, i, 0) for i in range(n)]\n"
            "    for _ in range(n):\n"
            "        updated = False\n"
            "        for u, v, w in ext:\n"
            "            if h[u] + w < h[v]:\n"
            "                h[v] = h[u] + w\n"
            "                updated = True\n"
            "        if not updated:\n"
            "            break\n"
            "    else:\n"
            "        for u, v, w in ext:\n"
            "            if h[u] + w < h[v] - 1e-12:\n"
            "                return None\n"
            "    adj = [[] for _ in range(n)]\n"
            "    for u, v, w in edges:\n"
            "        adj[u].append((v, w + h[u] - h[v]))\n"
            "    dist = []\n"
            "    for s in range(n):\n"
            "        d = [math.inf] * n\n"
            "        d[s] = 0.0\n"
            "        pq = [(0.0, s)]\n"
            "        while pq:\n"
            "            du, u = heapq.heappop(pq)\n"
            "            if du > d[u]:\n"
            "                continue\n"
            "            for v, w in adj[u]:\n"
            "                nd = du + w\n"
            "                if nd < d[v]:\n"
            "                    d[v] = nd\n"
            "                    heapq.heappush(pq, (nd, v))\n"
            "        row = []\n"
            "        for v in range(n):\n"
            "            if d[v] == math.inf:\n"
            "                row.append(None)\n"
            "            else:\n"
            "                row.append(round(d[v] - h[s] + h[v], 10))\n"
            "        dist.append(row)\n"
            "    return dist\n",
            lambda low: bool(
                re.search(r"\bjohnson(?:'s)?\b", low)
                and (
                    "shortest" in low
                    or "apsp" in low
                    or "all-pairs" in low
                    or "all pairs" in low
                    or "algorithm" in low
                )
            ),
            (
                ((3, [(0, 1, 1), (1, 2, 2), (0, 2, 4)]), [[0.0, 1.0, 3.0], [None, 0.0, 2.0], [None, None, 0.0]]),
                ((2, [(0, 1, -1), (1, 0, 2)]), [[0.0, -1.0], [2.0, 0.0]]),
            ),
        ),
    ]
