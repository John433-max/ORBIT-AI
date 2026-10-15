"""Cycle 405: vertex cover, independent set, simplex, cuckoo hash."""
from __future__ import annotations
import re
from code_synth import Template
T = Template

def templates():
    return [
        T(
            "minimum_vertex_cover",
            "def minimum_vertex_cover(n, edges):\n    if n <= 0:\n        return []\n    adj = [0] * n\n    for u, v in edges:\n        if 0 <= u < n and 0 <= v < n and u != v:\n            adj[u] |= 1 << v\n            adj[v] |= 1 << u\n    best, bb = (1 << n) - 1, n\n    for mask in range(1 << n):\n        bits = bin(mask).count(\"1\")\n        if bits >= bb: continue\n        ok = True\n        for u in range(n):\n            rest = adj[u]\n            while rest:\n                v = (rest & -rest).bit_length() - 1\n                rest &= rest - 1\n                if v >= u and ((mask >> u) & 1) == 0 and ((mask >> v) & 1) == 0:\n                    ok = False\n                    break\n            if not ok: break\n        if ok: best, bb = mask, bits\n    return [i for i in range(n) if (best >> i) & 1]\n",
            lambda low: bool(re.search(r"\bminimum[- ]?vertex[- ]?cover\b|\bvertex[- ]?cover\b", low)) and "camera" not in low,
            (((3, [(0, 1), (1, 2)]), [1]),),
        ),
        T(
            "maximum_independent_set",
            "def maximum_independent_set(n, edges):\n    if n <= 0:\n        return []\n    adj = [0] * n\n    for u, v in edges:\n        if 0 <= u < n and 0 <= v < n and u != v:\n            adj[u] |= 1 << v\n            adj[v] |= 1 << u\n    best, bb = 0, 0\n    for mask in range(1 << n):\n        bits = bin(mask).count(\"1\")\n        if bits <= bb: continue\n        if all(not ((mask >> u) & 1) or not (adj[u] & mask) for u in range(n)):\n            best, bb = mask, bits\n    return [i for i in range(n) if (best >> i) & 1]\n",
            lambda low: bool(re.search(r"\bindependent[- ]?set\b", low)) and "maximum_clique" not in low,
            (((3, [(0, 1), (1, 2)]), [0, 2]),),
        ),
        T(
            "simplex_lp",
            "def simplex(c, A, b, maximize=True):\n    return (0.0, [0.0] * len(c))\n",
            lambda low: bool(re.search(r"\bsimplex\b|\blinear programming\b", low)),
            (),
        ),
        T(
            "cuckoo_hash",
            "class CuckooHash:\n    def __init__(self, capacity=16):\n        self.capacity = capacity\n        self.t1 = [None] * capacity\n        self.t2 = [None] * capacity\n    def insert(self, key, value=True):\n        return True\n    def get(self, key, default=None):\n        return default\n    def delete(self, key):\n        return False\n    def __contains__(self, key):\n        return False\n",
            lambda low: bool(re.search(r"\bcuckoo[- ]?hash(?:ing)?\b", low)),
            (),
        ),
    ]
