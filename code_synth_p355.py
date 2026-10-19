"""Cycle 647 (p355): six classic educational templates.

longest_increasing_subsequence (300), non_overlapping_intervals (435),
minimum_path_sum (64), partition_equal_subset_sum (416),
climbing_stairs (70), kth_largest_element (215).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "longest_increasing_subsequence",
            '''def longest_increasing_subsequence(nums):
    """Length of longest strictly increasing subsequence (LeetCode 300).

    Patience sorting / binary search tails: O(n log n).
    """
    import bisect

    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
''',
            lambda low: bool(
                re.search(
                    r"\blongest[_ ]increasing[_ ]subsequence\b|"
                    r"\blis\b|"
                    r"\blength\s+of\s+(?:the\s+)?longest\s+(?:strictly\s+)?increasing\s+subsequence\b|"
                    r"\bleetcode\s+300\b",
                    low,
                )
            )
            and "path" not in low
            and "subarray" not in low
            and "nlogn" not in low
            and "patience" not in low
            and not re.search(r"\bn\s*log\s*n\b", low),
            (
                (([10, 9, 2, 5, 3, 7, 101, 18],), 4),
                (([0, 1, 0, 3, 2, 3],), 4),
                (([7, 7, 7, 7],), 1),
            ),
        ),
        T(
            "non_overlapping_intervals",
            '''def non_overlapping_intervals(intervals):
    """Minimum number of intervals to remove so the rest are non-overlapping (LeetCode 435).

    Sort by end; greedily keep the earliest-ending interval.
    """
    if not intervals:
        return 0
    intervals = sorted(intervals, key=lambda x: x[1])
    end = intervals[0][1]
    removed = 0
    for s, e in intervals[1:]:
        if s < end:
            removed += 1
        else:
            end = e
    return removed
''',
            lambda low: bool(
                re.search(
                    r"\bnon[_ ]overlapping[_ ]intervals?\b|"
                    r"\bminimum\s+(?:number\s+of\s+)?intervals?\s+to\s+remove\b|"
                    r"\berase\s+overlapping\s+intervals?\b|"
                    r"\bleetcode\s+435\b",
                    low,
                )
            )
            and "meeting" not in low,
            (
                (([[1, 2], [2, 3], [3, 4], [1, 3]],), 1),
                (([[1, 2], [1, 2], [1, 2]],), 2),
                (([[1, 2], [2, 3]],), 0),
            ),
        ),
        T(
            "minimum_path_sum",
            '''def minimum_path_sum(grid):
    """Minimum path sum from top-left to bottom-right (LeetCode 64).

    Only right and down moves. DP in-place on a copy.
    """
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    dp = [row[:] for row in grid]
    for j in range(1, n):
        dp[0][j] += dp[0][j - 1]
    for i in range(1, m):
        dp[i][0] += dp[i - 1][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] += min(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]
''',
            lambda low: bool(
                re.search(
                    r"\bminimum[_ ]path[_ ]sum\b|"
                    r"\bmin(?:imum)?\s+path\s+sum\b|"
                    r"\bpath\s+sum\s+from\s+top[- ]left\b|"
                    r"\bleetcode\s+64\b",
                    low,
                )
            )
            and "binary" not in low
            and "tree" not in low,
            (
                (([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), 7),
                (([[1, 2, 3], [4, 5, 6]],), 12),
            ),
        ),
        T(
            "partition_equal_subset_sum",
            '''def partition_equal_subset_sum(nums):
    """Whether the array can be partitioned into two equal-sum subsets (LeetCode 416).

    Classic 0/1 knapsack / subset-sum DP.
    """
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]
    return dp[target]
''',
            lambda low: bool(
                re.search(
                    r"\bpartition[_ ]equal[_ ]subset[_ ]sum\b|"
                    r"\bcan\s+partition\b|"
                    r"\bpartition\s+(?:into\s+)?two\s+equal\s+sum\b|"
                    r"\bleetcode\s+416\b",
                    low,
                )
            )
            and "list" not in low,
            (
                (([1, 5, 11, 5],), True),
                (([1, 2, 3, 5],), False),
            ),
        ),
        T(
            "climbing_stairs",
            '''def climbing_stairs(n):
    """Number of distinct ways to climb n stairs taking 1 or 2 steps (LeetCode 70).

    Fibonacci: ways(n) = ways(n-1) + ways(n-2).
    """
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
''',
            lambda low: bool(
                re.search(
                    r"\bclimbing[_ ]stairs\b|"
                    r"\bclimb\s+stairs\b|"
                    r"\bways\s+to\s+climb\s+n\s+stairs\b|"
                    r"\bleetcode\s+70\b",
                    low,
                )
            )
            and "min" not in low
            and "cost" not in low,
            (
                ((2,), 2),
                ((3,), 3),
                ((4,), 5),
            ),
        ),
        T(
            "kth_largest_element",
            '''def kth_largest_element(nums, k):
    """k-th largest element in an unsorted array (LeetCode 215).

    Quickselect / heap; here sorted for clarity (educational).
    """
    if k < 1 or k > len(nums):
        raise ValueError("k out of range")
    return sorted(nums, reverse=True)[k - 1]
''',
            lambda low: bool(
                re.search(
                    r"\bkth[_ ]largest[_ ]element\b|"
                    r"\bk[- ]th\s+largest\b|"
                    r"\bfind\s+the\s+kth\s+largest\b|"
                    r"\bleetcode\s+215\b",
                    low,
                )
            )
            and "in a stream" not in low
            and "sorted" not in low,
            (
                (([3, 2, 1, 5, 6, 4], 2), 5),
                (([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4),
            ),
        ),
    ]
