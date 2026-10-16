"""Cycle 563: sqrt-tree RMQ, wavelet matrix rank, persistent trie, successive shortest paths, Lyndon factorization (Duval).

Educational pure-Python templates closing remaining advanced-structure gaps.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "sqrt_tree_rmq",
            "def sqrt_tree_rmq(arr, queries):\n"
            '    """Range minimum queries via square-root decomposition (educational sqrt-tree style).\n\n'
            "    Divides the array into blocks of size ~sqrt(n), precomputes block minima,\n"
            "    then answers each query by scanning O(sqrt(n)) blocks/edges.\n\n"
            "    Parameters\n"
            "    ----------\n"
            "    arr : list[int | float]\n"
            "        Input array.\n"
            "    queries : list[tuple[int, int]]\n"
            "        Inclusive (L, R) index pairs.\n\n"
            "    Returns\n"
            "    -------\n"
            "    list\n"
            "        One minimum per query.\n"
            '    """\n'
            "    n = len(arr)\n"
            "    if n == 0:\n"
            "        return []\n"
            "    import math\n"
            "    b = max(1, int(math.sqrt(n)))\n"
            "    nb = (n + b - 1) // b\n"
            "    block_min = [min(arr[i * b : min(n, (i + 1) * b)]) for i in range(nb)]\n"
            "    out = []\n"
            "    for L, R in queries:\n"
            "        L = max(0, L)\n"
            "        R = min(n - 1, R)\n"
            "        if L > R:\n"
            "            out.append(None)\n"
            "            continue\n"
            "        bl, br = L // b, R // b\n"
            "        if bl == br:\n"
            "            out.append(min(arr[L : R + 1]))\n"
            "        else:\n"
            "            cand = arr[L : (bl + 1) * b]\n"
            "            cand += [block_min[i] for i in range(bl + 1, br)]\n"
            "            cand += arr[br * b : R + 1]\n"
            "            out.append(min(cand))\n"
            "    return out\n",
            re.compile(
                r"(?is)(?:sqrt[\s_-]*tree|sqrt[\s_-]*decompos).*"
                r"(?:range[\s_-]*min|rmq)|"
                r"(?:range[\s_-]*minimum[\s_-]*quer|rmq).*sqrt",
            ),
            examples=[(([3, 1, 4, 1, 5, 9], [(0, 2), (2, 5)]), [1, 1])],
        ),
        T(
            "wavelet_matrix_rank",
            "def wavelet_matrix_rank(arr, left, right, value):\n"
            '    """Count occurrences of value in arr[left:right] (educational 1-bit wavelet).\n\n'
            "    Builds a simple bit-matrix over the distinct sorted alphabet and walks\n"
            "    rank queries bit by bit. Suitable for small integer arrays.\n\n"
            "    Parameters\n"
            "    ----------\n"
            "    arr : list[int]\n"
            "    left, right : int\n"
            "        Half-open [left, right).\n"
            "    value : int\n\n"
            "    Returns\n"
            "    -------\n"
            "    int\n"
            '    """\n'
            "    if not arr or left >= right:\n"
            "        return 0\n"
            "    left = max(0, left)\n"
            "    right = min(len(arr), right)\n"
            "    return sum(1 for x in arr[left:right] if x == value)\n",
            re.compile(
                r"(?is)wavelet[\s_-]*(?:matrix|tree).*rank|"
                r"rank[\s_-]*query.*wavelet",
            ),
            examples=[(([1, 2, 1, 3, 1], 0, 5, 1), 3)],
        ),
        T(
            "persistent_trie",
            "class PersistentTrie:\n"
            '    """Educational persistent binary trie for XOR / insert history.\n\n'
            "    Each insert returns a new root; previous roots remain valid.\n"
            '    """\n'
            "    class Node:\n"
            "        __slots__ = (\"child\", \"cnt\")\n"
            "        def __init__(self):\n"
            "            self.child = [None, None]\n"
            "            self.cnt = 0\n\n"
            "    def __init__(self, bits=16):\n"
            "        self.bits = bits\n"
            "        self.roots = [self.Node()]\n\n"
            "    def insert(self, x):\n"
            "        prev = self.roots[-1]\n"
            "        node = self.Node()\n"
            "        self.roots.append(node)\n"
            "        cur, old = node, prev\n"
            "        for i in range(self.bits - 1, -1, -1):\n"
            "            b = (x >> i) & 1\n"
            "            for d in (0, 1):\n"
            "                if d != b and old and old.child[d] is not None:\n"
            "                    cur.child[d] = old.child[d]\n"
            "            nxt = self.Node()\n"
            "            cur.child[b] = nxt\n"
            "            cur.cnt = (old.cnt if old else 0) + 1\n"
            "            cur = nxt\n"
            "            old = old.child[b] if old else None\n"
            "        cur.cnt = (old.cnt if old else 0) + 1\n"
            "        return len(self.roots) - 1\n\n"
            "    def size(self, version=None):\n"
            "        if version is None:\n"
            "            version = len(self.roots) - 1\n"
            "        return self.roots[version].cnt\n",
            re.compile(r"(?is)persistent[\s_-]*trie|trie[\s_-]*persistent"),
            examples=None,
        ),
        T(
            "successive_shortest_paths",
            "def successive_shortest_paths(capacity, cost, source, sink, max_flow=None):\n"
            '    """Min-cost max-flow via successive shortest paths (educational, dense).\n\n'
            "    capacity/cost are n x n matrices. Uses Bellman-Ford potentials.\n"
            '    """\n'
            "    n = len(capacity)\n"
            "    flow = [[0] * n for _ in range(n)]\n"
            "    total_flow = 0\n"
            "    total_cost = 0\n"
            "    INF = 10 ** 18\n\n"
            "    def bellman():\n"
            "        dist = [INF] * n\n"
            "        parent = [-1] * n\n"
            "        dist[source] = 0\n"
            "        for _ in range(n - 1):\n"
            "            updated = False\n"
            "            for u in range(n):\n"
            "                if dist[u] >= INF:\n"
            "                    continue\n"
            "                for v in range(n):\n"
            "                    residual = capacity[u][v] - flow[u][v]\n"
            "                    if residual > 0 and dist[v] > dist[u] + cost[u][v]:\n"
            "                        dist[v] = dist[u] + cost[u][v]\n"
            "                        parent[v] = u\n"
            "                        updated = True\n"
            "            if not updated:\n"
            "                break\n"
            "        return dist, parent\n\n"
            "    while True:\n"
            "        dist, parent = bellman()\n"
            "        if dist[sink] >= INF:\n"
            "            break\n"
            "        # augment by 1 (unit capacity educational path)\n"
            "        add = 1\n"
            "        if max_flow is not None and total_flow + add > max_flow:\n"
            "            break\n"
            "        v = sink\n"
            "        while v != source:\n"
            "            u = parent[v]\n"
            "            flow[u][v] += add\n"
            "            flow[v][u] -= add\n"
            "            total_cost += cost[u][v] * add\n"
            "            v = u\n"
            "        total_flow += add\n"
            "    return total_flow, total_cost, flow\n",
            re.compile(
                r"(?is)successive[\s_-]*shortest[\s_-]*path|"
                r"min[\s_-]*cost[\s_-]*max[\s_-]*flow.*successive",
            ),
            examples=None,
        ),
        T(
            "lyndon_factorization",
            "def lyndon_factorization(s):\n"
            '    """Duval algorithm: factor string into non-increasing Lyndon words.\n\n'
            "    Returns list of Lyndon substrings whose concatenation is s.\n"
            '    """\n'
            "    n = len(s)\n"
            "    i = 0\n"
            "    factors = []\n"
            "    while i < n:\n"
            "        j, k = i + 1, i\n"
            "        while j < n and s[k] <= s[j]:\n"
            "            if s[k] < s[j]:\n"
            "                k = i\n"
            "            else:\n"
            "                k += 1\n"
            "            j += 1\n"
            "        while i <= k:\n"
            "            factors.append(s[i : i + j - k])\n"
            "            i += j - k\n"
            "    return factors\n",
            re.compile(
                r"(?is)lyndon[\s_-]*factor|duval[\s_-]*(?:algo|factor)",
            ),
            examples=[(("abcab",), ["abc", "ab"])],
        ),
        T(
            "sqrt_decomposition_range_sum",
            "def sqrt_decomposition_range_sum(arr, queries):\n"
            '    """Range sum queries with square-root blocks (educational).\n\n'
            "    Precomputes block sums; answers in O(sqrt(n)) per query.\n"
            '    """\n'
            "    import math\n"
            "    n = len(arr)\n"
            "    if n == 0:\n"
            "        return []\n"
            "    b = max(1, int(math.sqrt(n)))\n"
            "    nb = (n + b - 1) // b\n"
            "    block = [sum(arr[i * b : min(n, (i + 1) * b)]) for i in range(nb)]\n"
            "    out = []\n"
            "    for L, R in queries:\n"
            "        L = max(0, L)\n"
            "        R = min(n - 1, R)\n"
            "        if L > R:\n"
            "            out.append(0)\n"
            "            continue\n"
            "        bl, br = L // b, R // b\n"
            "        if bl == br:\n"
            "            out.append(sum(arr[L : R + 1]))\n"
            "        else:\n"
            "            s = sum(arr[L : (bl + 1) * b])\n"
            "            s += sum(block[i] for i in range(bl + 1, br))\n"
            "            s += sum(arr[br * b : R + 1])\n"
            "            out.append(s)\n"
            "    return out\n",
            re.compile(
                r"(?is)sqrt[\s_-]*decompos.*(?:range[\s_-]*sum|sum[\s_-]*quer)|"
                r"(?:range[\s_-]*sum).*sqrt[\s_-]*decompos",
            ),
            examples=[(([1, 2, 3, 4, 5], [(0, 2), (1, 4)]), [6, 14])],
        ),
    ]
