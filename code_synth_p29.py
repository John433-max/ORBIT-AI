"""Cycle 289: bottom-left / balanced / root-to-leaf binary sum / unival / deepest leaves / good nodes."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "find_bottom_left",
            "def find_bottom_left(root):\n"
            '    """Value of the leftmost node on the last level."""\n'
            "    if root is None:\n"
            "        return None\n"
            "    q = [root]\n"
            "    leftmost = root[0]\n"
            "    while q:\n"
            "        leftmost = q[0][0]\n"
            "        nxt = []\n"
            "        for node in q:\n"
            "            left = node[1] if len(node) > 1 else None\n"
            "            right = node[2] if len(node) > 2 else None\n"
            "            if left is not None:\n"
            "                nxt.append(left)\n"
            "            if right is not None:\n"
            "                nxt.append(right)\n"
            "        q = nxt\n"
            "    return leftmost\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]bottom[_ ]left\b|"
                    r"\bbottom[- ]left(?:most)? (?:tree )?value\b|"
                    r"\bleftmost (?:value|node) (?:on|in) (?:the )?(?:last|bottom|deepest) level\b|"
                    r"\bfind bottom left tree value\b",
                    low,
                )
            ),
            (
                (([2, [1, None, None], [3, None, None]],), 1),
                (([1, [2, [4, None, None], None], [3, [5, [7, None, None], None], [6, None, None]]],), 7),
                ((None,), None),
            ),
        ),
        T(
            "is_balanced",
            "def is_balanced(root):\n"
            '    """True if tree heights of every node differ by at most 1."""\n'
            "    def height(node):\n"
            "        if node is None:\n"
            "            return 0\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        lh = height(left)\n"
            "        if lh < 0:\n"
            "            return -1\n"
            "        rh = height(right)\n"
            "        if rh < 0 or abs(lh - rh) > 1:\n"
            "            return -1\n"
            "        return 1 + max(lh, rh)\n"
            "    return height(root) >= 0\n",
            lambda low: bool(
                re.search(
                    r"\bis[_ ]balanced\b|"
                    r"\bbalanced binary tree\b|"
                    r"\bheight[- ]balanced (?:binary )?tree\b|"
                    r"\bcheck (?:if )?(?:a |the )?tree is balanced\b",
                    low,
                )
            ),
            (
                (([3, [9, None, None], [20, [15, None, None], [7, None, None]]],), True),
                (([1, [2, [3, [4, None, None], [4, None, None]], [3, None, None]], [2, None, None]],), False),
                ((None,), True),
            ),
        ),
        T(
            "sum_root_to_leaf",
            "def sum_root_to_leaf(root):\n"
            '    """Sum of root-to-leaf binary numbers (0/1 nodes)."""\n'
            "    total = [0]\n"
            "    def walk(node, acc):\n"
            "        if node is None:\n"
            "            return\n"
            "        acc = (acc << 1) | int(node[0])\n"
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
                    r"\bsum_root_to_leaf\b|"
                    r"\bsum of root[- ]to[- ]leaf binary (?:numbers|paths)\b|"
                    r"\broot to leaf binary\b|"
                    r"\bbinary numbers from root to leaf\b",
                    low,
                )
            ),
            (
                (([1, [0, [0, None, None], [1, None, None]], [1, [0, None, None], [1, None, None]]],), 22),
                (([0, None, None],), 0),
                ((None,), 0),
            ),
        ),
        T(
            "is_unival_tree",
            "def is_unival_tree(root):\n"
            '    """True if every node has the same value."""\n'
            "    if root is None:\n"
            "        return True\n"
            "    target = root[0]\n"
            "    stack = [root]\n"
            "    while stack:\n"
            "        n = stack.pop()\n"
            "        if n is None:\n"
            "            continue\n"
            "        if n[0] != target:\n"
            "            return False\n"
            "        stack.append(n[1] if len(n) > 1 else None)\n"
            "        stack.append(n[2] if len(n) > 2 else None)\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bis[_ ]unival(?:ued)?[_ ]tree\b|"
                    r"\bunival(?:ued)? (?:binary )?tree\b|"
                    r"\ball nodes (?:have )?the same value\b|"
                    r"\bsingle[- ]valued tree\b",
                    low,
                )
            ),
            (
                (([1, [1, [1, None, None], [1, None, None]], [1, None, [1, None, None]]],), True),
                (([1, [1, None, None], [2, None, None]],), False),
                ((None,), True),
            ),
        ),
        T(
            "deepest_leaves_sum",
            "def deepest_leaves_sum(root):\n"
            '    """Sum of node values at the deepest level."""\n'
            "    if root is None:\n"
            "        return 0\n"
            "    q = [root]\n"
            "    while q:\n"
            "        level_sum = 0\n"
            "        nxt = []\n"
            "        for node in q:\n"
            "            level_sum += node[0]\n"
            "            left = node[1] if len(node) > 1 else None\n"
            "            right = node[2] if len(node) > 2 else None\n"
            "            if left is not None:\n"
            "                nxt.append(left)\n"
            "            if right is not None:\n"
            "                nxt.append(right)\n"
            "        if not nxt:\n"
            "            return level_sum\n"
            "        q = nxt\n"
            "    return 0\n",
            lambda low: bool(
                re.search(
                    r"\bdeepest[_ ]leaves[_ ]sum\b|"
                    r"\bsum of (?:the )?deepest leaves\b|"
                    r"\bdeepest leaf sum\b|"
                    r"\bdeepest level sum\b",
                    low,
                )
            ),
            (
                (([1, [2, [4, [7, None, None], None], [5, None, None]], [3, None, [6, None, [8, None, None]]]],), 15),
                (([1, None, None],), 1),
                ((None,), 0),
            ),
        ),
        T(
            "good_nodes",
            "def good_nodes(root):\n"
            '    """Count nodes whose value is >= every ancestor (good nodes)."""\n'
            "    def walk(node, best):\n"
            "        if node is None:\n"
            "            return 0\n"
            "        v = node[0]\n"
            "        good = 1 if v >= best else 0\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        nb = v if v > best else best\n"
            "        return good + walk(left, nb) + walk(right, nb)\n"
            "    if root is None:\n"
            "        return 0\n"
            "    return walk(root, root[0])\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]good[_ ]nodes\b|"
                    r"\bgood[_ ]nodes\b|"
                    r"\bcount (?:the )?good nodes\b|"
                    r"\bgood nodes in (?:a |the )?(?:binary )?tree\b",
                    low,
                )
            ),
            (
                (([3, [1, [3, None, None], None], [4, [1, None, None], [5, None, None]]],), 4),
                (([3, [3, [4, None, None], [2, None, None]], None],), 3),
                (([1, None, None],), 1),
            ),
        ),
    ]
