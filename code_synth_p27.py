"""Cycle 287: merge trees / search BST / level averages / left leaves / tilt / two-sum IV."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "merge_trees",
            "def merge_trees(t1, t2):\n"
            '    """Merge two binary trees encoded as [val, left, right] or None."""\n'
            "    if t1 is None:\n"
            "        return t2\n"
            "    if t2 is None:\n"
            "        return t1\n"
            "    v1, l1, r1 = t1[0], t1[1] if len(t1) > 1 else None, t1[2] if len(t1) > 2 else None\n"
            "    v2, l2, r2 = t2[0], t2[1] if len(t2) > 1 else None, t2[2] if len(t2) > 2 else None\n"
            "    return [v1 + v2, merge_trees(l1, l2), merge_trees(r1, r2)]\n",
            lambda low: bool(
                re.search(
                    r"\bmerge[_ ]trees\b|"
                    r"\bmerge (?:two )?binary trees\b|"
                    r"\bmerge two trees\b",
                    low,
                )
                and "linked" not in low
            ),
            (
                (
                    (
                        [1, [3, [5, None, None], None], [2, None, None]],
                        [2, [1, None, [4, None, None]], [3, None, [7, None, None]]],
                    ),
                    [3, [4, [5, None, None], [4, None, None]], [5, None, [7, None, None]]],
                ),
                ((None, [1, None, None]), [1, None, None]),
                ((None, None), None),
            ),
        ),
        T(
            "search_bst",
            "def search_bst(root, val):\n"
            '    """Return the subtree rooted at val, or None."""\n'
            "    cur = root\n"
            "    while cur is not None:\n"
            "        v = cur[0]\n"
            "        if v == val:\n"
            "            return cur\n"
            "        if val < v:\n"
            "            cur = cur[1] if len(cur) > 1 else None\n"
            "        else:\n"
            "            cur = cur[2] if len(cur) > 2 else None\n"
            "    return None\n",
            lambda low: bool(
                re.search(
                    r"\bsearch[_ ]bst\b|"
                    r"\bsearch (?:in )?(?:a |the )?binary search tree\b|"
                    r"\bsearch (?:a |the )?bst\b",
                    low,
                )
                and "matrix" not in low
                and "rotated" not in low
                and "insert" not in low
            ),
            (
                (([4, [2, [1, None, None], [3, None, None]], [7, None, None]], 2),
                 [2, [1, None, None], [3, None, None]]),
                (([4, [2, [1, None, None], [3, None, None]], [7, None, None]], 5), None),
            ),
        ),
        T(
            "average_of_levels",
            "def average_of_levels(root):\n"
            '    """Mean value of nodes on each level."""\n'
            "    if root is None:\n"
            "        return []\n"
            "    from collections import deque\n"
            "    q = deque([root])\n"
            "    out = []\n"
            "    while q:\n"
            "        n = len(q)\n"
            "        total = 0.0\n"
            "        for _ in range(n):\n"
            "            node = q.popleft()\n"
            "            total += node[0]\n"
            "            left = node[1] if len(node) > 1 else None\n"
            "            right = node[2] if len(node) > 2 else None\n"
            "            if left is not None:\n"
            "                q.append(left)\n"
            "            if right is not None:\n"
            "                q.append(right)\n"
            "        out.append(total / n)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\baverage[_ ]of[_ ]levels\b|"
                    r"\baverage of (?:the )?levels\b|"
                    r"\blevel averages?\b|"
                    r"\baverage (?:value )?of (?:nodes )?(?:in |on )?each level\b",
                    low,
                )
            ),
            (
                (([3, [9, None, None], [20, [15, None, None], [7, None, None]]],), [3.0, 14.5, 11.0]),
                (([1, None, None],), [1.0]),
            ),
        ),
        T(
            "sum_of_left_leaves",
            "def sum_of_left_leaves(root):\n"
            '    """Sum values of leaves that are left children."""\n'
            "    def walk(node, is_left):\n"
            "        if node is None:\n"
            "            return 0\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        if left is None and right is None:\n"
            "            return node[0] if is_left else 0\n"
            "        return walk(left, True) + walk(right, False)\n"
            "    return walk(root, False)\n",
            lambda low: bool(
                re.search(
                    r"\bsum[_ ]of[_ ]left[_ ]leaves\b|"
                    r"\bsum of left leaves\b|"
                    r"\bleft leaves? sum\b",
                    low,
                )
            ),
            (
                (([3, [9, None, None], [20, [15, None, None], [7, None, None]]],), 24),
                (([1, None, None],), 0),
            ),
        ),
        T(
            "find_tilt",
            "def find_tilt(root):\n"
            '    """Sum of |left-subtree-sum - right-subtree-sum| over every node."""\n'
            "    total = [0]\n"
            "    def dfs(node):\n"
            "        if node is None:\n"
            "            return 0\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        ls, rs = dfs(left), dfs(right)\n"
            "        total[0] += abs(ls - rs)\n"
            "        return node[0] + ls + rs\n"
            "    dfs(root)\n"
            "    return total[0]\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]tilt\b|"
                    r"\bbinary tree tilt\b|"
                    r"\btilt of (?:a |the )?binary tree\b",
                    low,
                )
            ),
            (
                (([1, [2, None, None], [3, None, None]],), 1),
                (([4, [2, [3, None, None], [5, None, None]], [9, None, [7, None, None]]],), 15),
                ((None,), 0),
            ),
        ),
        T(
            "two_sum_iv",
            "def two_sum_iv(root, k):\n"
            '    """True if two distinct BST nodes sum to k."""\n'
            "    seen = set()\n"
            "    stack = [root] if root is not None else []\n"
            "    while stack:\n"
            "        node = stack.pop()\n"
            "        if node is None:\n"
            "            continue\n"
            "        v = node[0]\n"
            "        if k - v in seen:\n"
            "            return True\n"
            "        seen.add(v)\n"
            "        if len(node) > 1 and node[1] is not None:\n"
            "            stack.append(node[1])\n"
            "        if len(node) > 2 and node[2] is not None:\n"
            "            stack.append(node[2])\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\btwo[_ ]sum[_ ]iv\b|"
                    r"\btwo[- ]sum (?:iv|4)\b|"
                    r"\btwo sum in (?:a |the )?bst\b|"
                    r"\btwo sum (?:in |of )?(?:a |the )?binary search tree\b",
                    low,
                )
            ),
            (
                (([5, [3, [2, None, None], [4, None, None]], [6, None, [7, None, None]]], 9), True),
                (([5, [3, [2, None, None], [4, None, None]], [6, None, [7, None, None]]], 28), False),
            ),
        ),
    ]
