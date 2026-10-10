"""Cycle 549: Bellman-Ford, Floyd-Warshall, longest common substring, Fenwick prefix.

Loaded first so these phrases beat draft stubs and the ensure_suffix stealer.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "bellman_ford",
            "def bellman_ford(n, edges, source):\n"
            '    """Shortest paths from source. edges is a list of (u, v, w)."""\n'
            "    INF = float(\"inf\")\n"
            "    dist = [INF] * n\n"
            "    if not (0 <= source < n):\n"
            "        return [None] * n\n"
            "    dist[source] = 0\n"
            "    for _ in range(max(n - 1, 0)):\n"
            "        updated = False\n"
            "        for u, v, w in edges:\n"
            "            if 0 <= u < n and 0 <= v < n and dist[u] < INF and dist[u] + w < dist[v]:\n"
            "                dist[v] = dist[u] + w\n"
            "                updated = True\n"
            "        if not updated:\n"
            "            break\n"
            "    return [None if d == INF else d for d in dist]\n",
            lambda low: bool(
                re.search(
                    r"\bbellman(?:[- ]ford)?\b|"
                    r"\bbellman ford\b",
                    low,
                )
            ),
            (
                ((3, [(0, 1, 1), (1, 2, 2), (0, 2, 4)], 0), [0, 1, 3]),
                ((3, [(0, 1, 5), (1, 2, -2)], 0), [0, 5, 3]),
                ((2, [(1, 0, 1)], 0), [0, None]),
            ),
        ),
        T(
            "floyd_warshall",
            "def floyd_warshall(n, edges):\n"
            '    """All-pairs shortest paths. edges is a list of directed (u, v, w)."""\n'
            "    INF = float(\"inf\")\n"
            "    dist = [[INF] * n for _ in range(n)]\n"
            "    for i in range(n):\n"
            "        dist[i][i] = 0\n"
            "    for u, v, w in edges:\n"
            "        if 0 <= u < n and 0 <= v < n:\n"
            "            dist[u][v] = min(dist[u][v], w)\n"
            "    for k in range(n):\n"
            "        for i in range(n):\n"
            "            dik = dist[i][k]\n"
            "            if dik == INF:\n"
            "                continue\n"
            "            for j in range(n):\n"
            "                cand = dik + dist[k][j]\n"
            "                if cand < dist[i][j]:\n"
            "                    dist[i][j] = cand\n"
            "    return [[None if d == INF else d for d in row] for row in dist]\n",
            lambda low: bool(
                re.search(
                    r"\bfloyd(?:[- ]warshall)?\b|"
                    r"\ball[- ]pairs shortest\b",
                    low,
                )
            ),
            (
                ((3, [(0, 1, 1), (1, 2, 2)]), [[0, 1, 3], [None, 0, 2], [None, None, 0]]),
                ((2, [(0, 1, 4), (1, 0, 5)]), [[0, 4], [5, 0]]),
            ),
        ),
        T(
            "longest_common_substring",
            "def longest_common_substring(a, b):\n"
            '    """Longest contiguous substring shared by a and b (first max)."""\n'
            "    if not a or not b:\n"
            "        return \"\"\n"
            "    m, n = len(a), len(b)\n"
            "    best = 0\n"
            "    end = 0\n"
            "    prev = [0] * (n + 1)\n"
            "    for i in range(1, m + 1):\n"
            "        curr = [0] * (n + 1)\n"
            "        ai = a[i - 1]\n"
            "        for j in range(1, n + 1):\n"
            "            if ai == b[j - 1]:\n"
            "                curr[j] = prev[j - 1] + 1\n"
            "                if curr[j] > best:\n"
            "                    best = curr[j]\n"
            "                    end = i\n"
            "        prev = curr\n"
            "    return a[end - best:end]\n",
            lambda low: bool(
                re.search(
                    r"\blongest common substring\b|"
                    r"\blongest shared substring\b|"
                    r"\blcs substring\b",
                    low,
                )
            )
            and "subsequence" not in low,
            (
                (("abcde", "abfde"), "ab"),
                (("hello", "yellow"), "ello"),
                (("abcxyz", "xyzabc"), "abc"),
                (("abc", "xyz"), ""),
                (("", "abc"), ""),
            ),
        ),
        T(
            "fenwick_prefix",
            "def fenwick_prefix(n, updates, queries):\n"
            '    """1-indexed Fenwick (binary indexed tree) prefix sums."""\n'
            "    bit = [0] * (n + 1)\n"
            "\n"
            "    def add(i, delta):\n"
            "        while i <= n:\n"
            "            bit[i] += delta\n"
            "            i += i & -i\n"
            "\n"
            "    def prefix(i):\n"
            "        s = 0\n"
            "        while i > 0:\n"
            "            s += bit[i]\n"
            "            i -= i & -i\n"
            "        return s\n"
            "\n"
            "    for i, delta in updates:\n"
            "        if 1 <= i <= n:\n"
            "            add(i, delta)\n"
            "    return [prefix(q) if 0 <= q <= n else None for q in queries]\n",
            lambda low: bool(
                re.search(
                    r"\bfenwick\b|"
                    r"\bbinary indexed tree\b|"
                    r"\bbit tree\b",
                    low,
                )
            ),
            (
                ((5, [(1, 3), (3, 2), (5, 1)], [1, 3, 5, 0]), [3, 5, 6, 0]),
                ((3, [(2, 10)], [1, 2, 3]), [0, 10, 10]),
            ),
        ),
    ]
