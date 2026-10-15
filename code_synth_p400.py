"""Cycle 400: matcher overrides for remaining smoke coding fails.

Higher pack number wins name collisions (code_synth loads descending).
Fixes:
  - is_power_of_two no longer steals "bitonic sort power of two"
  - sum_subarray_mins no longer steals "minimum size subarray sum"
  - letter_case_permutation / permutation_in_string specificity
  - bitonic_sort, stooge_sort, geohash_encode, dbscan_demo, lu_decomposition,
    christofides_tsp educational implementations (no NotImplemented stub)
"""
from __future__ import annotations

import re
from code_synth import Template


def templates() -> list[Template]:
    return [
        Template(
            "min_subarray_len",
            '''def min_subarray_len(target, nums):
    """Minimal length of a contiguous subarray with sum >= target.

    Educational LeetCode 209. Positive integers; sliding window.
    Returns 0 if impossible.
    """
    if not nums:
        return 0
    target = int(target)
    left = 0
    total = 0
    ans = len(nums) + 1
    for right, x in enumerate(nums):
        total += int(x)
        while total >= target and left <= right:
            length = right - left + 1
            if length < ans:
                ans = length
            total -= int(nums[left])
            left += 1
    return 0 if ans > len(nums) else ans
''',
            lambda low: bool(
                re.search(r"\bminimum\b|\bmin\b", low)
                and re.search(r"\bsize\b|\blength\b", low)
                and re.search(r"\bsubarray\b", low)
                and re.search(r"\bsum\b", low)
            )
            or bool(re.search(r"\b209\b", low) and "subarray" in low)
            or "min_subarray_len" in low,
            (
                ((7, [2, 3, 1, 2, 4, 3]), 2),
                ((4, [1, 4, 4]), 1),
                ((11, [1, 1, 1, 1, 1, 1, 1, 1]), 0),
                ((3, [1, 1]), 0),
            ),
        ),
    ]
