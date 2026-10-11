"""Cycle 564: SplayTree and Treap class asks that returned NotImplemented drafts.

Educational self-contained demos so synthesize_and_verify can self-check.
SplayTree is insert + splay + inorder. Treap is insert with fixed priorities + inorder.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "splay_tree_class",
            "def splay_tree_class_demo(values):\n"
            '    """Insert values into a SplayTree and return the sorted inorder list."""\n'
            "    tree = SplayTree()\n"
            "    for v in values:\n"
            "        tree.insert(v)\n"
            "    return tree.inorder()\n"
            "\n"
            "\n"
            "class SplayNode:\n"
            "    def __init__(self, key):\n"
            "        self.key = key\n"
            "        self.left = None\n"
            "        self.right = None\n"
            "\n"
            "\n"
            "class SplayTree:\n"
            '    """Splay tree with insert and inorder (splay on insert)."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.root = None\n"
            "\n"
            "    def _rotate_right(self, x):\n"
            "        y = x.left\n"
            "        x.left = y.right\n"
            "        y.right = x\n"
            "        return y\n"
            "\n"
            "    def _rotate_left(self, x):\n"
            "        y = x.right\n"
            "        x.right = y.left\n"
            "        y.left = x\n"
            "        return y\n"
            "\n"
            "    def _splay(self, root, key):\n"
            "        if root is None or root.key == key:\n"
            "            return root\n"
            "        if key < root.key:\n"
            "            if root.left is None:\n"
            "                return root\n"
            "            if key < root.left.key:\n"
            "                root.left.left = self._splay(root.left.left, key)\n"
            "                root = self._rotate_right(root)\n"
            "            elif key > root.left.key:\n"
            "                root.left.right = self._splay(root.left.right, key)\n"
            "                if root.left.right is not None:\n"
            "                    root.left = self._rotate_left(root.left)\n"
            "            if root.left is None:\n"
            "                return root\n"
            "            return self._rotate_right(root)\n"
            "        else:\n"
            "            if root.right is None:\n"
            "                return root\n"
            "            if key > root.right.key:\n"
            "                root.right.right = self._splay(root.right.right, key)\n"
            "                root = self._rotate_left(root)\n"
            "            elif key < root.right.key:\n"
            "                root.right.left = self._splay(root.right.left, key)\n"
            "                if root.right.left is not None:\n"
            "                    root.right = self._rotate_right(root.right)\n"
            "            if root.right is None:\n"
            "                return root\n"
            "            return self._rotate_left(root)\n"
            "\n"
            "    def insert(self, key):\n"
            "        self.root = self._insert(self.root, key)\n"
            "        self.root = self._splay(self.root, key)\n"
            "\n"
            "    def _insert(self, node, key):\n"
            "        if node is None:\n"
            "            return SplayNode(key)\n"
            "        if key < node.key:\n"
            "            node.left = self._insert(node.left, key)\n"
            "        elif key > node.key:\n"
            "            node.right = self._insert(node.right, key)\n"
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
            lambda low: bool(re.search(r"\bsplay(?:[- ]?tree)?\b", low))
            and "treap" not in low,
            (
                (([3, 1, 4, 2],), [1, 2, 3, 4]),
                (([5, 3, 7, 1],), [1, 3, 5, 7]),
                (([10, 20, 5],), [5, 10, 20]),
            ),
        ),
        T(
            "treap_class",
            "def treap_class_demo(pairs):\n"
            '    """Insert (key, priority) pairs into a Treap and return sorted keys."""\n'
            "    tree = Treap()\n"
            "    for key, pri in pairs:\n"
            "        tree.insert(key, pri)\n"
            "    return tree.inorder()\n"
            "\n"
            "\n"
            "class TreapNode:\n"
            "    def __init__(self, key, priority):\n"
            "        self.key = key\n"
            "        self.priority = priority\n"
            "        self.left = None\n"
            "        self.right = None\n"
            "\n"
            "\n"
            "class Treap:\n"
            '    """Treap (tree + heap) with insert by key and priority, plus inorder."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.root = None\n"
            "\n"
            "    def _rotate_right(self, y):\n"
            "        x = y.left\n"
            "        y.left = x.right\n"
            "        x.right = y\n"
            "        return x\n"
            "\n"
            "    def _rotate_left(self, x):\n"
            "        y = x.right\n"
            "        x.right = y.left\n"
            "        y.left = x\n"
            "        return y\n"
            "\n"
            "    def insert(self, key, priority):\n"
            "        self.root = self._insert(self.root, key, priority)\n"
            "\n"
            "    def _insert(self, node, key, priority):\n"
            "        if node is None:\n"
            "            return TreapNode(key, priority)\n"
            "        if key < node.key:\n"
            "            node.left = self._insert(node.left, key, priority)\n"
            "            if node.left.priority > node.priority:\n"
            "                node = self._rotate_right(node)\n"
            "        elif key > node.key:\n"
            "            node.right = self._insert(node.right, key, priority)\n"
            "            if node.right.priority > node.priority:\n"
            "                node = self._rotate_left(node)\n"
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
            lambda low: bool(re.search(r"\btreap\b", low))
            and "splay" not in low,
            (
                (([(3, 5), (1, 10), (4, 1), (2, 8)],), [1, 2, 3, 4]),
                (([(5, 3), (3, 7), (7, 1), (1, 9)],), [1, 3, 5, 7]),
                (([(10, 2), (20, 4), (5, 6)],), [5, 10, 20]),
            ),
        ),
    ]
