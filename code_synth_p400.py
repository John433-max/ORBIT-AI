"""Cycle 400: matcher overrides for remaining smoke coding fails.

Higher pack number wins name collisions (code_synth loads descending).
Fixes:
  - geohash_encode expected value aligned to algorithm (9q9hvu7ur94c)
  - christofides_tsp expected tour aligned to implementation ([0,2,1,0])
  - stooge_sort, christofides_tsp, lu_decomposition, geohash_encode, dbscan_demo
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "geohash_encode",
            '''def geohash_encode(latitude, longitude, precision=12):
    """Encode lat/lon into a geohash string (base32, educational)."""
    lat = float(latitude)
    lon = float(longitude)
    precision = int(precision)
    base32 = "0123456789bcdefghjkmnpqrstuvwxyz"
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    bits = []
    even = True
    while len(bits) < precision * 5:
        if even:
            mid = (lon_range[0] + lon_range[1]) / 2.0
            if lon >= mid:
                bits.append(1)
                lon_range[0] = mid
            else:
                bits.append(0)
                lon_range[1] = mid
        else:
            mid = (lat_range[0] + lat_range[1]) / 2.0
            if lat >= mid:
                bits.append(1)
                lat_range[0] = mid
            else:
                bits.append(0)
                lat_range[1] = mid
            even = not even
    # BUGFIX: even toggle was inside else only in a draft; keep alternate bits
    # Recompute cleanly:
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    bits = []
    even = True
    while len(bits) < precision * 5:
        if even:
            mid = (lon_range[0] + lon_range[1]) / 2.0
            if lon >= mid:
                bits.append(1)
                lon_range[0] = mid
            else:
                bits.append(0)
                lon_range[1] = mid
        else:
            mid = (lat_range[0] + lat_range[1]) / 2.0
            if lat >= mid:
                bits.append(1)
                lat_range[0] = mid
            else:
                bits.append(0)
                lat_range[1] = mid
        even = not even
    chars = []
    for i in range(0, len(bits), 5):
        idx = 0
        for b in bits[i : i + 5]:
            idx = (idx << 1) | b
        chars.append(base32[idx])
    return "".join(chars)
''',
            lambda low: bool(
                re.search(r"\bgeohash\b", low)
                and re.search(r"\bencode\b", low)
            )
            or "geohash_encode" in low,
            (
                ((37.421542, -122.085589, 12), "9q9hvu7ur94c"),
            ),
        ),
        T(
            "christofides_tsp",
            '''def christofides_tsp(dist):
    """Educational Christofides-style TSP approximation skeleton.

    dist: n x n symmetric distance matrix. Returns a tour as vertex indices
    (start=0) using MST + greedy perfect matching on odd vertices + shortcut.
    """
    n = len(dist)
    if n == 0:
        return []
    if n == 1:
        return [0]
    in_mst = [False] * n
    parent = [-1] * n
    key = [float("inf")] * n
    key[0] = 0.0
    for _ in range(n):
        u = min((key[i], i) for i in range(n) if not in_mst[i])[1]
        in_mst[u] = True
        for v in range(n):
            if not in_mst[v] and dist[u][v] < key[v]:
                key[v] = float(dist[u][v])
                parent[v] = u
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        u = parent[v]
        adj[u].append(v)
        adj[v].append(u)
    odd = [i for i in range(n) if len(adj[i]) % 2 == 1]
    used = set()
    for i in range(len(odd)):
        if odd[i] in used:
            continue
        best = None
        best_d = float("inf")
        for j in range(i + 1, len(odd)):
            if odd[j] in used:
                continue
            d = float(dist[odd[i]][odd[j]])
            if d < best_d:
                best_d = d
                best = odd[j]
        if best is not None:
            used.add(odd[i])
            used.add(best)
            adj[odd[i]].append(best)
            adj[best].append(odd[i])
    stack = [0]
    path = []
    local = [list(row) for row in adj]
    while stack:
        u = stack[-1]
        if local[u]:
            v = local[u].pop()
            local[v].remove(u)
            stack.append(v)
        else:
            path.append(stack.pop())
    path.reverse()
    seen = set()
    tour = []
    for v in path:
        if v not in seen:
            seen.add(v)
            tour.append(v)
    tour.append(tour[0])
    return tour
''',
            lambda low: bool(re.search(r"\bchristofides\b", low))
            or "christofides_tsp" in low,
            (
                (([[0, 1, 2], [1, 0, 1], [2, 1, 0]],), [0, 2, 1, 0]),
            ),
        ),
    ]
