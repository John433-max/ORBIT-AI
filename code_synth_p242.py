"""Cycle 545: path sum III, next-right connect, inorder+postorder tree."""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "path_sum_iii",
            "def path_sum_iii(root, target):\n"
            '    """Count downward paths (any start) that sum to target on a [val, left, right] tree."""\n'
            "    count = 0\n"
            "\n"
            "    def dfs(node, curr, prefix):\n"
            "        nonlocal count\n"
            "        if node is None:\n"
            "            return\n"
            "        val = node[0]\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        curr += val\n"
            "        count += prefix.get(curr - target, 0)\n"
            "        prefix[curr] = prefix.get(curr, 0) + 1\n"
            "        dfs(left, curr, prefix)\n"
            "        dfs(right, curr, prefix)\n"
            "        prefix[curr] -= 1\n"
            "\n"
            "    dfs(root, 0, {0: 1})\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\bpath[- ]?sum[- ]?(?:iii|3)\b|"
                    r"\bcount (?:the )?paths?(?: that)? sum\b|"
                    r"\bnumber of paths?(?: that)? sum\b|"
                    r"\bpath_sum_iii\b|"
                    r"\bpaths? equal to (?:a )?target\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            10,
                            [5, [3, [3, None, None], [-2, None, None]], [2, None, [1, None, None]]],
                            [-3, None, [11, None, None]],
                        ],
                        8,
                    ),
                    3,
                ),
                (([1, None, None], 1), 1),
                ((None, 0), 0),
            ),
        ),
        T(
            "connect_next_right",
            "def connect_next_right(root):\n"
            '    """Link each node to the next node on its level. Node is [val, left, right, next]."""\n'
            "    if root is None:\n"
            "        return None\n"
            "    # Ensure 4 slots.\n"
            "    def norm(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        val = node[0]\n"
            "        left = norm(node[1] if len(node) > 1 else None)\n"
            "        right = norm(node[2] if len(node) > 2 else None)\n"
            "        return [val, left, right, None]\n"
            "\n"
            "    root = norm(root)\n"
            "    level = [root]\n"
            "    while level:\n"
            "        nxt = []\n"
            "        for i, node in enumerate(level):\n"
            "            node[3] = level[i + 1][0] if i + 1 < len(level) else None\n"
            "            if node[1] is not None:\n"
            "                nxt.append(node[1])\n"
            "            if node[2] is not None:\n"
            "                nxt.append(node[2])\n"
            "        level = nxt\n"
            "    return root\n",
            lambda low: bool(
                re.search(
                    r"\bnext[- ]right\b|"
                    r"\bpopulat(?:e|ing) next right\b|"
                    r"\bconnect(?: nodes)? at (?:the )?same level\b|"
                    r"\bconnect_next_right\b|"
                    r"\bright pointer\b|"
                    r"\bnext pointer(?:s)? in (?:each|a) node\b",
                    low,
                )
            ),
            (
                (
                    ([1, [2, [4, None, None], [5, None, None]], [3, [6, None, None], [7, None, None]]],),
                    [
                        1,
                        [2, [4, None, None, 5], [5, None, None, 6], 3],
                        [3, [6, None, None, 7], [7, None, None, None], None],
                        None,
                    ],
                ),
            ),
        ),
        T(
            "build_tree_post",
            "def build_tree_post(inorder, postorder):\n"
            '    """Construct a [val, left, right] tree from inorder and postorder traversals."""\n'
            "    if not inorder or not postorder:\n"
            "        return None\n"
            "    root_val = postorder[-1]\n"
            "    i = inorder.index(root_val)\n"
            "    left = build_tree_post(inorder[:i], postorder[:i])\n"
            "    right = build_tree_post(inorder[i + 1 :], postorder[i:-1])\n"
            "    return [root_val, left, right]\n",
            lambda low: bool(
                re.search(
                    r"\b(?:construct|build|create).{0,40}(?:inorder|in-order).{0,40}(?:postorder|post-order)\b|"
                    r"\b(?:inorder|in-order).{0,40}(?:postorder|post-order).{0,24}(?:tree|traversal)\b|"
                    r"\bbuild_tree_post\b|"
                    r"\bfrom inorder and postorder\b",
                    low,
                )
            ),
            (
                (([9, 3, 15, 20, 7], [9, 15, 7, 20, 3]), [3, [9, None, None], [20, [15, None, None], [7, None, None]]]),
                (([], []), None),
            ),
        ),
    ]
