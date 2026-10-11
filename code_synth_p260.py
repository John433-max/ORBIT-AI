"""Cycle 563: AVLTree and FenwickTree class asks that returned NotImplemented drafts.

Educational self-contained demos so synthesize_and_verify can self-check.
AVL is insert + inorder (balanced BST). Fenwick is 1-indexed prefix sums.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "avl_tree_class",
            "def avl_tree_class_demo(values):\n"
            '    """Insert values into an AVLTree and return the sorted inorder list."""\n'
            "    tree = AVLTree()\n"
            "    for v in values:\n"
            "        tree.insert(v)\n"
            "    return tree.inorder()\n"
            "\n"
            "\n"
            "class AVLNode:\n"
            "    def __init__(self, key):\n"
            "        self.key = key\n"
            "        self.left = None\n"
            "        self.right = None\n"
            "        self.height = 1\n"
            "\n"
            "\n"
            "class AVLTree:\n"
            '    """Self-balancing BST (AVL) with insert and inorder traversal."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.root = None\n"
            "\n"
            "    def height(self, node):\n"
            "        return node.height if node else 0\n"
            "\n"
            "    def balance(self, node):\n"
            "        if not node:\n"
            "            return 0\n"
            "        return self.height(node.left) - self.height(node.right)\n"
            "\n"
            "    def right_rotate(self, y):\n"
            "        x = y.left\n"
            "        T2 = x.right\n"
            "        x.right = y\n"
            "        y.left = T2\n"
            "        y.height = 1 + max(self.height(y.left), self.height(y.right))\n"
            "        x.height = 1 + max(self.height(x.left), self.height(x.right))\n"
            "        return x\n"
            "\n"
            "    def left_rotate(self, x):\n"
            "        y = x.right\n"
            "        T2 = y.left\n"
            "        y.left = x\n"
            "        x.right = T2\n"
            "        x.height = 1 + max(self.height(x.left), self.height(x.right))\n"
            "        y.height = 1 + max(self.height(y.left), self.height(y.right))\n"
            "        return y\n"
            "\n"
            "    def insert(self, key):\n"
            "        self.root = self._insert(self.root, key)\n"
            "\n"
            "    def _insert(self, node, key):\n"
            "        if not node:\n"
            "            return AVLNode(key)\n"
            "        if key < node.key:\n"
            "            node.left = self._insert(node.left, key)\n"
            "        else:\n"
            "            node.right = self._insert(node.right, key)\n"
            "        node.height = 1 + max(self.height(node.left), self.height(node.right))\n"
            "        bal = self.balance(node)\n"
            "        if bal > 1 and key < node.left.key:\n"
            "            return self.right_rotate(node)\n"
            "        if bal < -1 and key > node.right.key:\n"
            "            return self.left_rotate(node)\n"
            "        if bal > 1 and key > node.left.key:\n"
            "            node.left = self.left_rotate(node.left)\n"
            "            return self.right_rotate(node)\n"
            "        if bal < -1 and key < node.right.key:\n"
            "            node.right = self.right_rotate(node.right)\n"
            "            return self.left_rotate(node)\n"
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
            lambda low: "class" in low and bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a| an)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| an| the)? avl(?:[- ]?tree)?\b|"
                    r"\bavl(?:[- ]?tree)? class\b|"
                    r"\bclass for(?: a| the)? avl(?:[- ]?tree)?\b|"
                    r"\bAVLTree class\b|"
                    r"\bimplements? an? avl(?:[- ]?tree)? class\b",
                    low,
                )
            )
            and "fenwick" not in low
            and "binary indexed" not in low,
            (
                (([3, 1, 4, 2],), [1, 2, 3, 4]),
                (([5, 3, 7, 1],), [1, 3, 5, 7]),
                (([10, 20, 5],), [5, 10, 20]),
            ),
        ),
        T(
            "fenwick_tree_class",
            "def fenwick_tree_class_demo(n, updates, queries):\n"
            '    """Build a FenwickTree, apply updates, return 1-indexed prefix queries."""\n'
            "    ft = FenwickTree(n)\n"
            "    for i, delta in updates:\n"
            "        if 1 <= i <= n:\n"
            "            ft.update(i, delta)\n"
            "    return [ft.query(q) if 0 <= q <= n else None for q in queries]\n"
            "\n"
            "\n"
            "class FenwickTree:\n"
            '    """1-indexed Fenwick tree (binary indexed tree) for prefix sums."""\n'
            "\n"
            "    def __init__(self, n):\n"
            "        self.n = n\n"
            "        self.tree = [0] * (n + 1)\n"
            "\n"
            "    def update(self, i, delta):\n"
            "        while i <= self.n:\n"
            "            self.tree[i] += delta\n"
            "            i += i & -i\n"
            "\n"
            "    def query(self, i):\n"
            "        s = 0\n"
            "        while i > 0:\n"
            "            s += self.tree[i]\n"
            "            i -= i & -i\n"
            "        return s\n"
            "\n"
            "    def range_query(self, left, right):\n"
            "        if left > right:\n"
            "            return 0\n"
            "        return self.query(right) - self.query(left - 1)\n",
            lambda low: "class" in low and bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a| an)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| an| the)? (?:fenwick|binary[- ]indexed)(?:[- ]?tree)?\b|"
                    r"\b(?:fenwick|binary[- ]indexed)(?:[- ]?tree)? class\b|"
                    r"\bclass for(?: a| the)? (?:fenwick|binary[- ]indexed)(?:[- ]?tree)?\b|"
                    r"\bFenwickTree class\b|"
                    r"\bimplements? a (?:fenwick|binary[- ]indexed)(?:[- ]?tree)? class\b|"
                    r"\bBIT class\b",
                    low,
                )
            )
            and "avl" not in low,
            (
                ((5, [(1, 3), (3, 2), (5, 1)], [1, 3, 5, 0]), [3, 5, 6, 0]),
                ((3, [(2, 10)], [1, 2, 3]), [0, 10, 10]),
                ((4, [(1, 1), (4, 5)], [2, 4]), [1, 6]),
            ),
        ),
    ]
