"""Cycle 588: PageRank, k-means, Burrows-Wheeler, tortoise-hare, LZ77, HITS.

page_rank, k_means, burrows_wheeler_transform, tortoise_hare,
lz77_compress, hits_algorithm.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "page_rank",
            "def page_rank(n, edges, damping=0.85, iters=20):\n"
            '    """PageRank by power iteration on a directed graph.\n'
            "\n"
            "    edges: list of (u, v) directed links. Returns ranks rounded to 6 decimals.\n"
            "    Educational pure-Python implementation (Brin & Page).\n"
            '    """\n'
            "    if n <= 0:\n"
            "        return []\n"
            "    out = [0] * n\n"
            "    for u, v in edges:\n"
            "        out[u] += 1\n"
            "    rank = [1.0 / n] * n\n"
            "    for _ in range(iters):\n"
            "        new = [(1.0 - damping) / n] * n\n"
            "        dangling = 0.0\n"
            "        for u in range(n):\n"
            "            if out[u] == 0:\n"
            "                dangling += rank[u]\n"
            "        for u, v in edges:\n"
            "            new[v] += damping * rank[u] / out[u]\n"
            "        for v in range(n):\n"
            "            new[v] += damping * dangling / n\n"
            "        rank = new\n"
            "    return [round(r, 6) for r in rank]\n",
            lambda q: bool(re.search(r"page\s*rank|pagerank", q, re.I)),
            examples=(
                ((2, [(0, 1)], 0.85, 30), [0.350877, 0.649123]),
                ((1, [], 0.85, 5), [1.0]),
                ((3, [(0, 1), (1, 2), (2, 0)], 0.85, 20), [0.333333, 0.333333, 0.333333]),
            ),
        ),
        T(
            "k_means",
            "def k_means(points, k, max_iter=20):\n"
            '    """Lloyd k-means with deterministic first-k-point init.\n'
            "\n"
            "    points: list of numbers or sequences. Returns centers rounded to 6 decimals.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    pts = []\n"
            "    for p in points:\n"
            "        if isinstance(p, (int, float)):\n"
            "            pts.append((float(p),))\n"
            "        else:\n"
            "            pts.append(tuple(float(x) for x in p))\n"
            "    if not pts or k <= 0:\n"
            "        return []\n"
            "    k = min(k, len(pts))\n"
            "    centers = list(pts[:k])\n"
            "    dim = len(pts[0])\n"
            "    for _ in range(max_iter):\n"
            "        clusters = [[] for _ in range(k)]\n"
            "        for p in pts:\n"
            "            best = 0\n"
            "            best_d = float('inf')\n"
            "            for i in range(k):\n"
            "                d = sum((a - b) ** 2 for a, b in zip(p, centers[i]))\n"
            "                if d < best_d:\n"
            "                    best_d = d\n"
            "                    best = i\n"
            "            clusters[best].append(p)\n"
            "        new_centers = []\n"
            "        for i in range(k):\n"
            "            if not clusters[i]:\n"
            "                new_centers.append(centers[i])\n"
            "                continue\n"
            "            c = tuple(\n"
            "                round(sum(p[d] for p in clusters[i]) / len(clusters[i]), 6)\n"
            "                for d in range(dim)\n"
            "            )\n"
            "            new_centers.append(c)\n"
            "        if new_centers == centers:\n"
            "            break\n"
            "        centers = new_centers\n"
            "    return centers\n",
            lambda q: bool(re.search(r"k[- ]?means|kmeans", q, re.I)),
            examples=(
                (([0, 0, 10, 10], 2), [(10.0,), (0.0,)]),
                (([(0, 0), (0, 1), (10, 10), (11, 10)], 2), [(0.0, 0.5), (10.5, 10.0)]),
                (([1, 2, 3], 1), [(2.0,)]),
            ),
        ),
        T(
            "burrows_wheeler_transform",
            "def burrows_wheeler_transform(s):\n"
            '    """Burrows-Wheeler transform.\n'
            "\n"
            "    Appends a sentinel '$' (must not already be in s), sorts rotations,\n"
            "    and returns (last-column string, index of the original).\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    if '$' in s:\n"
            "        raise ValueError('sentinel $ must not appear in s')\n"
            "    s = s + '$'\n"
            "    rots = [s[i:] + s[:i] for i in range(len(s))]\n"
            "    rots.sort()\n"
            "    bwt = ''.join(r[-1] for r in rots)\n"
            "    idx = rots.index(s)\n"
            "    return bwt, idx\n",
            lambda q: bool(re.search(r"burrows[- ]wheeler|\bbwt\b", q, re.I)),
            examples=(
                (("banana",), ("annb$aa", 4)),
                (("abc",), ("c$ab", 1)),
                (("",), ("$", 0)),
            ),
        ),
        T(
            "tortoise_hare",
            "def tortoise_hare(seq):\n"
            '    """Floyd tortoise-and-hare cycle detection on a finite sequence treated as a functional graph.\n'
            "\n"
            "    seq[i] is the next index. Returns (mu, lambda) start and length of the cycle,\n"
            "    or (-1, -1) if no cycle is found within the sequence bounds.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    n = len(seq)\n"
            "    if n == 0:\n"
            "        return (-1, -1)\n"
            "    def nxt(i):\n"
            "        if i < 0 or i >= n:\n"
            "            return -1\n"
            "        return seq[i]\n"
            "    tortoise = nxt(0)\n"
            "    hare = nxt(nxt(0))\n"
            "    while tortoise != hare and tortoise != -1 and hare != -1:\n"
            "        tortoise = nxt(tortoise)\n"
            "        hare = nxt(nxt(hare))\n"
            "        if hare == -1:\n"
            "            break\n"
            "    if tortoise == -1 or hare == -1 or tortoise != hare:\n"
            "        return (-1, -1)\n"
            "    mu = 0\n"
            "    tortoise = 0\n"
            "    while tortoise != hare:\n"
            "        tortoise = nxt(tortoise)\n"
            "        hare = nxt(hare)\n"
            "        mu += 1\n"
            "    lam = 1\n"
            "    hare = nxt(tortoise)\n"
            "    while tortoise != hare:\n"
            "        hare = nxt(hare)\n"
            "        lam += 1\n"
            "    return (mu, lam)\n",
            lambda q: bool(
                re.search(r"tortoise|hare|floyd\s+cycle", q, re.I)
            )
            and "warshall" not in q.lower()
            and "all pairs" not in q.lower(),
            examples=(
                (([1, 2, 3, 1],), (1, 3)),
                (([1, 2, 0],), (0, 3)),
                (([1, 2, 3],), (-1, -1)),
            ),
        ),
        T(
            "lz77_compress",
            "def lz77_compress(s, window=32):\n"
            '    """Simple LZ77 compressor.\n'
            "\n"
            "    Returns a list of (offset, length, next_char) triples.\n"
            "    Educational pure-Python implementation (Lempel-Ziv 1977).\n"
            '    """\n'
            "    out = []\n"
            "    i = 0\n"
            "    n = len(s)\n"
            "    while i < n:\n"
            "        best_off, best_len = 0, 0\n"
            "        start = max(0, i - window)\n"
            "        for j in range(start, i):\n"
            "            length = 0\n"
            "            while (\n"
            "                i + length < n\n"
            "                and s[j + length] == s[i + length]\n"
            "                and length < window\n"
            "            ):\n"
            "                length += 1\n"
            "            if length > best_len:\n"
            "                best_len = length\n"
            "                best_off = i - j\n"
            "        nxt = s[i + best_len] if i + best_len < n else ''\n"
            "        out.append((best_off, best_len, nxt))\n"
            "        i += best_len + (1 if nxt else 0)\n"
            "        if not nxt and best_len == 0:\n"
            "            break\n"
            "    return out\n",
            lambda q: bool(re.search(r"\blz77\b|lempel[- ]ziv", q, re.I)),
            examples=(
                (("abcabc",), [(0, 0, "a"), (0, 0, "b"), (0, 0, "c"), (3, 3, "")]),
                (("aaaa",), [(0, 0, "a"), (1, 3, "")]),
                (("",), []),
            ),
        ),
        T(
            "hits_algorithm",
            "def hits_algorithm(n, edges, iters=20):\n"
            '    """HITS (Hyperlink-Induced Topic Search) authority/hub scores.\n'
            "\n"
            "    edges: directed (u, v) meaning u links to v.\n"
            "    Returns (authorities, hubs) rounded to 6 decimals after L2 normalization.\n"
            "    Educational pure-Python implementation (Kleinberg).\n"
            '    """\n'
            "    if n <= 0:\n"
            "        return [], []\n"
            "    auth = [1.0] * n\n"
            "    hub = [1.0] * n\n"
            "    for _ in range(iters):\n"
            "        new_auth = [0.0] * n\n"
            "        for u, v in edges:\n"
            "            new_auth[v] += hub[u]\n"
            "        new_hub = [0.0] * n\n"
            "        for u, v in edges:\n"
            "            new_hub[u] += new_auth[v]\n"
            "        def l2(xs):\n"
            "            s = sum(x * x for x in xs) ** 0.5\n"
            "            return [x / s if s else 0.0 for x in xs]\n"
            "        auth = l2(new_auth)\n"
            "        hub = l2(new_hub)\n"
            "    return (\n"
            "        [round(a, 6) for a in auth],\n"
            "        [round(h, 6) for h in hub],\n"
            "    )\n",
            lambda q: bool(re.search(r"\bhits\b|hyperlink[- ]induced", q, re.I))
            and "cache" not in q.lower(),
            examples=(
                ((2, [(0, 1)], 10), ([0.0, 1.0], [1.0, 0.0])),
                ((3, [(0, 2), (1, 2)], 10), ([0.0, 0.0, 1.0], [0.707107, 0.707107, 0.0])),
                ((1, [], 5), ([0.0], [0.0])),
            ),
        ),
    ]
