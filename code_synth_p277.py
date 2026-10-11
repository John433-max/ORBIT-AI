"""Cycle 579: Textbook algorithms — Karatsuba, Möbius sieve, Berlekamp–Massey,
tree diameter, Lagrange interpolation, virtual tree.

Matchers are phrase-specific so existing multiply / prime / convex / tree
templates are not stolen. Self-checking examples keep verification deterministic.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "karatsuba_mul",
            "def karatsuba_mul(x, y):\n"
            '    """Multiply two non-negative integers with Karatsuba (O(n^1.58))."""\n'
            "    if x < 0 or y < 0:\n"
            "        return karatsuba_mul(abs(x), abs(y)) * ((-1) if (x < 0) ^ (y < 0) else 1)\n"
            "    if x < 10 or y < 10:\n"
            "        return x * y\n"
            "    n = max(len(str(x)), len(str(y)))\n"
            "    m = n // 2\n"
            "    p = 10 ** m\n"
            "    a, b = divmod(x, p)\n"
            "    c, d = divmod(y, p)\n"
            "    ac = karatsuba_mul(a, c)\n"
            "    bd = karatsuba_mul(b, d)\n"
            "    ad_bc = karatsuba_mul(a + b, c + d) - ac - bd\n"
            "    return ac * (p * p) + ad_bc * p + bd\n",
            lambda low: bool(
                re.search(r"\bkaratsuba\b", low)
                or re.search(r"\bbig[- ]integer[- ]multiply\b", low)
                or re.search(r"\bfast[- ]integer[- ]multiplication\b", low)
            ),
            examples=(
                ((123456, 789012), 123456 * 789012),
                ((999, 999), 999 * 999),
                ((0, 42), 0),
                ((7, 8), 56),
            ),
        ),
        T(
            "mobius_sieve",
            "def mobius_sieve(n):\n"
            '    """Linear sieve for Möbius function μ(0)..μ(n). μ(0)=0, μ(1)=1."""\n'
            "    if n < 0:\n"
            "        raise ValueError('n >= 0')\n"
            "    mu = [0] * (n + 1)\n"
            "    if n < 1:\n"
            "        return mu\n"
            "    mu[1] = 1\n"
            "    primes = []\n"
            "    lp = [0] * (n + 1)\n"
            "    for i in range(2, n + 1):\n"
            "        if lp[i] == 0:\n"
            "            lp[i] = i\n"
            "            primes.append(i)\n"
            "            mu[i] = -1\n"
            "        for p in primes:\n"
            "            if p > lp[i] or i * p > n:\n"
            "                break\n"
            "            lp[i * p] = p\n"
            "            if p == lp[i]:\n"
            "                mu[i * p] = 0\n"
            "            else:\n"
            "                mu[i * p] = -mu[i]\n"
            "    return mu\n",
            lambda low: bool(
                re.search(r"\bm[oö]bius\b", low)
                or re.search(r"\bmu[- ]function\b", low)
                or re.search(r"\blinear[- ]sieve\b.{0,20}\b(mu|mobius|möbius)\b", low)
            ),
            examples=(
                ((10,), [0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1]),
                ((1,), [0, 1]),
                ((6,), [0, 1, -1, -1, 0, -1, 1]),
            ),
        ),
        T(
            "berlekamp_massey",
            "def berlekamp_massey(seq, mod):\n"
            '    """Minimal linear recurrence connection coefficients over Z/modZ.\n\n'
            "    Returns C[1..] such that a[n] ≡ -sum(C[i] * a[n-i]) (mod mod)\n"
            "    for the shortest LFSR generating seq (when length is sufficient).\n"
            '    """\n'
            "    n = len(seq)\n"
            "    C = [1] + [0] * n\n"
            "    B = [1] + [0] * n\n"
            "    L = 0\n"
            "    m = 1\n"
            "    b = 1\n"
            "    for N in range(n):\n"
            "        d = seq[N] % mod\n"
            "        for i in range(1, L + 1):\n"
            "            d = (d + C[i] * seq[N - i]) % mod\n"
            "        if d == 0:\n"
            "            m += 1\n"
            "        else:\n"
            "            coef = (d * pow(b, -1, mod)) % mod\n"
            "            T = C[:]\n"
            "            for i in range(m, n + 1):\n"
            "                if i - m < len(B):\n"
            "                    C[i] = (C[i] - coef * B[i - m]) % mod\n"
            "            if 2 * L <= N:\n"
            "                L = N + 1 - L\n"
            "                B = T\n"
            "                b = d\n"
            "                m = 1\n"
            "            else:\n"
            "                m += 1\n"
            "    return [c % mod for c in C[1 : L + 1]]\n",
            lambda low: bool(
                re.search(r"\bberlekamp[- ]?massey\b", low)
                or re.search(r"\bminimal[- ]linear[- ]recurrence\b", low)
                or re.search(r"\blfsr[- ]connection\b", low)
            ),
            examples=(
                (([1, 1, 2, 3, 5, 8, 3, 1], 10), [9, 9]),
                (([1, 2, 1, 2, 1, 2], 7), [0, 6]),
            ),
        ),
        T(
            "tree_diameter",
            "def tree_diameter(adj):\n"
            '    """Diameter (number of edges) of an undirected tree.\n\n'
            "    adj: dict node -> list of neighbors (or any mapping).\n"
            "    Returns 0 for empty graph.\n"
            '    """\n'
            "    from collections import deque\n"
            "    if not adj:\n"
            "        return 0\n"
            "    def far(start):\n"
            "        q = deque([(start, 0)])\n"
            "        seen = {start}\n"
            "        best = (start, 0)\n"
            "        while q:\n"
            "            u, d = q.popleft()\n"
            "            if d > best[1]:\n"
            "                best = (u, d)\n"
            "            for v in adj.get(u, []):\n"
            "                if v not in seen:\n"
            "                    seen.add(v)\n"
            "                    q.append((v, d + 1))\n"
            "        return best\n"
            "    start = next(iter(adj))\n"
            "    u, _ = far(start)\n"
            "    _, diam = far(u)\n"
            "    return diam\n",
            lambda low: bool(
                re.search(r"\btree[- ]diameter\b", low)
                or re.search(r"\bdiameter of (?:an? )?(?:undirected )?tree\b", low)
                or re.search(r"\blongest path in (?:an? )?(?:undirected )?tree\b", low)
            ),
            examples=(
                (({1: [2], 2: [1, 3], 3: [2, 4], 4: [3]},), 3),
                (({0: [1], 1: [0]},), 1),
                (({},), 0),
            ),
        ),
        T(
            "lagrange_interpolate",
            "def lagrange_interpolate(points, xq):\n"
            '    """Evaluate the unique Lagrange polynomial through points at xq.\n\n'
            "    points: sequence of (x, y) with distinct x.\n"
            "    Returns an int when the result is integral, else float.\n"
            '    """\n'
            "    from fractions import Fraction\n"
            "    result = Fraction(0)\n"
            "    for i, (xi, yi) in enumerate(points):\n"
            "        term = Fraction(yi)\n"
            "        for j, (xj, _) in enumerate(points):\n"
            "            if i == j:\n"
            "                continue\n"
            "            term *= Fraction(xq - xj, xi - xj)\n"
            "        result += term\n"
            "    if result.denominator == 1:\n"
            "        return int(result)\n"
            "    return float(result)\n",
            lambda low: bool(
                re.search(r"\blagrange\b", low)
                or re.search(r"\bpolynomial[- ]interpolation\b", low)
                or re.search(r"\binterpolate[- ]polynomial\b", low)
            ),
            examples=(
                (([(0, 1), (1, 2), (2, 5)], 3), 10),  # x^2 + 1
                (([(0, 0), (1, 1), (2, 4)], 3), 9),  # x^2
                (([(1, 4), (2, 7)], 0), 1),  # 3x + 1
            ),
        ),
        T(
            "virtual_tree",
            "def virtual_tree(parent, root, nodes):\n"
            '    """Build the virtual tree (compressed tree) on a set of nodes.\n\n'
            "    parent: list where parent[u] is parent of u (parent[root] = -1 or root).\n"
            "    nodes: iterable of node indices in the tree.\n"
            "    Returns sorted list of edges (u, v) in the virtual tree\n"
            "    (including the LCA chain of the selected nodes).\n"
            '    """\n'
            "    nodes = list(dict.fromkeys(nodes))\n"
            "    if not nodes:\n"
            "        return []\n"
            "    n = len(parent)\n"
            "    # binary lifting for LCA\n"
            "    LOG = 1\n"
            "    while (1 << LOG) <= n:\n"
            "        LOG += 1\n"
            "    up = [[-1] * n for _ in range(LOG)]\n"
            "    depth = [0] * n\n"
            "    children = [[] for _ in range(n)]\n"
            "    for u in range(n):\n"
            "        p = parent[u]\n"
            "        if p != -1 and p != u:\n"
            "            children[p].append(u)\n"
            "            up[0][u] = p\n"
            "    # DFS depth + lift\n"
            "    stack = [root]\n"
            "    seen = [False] * n\n"
            "    seen[root] = True\n"
            "    order = []\n"
            "    while stack:\n"
            "        u = stack.pop()\n"
            "        order.append(u)\n"
            "        for v in children[u]:\n"
            "            if not seen[v]:\n"
            "                seen[v] = True\n"
            "                depth[v] = depth[u] + 1\n"
            "                up[0][v] = u\n"
            "                stack.append(v)\n"
            "    for k in range(1, LOG):\n"
            "        for u in range(n):\n"
            "            mid = up[k - 1][u]\n"
            "            up[k][u] = up[k - 1][mid] if mid != -1 else -1\n"
            "    def lca(a, b):\n"
            "        if depth[a] < depth[b]:\n"
            "            a, b = b, a\n"
            "        diff = depth[a] - depth[b]\n"
            "        for k in range(LOG):\n"
            "            if diff & (1 << k):\n"
            "                a = up[k][a]\n"
            "        if a == b:\n"
            "            return a\n"
            "        for k in range(LOG - 1, -1, -1):\n"
            "            if up[k][a] != up[k][b]:\n"
            "                a = up[k][a]\n"
            "                b = up[k][b]\n"
            "        return up[0][a]\n"
            "    # include all LCAs\n"
            "    key = sorted(set(nodes))\n"
            "    extra = []\n"
            "    for i in range(1, len(key)):\n"
            "        extra.append(lca(key[i - 1], key[i]))\n"
            "    key = sorted(set(key + extra))\n"
            "    # edges: each node except root of virtual connects to its nearest ancestor in key\n"
            "    edges = []\n"
            "    for i, u in enumerate(key):\n"
            "        if i == 0:\n"
            "            continue\n"
            "        # nearest ancestor in key is the LCA of u and previous, or walk\n"
            "        # simpler: parent in virtual is the highest key that is ancestor\n"
            "        anc = key[0]\n"
            "        for v in key[:i]:\n"
            "            if depth[v] < depth[u] and lca(v, u) == v:\n"
            "                if depth[v] > depth[anc]:\n"
            "                    anc = v\n"
            "        edges.append((anc, u))\n"
            "    return sorted(edges)\n",
            lambda low: bool(
                re.search(r"\bvirtual[- ]tree\b", low)
                or re.search(r"\bcompressed[- ]tree\b", low)
                or re.search(r"\bvirtual tree on\b", low)
            ),
            examples=(
                # tree: 0-1-2, 0-3. virtual on {2,3} should include LCA 0: edges (0,2),(0,3)
                (([ -1, 0, 1, 0 ], 0, [2, 3]), [(0, 2), (0, 3)]),
                # single node
                (([-1], 0, [0]), []),
            ),
        ),
    ]
