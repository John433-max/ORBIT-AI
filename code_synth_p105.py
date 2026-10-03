"""Cycle 383: Easy prompts still absent from the template index.

LeetCode 2022 / 2235 / 2341 / 2455 / 2600 / 2605 / 3038 were not referenced
by any pack. Matchers stay ID- or phrase-specific so arithmetic add/average
and pair-count templates keep their existing prompts.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "construct_2d_array",
            "def construct_2d_array(original, m, n):\n"
            '    """Reshape a 1D array into m x n, or [] if it does not fit (LeetCode 2022)."""\n'
            "    if m * n != len(original):\n"
            "        return []\n"
            "    return [original[i * n:(i + 1) * n] for i in range(m)]\n"
            "\n"
            "def construct2DArray(original, m, n):\n"
            "    return construct_2d_array(original, m, n)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2022\b|\b1d array into 2d\b|\bconvert 1d array\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4], 2, 2), [[1, 2], [3, 4]]),
                (([1, 2, 3], 1, 3), [[1, 2, 3]]),
                (([1, 2], 1, 1), []),
            ),
        ),
        T(
            "add_two_integers",
            "def add_two_integers(num1, num2):\n"
            '    """Sum of two integers (LeetCode 2235)."""\n'
            "    return num1 + num2\n"
            "\n"
            "def sum(num1, num2):\n"
            "    return add_two_integers(num1, num2)\n",
            lambda low: bool(
                re.search(r"\bleetcode 2235\b|\badd two integers\b", low)
            ),
            (
                ((12, 5), 17),
                ((-10, 4), -6),
            ),
        ),
        T(
            "number_of_pairs_in_array",
            "def number_of_pairs_in_array(nums):\n"
            '    """Equal pairs formed, and leftover count (LeetCode 2341)."""\n'
            "    from collections import Counter\n"
            "    counts = Counter(nums)\n"
            "    pairs = sum(c // 2 for c in counts.values())\n"
            "    leftover = sum(c % 2 for c in counts.values())\n"
            "    return [pairs, leftover]\n"
            "\n"
            "def numberOfPairs(nums):\n"
            "    return number_of_pairs_in_array(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2341\b|\bmaximum number of pairs in array\b",
                    low,
                )
            ),
            (
                (([1, 3, 2, 1, 3, 2, 2],), [3, 1]),
                (([1, 1],), [1, 0]),
                (([0],), [0, 1]),
            ),
        ),
        T(
            "average_even_divisible_by_three",
            "def average_even_divisible_by_three(nums):\n"
            '    """Floor average of values divisible by 6, else 0 (LeetCode 2455)."""\n'
            "    picked = [x for x in nums if x % 6 == 0]\n"
            "    if not picked:\n"
            "        return 0\n"
            "    return sum(picked) // len(picked)\n"
            "\n"
            "def averageValue(nums):\n"
            "    return average_even_divisible_by_three(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2455\b|\baverage value of even numbers that are divisible by three\b",
                    low,
                )
            ),
            (
                (([1, 3, 6, 10, 12, 15],), 9),
                (([1, 2, 4, 7, 10],), 0),
            ),
        ),
        T(
            "k_items_with_maximum_sum",
            "def k_items_with_maximum_sum(num_ones, num_zeros, num_neg_ones, k):\n"
            '    """Sum of k picks preferring 1, then 0, then -1 (LeetCode 2600)."""\n'
            "    take = min(k, num_ones)\n"
            "    total = take\n"
            "    k -= take\n"
            "    take = min(k, num_zeros)\n"
            "    k -= take\n"
            "    total -= min(k, num_neg_ones)\n"
            "    return total\n"
            "\n"
            "def kItemsWithMaximumSum(numOnes, numZeros, numNegOnes, k):\n"
            "    return k_items_with_maximum_sum(numOnes, numZeros, numNegOnes, k)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2600\b|\bk items with the maximum sum\b",
                    low,
                )
            ),
            (
                ((3, 2, 0, 2), 2),
                ((3, 2, 0, 4), 3),
            ),
        ),
        T(
            "min_number_from_two_digit_arrays",
            "def min_number_from_two_digit_arrays(nums1, nums2):\n"
            '    """Smallest number using one digit from each array (LeetCode 2605)."""\n'
            "    common = set(nums1) & set(nums2)\n"
            "    if common:\n"
            "        return min(common)\n"
            "    a, b = min(nums1), min(nums2)\n"
            "    return min(a * 10 + b, b * 10 + a)\n"
            "\n"
            "def minNumber(nums1, nums2):\n"
            "    return min_number_from_two_digit_arrays(nums1, nums2)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2605\b|\bsmallest number from two digit arrays\b",
                    low,
                )
            ),
            (
                (([4, 1, 3], [5, 7]), 15),
                (([3, 5, 2, 6], [3, 1, 7]), 3),
            ),
        ),
        T(
            "max_operations_same_score",
            "def max_operations_same_score(nums):\n"
            '    """Prefix pair-deletes that keep the first pair score (LeetCode 3038)."""\n'
            "    if len(nums) < 2:\n"
            "        return 0\n"
            "    score = nums[0] + nums[1]\n"
            "    ops = 0\n"
            "    for i in range(0, len(nums) - 1, 2):\n"
            "        if nums[i] + nums[i + 1] != score:\n"
            "            break\n"
            "        ops += 1\n"
            "    return ops\n"
            "\n"
            "def maxOperations(nums):\n"
            "    return max_operations_same_score(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3038\b|\bsame score i\b|\boperations with the same score\b",
                    low,
                )
            ),
            (
                (([3, 2, 1, 4, 5],), 2),
                (([3, 2, 6, 1, 4],), 1),
            ),
        ),
    ]
