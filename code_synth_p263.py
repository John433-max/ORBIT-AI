"""Cycle 565: LFUCache, WeightedGraph, SparseTable, BinaryHeap class asks.

Educational self-contained demos so synthesize_and_verify can self-check.
Closes natural-language class asks that previously returned NotImplemented drafts.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "lfu_cache_class",
            "def lfu_cache_class_demo(capacity, ops):\n"
            '    """Replay put/get on LFUCache; return list of get results (put→None)."""\n'
            "    cache = LFUCache(capacity)\n"
            "    out = []\n"
            "    for op, args in ops:\n"
            "        if op == 'put':\n"
            "            cache.put(*args)\n"
            "            out.append(None)\n"
            "        else:\n"
            "            out.append(cache.get(*args))\n"
            "    return out\n"
            "\n"
            "\n"
            "class LFUCache:\n"
            '    """Least-frequently-used cache; ties broken by least-recent access."""\n'
            "\n"
            "    def __init__(self, capacity):\n"
            "        self.cap = int(capacity)\n"
            "        self.val = {}\n"
            "        self.freq = {}\n"
            "        self.stamp = {}\n"
            "        self.t = 0\n"
            "\n"
            "    def _touch(self, key):\n"
            "        self.t += 1\n"
            "        self.freq[key] = self.freq.get(key, 0) + 1\n"
            "        self.stamp[key] = self.t\n"
            "\n"
            "    def get(self, key):\n"
            "        if key not in self.val:\n"
            "            return -1\n"
            "        self._touch(key)\n"
            "        return self.val[key]\n"
            "\n"
            "    def put(self, key, value):\n"
            "        if self.cap <= 0:\n"
            "            return\n"
            "        if key in self.val:\n"
            "            self.val[key] = value\n"
            "            self._touch(key)\n"
            "            return\n"
            "        if len(self.val) >= self.cap:\n"
            "            victim = min(self.val, key=lambda k: (self.freq[k], self.stamp[k]))\n"
            "            del self.val[victim]\n"
            "            del self.freq[victim]\n"
            "            del self.stamp[victim]\n"
            "        self.val[key] = value\n"
            "        self.freq[key] = 0\n"
            "        self._touch(key)\n",
            lambda low: "class" in low
            and bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a| an)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| an| the)? lfu[-_ ]?cache\b|"
                    r"\blfu[-_ ]?cache class\b|"
                    r"\bclass for(?: a| the)? lfu[-_ ]?cache\b|"
                    r"\bLFUCache class\b|"
                    r"\bimplements? an? lfu[-_ ]?cache class\b|"
                    r"\bleast[- ]frequently[- ]used cache class\b",
                    low,
                )
            ),
            (
                (
                    (
                        2,
                        [
                            ("put", (1, 1)),
                            ("put", (2, 2)),
                            ("get", (1,)),
                            ("put", (3, 3)),
                            ("get", (2,)),
                            ("get", (3,)),
                        ],
                    ),
                    [None, None, 1, None, -1, 3],
                ),
                (
                    (
                        1,
                        [
                            ("put", (1, 10)),
                            ("put", (2, 20)),
                            ("get", (1,)),
                            ("get", (2,)),
                        ],
                    ),
                    [None, None, -1, 20],
                ),
            ),
        ),
        T(
            "weighted_graph_class",
            "def weighted_graph_class_demo(n, edges, src):\n"
            '    """Build WeightedGraph, return Dijkstra distances from src (inf→-1)."""\n'
            "    g = WeightedGraph(n)\n"
            "    for u, v, w in edges:\n"
            "        g.add_edge(u, v, w)\n"
            "    dist = g.dijkstra(src)\n"
            "    return [d if d < 10**18 else -1 for d in dist]\n"
            "\n"
            "\n"
            "class WeightedGraph:\n"
            '    """Directed weighted graph with Dijkstra shortest paths."""\n'
            "\n"
            "    def __init__(self, n):\n"
            "        self.n = int(n)\n"
            "        self.adj = [[] for _ in range(self.n)]\n"
            "\n"
            "    def add_edge(self, u, v, w):\n"
            "        self.adj[u].append((v, w))\n"
            "\n"
            "    def dijkstra(self, src):\n"
            "        import heapq\n"
            "        INF = 10**18\n"
            "        dist = [INF] * self.n\n"
            "        dist[src] = 0\n"
            "        pq = [(0, src)]\n"
            "        while pq:\n"
            "            d, u = heapq.heappop(pq)\n"
            "            if d != dist[u]:\n"
            "                continue\n"
            "            for v, w in self.adj[u]:\n"
            "                nd = d + w\n"
            "                if nd < dist[v]:\n"
            "                    dist[v] = nd\n"
            "                    heapq.heappush(pq, (nd, v))\n"
            "        return dist\n",
            lambda low: "class" in low
            and bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a| an)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| an| the)? weighted[-_ ]?graph\b|"
                    r"\bweighted[-_ ]?graph class\b|"
                    r"\bclass for(?: a| the)? weighted[-_ ]?graph\b|"
                    r"\bWeightedGraph class\b|"
                    r"\bimplements? an? weighted[-_ ]?graph class\b",
                    low,
                )
            ),
            (
                ((4, [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 6), (2, 3, 3)], 0), [0, 1, 3, 6]),
                ((3, [(0, 1, 5), (1, 2, 2)], 0), [0, 5, 7]),
                ((2, [(0, 1, 10)], 1), [-1, 0]),
            ),
        ),
        T(
            "sparse_table_class",
            "def sparse_table_class_demo(arr, queries):\n"
            '    """Build SparseTable for RMQ (min) and answer [L,R] inclusive queries."""\n'
            "    st = SparseTable(arr)\n"
            "    return [st.query(l, r) for l, r in queries]\n"
            "\n"
            "\n"
            "class SparseTable:\n"
            '    """Static RMQ sparse table (idempotent min over ranges)."""\n'
            "\n"
            "    def __init__(self, arr):\n"
            "        self.n = len(arr)\n"
            "        self.log = [0] * (self.n + 1)\n"
            "        for i in range(2, self.n + 1):\n"
            "            self.log[i] = self.log[i // 2] + 1\n"
            "        k = self.log[self.n] + 1\n"
            "        self.st = [[0] * self.n for _ in range(k)]\n"
            "        self.st[0] = list(arr)\n"
            "        j = 1\n"
            "        while (1 << j) <= self.n:\n"
            "            i = 0\n"
            "            while i + (1 << j) <= self.n:\n"
            "                self.st[j][i] = min(\n"
            "                    self.st[j - 1][i], self.st[j - 1][i + (1 << (j - 1))]\n"
            "                )\n"
            "                i += 1\n"
            "            j += 1\n"
            "\n"
            "    def query(self, l, r):\n"
            "        j = self.log[r - l + 1]\n"
            "        return min(self.st[j][l], self.st[j][r - (1 << j) + 1])\n",
            lambda low: "class" in low
            and bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a| an)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| an| the)? sparse[-_ ]?table\b|"
                    r"\bsparse[-_ ]?table class\b|"
                    r"\bclass for(?: a| the)? sparse[-_ ]?table\b|"
                    r"\bSparseTable class\b|"
                    r"\bimplements? an? sparse[-_ ]?table class\b",
                    low,
                )
            ),
            (
                (([1, 3, 4, 8, 6, 1, 4, 2], [(0, 2), (3, 5), (1, 6)]), [1, 1, 1]),
                (([5, 2, 9], [(0, 0), (0, 2), (1, 1)]), [5, 2, 2]),
                (([7], [(0, 0)]), [7]),
            ),
        ),
        T(
            "binary_heap_class",
            "def binary_heap_class_demo(values):\n"
            '    """Push values into BinaryHeap (min) and return ascending pops."""\n'
            "    h = BinaryHeap()\n"
            "    for v in values:\n"
            "        h.push(v)\n"
            "    out = []\n"
            "    while len(h):\n"
            "        out.append(h.pop())\n"
            "    return out\n"
            "\n"
            "\n"
            "class BinaryHeap:\n"
            '    """Binary min-heap with push/pop/peek."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self._a = []\n"
            "\n"
            "    def __len__(self):\n"
            "        return len(self._a)\n"
            "\n"
            "    def push(self, x):\n"
            "        self._a.append(x)\n"
            "        i = len(self._a) - 1\n"
            "        while i > 0:\n"
            "            p = (i - 1) // 2\n"
            "            if self._a[p] <= self._a[i]:\n"
            "                break\n"
            "            self._a[p], self._a[i] = self._a[i], self._a[p]\n"
            "            i = p\n"
            "\n"
            "    def pop(self):\n"
            "        if not self._a:\n"
            "            raise IndexError('pop from empty BinaryHeap')\n"
            "        a = self._a\n"
            "        top = a[0]\n"
            "        last = a.pop()\n"
            "        if a:\n"
            "            a[0] = last\n"
            "            i = 0\n"
            "            n = len(a)\n"
            "            while True:\n"
            "                l, r = 2 * i + 1, 2 * i + 2\n"
            "                smallest = i\n"
            "                if l < n and a[l] < a[smallest]:\n"
            "                    smallest = l\n"
            "                if r < n and a[r] < a[smallest]:\n"
            "                    smallest = r\n"
            "                if smallest == i:\n"
            "                    break\n"
            "                a[i], a[smallest] = a[smallest], a[i]\n"
            "                i = smallest\n"
            "        return top\n"
            "\n"
            "    def peek(self):\n"
            "        if not self._a:\n"
            "            raise IndexError('peek from empty BinaryHeap')\n"
            "        return self._a[0]\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a| an)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| an| the)? binary[-_ ]?heap\b|"
                    r"\bbinary[-_ ]?heap class\b|"
                    r"\bclass for(?: a| the)? binary[-_ ]?heap\b|"
                    r"\bBinaryHeap class\b|"
                    r"\bimplements? an? binary[-_ ]?heap class\b|"
                    r"\bbinary[-_ ]?(?:min[-_ ]?)?heap\b|"
                    r"\b(?:min[-_ ]?)?heap (?:insert|push|pop|extract|operations?)\b|"
                    r"\b(?:insert|push|pop|extract) (?:and )?(?:from |into )?(?:a |an )?(?:binary[-_ ]?)?(?:min[-_ ]?)?heap\b",
                    low,
                )
            )
            and "max" not in low
            and "sort" not in low
            and "priority" not in low
            and "fibonacci" not in low,
            (
                (([3, 1, 4, 1, 5, 9],), [1, 1, 3, 4, 5, 9]),
                (([10, 20, 5],), [5, 10, 20]),
                (([7],), [7]),
            ),
        ),
    ]
