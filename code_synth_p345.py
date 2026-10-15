"""Cycle 638 (p345): educational pure-Python templates for remaining Medium gaps.

Fills natural-language asks that currently fall through to a stub:
  - Palindrome Partitioning (131) — backtracking
  - Longest Increasing Subsequence (300) — DP
  - Longest Consecutive Sequence (128) — hash set
  - Recover Binary Search Tree (99) — inorder + swap (list-tree)
  - Construct Binary Tree from Preorder and Inorder (105) — recursive
  - Partition Equal Subset Sum (416) — 0/1 knapsack DP

Matchers are phrase-gated so existing neighbors hold.
Trees use the educational [val, left, right] list representation.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "palindrome_partitioning",
            '''def palindrome_partitioning(s):
    """All ways to partition s into palindromic substrings.

    Educational LeetCode 131. Backtracking + is-palindrome check.
    Returns a list of lists of strings.
    """
    s = str(s)
    n = len(s)
    ans = []
    path = []

    def is_pal(i, j):
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    def dfs(start):
        if start == n:
            ans.append(path[:])
            return
        for end in range(start, n):
            if is_pal(start, end):
                path.append(s[start:end + 1])
                dfs(end + 1)
                path.pop()

    dfs(0)
    return ans
''',
            lambda low: bool(
                re.search(r"\bpalindrome\b", low)
                and re.search(r"\b(partition|partitioning)\b", low)
                and not re.search(r"\b(ii|2|min.?cut|minimum.?cuts?)\b", low)
            ),
            (
                (("aab",), [["a", "a", "b"], ["aa", "b"]]),
                (("a",), [["a"]]),
            ),
        ),
        T(
            # Smoke code_53 + unit test expect def lis (not long name).
            "lis",
            '''def lis(nums):
    """Length of the longest strictly increasing subsequence.

    Educational LeetCode 300. Classic O(n^2) DP.
    dp[i] = 1 + max(dp[j] for j < i and nums[j] < nums[i]).
    """
    nums = list(nums)
    n = len(nums)
    if n == 0:
        return 0
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
''',
            lambda low: bool(
                re.search(r"\blongest\b", low)
                and re.search(r"\bincreasing\b", low)
                and re.search(r"\b(subsequence|lis)\b", low)
            )
            and "path" not in low
            and "matrix" not in low,
            (
                (([10, 9, 2, 5, 3, 7, 101, 18],), 4),
                (([0, 1, 0, 3, 2, 3],), 4),
                (([7, 7, 7],), 1),
            ),
        ),
        T(
            "longest_consecutive_sequence",
            '''def longest_consecutive_sequence(nums):
    """Length of the longest consecutive elements sequence.

    Educational LeetCode 128. Hash set O(n) scan from sequence starts.
    """
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:
            y = x
            while y in s:
                y += 1
            best = max(best, y - x)
    return best
''',
            lambda low: bool(
                re.search(r"\blongest\b", low)
                and re.search(r"\bconsecutive\b", low)
                and re.search(r"\b(sequence|seq)\b", low)
            ),
            (
                (([100, 4, 200, 1, 3, 2],), 4),
                (([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), 9),
            ),
        ),
        T(
            "recover_bst",
            '''def recover_bst(root):
    """Recover BST with two nodes swapped (list-tree form).

    Educational LeetCode 99. Inorder collect, find swap pair, restore.
    Tree nodes are [val, left, right] lists (None for missing children).
    """
    nodes = []

    def inorder(n):
        if n is None:
            return
        inorder(n[1])
        nodes.append(n)
        inorder(n[2])

    inorder(root)
    vals = [n[0] for n in nodes]
    sorted_vals = sorted(vals)
    bad = [i for i, (a, b) in enumerate(zip(vals, sorted_vals)) if a != b]
    if len(bad) >= 2:
        i, j = bad[0], bad[-1]
        nodes[i][0], nodes[j][0] = nodes[j][0], nodes[i][0]
    elif len(bad) == 1:
        # single inversion edge case — swap with next
        i = bad[0]
        if i + 1 < len(nodes):
            nodes[i][0], nodes[i + 1][0] = nodes[i + 1][0], nodes[i][0]
    return root
''',
            lambda low: bool(
                re.search(r"\brecover\b", low)
                and re.search(r"\b(bst|binary.?search.?tree)\b", low)
            ),
            (
                (([1, [3, None, [2, None, None]], None],), [3, [1, None, [2, None, None]], None]),
            ),
        ),
        T(
            "build_tree_pre_in",
            '''def build_tree_pre_in(preorder, inorder):
    """Construct binary tree from preorder and inorder traversals.

    Educational LeetCode 105. Recursive split on inorder root index.
    Returns [val, left, right] list-tree (None leaves).
    """
    if not preorder or not inorder:
        return None
    root_val = preorder[0]
    mid = inorder.index(root_val)
    left = build_tree_pre_in(preorder[1:mid + 1], inorder[:mid])
    right = build_tree_pre_in(preorder[mid + 1:], inorder[mid + 1:])
    return [root_val, left, right]
''',
            lambda low: bool(
                re.search(r"\b(construct|build|from)\b", low)
                and re.search(r"\bpreorder\b", low)
                and re.search(r"\binorder\b", low)
            ),
            (
                (([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]), [3, [9, None, None], [20, [15, None, None], [7, None, None]]]),
                (([1], [1]), [1, None, None]),
            ),
        ),
        T(
            # Unit tests + smoke expect def can_partition (LeetCode 416 name).
            "can_partition",
            '''def can_partition(nums):
    """Whether the array can be partitioned into two equal-sum subsets.

    Educational LeetCode 416. 0/1 knapsack DP targeting sum/2.
    """
    nums = list(nums)
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for j in range(target, x - 1, -1):
            if dp[j - x]:
                dp[j] = True
    return dp[target]
''',
            lambda low: bool(
                re.search(r"\bpartition\b", low)
                and re.search(r"\bequal\b", low)
                and re.search(r"\b(subset|sum)\b", low)
            )
            or bool(re.search(r"\b416\b", low)),
            (
                (([1, 5, 11, 5],), True),
                (([1, 2, 3, 5],), False),
            ),
        ),
    ]
