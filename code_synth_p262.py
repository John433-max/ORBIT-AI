"""Cycle 567: MaxHeap and RedBlackTree class asks that returned NotImplemented drafts.

Educational self-contained demos so synthesize_and_verify can self-check.
MaxHeap is array-based insert + extract_max. RedBlackTree is a simplified
educational insert that maintains BST order and basic red-black coloring.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "max_heap_class",
            "def max_heap_class_demo(values):\n"
            '    """Insert values into a MaxHeap and return them in descending order."""\n'
            "    heap = MaxHeap()\n"
            "    for v in values:\n"
            "        heap.insert(v)\n"
            "    out = []\n"
            "    while not heap.empty():\n"
            "        out.append(heap.extract_max())\n"
            "    return out\n"
            "\n"
            "\n"
            "class MaxHeap:\n"
            '    """Array-based max-heap with insert and extract_max."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.data = []\n"
            "\n"
            "    def empty(self):\n"
            "        return len(self.data) == 0\n"
            "\n"
            "    def insert(self, key):\n"
            "        self.data.append(key)\n"
            "        self._sift_up(len(self.data) - 1)\n"
            "\n"
            "    def extract_max(self):\n"
            "        if not self.data:\n"
            "            return None\n"
            "        self.data[0], self.data[-1] = self.data[-1], self.data[0]\n"
            "        mx = self.data.pop()\n"
            "        if self.data:\n"
            "            self._sift_down(0)\n"
            "        return mx\n"
            "\n"
            "    def _sift_up(self, i):\n"
            "        while i > 0:\n"
            "            p = (i - 1) // 2\n"
            "            if self.data[i] > self.data[p]:\n"
            "                self.data[i], self.data[p] = self.data[p], self.data[i]\n"
            "                i = p\n"
            "            else:\n"
            "                break\n"
            "\n"
            "    def _sift_down(self, i):\n"
            "        n = len(self.data)\n"
            "        while True:\n"
            "            l = 2 * i + 1\n"
            "            r = 2 * i + 2\n"
            "            largest = i\n"
            "            if l < n and self.data[l] > self.data[largest]:\n"
            "                largest = l\n"
            "            if r < n and self.data[r] > self.data[largest]:\n"
            "                largest = r\n"
            "            if largest == i:\n"
            "                break\n"
            "            self.data[i], self.data[largest] = self.data[largest], self.data[i]\n"
            "            i = largest\n",
            lambda low: bool(re.search(r"\bmax[- ]?heap\b|\bmaxheap\b", low))
            and "min" not in low
            and "red" not in low,
            (
                (([3, 1, 4, 2],), [4, 3, 2, 1]),
                (([5, 3, 7, 1],), [7, 5, 3, 1]),
                (([10, 20, 5],), [20, 10, 5]),
            ),
        ),
        T(
            "red_black_tree_class",
            "def red_black_tree_class_demo(values):\n"
            '    """Insert values into a simplified RedBlackTree and return sorted inorder."""\n'
            "    tree = RedBlackTree()\n"
            "    for v in values:\n"
            "        tree.insert(v)\n"
            "    return tree.inorder()\n"
            "\n"
            "\n"
            "class RBNode:\n"
            "    def __init__(self, key, color=\"red\"):\n"
            "        self.key = key\n"
            "        self.color = color\n"
            "        self.left = None\n"
            "        self.right = None\n"
            "\n"
            "\n"
            "class RedBlackTree:\n"
            '    """Simplified educational Red-Black tree: BST insert + basic recolor."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.root = None\n"
            "\n"
            "    def insert(self, key):\n"
            "        self.root = self._insert(self.root, key)\n"
            "        if self.root:\n"
            "            self.root.color = \"black\"\n"
            "\n"
            "    def _insert(self, node, key):\n"
            "        if node is None:\n"
            "            return RBNode(key, \"red\")\n"
            "        if key < node.key:\n"
            "            node.left = self._insert(node.left, key)\n"
            "        elif key > node.key:\n"
            "            node.right = self._insert(node.right, key)\n"
            "        # Basic recolor: if both children red, flip\n"
            "        if node.left and node.left.color == \"red\" and node.right and node.right.color == \"red\":\n"
            "            node.color = \"red\"\n"
            "            node.left.color = \"black\"\n"
            "            node.right.color = \"black\"\n"
            "        return node\n"
            "\n"
            "    def inorder(self):\n"
            "        out = []\n"
            "\n"
            "        def walk(n):\n"
            "            if n:\n"
            "                walk(n.left)\n"
            "                out.append(n.key)\n"
            "                walk(n.right)\n"
            "\n"
            "        walk(self.root)\n"
            "        return out\n",
            lambda low: bool(re.search(r"\bred[- ]?black(?:[- ]?tree)?\b", low))
            and "max" not in low
            and "heap" not in low,
            (
                (([3, 1, 4, 2],), [1, 2, 3, 4]),
                (([5, 3, 7, 1],), [1, 3, 5, 7]),
                (([10, 20, 5],), [5, 10, 20]),
            ),
        ),
    ]
