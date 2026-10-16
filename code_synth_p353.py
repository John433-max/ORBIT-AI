"""Cycle 644 (p353): coding-smoke gaps.

construct_maximum_binary_tree (654), delete_node_bst (450),
count_binary_substrings (696).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "construct_maximum_binary_tree",
            '''def construct_maximum_binary_tree(nums):
    """Build maximum binary tree from array (LeetCode 654, educational).

    Root is max(nums); left/right subtrees from subarrays left/right of max.
    Returns nested list [val, left, right] (None children as None).
    """
    if not nums:
        return None

    def build(lo, hi):
        if lo > hi:
            return None
        mx = lo
        for i in range(lo, hi + 1):
            if nums[i] > nums[mx]:
                mx = i
        return [nums[mx], build(lo, mx - 1), build(mx + 1, hi)]

    return build(0, len(nums) - 1)
''',
            lambda low: bool(
                re.search(r"\bconstruct[_ ]maximum[_ ]binary[_ ]tree\b", low)
                or re.search(r"\bmaximum[_ ]binary[_ ]tree\b", low)
                or re.search(r"\bmax[_ ]binary[_ ]tree\b", low)
                or re.search(r"\bleetcode\s+654\b", low)
            ),
            (
                (([3, 2, 1, 6, 0, 5],), [6, [3, None, [2, None, [1, None, None]]], [5, [0, None, None], None]]),
                (([3, 2, 1],), [3, None, [2, None, [1, None, None]]]),
            ),
        ),
        T(
            "delete_node_bst",
            '''def delete_node_bst(root, key):
    """Delete key from BST; return new root as nested [val, left, right] (LeetCode 450)."""
    def delete(node, k):
        if node is None:
            return None
        val, left, right = node[0], node[1], node[2]
        if k < val:
            return [val, delete(left, k), right]
        if k > val:
            return [val, left, delete(right, k)]
        if left is None:
            return right
        if right is None:
            return left
        succ = right
        while succ[1] is not None:
            succ = succ[1]
        return [succ[0], left, delete(right, succ[0])]

    return delete(root, key)
''',
            lambda low: bool(
                re.search(
                    r"\bdelete[_ ]node[_ ](?:in[_ ]a[_ ]|from[_ ]a[_ ])?bst\b|"
                    r"\bdelet(?:e|es|ing)\s+(?:a\s+)?node\s+in\s+(?:a\s+)?bst\b|"
                    r"\bdelet(?:e|es|ing)\s+(?:a\s+)?bst\s+node\b|"
                    r"\bleetcode\s+450\b",
                    low,
                )
            )
            and "linked" not in low,
            (
                (
                    (
                        [5, [3, [2, None, None], [4, None, None]], [6, None, [7, None, None]]],
                        3,
                    ),
                    [5, [4, [2, None, None], None], [6, None, [7, None, None]]],
                ),
                (
                    (
                        [5, [3, [2, None, None], [4, None, None]], [6, None, [7, None, None]]],
                        0,
                    ),
                    [5, [3, [2, None, None], [4, None, None]], [6, None, [7, None, None]]],
                ),
            ),
        ),
        T(
            "count_binary_substrings",
            '''def count_binary_substrings(s):
    """Count substrings with equal 0s and 1s, all 0s/1s grouped (LeetCode 696)."""
    groups = []
    prev = s[0] if s else ""
    cnt = 0
    for ch in s:
        if ch == prev:
            cnt += 1
        else:
            groups.append(cnt)
            prev = ch
            cnt = 1
    if cnt:
        groups.append(cnt)
    ans = 0
    for i in range(1, len(groups)):
        ans += min(groups[i - 1], groups[i])
    return ans
''',
            lambda low: bool(
                re.search(r"\bcount[_ ]binary[_ ]substrings?\b", low)
                or re.search(r"\bbinary[_ ]substrings?\b", low)
                or re.search(r"\bleetcode\s+696\b", low)
            ),
            (
                (("00110011",), 6),
                (("10101",), 4),
                (("00110",), 3),
            ),
        ),
    ]
