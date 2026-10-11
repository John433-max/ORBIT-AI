"""Cycle 569: FibonacciHeap, KDTree, QuadTree, and SuffixTree class templates.

Loaded first so class phrases beat broad string matchers (ensure_suffix
steals "SuffixTree") and draft stubs. Educational, self-checkable demos.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "fibonacci_heap_class",
            "def fib_heap_demo(values):\n"
            '    """Insert then extract-min to exercise FibonacciHeap."""\n'
            "    heap = FibonacciHeap()\n"
            "    for value in values:\n"
            "        heap.insert(value)\n"
            "    out = []\n"
            "    while heap.find_min() is not None:\n"
            "        out.append(heap.extract_min())\n"
            "    return out\n"
            "\n"
            "\n"
            "class _FHNode:\n"
            "    def __init__(self, key):\n"
            "        self.key = key\n"
            "        self.child = None\n"
            "        self.next = self\n"
            "        self.degree = 0\n"
            "\n"
            "\n"
            "class FibonacciHeap:\n"
            '    """Educational Fibonacci heap: insert, find_min, extract_min."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.min = None\n"
            "        self.n = 0\n"
            "\n"
            "    def insert(self, key):\n"
            "        node = _FHNode(key)\n"
            "        if self.min is None:\n"
            "            self.min = node\n"
            "        else:\n"
            "            node.next = self.min.next\n"
            "            self.min.next = node\n"
            "            if key < self.min.key:\n"
            "                self.min = node\n"
            "        self.n += 1\n"
            "        return node\n"
            "\n"
            "    def find_min(self):\n"
            "        return None if self.min is None else self.min.key\n"
            "\n"
            "    def extract_min(self):\n"
            "        if self.min is None:\n"
            "            return None\n"
            "        z = self.min\n"
            "        if z.child is not None:\n"
            "            kids = []\n"
            "            c = z.child\n"
            "            while True:\n"
            "                kids.append(c)\n"
            "                c = c.next\n"
            "                if c is z.child:\n"
            "                    break\n"
            "            for c in kids:\n"
            "                c.next = self.min.next\n"
            "                self.min.next = c\n"
            "        if z.next is z:\n"
            "            self.min = None\n"
            "        else:\n"
            "            prev = z\n"
            "            while prev.next is not z:\n"
            "                prev = prev.next\n"
            "            prev.next = z.next\n"
            "            self.min = z.next\n"
            "            self._consolidate()\n"
            "        self.n -= 1\n"
            "        return z.key\n"
            "\n"
            "    def _roots(self):\n"
            "        if self.min is None:\n"
            "            return []\n"
            "        out = []\n"
            "        x = self.min\n"
            "        while True:\n"
            "            out.append(x)\n"
            "            x = x.next\n"
            "            if x is self.min:\n"
            "                break\n"
            "        return out\n"
            "\n"
            "    def _consolidate(self):\n"
            "        roots = self._roots()\n"
            "        if not roots:\n"
            "            return\n"
            "        degree_table = {}\n"
            "        for w in roots:\n"
            "            x = w\n"
            "            d = x.degree\n"
            "            while d in degree_table:\n"
            "                y = degree_table[d]\n"
            "                if x.key > y.key:\n"
            "                    x, y = y, x\n"
            "                x.degree += 1\n"
            "                if x.child is None:\n"
            "                    y.next = y\n"
            "                else:\n"
            "                    y.next = x.child.next\n"
            "                    x.child.next = y\n"
            "                x.child = y\n"
            "                del degree_table[d]\n"
            "                d = x.degree\n"
            "            degree_table[d] = x\n"
            "        self.min = None\n"
            "        for node in degree_table.values():\n"
            "            node.next = node\n"
            "            if self.min is None:\n"
            "                self.min = node\n"
            "            else:\n"
            "                node.next = self.min.next\n"
            "                self.min.next = node\n"
            "                if node.key < self.min.key:\n"
            "                    self.min = node\n",
            lambda low: bool(
                re.search(
                    r"\bfibonacci[- ]?heap\b|"
                    r"\bfibonacciheap\b|"
                    r"\bfib[- ]heap\b",
                    low,
                )
            )
            and "function" not in low
            and "number" not in low,
            (
                (([5, 1, 9, 3, 1],), [1, 1, 3, 5, 9]),
                (([],), []),
                (([4],), [4]),
            ),
        ),
        T(
            "kd_tree_class",
            "def kd_tree_demo(points, query):\n"
            '    """Insert 2D points and return the nearest neighbor."""\n'
            "    tree = KDTree()\n"
            "    for point in points:\n"
            "        tree.insert(point)\n"
            "    return tree.nearest(query)\n"
            "\n"
            "\n"
            "class _KDNode:\n"
            "    def __init__(self, point, axis):\n"
            "        self.point = point\n"
            "        self.axis = axis\n"
            "        self.left = None\n"
            "        self.right = None\n"
            "\n"
            "\n"
            "class KDTree:\n"
            '    """Educational 2D KD-tree: insert + nearest neighbor."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.root = None\n"
            "\n"
            "    def insert(self, point):\n"
            "        def _ins(node, pt, axis):\n"
            "            if node is None:\n"
            "                return _KDNode(tuple(pt), axis)\n"
            "            if pt[axis] < node.point[axis]:\n"
            "                node.left = _ins(node.left, pt, 1 - axis)\n"
            "            else:\n"
            "                node.right = _ins(node.right, pt, 1 - axis)\n"
            "            return node\n"
            "\n"
            "        self.root = _ins(self.root, tuple(point), 0)\n"
            "\n"
            "    def nearest(self, query):\n"
            "        best = [None, float(\"inf\")]\n"
            "\n"
            "        def _nn(node):\n"
            "            if node is None:\n"
            "                return\n"
            "            dx = node.point[0] - query[0]\n"
            "            dy = node.point[1] - query[1]\n"
            "            dist = dx * dx + dy * dy\n"
            "            if dist < best[1]:\n"
            "                best[0] = node.point\n"
            "                best[1] = dist\n"
            "            diff = query[node.axis] - node.point[node.axis]\n"
            "            first, second = (\n"
            "                (node.left, node.right)\n"
            "                if diff < 0\n"
            "                else (node.right, node.left)\n"
            "            )\n"
            "            _nn(first)\n"
            "            if diff * diff < best[1]:\n"
            "                _nn(second)\n"
            "\n"
            "        _nn(self.root)\n"
            "        return best[0]\n",
            lambda low: bool(
                re.search(
                    r"\bkd[- ]?tree\b|"
                    r"\bk[- ]d tree\b|"
                    r"\bkdtree\b",
                    low,
                )
            ),
            (
                (([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]], [9, 2]), (8, 1)),
                (([[0, 0]], [1, 1]), (0, 0)),
            ),
        ),
        T(
            "quad_tree_class",
            "def quad_tree_demo(points, region):\n"
            '    """Insert points into a QuadTree and query a rectangular region."""\n'
            "    tree = QuadTree((0, 0, 100, 100))\n"
            "    for point in points:\n"
            "        tree.insert(point)\n"
            "    return sorted(tree.query(region))\n"
            "\n"
            "\n"
            "class QuadTree:\n"
            '    """Educational point QuadTree: insert + rectangular query."""\n'
            "\n"
            "    def __init__(self, boundary, capacity=4):\n"
            "        self.x0, self.y0, self.x1, self.y1 = boundary\n"
            "        self.capacity = capacity\n"
            "        self.points = []\n"
            "        self.divided = False\n"
            "        self.nw = None\n"
            "        self.ne = None\n"
            "        self.sw = None\n"
            "        self.se = None\n"
            "\n"
            "    def insert(self, point):\n"
            "        x, y = point\n"
            "        if not (self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1):\n"
            "            return False\n"
            "        if len(self.points) < self.capacity and not self.divided:\n"
            "            self.points.append((x, y))\n"
            "            return True\n"
            "        if not self.divided:\n"
            "            self._subdivide()\n"
            "        return (\n"
            "            self.nw.insert(point)\n"
            "            or self.ne.insert(point)\n"
            "            or self.sw.insert(point)\n"
            "            or self.se.insert(point)\n"
            "        )\n"
            "\n"
            "    def _subdivide(self):\n"
            "        mx = (self.x0 + self.x1) / 2\n"
            "        my = (self.y0 + self.y1) / 2\n"
            "        self.nw = QuadTree((self.x0, my, mx, self.y1), self.capacity)\n"
            "        self.ne = QuadTree((mx, my, self.x1, self.y1), self.capacity)\n"
            "        self.sw = QuadTree((self.x0, self.y0, mx, my), self.capacity)\n"
            "        self.se = QuadTree((mx, self.y0, self.x1, my), self.capacity)\n"
            "        self.divided = True\n"
            "        old = self.points\n"
            "        self.points = []\n"
            "        for p in old:\n"
            "            self.insert(p)\n"
            "\n"
            "    def query(self, region):\n"
            "        rx0, ry0, rx1, ry1 = region\n"
            "        if rx1 < self.x0 or rx0 > self.x1 or ry1 < self.y0 or ry0 > self.y1:\n"
            "            return []\n"
            "        found = [\n"
            "            p\n"
            "            for p in self.points\n"
            "            if rx0 <= p[0] <= rx1 and ry0 <= p[1] <= ry1\n"
            "        ]\n"
            "        if self.divided:\n"
            "            found += self.nw.query(region)\n"
            "            found += self.ne.query(region)\n"
            "            found += self.sw.query(region)\n"
            "            found += self.se.query(region)\n"
            "        return found\n",
            lambda low: bool(
                re.search(
                    r"\bquad[- ]?tree\b|"
                    r"\bquadtree\b",
                    low,
                )
            ),
            (
                (
                    ([(1, 1), (10, 10), (50, 50), (90, 90), (5, 5)], (0, 0, 20, 20)),
                    [(1, 1), (5, 5), (10, 10)],
                ),
                (([], (0, 0, 10, 10)), []),
            ),
        ),
        T(
            "suffix_tree_class",
            "def suffix_tree_demo(text, patterns):\n"
            '    """Build a SuffixTree and test which patterns occur."""\n'
            "    tree = SuffixTree(text)\n"
            "    return [tree.search(pattern) for pattern in patterns]\n"
            "\n"
            "\n"
            "class SuffixTree:\n"
            '    """Educational naive suffix tree: build + search."""\n'
            "\n"
            "    def __init__(self, text=\"\"):\n"
            "        self.text = str(text) + \"$\"\n"
            "        self.root = {}\n"
            "        self._build()\n"
            "\n"
            "    def _build(self):\n"
            "        for i in range(len(self.text)):\n"
            "            node = self.root\n"
            "            for ch in self.text[i:]:\n"
            "                node = node.setdefault(ch, {})\n"
            "\n"
            "    def search(self, pattern):\n"
            "        node = self.root\n"
            "        for ch in str(pattern):\n"
            "            if ch not in node:\n"
            "                return False\n"
            "            node = node[ch]\n"
            "        return True\n",
            lambda low: bool(
                re.search(
                    r"\bsuffix[- ]?tree\b|"
                    r"\bsuffixtree\b",
                    low,
                )
            )
            and "array" not in low
            and "sums" not in low,
            (
                (("banana", ["ana", "ban", "nana", "xyz", ""]), [True, True, True, False, True]),
                (("abc", ["abc", "bc", "d"]), [True, True, False]),
            ),
        ),
    ]
