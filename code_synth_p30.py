"""Cycle 290: left leaves / cousins / row max / max level sum / insert BST / closest BST value."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_nodes",
            "def count_nodes(root):\n"
            '    """Count nodes in a complete binary tree (works for any binary tree)."""\n'
            "    def walk(node):\n"
            "        if node is None:\n"
            "            return 0\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        return 1 + walk(left) + walk(right)\n"
            "    return walk(root)\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]nodes\b|"
                    r"\bcount (?:complete )?(?:tree )?nodes\b|"
                    r"\bcount nodes in (?:a |the )?(?:complete )?(?:binary )?tree\b|"
                    r"\bcomplete binary tree nodes\b",
                    low,
                )
            ),
            (
                (([1, [2, [4, None, None], [5, None, None]], [3, [6, None, None], None]],), 6),
                (([1, None, None],), 1),
                ((None,), 0),
            ),
        ),
        T(
            "is_cousins",
            "def is_cousins(root, x, y):\n"
            '    """True if x and y are at the same depth with different parents."""\n'
            "    if root is None:\n"
            "        return False\n"
            "    found = {}\n"
            "    q = [(root, None, 0)]\n"
            "    while q:\n"
            "        node, parent, depth = q.pop(0)\n"
            "        val = node[0]\n"
            "        if val == x or val == y:\n"
            "            found[val] = (parent, depth)\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        if left is not None:\n"
            "            q.append((left, val, depth + 1))\n"
            "        if right is not None:\n"
            "            q.append((right, val, depth + 1))\n"
            "    if x not in found or y not in found:\n"
            "        return False\n"
            "    px, dx = found[x]\n"
            "    py, dy = found[y]\n"
            "    return dx == dy and px != py\n",
            lambda low: bool(
                re.search(
                    r"\bis[_ ]cousins\b|"
                    r"\bcousins in (?:a |the )?(?:binary )?tree\b|"
                    r"\bcheck (?:if )?(?:two )?nodes are cousins\b|"
                    r"\bare (?:two )?nodes cousins\b",
                    low,
                )
            ),
            (
                (([1, [2, [4, None, None], None], [3, None, None]], 4, 3), False),
                (([1, [2, None, [4, None, None]], [3, None, [5, None, None]]], 5, 4), True),
                (([1, [2, None, None], [3, None, None]], 2, 3), False),
            ),
        ),
        T(
            "largest_values",
            "def largest_values(root):\n"
            '    """Largest value in each tree row (level-order)."""\n'
            "    if root is None:\n"
            "        return []\n"
            "    out = []\n"
            "    q = [root]\n"
            "    while q:\n"
            "        best = q[0][0]\n"
            "        nxt = []\n"
            "        for node in q:\n"
            "            if node[0] > best:\n"
            "                best = node[0]\n"
            "            left = node[1] if len(node) > 1 else None\n"
            "            right = node[2] if len(node) > 2 else None\n"
            "            if left is not None:\n"
            "                nxt.append(left)\n"
            "            if right is not None:\n"
            "                nxt.append(right)\n"
            "        out.append(best)\n"
            "        q = nxt\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\blargest[_ ]values\b|"
                    r"\bfind largest value in each (?:tree )?row\b|"
                    r"\blargest value(?:s)? in each (?:tree )?row\b|"
                    r"\brow[- ]max(?:imum)? (?:in )?(?:a |the )?(?:binary )?tree\b",
                    low,
                )
            ),
            (
                (([1, [3, [5, None, None], [3, None, None]], [2, None, [9, None, None]]],), [1, 3, 9]),
                (([1, [2, None, None], [3, None, None]],), [1, 3]),
                ((None,), []),
            ),
        ),
        T(
            "max_level_sum",
            "def max_level_sum(root):\n"
            '    """1-indexed level whose node values sum to the maximum."""\n'
            "    if root is None:\n"
            "        return 0\n"
            "    best_sum = root[0]\n"
            "    best_lvl = 1\n"
            "    q = [root]\n"
            "    lvl = 1\n"
            "    while q:\n"
            "        s = 0\n"
            "        nxt = []\n"
            "        for node in q:\n"
            "            s += node[0]\n"
            "            left = node[1] if len(node) > 1 else None\n"
            "            right = node[2] if len(node) > 2 else None\n"
            "            if left is not None:\n"
            "                nxt.append(left)\n"
            "            if right is not None:\n"
            "                nxt.append(right)\n"
            "        if s > best_sum:\n"
            "            best_sum = s\n"
            "            best_lvl = lvl\n"
            "        q = nxt\n"
            "        lvl += 1\n"
            "    return best_lvl\n",
            lambda low: bool(
                re.search(
                    r"\bmax[_ ]level[_ ]sum\b|"
                    r"\bmaximum level sum\b|"
                    r"\bmax(?:imum)? level sum of (?:a |the )?(?:binary )?tree\b|"
                    r"\blevel with (?:the )?maximum sum\b",
                    low,
                )
            ),
            (
                (([1, [7, [7, None, None], [-8, None, None]], [0, None, None]],), 2),
                (([989, None, [10250, [98693, None, None], [-89388, None, [-32127, None, None]]]],), 2),
                (([1, None, None],), 1),
            ),
        ),
        T(
            "insert_into_bst",
            "def insert_into_bst(root, val):\n"
            '    """Insert val into a BST represented as [v, left, right]."""\n'
            "    node = [val, None, None]\n"
            "    if root is None:\n"
            "        return node\n"
            "    cur = root\n"
            "    while True:\n"
            "        if val < cur[0]:\n"
            "            left = cur[1] if len(cur) > 1 else None\n"
            "            if left is None:\n"
            "                if len(cur) < 2:\n"
            "                    cur.append(node)\n"
            "                    cur.append(None)\n"
            "                else:\n"
            "                    cur[1] = node\n"
            "                return root\n"
            "            cur = left\n"
            "        else:\n"
            "            right = cur[2] if len(cur) > 2 else None\n"
            "            if right is None:\n"
            "                while len(cur) < 3:\n"
            "                    cur.append(None)\n"
            "                cur[2] = node\n"
            "                return root\n"
            "            cur = right\n",
            lambda low: bool(
                re.search(
                    r"\binsert[_ ]into[_ ]bst\b|"
                    r"\binsert into (?:a |the )?bst\b|"
                    r"\binsert (?:a )?value into (?:a |the )?(?:binary search tree|bst)\b|"
                    r"\bbst insert\b",
                    low,
                )
            ),
            (
                (([4, [2, [1, None, None], [3, None, None]], [7, None, None]], 5),
                 [4, [2, [1, None, None], [3, None, None]], [7, [5, None, None], None]]),
                ((None, 2), [2, None, None]),
                (([1, None, None], 2), [1, None, [2, None, None]]),
            ),
        ),
        T(
            "closest_value",
            "def closest_value(root, target):\n"
            '    """BST value closest to target (ties: smaller value)."""\n'
            "    closest = root[0]\n"
            "    cur = root\n"
            "    while cur is not None:\n"
            "        v = cur[0]\n"
            "        dv = abs(v - target)\n"
            "        dc = abs(closest - target)\n"
            "        if dv < dc or (dv == dc and v < closest):\n"
            "            closest = v\n"
            "        if target < v:\n"
            "            cur = cur[1] if len(cur) > 1 else None\n"
            "        else:\n"
            "            cur = cur[2] if len(cur) > 2 else None\n"
            "    return closest\n",
            lambda low: bool(
                re.search(
                    r"\bclosest[_ ]value\b|"
                    r"\bclosest (?:bst |binary search tree )?value\b|"
                    r"\bclosest value in (?:a |the )?(?:bst|binary search tree)\b|"
                    r"\bfind closest value\b",
                    low,
                )
            ),
            (
                (([4, [2, [1, None, None], [3, None, None]], [5, None, None]], 3.714), 4),
                (([1, None, None], 4.4), 1),
                (([4, [2, None, None], [5, None, None]], 3.5), 4),
            ),
        ),
    ]
