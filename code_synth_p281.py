"""Cycle 584: unmatched textbook algorithms (push-relabel, SPFA, Borůvka MST,
linear recurrence, maximum clique / Bron-Kerbosch, chromatic number).

Natural-language probes for these still returned None from code_synth; this pack
adds educational pure-Python implementations with phrase-gated matchers.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "push_relabel_max_flow",
            '''def push_relabel_max_flow(capacity, source=0, sink=None):
    """Educational push-relabel max-flow (FIFO variant).

    capacity: n x n residual-capacity matrix (list of lists). Returns max flow value.
    """
    n = len(capacity)
    if sink is None:
        sink = n - 1
    C = [row[:] for row in capacity]
    height = [0] * n
    excess = [0] * n
    height[source] = n
    for v in range(n):
        if C[source][v] > 0:
            excess[v] += C[source][v]
            excess[source] -= C[source][v]
            C[v][source] += C[source][v]
            C[source][v] = 0

    def push(u, v):
        send = min(excess[u], C[u][v])
        C[u][v] -= send
        C[v][u] += send
        excess[u] -= send
        excess[v] += send

    def relabel(u):
        m = min(height[v] for v in range(n) if C[u][v] > 0)
        height[u] = m + 1

    active = [i for i in range(n) if i != source and i != sink and excess[i] > 0]
    while active:
        u = active.pop(0)
        pushed = False
        for v in range(n):
            if C[u][v] > 0 and height[u] == height[v] + 1:
                push(u, v)
                if v != source and v != sink and excess[v] > 0 and v not in active:
                    active.append(v)
                pushed = True
                if excess[u] == 0:
                    break
        if excess[u] > 0:
            relabel(u)
            active.append(u)
    return excess[sink]
''',
            lambda low: bool(
                re.search(r"\bpush[- ]?relabel\b|\bpreflow[- ]?push\b", low)
            ),
            (
                (([[0, 3, 2], [0, 0, 5], [0, 0, 0]], 0, 2), 5),
            ),
        ),
        T(
            "spfa_shortest_paths",
            '''def spfa_shortest_paths(n, edges, source=0):
    """Educational SPFA (queue-based Bellman-Ford) shortest paths.

    edges: list of (u, v, w). Returns distance list (inf if unreachable).
    """
    INF = 10 ** 18
    dist = [INF] * n
    dist[source] = 0
    q = [source]
    inq = [False] * n
    inq[source] = True
    while q:
        u = q.pop(0)
        inq[u] = False
        for a, b, w in edges:
            if a != u:
                continue
            if dist[u] + w < dist[b]:
                dist[b] = dist[u] + w
                if not inq[b]:
                    q.append(b)
                    inq[b] = True
    return dist
''',
            lambda low: bool(re.search(r"\bspfa\b|\bshortest.?path.?faster\b", low)),
            (
                ((3, [(0, 1, 1), (1, 2, 1), (0, 2, 5)], 0), [0, 1, 2]),
            ),
        ),
        T(
            "boruvka_mst",
            '''def boruvka_mst(n, edges):
    """Educational Borůvka MST. edges: (u, v, w). Returns total MST weight.
    """
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    components = n
    while components > 1:
        cheapest = [-1] * n
        for i, (u, v, w) in enumerate(edges):
            a, b = find(u), find(v)
            if a == b:
                continue
            if cheapest[a] == -1 or w < edges[cheapest[a]][2]:
                cheapest[a] = i
            if cheapest[b] == -1 or w < edges[cheapest[b]][2]:
                cheapest[b] = i
        added = False
        for i in range(n):
            if cheapest[i] == -1:
                continue
            u, v, w = edges[cheapest[i]]
            a, b = find(u), find(v)
            if a != b:
                parent[a] = b
                total += w
                components -= 1
                added = True
        if not added:
            break
    return total
''',
            lambda low: bool(re.search(r"\bbor[uů]vka\b|\bboruvka\b", low)),
            (
                ((3, [(0, 1, 1), (1, 2, 2), (0, 2, 4)]), 3),
            ),
        ),
        T(
            "linear_recurrence_next",
            '''def linear_recurrence_next(init, coeffs, steps):
    """Advance a linear recurrence init[0..] with coeffs for `steps` terms.

    Educational: s_{k} = sum(coeffs[i] * s_{k-1-i}). Returns the last term.
    """
    seq = list(init)
    order = len(coeffs)
    for _ in range(steps):
        nxt = 0
        for i, c in enumerate(coeffs):
            nxt += c * seq[-(i + 1)]
        seq.append(nxt)
    return seq[-1]
''',
            lambda low: bool(
                re.search(
                    r"\blinear[- ]recurrence\b|\bnext term.*recurrence\b|\brecurrence sequence\b",
                    low,
                )
                and not re.search(r"\bberlekamp\b|\bmassey\b", low)
            ),
            (
                (([1, 1], [0, 1], 10), 55),  # Fibonacci-like: F10=55 if F0=0,F1=1
            ),
        ),
        T(
            "bron_kerbosch_max_clique",
            '''def bron_kerbosch_max_clique(adj):
    """Educational Bron-Kerbosch (with pivoting omitted) max clique size.

    adj: n x n 0/1 adjacency (undirected). Returns size of maximum clique.
    """
    n = len(adj)
    best = [0]

    def bk(R, P, X):
        if not P and not X:
            best[0] = max(best[0], len(R))
            return
        for v in list(P):
            neighbors = {u for u in range(n) if adj[v][u]}
            bk(R | {v}, P & neighbors, X & neighbors)
            P.remove(v)
            X.add(v)

    bk(set(), set(range(n)), set())
    return best[0]
''',
            lambda low: bool(
                re.search(r"\bbron[- ]?kerbosch\b|\bmaximum clique\b|\bmax clique\b", low)
            ),
            (
                (([[0, 1, 1], [1, 0, 1], [1, 1, 0]],), 3),
            ),
        ),
        T(
            "chromatic_number",
            '''def chromatic_number(n, edges):
    """Educational chromatic number via backtracking (small n).

    edges: list of (u, v). Returns minimum colors needed.
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * n

    def ok(v, c):
        return all(color[u] != c for u in adj[v])

    def solve(v, k):
        if v == n:
            return True
        for c in range(k):
            if ok(v, c):
                color[v] = c
                if solve(v + 1, k):
                    return True
                color[v] = -1
        return False

    for k in range(1, n + 1):
        color[:] = [-1] * n
        if solve(0, k):
            return k
    return n
''',
            lambda low: bool(re.search(r"\bchromatic\b|\bgraph coloring\b|\bcolouring\b", low)),
            (
                ((2, [(0, 1)]), 2),
                ((1, []), 1),
            ),
        ),
    ]
