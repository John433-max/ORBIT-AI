"""Cycle 585: number theory and graph algorithms missing from prior packs.

modular_inverse, mod_pow (binary exp), max_bipartite_matching (Kuhn DFS),
articulation_points (Tarjan), binary_lifting is already present.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "modular_inverse",
            "def modular_inverse(a, m):\n"
            '    """Return modular multiplicative inverse of a modulo m, or None if none exists.\n'
            "\n"
            "    Uses extended Euclidean algorithm. Requires gcd(a, m) == 1.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    def egcd(x, y):\n"
            "        if y == 0:\n"
            "            return x, 1, 0\n"
            "        g, s, t = egcd(y, x % y)\n"
            "        return g, t, s - (x // y) * t\n"
            "    g, x, _ = egcd(a % m, m)\n"
            "    if g != 1:\n"
            "        return None\n"
            "    return x % m\n",
            # "returns the modular inverse" is owned by mod_inverse (p173, def mod_inverse).
            lambda q: bool(re.search(r"modular[_ ]inverse|mod[_ ]inverse|multiplicative\s+inverse", q, re.I))
            and not re.search(r"returns?\s+the\s+(modular|mod)\s+inverse", q, re.I),
            examples=(((3, 11), 4), ((7, 26), 15), ((2, 4), None)),
        ),
        T(
            "mod_pow",
            "def mod_pow(base, exp, mod):\n"
            '    """Compute (base ** exp) % mod using binary exponentiation.\n'
            "\n"
            "    O(log exp) multiplications. Handles negative base by reduction.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    if mod == 1:\n"
            "        return 0\n"
            "    result = 1\n"
            "    base %= mod\n"
            "    while exp > 0:\n"
            "        if exp & 1:\n"
            "            result = (result * base) % mod\n"
            "        base = (base * base) % mod\n"
            "        exp >>= 1\n"
            "    return result\n",
            lambda q: bool(re.search(r"\bmod[_ ]?pow\b|powmod|modpow|binary\s+exponentiation", q, re.I)) and not re.search(r"modular\s+exponentiation", q, re.I),
            examples=(((2, 10, 1000), 24), ((3, 5, 13), 9), ((5, 0, 7), 1)),
        ),
        T(
            "max_bipartite_matching",
            "def max_bipartite_matching(graph):\n"
            '    """Maximum bipartite matching via Kuhn DFS (left-to-right adjacency list).\n'
            "\n"
            "    graph[u] is the list of right-side neighbors of left vertex u.\n"
            "    Returns the size of a maximum matching.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    n_left = len(graph)\n"
            "    match_r = {}\n"
            "    def dfs(u, seen):\n"
            "        for v in graph[u]:\n"
            "            if v in seen:\n"
            "                continue\n"
            "            seen.add(v)\n"
            "            if v not in match_r or dfs(match_r[v], seen):\n"
            "                match_r[v] = u\n"
            "                return True\n"
            "        return False\n"
            "    matching = 0\n"
            "    for u in range(n_left):\n"
            "        if dfs(u, set()):\n"
            "            matching += 1\n"
            "    return matching\n",
            # Kuhn DFS only. Hopcroft-Karp / "bipartite matching" -> hopcroft_karp;
            # Kuhn-Munkres / hungarian / assignment problem -> hungarian_assignment.
            lambda q: bool(re.search(r"\bkuhn\b|dfs\s+matching", q, re.I))
            and not re.search(r"\bhopcroft\b|\bmunkres\b|\bhungarian\b|\bassignment\b", q, re.I),
            examples=((
                ([[0, 1], [0], [1]],),
                2,
            ), (
                ([[0], [1], [2]],),
                3,
            ), (
                ([[0, 1], [0, 1]],),
                2,
            )),
        ),
        T(
            "articulation_points",
            "def articulation_points(n, edges):\n"
            '    """Find articulation points (cut vertices) in an undirected graph via Tarjan DFS.\n'
            "\n"
            "    edges are pairs of vertices in 0..n-1. Returns sorted list of cut vertices.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    g = [[] for _ in range(n)]\n"
            "    for a, b in edges:\n"
            "        g[a].append(b)\n"
            "        g[b].append(a)\n"
            "    disc = [-1] * n\n"
            "    low = [0] * n\n"
            "    parent = [-1] * n\n"
            "    ap = [False] * n\n"
            "    time = [0]\n"
            "    def dfs(u):\n"
            "        children = 0\n"
            "        disc[u] = low[u] = time[0]\n"
            "        time[0] += 1\n"
            "        for v in g[u]:\n"
            "            if disc[v] == -1:\n"
            "                parent[v] = u\n"
            "                children += 1\n"
            "                dfs(v)\n"
            "                low[u] = min(low[u], low[v])\n"
            "                if parent[u] == -1 and children > 1:\n"
            "                    ap[u] = True\n"
            "                if parent[u] != -1 and low[v] >= disc[u]:\n"
            "                    ap[u] = True\n"
            "            elif v != parent[u]:\n"
            "                low[u] = min(low[u], disc[v])\n"
            "    for i in range(n):\n"
            "        if disc[i] == -1:\n"
            "            dfs(i)\n"
            "    return [i for i in range(n) if ap[i]]\n",
            lambda q: bool(re.search(r"articulation\s+point|cut\s+vertex|cut\s+vertices|tarjan\s+cut", q, re.I)),
            examples=((
                (5, [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]),
                [1, 3],
            ), (
                (4, [(0, 1), (1, 2), (2, 3)]),
                [1, 2],
            ), (
                (3, [(0, 1), (1, 2), (2, 0)]),
                [],
            )),
        ),
        T(
            "extended_gcd",
            "def extended_gcd(a, b):\n"
            '    """Return (g, x, y) such that a*x + b*y = g = gcd(a, b).\n'
            "\n"
            "    Classic extended Euclidean algorithm.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    if b == 0:\n"
            "        return a, 1, 0\n"
            "    g, x1, y1 = extended_gcd(b, a % b)\n"
            "    return g, y1, x1 - (a // b) * y1\n",
            lambda q: bool(re.search(r"extended\s+(euclid|gcd)|bezout", q, re.I)),
            examples=(((30, 18), (6, -1, 2)), ((35, 15), (5, 1, -2)), ((17, 0), (17, 1, 0))),
        ),
        T(
            "sieve_of_eratosthenes",
            "def sieve_of_eratosthenes(n):\n"
            '    """Return all primes <= n using the Sieve of Eratosthenes.\n'
            "\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    if n < 2:\n"
            "        return []\n"
            "    is_prime = [True] * (n + 1)\n"
            "    is_prime[0] = is_prime[1] = False\n"
            "    p = 2\n"
            "    while p * p <= n:\n"
            "        if is_prime[p]:\n"
            "            for i in range(p * p, n + 1, p):\n"
            "                is_prime[i] = False\n"
            "        p += 1\n"
            "    return [i for i in range(2, n + 1) if is_prime[i]]\n",
            lambda q: bool(re.search(r"sieve\s+of\s+eratosthenes|eratosthenes", q, re.I)),
            examples=(((10,), [2, 3, 5, 7]), ((20,), [2, 3, 5, 7, 11, 13, 17, 19]), ((1,), [])),
        ),
    ]
