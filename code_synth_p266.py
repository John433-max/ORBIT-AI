"""Cycle 568: educational B-Tree class and MinMaxStack class.

Self-checkable demos so natural-language "implement a BTree / MinMaxStack class"
asks synthesize and verify instead of returning NotImplemented drafts.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "btree_class",
            "def btree_demo(values):\n"
            '    """Insert then inorder to exercise BTree (order 3)."""\n'
            "    tree = BTree()\n"
            "    for value in values:\n"
            "        tree.insert(value)\n"
            "    return tree.inorder()\n"
            "\n"
            "\n"
            "class _BNode:\n"
            "    def __init__(self, leaf=True):\n"
            "        self.keys = []\n"
            "        self.children = []\n"
            "        self.leaf = leaf\n"
            "\n"
            "\n"
            "class BTree:\n"
            '    """Educational B-tree of order 3 (max 2 keys per node)."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.root = _BNode()\n"
            "        self.t = 2  # min degree; max keys = 2*t - 1 = 3? Wait order 3 => max 2 keys\n"
            "\n"
            "    def insert(self, key):\n"
            "        root = self.root\n"
            "        if len(root.keys) == 2:  # split full root (max 2 keys for this educational order)\n"
            "            new_root = _BNode(leaf=False)\n"
            "            new_root.children.append(root)\n"
            "            self._split_child(new_root, 0)\n"
            "            self.root = new_root\n"
            "        self._insert_nonfull(self.root, key)\n"
            "\n"
            "    def _split_child(self, parent, i):\n"
            "        t = self.t\n"
            "        full = parent.children[i]\n"
            "        mid = full.keys[1]\n"
            "        left = _BNode(leaf=full.leaf)\n"
            "        right = _BNode(leaf=full.leaf)\n"
            "        left.keys = full.keys[:1]\n"
            "        right.keys = full.keys[2:]\n"
            "        if not full.leaf:\n"
            "            left.children = full.children[:2]\n"
            "            right.children = full.children[2:]\n"
            "        parent.keys.insert(i, mid)\n"
            "        parent.children[i] = left\n"
            "        parent.children.insert(i + 1, right)\n"
            "\n"
            "    def _insert_nonfull(self, node, key):\n"
            "        if node.leaf:\n"
            "            i = 0\n"
            "            while i < len(node.keys) and key > node.keys[i]:\n"
            "                i += 1\n"
            "            if i < len(node.keys) and node.keys[i] == key:\n"
            "                return\n"
            "            node.keys.insert(i, key)\n"
            "            return\n"
            "        i = 0\n"
            "        while i < len(node.keys) and key > node.keys[i]:\n"
            "            i += 1\n"
            "        if i < len(node.keys) and node.keys[i] == key:\n"
            "            return\n"
            "        child = node.children[i]\n"
            "        if len(child.keys) == 2:\n"
            "            self._split_child(node, i)\n"
            "            if key > node.keys[i]:\n"
            "                i += 1\n"
            "            elif key == node.keys[i]:\n"
            "                return\n"
            "        self._insert_nonfull(node.children[i], key)\n"
            "\n"
            "    def inorder(self):\n"
            "        out = []\n"
            "\n"
            "        def walk(node):\n"
            "            if node is None:\n"
            "                return\n"
            "            if node.leaf:\n"
            "                out.extend(node.keys)\n"
            "                return\n"
            "            for i, k in enumerate(node.keys):\n"
            "                walk(node.children[i])\n"
            "                out.append(k)\n"
            "            walk(node.children[-1])\n"
            "\n"
            "        walk(self.root)\n"
            "        return out\n"
            "\n"
            "    def search(self, key):\n"
            "        def _s(node):\n"
            "            if node is None:\n"
            "                return False\n"
            "            i = 0\n"
            "            while i < len(node.keys) and key > node.keys[i]:\n"
            "                i += 1\n"
            "            if i < len(node.keys) and node.keys[i] == key:\n"
            "                return True\n"
            "            if node.leaf:\n"
            "                return False\n"
            "            return _s(node.children[i])\n"
            "        return _s(self.root)\n",
            lambda low: bool(re.search(r"\b(?:b[- ]?tree|btree)\b", low))
            and "binary" not in low
            and "bst" not in low
            and "binary tree" not in low,
            examples=(
                (([10, 20, 5, 6, 12, 30, 7, 17],), [5, 6, 7, 10, 12, 17, 20, 30]),
                (([1],), [1]),
                (([],), []),
            ),
        ),
        T(
            "min_max_stack_class",
            "def min_max_stack_demo(ops):\n"
            '    """Apply push/pop/min/max ops. ops: list of (\'push\', v) or (\'pop\',) or (\'min\',) or (\'max\',)."""\n'
            "    st = MinMaxStack()\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        if op[0] == 'push':\n"
            "            st.push(op[1])\n"
            "            out.append(None)\n"
            "        elif op[0] == 'pop':\n"
            "            out.append(st.pop())\n"
            "        elif op[0] == 'min':\n"
            "            out.append(st.get_min())\n"
            "        elif op[0] == 'max':\n"
            "            out.append(st.get_max())\n"
            "    return out\n"
            "\n"
            "\n"
            "class MinMaxStack:\n"
            '    """Stack with O(1) get_min and get_max via auxiliary stacks."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self._data = []\n"
            "        self._mins = []\n"
            "        self._maxs = []\n"
            "\n"
            "    def push(self, val):\n"
            "        self._data.append(val)\n"
            "        self._mins.append(val if not self._mins else min(val, self._mins[-1]))\n"
            "        self._maxs.append(val if not self._maxs else max(val, self._maxs[-1]))\n"
            "\n"
            "    def pop(self):\n"
            "        if not self._data:\n"
            "            return None\n"
            "        self._mins.pop()\n"
            "        self._maxs.pop()\n"
            "        return self._data.pop()\n"
            "\n"
            "    def get_min(self):\n"
            "        return self._mins[-1] if self._mins else None\n"
            "\n"
            "    def get_max(self):\n"
            "        return self._maxs[-1] if self._maxs else None\n"
            "\n"
            "    def top(self):\n"
            "        return self._data[-1] if self._data else None\n",
            lambda low: bool(re.search(r"\bmin[-_ ]?max[-_ ]?stack\b|\bminmaxstack\b", low))
            and "min stack" not in low.replace("min-max", "minmax").replace("min_max", "minmax"),
            examples=(
                (([("push", 3), ("push", 1), ("min",), ("max",), ("pop",), ("min",)],), [None, None, 1, 3, 1, 3]),
                (([("push", 5), ("max",), ("min",)],), [None, 5, 5]),
                (([],), []),
            ),
        ),
    ]
