"""Cycle 288: convert BST / subtree / leaf-similar / trim BST / increasing BST / BST mode."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "convert_bst",
            "def convert_bst(root):\n"
            '    """Convert BST to greater tree: each node += sum of larger keys."""\n'
            "    acc = [0]\n"
            "    def walk(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        v = node[0]\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        nr = walk(right)\n"
            "        acc[0] += v\n"
            "        return [acc[0], walk(left), nr]\n"
            "    return walk(root)\n",
            lambda low: bool(
                re.search(
                    r"\bconvert[_ ]bst\b|"
                    r"\bgreater (?:sum )?tree\b|"
                    r"\bconvert (?:a |the )?bst to (?:a |the )?greater\b|"
                    r"\bbst to greater tree\b",
                    low,
                )
            ),
            (
                (([4, [1, None, None], [6, None, None]],),
                 [10, [11, None, None], [6, None, None]]),
                (([0, None, [1, None, None]],), [1, None, [1, None, None]]),
                ((None,), None),
            ),
        ),
        T(
            "is_subtree",
            "def is_subtree(root, sub):\n"
            '    """True if sub is a subtree of root ([val, left, right] encoding)."""\n'
            "    def same(a, b):\n"
            "        if a is None or b is None:\n"
            "            return a is b\n"
            "        if a[0] != b[0]:\n"
            "            return False\n"
            "        al = a[1] if len(a) > 1 else None\n"
            "        ar = a[2] if len(a) > 2 else None\n"
            "        bl = b[1] if len(b) > 1 else None\n"
            "        br = b[2] if len(b) > 2 else None\n"
            "        return same(al, bl) and same(ar, br)\n"
            "    if sub is None:\n"
            "        return True\n"
            "    if root is None:\n"
            "        return False\n"
            "    if same(root, sub):\n"
            "        return True\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    return is_subtree(left, sub) or is_subtree(right, sub)\n",
            lambda low: bool(
                re.search(
                    r"\bis[_ ]subtree\b|"
                    r"\bsubtree of another tree\b|"
                    r"\bis (?:a )?subtree\b",
                    low,
                )
                and "flatten" not in low
            ),
            (
                (
                    (
                        [3, [4, [1, None, None], [2, None, None]], [5, None, None]],
                        [4, [1, None, None], [2, None, None]],
                    ),
                    True,
                ),
                (
                    (
                        [3, [4, [1, None, None], [2, [0, None, None], None]], [5, None, None]],
                        [4, [1, None, None], [2, None, None]],
                    ),
                    False,
                ),
                ((None, None), True),
            ),
        ),
        T(
            "leaf_similar",
            "def leaf_similar(t1, t2):\n"
            '    """True if two trees have the same left-to-right leaf sequence."""\n'
            "    def leaves(node):\n"
            "        out = []\n"
            "        stack = [node]\n"
            "        while stack:\n"
            "            n = stack.pop()\n"
            "            if n is None:\n"
            "                continue\n"
            "            left = n[1] if len(n) > 1 else None\n"
            "            right = n[2] if len(n) > 2 else None\n"
            "            if left is None and right is None:\n"
            "                out.append(n[0])\n"
            "            else:\n"
            "                stack.append(right)\n"
            "                stack.append(left)\n"
            "        return out\n"
            "    return leaves(t1) == leaves(t2)\n",
            lambda low: bool(
                re.search(
                    r"\bleaf[_ ]similar\b|"
                    r"\bleaf[- ]similar trees\b|"
                    r"\bsimilar leaf\b",
                    low,
                )
            ),
            (
                (
                    (
                        [3, [5, [6, None, None], [2, [7, None, None], [4, None, None]]], [1, [9, None, None], [8, None, None]]],
                        [3, [5, [6, None, None], [7, None, None]], [1, [4, None, None], [2, [9, None, None], [8, None, None]]]],
                    ),
                    True,
                ),
                (([1, [2, None, None], [3, None, None]], [1, [3, None, None], [2, None, None]]), False),
            ),
        ),
        T(
            "trim_bst",
            "def trim_bst(root, low, high):\n"
            '    """Trim a BST so every remaining node is in [low, high]."""\n'
            "    if root is None:\n"
            "        return None\n"
            "    v = root[0]\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    if v < low:\n"
            "        return trim_bst(right, low, high)\n"
            "    if v > high:\n"
            "        return trim_bst(left, low, high)\n"
            "    return [v, trim_bst(left, low, high), trim_bst(right, low, high)]\n",
            lambda low: bool(
                re.search(
                    r"\btrim[_ ]bst\b|"
                    r"\btrim (?:a |the )?binary search tree\b|"
                    r"\btrim (?:a |the )?bst\b",
                    low,
                )
            ),
            (
                (([1, [0, None, None], [2, None, None]], 1, 2), [1, None, [2, None, None]]),
                (([3, [0, None, [2, [1, None, None], None]], [4, None, None]], 1, 3),
                 [3, [2, [1, None, None], None], None]),
            ),
        ),
        T(
            "increasing_bst",
            "def increasing_bst(root):\n"
            '    """Relink a BST into a right spine in increasing order."""\n'
            "    nodes = []\n"
            "    def walk(n):\n"
            "        if n is None:\n"
            "            return\n"
            "        walk(n[1] if len(n) > 1 else None)\n"
            "        nodes.append(n[0])\n"
            "        walk(n[2] if len(n) > 2 else None)\n"
            "    walk(root)\n"
            "    sentinel = [0, None, None]\n"
            "    cur = sentinel\n"
            "    for v in nodes:\n"
            "        nxt = [v, None, None]\n"
            "        cur[2] = nxt\n"
            "        cur = nxt\n"
            "    return sentinel[2]\n",
            lambda low: bool(
                re.search(
                    r"\bincreasing[_ ]bst\b|"
                    r"\bincreasing order search tree\b|"
                    r"\brelink (?:a |the )?bst\b",
                    low,
                )
            ),
            (
                (([5, [3, [2, None, None], [4, None, None]], [6, None, None]],),
                 [2, None, [3, None, [4, None, [5, None, [6, None, None]]]]]),
                (([1, None, None],), [1, None, None]),
            ),
        ),
        T(
            "find_mode_bst",
            "def find_mode_bst(root):\n"
            '    """Return the mode(s) of a BST (most frequent values)."""\n'
            "    from collections import Counter\n"
            "    cnt = Counter()\n"
            "    stack = [root]\n"
            "    while stack:\n"
            "        n = stack.pop()\n"
            "        if n is None:\n"
            "            continue\n"
            "        cnt[n[0]] += 1\n"
            "        stack.append(n[1] if len(n) > 1 else None)\n"
            "        stack.append(n[2] if len(n) > 2 else None)\n"
            "    if not cnt:\n"
            "        return []\n"
            "    best = max(cnt.values())\n"
            "    return sorted(k for k, v in cnt.items() if v == best)\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]mode[_ ]bst\b|"
                    r"\bfind mode(?:s)? (?:in )?(?:a |the )?(?:bst|binary search tree)\b|"
                    r"\bmode(?:s)? of (?:a |the )?(?:bst|binary search tree)\b",
                    low,
                )
            ),
            (
                (([1, None, [2, [2, None, None], None]],), [2]),
                (([1, None, None],), [1]),
                ((None,), []),
            ),
        ),
    ]
