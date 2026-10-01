"""Cycle 291: tree width / min BST diff / 2nd-min / LCA-BST / complete tree / sum numbers."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "width_of_binary_tree",
            "def width_of_binary_tree(root):\n"
            '    """Maximum width of a binary tree (end-to-end nodes per level)."""\n'
            "    if root is None:\n"
            "        return 0\n"
            "    best = 1\n"
            "    q = [(root, 0)]\n"
            "    while q:\n"
            "        best = max(best, q[-1][1] - q[0][1] + 1)\n"
            "        nxt = []\n"
            "        for node, i in q:\n"
            "            left = node[1] if len(node) > 1 else None\n"
            "            right = node[2] if len(node) > 2 else None\n"
            "            if left is not None:\n"
            "                nxt.append((left, 2 * i))\n"
            "            if right is not None:\n"
            "                nxt.append((right, 2 * i + 1))\n"
            "        q = nxt\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bwidth[_ ]of[_ ]binary[_ ]tree\b|"
                    r"\bmaximum width of (?:a |the )?(?:binary )?tree\b|"
                    r"\bmax(?:imum)? width of (?:a |the )?binary tree\b|"
                    r"\bwidth of (?:a |the )?(?:binary )?tree\b",
                    low,
                )
            ),
            (
                (([1, [3, [5, None, None], [3, None, None]], [2, None, [9, None, None]]],), 4),
                (([1, [3, [5, None, None], None], [2, None, None]],), 2),
                (([1, None, None],), 1),
            ),
        ),
        T(
            "min_diff_bst",
            "def min_diff_bst(root):\n"
            '    """Minimum absolute difference between any two BST node values."""\n'
            "    vals = []\n"
            "    def walk(node):\n"
            "        if node is None:\n"
            "            return\n"
            "        walk(node[1] if len(node) > 1 else None)\n"
            "        vals.append(node[0])\n"
            "        walk(node[2] if len(node) > 2 else None)\n"
            "    walk(root)\n"
            "    if len(vals) < 2:\n"
            "        return 0\n"
            "    best = abs(vals[1] - vals[0])\n"
            "    for i in range(1, len(vals)):\n"
            "        d = abs(vals[i] - vals[i - 1])\n"
            "        if d < best:\n"
            "            best = d\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmin[_ ]diff[_ ]bst\b|"
                    r"\bget[_ ]minimum[_ ]difference\b|"
                    r"\bminimum (?:absolute )?difference (?:in|between).{0,24}bst\b|"
                    r"\bminimum (?:absolute )?difference in (?:a |the )?(?:binary search tree|bst)\b|"
                    r"\bbst minimum (?:absolute )?difference\b",
                    low,
                )
            ),
            (
                (([4, [2, [1, None, None], [3, None, None]], [6, None, None]],), 1),
                (([1, None, [3, [2, None, None], None]],), 1),
                (([90, [69, None, [89, [52, None, None], None]], None],), 1),
            ),
        ),
        T(
            "find_second_minimum",
            "def find_second_minimum(root):\n"
            '    """Second minimum in a special tree (root = min(children)). -1 if none."""\n'
            "    if root is None:\n"
            "        return -1\n"
            "    first = root[0]\n"
            "    second = [None]\n"
            "    def walk(node):\n"
            "        if node is None:\n"
            "            return\n"
            "        v = node[0]\n"
            "        if v > first and (second[0] is None or v < second[0]):\n"
            "            second[0] = v\n"
            "        if v == first:\n"
            "            walk(node[1] if len(node) > 1 else None)\n"
            "            walk(node[2] if len(node) > 2 else None)\n"
            "    walk(root)\n"
            "    return -1 if second[0] is None else second[0]\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]second[_ ]minimum\b|"
                    r"\bsecond minimum (?:node )?(?:in|of) (?:a |the )?(?:binary )?tree\b|"
                    r"\bsecond min(?:imum)? value in (?:a |the )?(?:binary )?tree\b|"
                    r"\bsecond smallest (?:value )?in (?:a |the )?(?:binary )?tree\b",
                    low,
                )
            )
            and not re.search(r"\bkth\b|\bthird\b", low),
            (
                (([2, [2, None, None], [5, [5, None, None], [7, None, None]]],), 5),
                (([2, [2, None, None], [2, None, None]],), -1),
                (([1, None, None],), -1),
            ),
        ),
        T(
            "lowest_common_ancestor_bst",
            "def lowest_common_ancestor_bst(root, p, q):\n"
            '    """LCA value of p and q in a BST [val, left, right]."""\n'
            "    cur = root\n"
            "    while cur is not None:\n"
            "        v = cur[0]\n"
            "        if p < v and q < v:\n"
            "            cur = cur[1] if len(cur) > 1 else None\n"
            "        elif p > v and q > v:\n"
            "            cur = cur[2] if len(cur) > 2 else None\n"
            "        else:\n"
            "            return v\n"
            "    return None\n",
            lambda low: bool(
                re.search(
                    r"\blowest[_ ]common[_ ]ancestor[_ ]bst\b|"
                    r"\blca[_ ]bst\b|"
                    r"\blowest common ancestor (?:of|in) (?:a |the )?(?:bst|binary search tree)\b|"
                    r"\blca (?:of|in) (?:a |the )?(?:bst|binary search tree)\b|"
                    r"\bbst lowest common ancestor\b",
                    low,
                )
            ),
            (
                (([6, [2, [0, None, None], [4, [3, None, None], [5, None, None]]], [8, [7, None, None], [9, None, None]]], 2, 8), 6),
                (([6, [2, [0, None, None], [4, [3, None, None], [5, None, None]]], [8, [7, None, None], [9, None, None]]], 2, 4), 2),
                (([2, [1, None, None], None], 2, 1), 2),
            ),
        ),
        T(
            "is_complete_tree",
            "def is_complete_tree(root):\n"
            '    """True if the binary tree is complete (level-order, no holes)."""\n'
            "    if root is None:\n"
            "        return True\n"
            "    q = [root]\n"
            "    seen_null = False\n"
            "    while q:\n"
            "        node = q.pop(0)\n"
            "        if node is None:\n"
            "            seen_null = True\n"
            "            continue\n"
            "        if seen_null:\n"
            "            return False\n"
            "        q.append(node[1] if len(node) > 1 else None)\n"
            "        q.append(node[2] if len(node) > 2 else None)\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bis[_ ]complete[_ ]tree\b|"
                    r"\bcheck (?:if )?(?:a |the )?(?:binary )?tree is complete\b|"
                    r"\bis (?:a |the )?(?:binary )?tree complete\b|"
                    r"\bcomplete(?:ness of)? (?:a |the )?binary tree\b|"
                    r"\bcheck completeness of (?:a |the )?binary tree\b",
                    low,
                )
            )
            and not re.search(r"\bcount[_ ]nodes\b|\bcount nodes in (?:a |the )?complete\b", low),
            (
                (([1, [2, [4, None, None], [5, None, None]], [3, [6, None, None], None]],), True),
                (([1, [2, [4, None, None], [5, None, None]], [3, None, [7, None, None]]],), False),
                ((None,), True),
            ),
        ),
        T(
            "sum_numbers",
            "def sum_numbers(root):\n"
            '    """Sum of root-to-leaf decimal numbers formed by node digits."""\n'
            "    total = [0]\n"
            "    def walk(node, acc):\n"
            "        if node is None:\n"
            "            return\n"
            "        acc = acc * 10 + int(node[0])\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        if left is None and right is None:\n"
            "            total[0] += acc\n"
            "            return\n"
            "        walk(left, acc)\n"
            "        walk(right, acc)\n"
            "    walk(root, 0)\n"
            "    return total[0]\n",
            lambda low: bool(
                re.search(
                    r"\bsum[_ ]numbers\b|"
                    r"\bsum root to leaf numbers\b|"
                    r"\bsum of root[- ]to[- ]leaf numbers\b|"
                    r"\broot[- ]to[- ]leaf numbers?\b",
                    low,
                )
            )
            and not re.search(r"\bbinary\b|\bsum_root_to_leaf\b|\bpath[_ ]sum\b", low),
            (
                (([1, [2, None, None], [3, None, None]],), 25),
                (([4, [9, [5, None, None], [1, None, None]], [0, None, None]],), 1026),
                ((None,), 0),
            ),
        ),
    ]
