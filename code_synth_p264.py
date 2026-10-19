"""Cycle 556: heavy-light decomposition, centroid decomposition,
rotating-calipers diameter, and educational link-cut path aggregate.

Self-checkable educational demos so CodeAgent probes stop returning
NotImplemented drafts for these classic advanced structures.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "sparse_table_alias_probe",
            # Keep a thin alias-free path only if p253 matcher still misses;
            # primary RMQ lives in p253. This entry is intentionally not used
            # as primary — registration order prefers earlier packs.
            "def sparse_table_rmq(arr, queries):\n"
            '    """Range minimum queries via sparse table. queries are inclusive (l, r)."""\n'
            "    n = len(arr)\n"
            "    if n == 0:\n"
            "        return [None for _ in queries]\n"
            "    import math\n"
            "    log = [0] * (n + 1)\n"
            "    for i in range(2, n + 1):\n"
            "        log[i] = log[i // 2] + 1\n"
            "    kmax = log[n] + 1\n"
            "    st = [[0] * n for _ in range(kmax)]\n"
            "    for i in range(n):\n"
            "        st[0][i] = arr[i]\n"
            "    for k in range(1, kmax):\n"
            "        half = 1 << (k - 1)\n"
            "        for i in range(n - (1 << k) + 1):\n"
            "            st[k][i] = min(st[k - 1][i], st[k - 1][i + half])\n"
            "    out = []\n"
            "    for l, r in queries:\n"
            "        if l > r or l < 0 or r >= n:\n"
            "            out.append(None)\n"
            "            continue\n"
            "        k = log[r - l + 1]\n"
            "        out.append(min(st[k][l], st[k][r - (1 << k) + 1]))\n"
            "    return out\n",
            lambda low: False,  # disabled; p253 owns the matcher after widen
            (),
        ),
        T(
            "heavy_light_path_sum",
            "def heavy_light_path_sum(n, edges, values, queries):\n"
            '    """Heavy-light decomposition path sums on a tree (0-indexed nodes).\n'
            "    edges: undirected (u, v); values[i] is node i weight.\n"
            "    queries: list of (u, v) — sum of node weights on the unique path.\n"
            '    Returns a list of path sums."""\n'
            "    g = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        g[u].append(v)\n"
            "        g[v].append(u)\n"
            "    parent = [-1] * n\n"
            "    depth = [0] * n\n"
            "    size = [1] * n\n"
            "    heavy = [-1] * n\n"
            "\n"
            "    def dfs_sz(u, p):\n"
            "        parent[u] = p\n"
            "        max_sz = 0\n"
            "        for v in g[u]:\n"
            "            if v == p:\n"
            "                continue\n"
            "            depth[v] = depth[u] + 1\n"
            "            dfs_sz(v, u)\n"
            "            size[u] += size[v]\n"
            "            if size[v] > max_sz:\n"
            "                max_sz = size[v]\n"
            "                heavy[u] = v\n"
            "\n"
            "    dfs_sz(0, -1)\n"
            "    head = [0] * n\n"
            "    pos = [0] * n\n"
            "    order = []\n"
            "\n"
            "    def dfs_hld(u, h):\n"
            "        head[u] = h\n"
            "        pos[u] = len(order)\n"
            "        order.append(u)\n"
            "        if heavy[u] != -1:\n"
            "            dfs_hld(heavy[u], h)\n"
            "            for v in g[u]:\n"
            "                if v != parent[u] and v != heavy[u]:\n"
            "                    dfs_hld(v, v)\n"
            "\n"
            "    dfs_hld(0, 0)\n"
            "    # Fenwick on HLD order for node values\n"
            "    bit = [0] * (n + 1)\n"
            "\n"
            "    def bit_add(i, delta):\n"
            "        i += 1\n"
            "        while i <= n:\n"
            "            bit[i] += delta\n"
            "            i += i & -i\n"
            "\n"
            "    def bit_sum(i):\n"
            "        s = 0\n"
            "        i += 1\n"
            "        while i > 0:\n"
            "            s += bit[i]\n"
            "            i -= i & -i\n"
            "        return s\n"
            "\n"
            "    def bit_range(l, r):\n"
            "        return bit_sum(r) - (bit_sum(l - 1) if l else 0)\n"
            "\n"
            "    for u in range(n):\n"
            "        bit_add(pos[u], values[u])\n"
            "\n"
            "    def path_sum(u, v):\n"
            "        res = 0\n"
            "        while head[u] != head[v]:\n"
            "            if depth[head[u]] < depth[head[v]]:\n"
            "                u, v = v, u\n"
            "            h = head[u]\n"
            "            res += bit_range(pos[h], pos[u])\n"
            "            u = parent[h]\n"
            "        if depth[u] > depth[v]:\n"
            "            u, v = v, u\n"
            "        res += bit_range(pos[u], pos[v])\n"
            "        return res\n"
            "\n"
            "    return [path_sum(u, v) for u, v in queries]\n",
            lambda low: bool(
                re.search(
                    r"\bheavy[- ]?light\b|"
                    r"\bhld\b|"
                    r"\bheavy light decomposition\b|"
                    r"\bpath sum\b.{0,40}\b(?:tree|hld|heavy)\b",
                    low,
                )
            )
            and "centroid" not in low
            and "link" not in low
            and "binary tree" not in low
            and "maximum path sum" not in low
            and "max path sum" not in low,
            (
                (
                    (
                        4,
                        [(0, 1), (1, 2), (1, 3)],
                        [1, 2, 3, 4],
                        [(0, 3), (2, 3), (0, 0)],
                    ),
                    [7, 9, 1],
                ),
                (
                    (
                        3,
                        [(0, 1), (0, 2)],
                        [5, 1, 1],
                        [(1, 2)],
                    ),
                    [7],
                ),
                (
                    (
                        2,
                        [(0, 1)],
                        [10, 20],
                        [(0, 1)],
                    ),
                    [30],
                ),
            ),
        ),
        T(
            "centroid_decomposition_sizes",
            "def centroid_decomposition_sizes(n, edges):\n"
            '    """Return the centroid (or any centroid) of the tree and subtree sizes\n'
            "    after removing it. edges undirected, 0-indexed.\n"
            '    Returns (centroid, sizes_dict) where sizes_dict maps remaining roots to size."""\n'
            "    g = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        g[u].append(v)\n"
            "        g[v].append(u)\n"
            "    size = [0] * n\n"
            "    dead = [False] * n\n"
            "\n"
            "    def dfs_size(u, p):\n"
            "        size[u] = 1\n"
            "        for v in g[u]:\n"
            "            if v != p and not dead[v]:\n"
            "                dfs_size(v, u)\n"
            "                size[u] += size[v]\n"
            "\n"
            "    def find_centroid(u, p, total):\n"
            "        for v in g[u]:\n"
            "            if v != p and not dead[v] and size[v] > total // 2:\n"
            "                return find_centroid(v, u, total)\n"
            "        return u\n"
            "\n"
            "    dfs_size(0, -1)\n"
            "    c = find_centroid(0, -1, size[0])\n"
            "    dead[c] = True\n"
            "    parts = {}\n"
            "    for v in g[c]:\n"
            "        if not dead[v]:\n"
            "            dfs_size(v, c)\n"
            "            parts[v] = size[v]\n"
            "    return c, parts\n",
            lambda low: bool(
                re.search(
                    r"\bcentroid[- ]?decomposition\b|"
                    r"\bcentroid of (?:a |the )?tree\b|"
                    r"\bfind(?: the)? centroid\b|"
                    r"\bcentroid decompos",
                    low,
                )
            ),
            (
                ((4, [(0, 1), (1, 2), (1, 3)]), (1, {0: 1, 2: 1, 3: 1})),
                ((3, [(0, 1), (1, 2)]), (1, {0: 1, 2: 1})),
                ((2, [(0, 1)]), (0, {1: 1})),
            ),
        ),
        T(
            "rotating_calipers_diameter",
            "def rotating_calipers_diameter(points):\n"
            '    """Diameter (max pairwise distance) of a convex polygon given in\n'
            "    counterclockwise order as list of (x, y). Uses rotating calipers.\n"
            '    Returns the squared diameter (integer-friendly)."""\n'
            "    pts = list(points)\n"
            "    n = len(pts)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    if n == 1:\n"
            "        return 0\n"
            "    if n == 2:\n"
            "        (x1, y1), (x2, y2) = pts\n"
            "        return (x1 - x2) ** 2 + (y1 - y2) ** 2\n"
            "\n"
            "    def cross(o, a, b):\n"
            "        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])\n"
            "\n"
            "    def dist2(a, b):\n"
            "        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2\n"
            "\n"
            "    # Ensure strict CCW and no duplicate consecutive points\n"
            "    j = 1\n"
            "    best = 0\n"
            "    for i in range(n):\n"
            "        while True:\n"
            "            ni = (i + 1) % n\n"
            "            nj = (j + 1) % n\n"
            "            # advance j while edge i->ni is left of edge j->nj relative to origin of motion\n"
            "            if cross(pts[i], pts[ni], (pts[ni][0] + pts[nj][0] - pts[j][0], pts[ni][1] + pts[nj][1] - pts[j][1])) > 0:\n"
            "                j = nj\n"
            "            else:\n"
            "                break\n"
            "        best = max(best, dist2(pts[i], pts[j]), dist2(pts[ni], pts[j]))\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\brotating[- ]?calipers?\b|"
                    r"\bcalipers?\b.{0,32}\bdiameter\b|"
                    r"\bdiameter\b.{0,40}\bconvex\b|"
                    r"\bconvex polygon\b.{0,40}\bdiameter\b",
                    low,
                )
            ),
            (
                (([(0, 0), (2, 0), (2, 2), (0, 2)],), 8),
                (([(0, 0), (1, 0), (0, 1)],), 2),
                (([(0, 0), (3, 0), (3, 4), (0, 4)],), 25),
            ),
        ),
        T(
            "link_cut_path_aggregate",
            "def link_cut_path_aggregate(ops):\n"
            '    """Educational path-aggregate over a forest using explicit parent links.\n'
            "    Not a full splay-based LCT; supports link/cut/path_sum for demos.\n"
            "    ops: list of tuples:\n"
            "      ('make', u, val)  — create node u with value val (idempotent)\n"
            "      ('link', u, v)   — make u a child of v (u must be root)\n"
            "      ('cut', u)       — detach u from its parent\n"
            "      ('sum', u, v)    — sum of node values on path u..v (same tree)\n"
            '    Returns list of results for each sum op (None if disconnected)."""\n'
            "    parent = {}\n"
            "    value = {}\n"
            "    children = {}\n"
            "\n"
            "    def ensure(u, val=0):\n"
            "        if u not in parent:\n"
            "            parent[u] = None\n"
            "            value[u] = val\n"
            "            children[u] = set()\n"
            "\n"
            "    def root(u):\n"
            "        while parent[u] is not None:\n"
            "            u = parent[u]\n"
            "        return u\n"
            "\n"
            "    def path_to_root(u):\n"
            "        chain = []\n"
            "        while u is not None:\n"
            "            chain.append(u)\n"
            "            u = parent[u]\n"
            "        return chain\n"
            "\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        kind = op[0]\n"
            "        if kind == 'make':\n"
            "            _, u, val = op\n"
            "            ensure(u, val)\n"
            "            value[u] = val\n"
            "        elif kind == 'link':\n"
            "            _, u, v = op\n"
            "            ensure(u)\n"
            "            ensure(v)\n"
            "            if root(u) == root(v):\n"
            "                continue\n"
            "            if parent[u] is not None:\n"
            "                continue\n"
            "            parent[u] = v\n"
            "            children[v].add(u)\n"
            "        elif kind == 'cut':\n"
            "            _, u = op\n"
            "            ensure(u)\n"
            "            p = parent[u]\n"
            "            if p is not None:\n"
            "                children[p].discard(u)\n"
            "                parent[u] = None\n"
            "        elif kind == 'sum':\n"
            "            _, u, v = op\n"
            "            ensure(u)\n"
            "            ensure(v)\n"
            "            if root(u) != root(v):\n"
            "                out.append(None)\n"
            "                continue\n"
            "            a = path_to_root(u)\n"
            "            b = path_to_root(v)\n"
            "            sa, sb = set(a), set(b)\n"
            "            # nodes on path = a + b - 2*(lca exclusive ancestors) + lca\n"
            "            i = len(a) - 1\n"
            "            j = len(b) - 1\n"
            "            while i >= 0 and j >= 0 and a[i] == b[j]:\n"
            "                i -= 1\n"
            "                j -= 1\n"
            "            lca = a[i + 1]\n"
            "            nodes = set(a[: i + 1]) | set(b[: j + 1]) | {lca}\n"
            "            out.append(sum(value[x] for x in nodes))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\blink[- ]?cut(?:[- ]?tree)?\b|"
                    r"\blct\b|"
                    r"\blink cut tree\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("make", 1, 3),
                            ("make", 2, 4),
                            ("make", 3, 5),
                            ("link", 1, 2),
                            ("link", 2, 3),
                            ("sum", 1, 3),
                            ("cut", 1),
                            ("sum", 1, 3),
                        ],
                    ),
                    [12, None],
                ),
                (
                    (
                        [
                            ("make", 0, 10),
                            ("make", 1, 1),
                            ("link", 1, 0),
                            ("sum", 0, 1),
                        ],
                    ),
                    [11],
                ),
            ),
        ),
    ]
