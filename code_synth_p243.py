"""Cycle 546: recover BST and serialize/deserialize BST."""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "recover_bst",
            "def recover_bst(root):\n"
            '    """Fix a BST with exactly two values swapped. Nodes are [val, left, right]."""\n'
            "    nodes = []\n"
            "\n"
            "    def inorder(node):\n"
            "        if node is None:\n"
            "            return\n"
            "        inorder(node[1] if len(node) > 1 else None)\n"
            "        nodes.append(node)\n"
            "        inorder(node[2] if len(node) > 2 else None)\n"
            "\n"
            "    inorder(root)\n"
            "    first = second = None\n"
            "    for i in range(len(nodes) - 1):\n"
            "        if nodes[i][0] > nodes[i + 1][0]:\n"
            "            if first is None:\n"
            "                first = nodes[i]\n"
            "            second = nodes[i + 1]\n"
            "    if first is not None and second is not None:\n"
            "        first[0], second[0] = second[0], first[0]\n"
            "    return root\n",
            lambda low: bool(
                re.search(
                    r"\brecover (?:a |the )?binary search tree\b|"
                    r"\brecover bst\b|"
                    r"\bfix (?:a )?bst\b|"
                    r"\btwo nodes? (?:were )?swapped\b|"
                    r"\brecover_bst\b",
                    low,
                )
            ),
            (
                (
                    ([1, [3, None, [2, None, None]], None],),
                    [3, [1, None, [2, None, None]], None],
                ),
                (
                    ([3, [1, None, None], [4, [2, None, None], None]],),
                    [2, [1, None, None], [4, [3, None, None], None]],
                ),
                ((None,), None),
            ),
        ),
        T(
            "serialize_bst",
            "def serialize_bst(root):\n"
            '    """Preorder-serialize a BST (no null markers). Nodes are [val, left, right]."""\n'
            "    vals = []\n"
            "\n"
            "    def pre(node):\n"
            "        if node is None:\n"
            "            return\n"
            "        vals.append(str(node[0]))\n"
            "        pre(node[1] if len(node) > 1 else None)\n"
            "        pre(node[2] if len(node) > 2 else None)\n"
            "\n"
            "    pre(root)\n"
            "    return \",\".join(vals)\n",
            lambda low: bool(
                re.search(
                    r"\bserialize (?:and deserialize )?bst\b|"
                    r"\bserialize binary search tree\b|"
                    r"\bserialize_bst\b|"
                    r"\bencode (?:a )?bst\b|"
                    r"\bserialize and deserialize (?:a )?bst\b",
                    low,
                )
            ),
            (
                (([2, [1, None, None], [3, None, None]],), "2,1,3"),
                (([5, [3, [2, None, None], [4, None, None]], [7, None, None]],), "5,3,2,4,7"),
                ((None,), ""),
            ),
        ),
        T(
            "deserialize_bst",
            "def deserialize_bst(data):\n"
            '    """Rebuild a BST from preorder CSV (bounds method). Returns [val, left, right]."""\n'
            "    if not data:\n"
            "        return None\n"
            "    vals = [int(x) for x in data.split(\",\") if x]\n"
            "    idx = [0]\n"
            "\n"
            "    def build(lo, hi):\n"
            "        if idx[0] >= len(vals):\n"
            "            return None\n"
            "        v = vals[idx[0]]\n"
            "        if v < lo or v > hi:\n"
            "            return None\n"
            "        idx[0] += 1\n"
            "        node = [v, None, None]\n"
            "        node[1] = build(lo, v)\n"
            "        node[2] = build(v, hi)\n"
            "        return node\n"
            "\n"
            "    return build(float(\"-inf\"), float(\"inf\"))\n",
            lambda low: bool(
                re.search(
                    r"\bdeserialize (?:a |the )?bst\b|"
                    r"\bdeserialize binary search tree\b|"
                    r"\bdeserialize_bst\b|"
                    r"\bdecode (?:a )?bst\b",
                    low,
                )
                and "serialize and" not in low
            ),
            (
                (("2,1,3",), [2, [1, None, None], [3, None, None]]),
                (("5,3,2,4,7",), [5, [3, [2, None, None], [4, None, None]], [7, None, None]]),
                (("",), None),
            ),
        ),
    ]
