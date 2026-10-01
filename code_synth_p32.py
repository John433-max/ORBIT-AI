"""Cycle 292: tree2str / prune / univalue path / smallest-from-leaf / ancestor-diff / array pair sum."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "tree2str",
            "def tree2str(root):\n"
            '    """Construct a string from a binary tree (LeetCode 606)."""\n'
            "    if root is None:\n"
            "        return ''\n"
            "    val = str(root[0])\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    if left is None and right is None:\n"
            "        return val\n"
            "    if right is None:\n"
            "        return val + '(' + tree2str(left) + ')'\n"
            "    return val + '(' + tree2str(left) + ')(' + tree2str(right) + ')'\n",
            lambda low: bool(
                re.search(
                    r"\btree2str\b|"
                    r"\bconstruct[_ ]string[_ ]from[_ ](?:a |the )?(?:binary )?tree\b|"
                    r"\bconstruct a string from (?:a |the )?binary tree\b|"
                    r"\btree to string\b|"
                    r"\bstring from (?:a |the )?binary tree\b",
                    low,
                )
            ),
            (
                (([1, [2, [4, None, None], None], [3, None, None]],), "1(2(4))(3)"),
                (([1, [2, None, [4, None, None]], [3, None, None]],), "1(2()(4))(3)"),
                (([1, None, None],), "1"),
            ),
        ),
        T(
            "prune_tree",
            "def prune_tree(root):\n"
            '    """Remove subtrees that contain no 1 (LeetCode 814)."""\n'
            "    if root is None:\n"
            "        return None\n"
            "    left = prune_tree(root[1] if len(root) > 1 else None)\n"
            "    right = prune_tree(root[2] if len(root) > 2 else None)\n"
            "    if root[0] == 0 and left is None and right is None:\n"
            "        return None\n"
            "    return [root[0], left, right]\n",
            lambda low: bool(
                re.search(
                    r"\bprune[_ ]tree\b|"
                    r"\bbinary[_ ]tree[_ ]pruning\b|"
                    r"\bprune (?:a |the )?binary tree\b|"
                    r"\bpruning (?:a |the )?binary tree\b|"
                    r"\bremove subtrees? (?:containing |with )?no 1\b",
                    low,
                )
            ),
            (
                (([1, None, [0, [0, None, None], [1, None, None]]],), [1, None, [0, None, [1, None, None]]]),
                (([1, [0, [0, None, None], [0, None, None]], [1, [0, None, None], [1, None, None]]],),
                 [1, None, [1, None, [1, None, None]]]),
                (([0, None, None],), None),
            ),
        ),
        T(
            "longest_univalue_path",
            "def longest_univalue_path(root):\n"
            '    """Longest path where every node has the same value (edges)."""\n'
            "    best = [0]\n"
            "\n"
            "    def dfs(node):\n"
            "        if node is None:\n"
            "            return 0\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        lo = dfs(left)\n"
            "        ro = dfs(right)\n"
            "        lsame = lo + 1 if left is not None and left[0] == node[0] else 0\n"
            "        rsame = ro + 1 if right is not None and right[0] == node[0] else 0\n"
            "        best[0] = max(best[0], lsame + rsame)\n"
            "        return max(lsame, rsame)\n"
            "\n"
            "    dfs(root)\n"
            "    return best[0]\n",
            lambda low: bool(
                re.search(
                    r"\blongest[_ ]univalue[_ ]path\b|"
                    r"\blongest univalue path\b|"
                    r"\blongest (?:same[- ]value|unival(?:ue|ued)?) path\b",
                    low,
                )
            ),
            (
                (([5, [4, [1, None, None], [1, None, None]], [5, None, [5, None, None]]],), 2),
                (([1, [4, [4, None, None], [4, None, None]], [5, None, [5, None, None]]],), 2),
                (([1, None, None],), 0),
            ),
        ),
        T(
            "smallest_from_leaf",
            "def smallest_from_leaf(root):\n"
            '    """Smallest string starting from leaf (a=0) to root."""\n'
            "    best = [None]\n"
            "\n"
            "    def dfs(node, acc):\n"
            "        if node is None:\n"
            "            return\n"
            "        ch = chr(ord('a') + int(node[0]))\n"
            "        cur = ch + acc\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        if left is None and right is None:\n"
            "            if best[0] is None or cur < best[0]:\n"
            "                best[0] = cur\n"
            "            return\n"
            "        dfs(left, cur)\n"
            "        dfs(right, cur)\n"
            "\n"
            "    dfs(root, '')\n"
            "    return best[0] or ''\n",
            lambda low: bool(
                re.search(
                    r"\bsmallest[_ ]from[_ ]leaf\b|"
                    r"\bsmallest string starting from leaf\b|"
                    r"\bsmallest string from leaf\b|"
                    r"\bsmallest leaf to root string\b",
                    low,
                )
            ),
            (
                (([0, [1, [3, None, None], [4, None, None]], [2, [3, None, None], [4, None, None]]],), "dba"),
                (([25, [1, [1, None, None], [3, None, None]], [3, [0, None, None], [2, None, None]]],), "adz"),
                (([2, [2, None, [1, [0, None, None], None]], [1, [0, None, None], None]],), "abc"),
            ),
        ),
        T(
            "max_ancestor_diff",
            "def max_ancestor_diff(root):\n"
            '    """Max |ancestor - descendant| in a binary tree."""\n'
            "    best = [0]\n"
            "\n"
            "    def dfs(node, lo, hi):\n"
            "        if node is None:\n"
            "            return\n"
            "        v = node[0]\n"
            "        best[0] = max(best[0], abs(v - lo), abs(v - hi))\n"
            "        nlo, nhi = min(lo, v), max(hi, v)\n"
            "        dfs(node[1] if len(node) > 1 else None, nlo, nhi)\n"
            "        dfs(node[2] if len(node) > 2 else None, nlo, nhi)\n"
            "\n"
            "    if root is None:\n"
            "        return 0\n"
            "    dfs(root, root[0], root[0])\n"
            "    return best[0]\n",
            lambda low: bool(
                re.search(
                    r"\bmax[_ ]ancestor[_ ]diff\b|"
                    r"\bmaximum difference between node and ancestor\b|"
                    r"\bmax(?:imum)? ancestor (?:value )?diff(?:erence)?\b|"
                    r"\bmax(?:imum)? \|?ancestor[- ]descendant\|?\b",
                    low,
                )
            ),
            (
                (([8, [3, [1, None, None], [6, [4, None, None], [7, None, None]]], [10, None, [14, [13, None, None], None]]],), 7),
                (([1, None, [2, None, [0, [3, None, None], None]]],), 3),
                (([1, None, None],), 0),
            ),
        ),
        T(
            "array_pair_sum",
            "def array_pair_sum(nums):\n"
            '    """Max sum of min(a,b) over n pairs (LeetCode 561)."""\n'
            "    xs = sorted(nums)\n"
            "    return sum(xs[i] for i in range(0, len(xs), 2))\n",
            lambda low: bool(
                re.search(
                    r"\barray[_ ]pair[_ ]sum\b|"
                    r"\barray partition i\b|"
                    r"\barray pair sum\b|"
                    r"\bmax(?:imize|imum)? sum of min(?:imum)?s? of pairs\b|"
                    r"\bsum of min of n pairs\b",
                    low,
                )
            ),
            (
                (([1, 4, 3, 2],), 4),
                (([6, 2, 6, 5, 1, 2],), 9),
                (([1, 1],), 1),
            ),
        ),
    ]
