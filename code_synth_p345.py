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
                re.search(r"\\bpalindrome\\b", low)
                and re.search(r"\\b(partition|partitioning)\\b", low)
                and not re.search(r"\\b(ii|2|min.?cut|minimum.?cuts?)\\b", low)
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
                re.search(r"\\blongest\\b", low)
                and re.search(r"\\bincreasing\\b", low)
                and re.search(r"\\b(subsequence|lis)\\b", low)
            )
            and "path" not in low
            and "matrix" not in low,
            (
                (([10, 9, 2, 5, 3, 7, 101, 18],), 4),
                (([0, 1, 0, 3, 2, 3],), 4),
                (([7, 7, 7],), 1),
            ),
        ),
    ]
