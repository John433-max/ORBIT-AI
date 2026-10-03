"""Cycle 379: unmatched coding prompts that fell through to stubs or sum_list.

3512 was stolen by sum_list (sum + array). 2683 / 3133 / 1963 / 3223 / 3011
were NotImplemented drafts. Examples follow published LeetCode samples.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "min_operations_sum_divisible_by_k",
            "def min_operations_sum_divisible_by_k(nums, k):\n"
            '    """Min decrements so the array sum is divisible by k (LeetCode 3512)."""\n'
            "    return sum(nums) % k\n"
            "\n"
            "def minOperations(nums, k):\n"
            "    return min_operations_sum_divisible_by_k(nums, k)\n",
            lambda low: bool(
                re.search(r"\bleetcode 3512\b|\bsum divisible by k\b", low)
            )
            or (
                "divisible" in low
                and "sum" in low
                and "operation" in low
            ),
            (
                (([3, 9, 7], 5), 4),
                (([4, 1, 3], 4), 0),
                (([3, 2], 6), 5),
            ),
        ),
        T(
            "does_valid_array_exist",
            "def does_valid_array_exist(derived):\n"
            '    """True if derived is a neighboring XOR of some binary array (LeetCode 2683)."""\n'
            "    acc = 0\n"
            "    for x in derived:\n"
            "        acc ^= x\n"
            "    return acc == 0\n"
            "\n"
            "def doesValidArrayExist(derived):\n"
            "    return does_valid_array_exist(derived)\n",
            lambda low: bool(
                re.search(r"\bleetcode 2683\b|\bneighboring bitwise xor\b", low)
            ),
            (
                (([1, 1, 0],), True),
                (([1, 1],), True),
                (([1, 0],), False),
            ),
        ),
        T(
            "min_array_end",
            "def min_array_end(n, x):\n"
            '    """Minimum last value of a strictly increasing AND-x array (LeetCode 3133)."""\n'
            "    n -= 1\n"
            "    res = x\n"
            "    bit = 1\n"
            "    while n:\n"
            "        if (res & bit) == 0:\n"
            "            if n & 1:\n"
            "                res |= bit\n"
            "            n >>= 1\n"
            "        bit <<= 1\n"
            "    return res\n"
            "\n"
            "def minEnd(n, x):\n"
            "    return min_array_end(n, x)\n",
            lambda low: bool(
                re.search(r"\bleetcode 3133\b|\bminimum array end\b", low)
            ),
            (
                ((3, 4), 6),
                ((2, 7), 15),
            ),
        ),
        T(
            "min_swaps_balanced",
            "def min_swaps_balanced(s):\n"
            '    """Minimum swaps to balance a bracket string (LeetCode 1963)."""\n'
            "    balance = 0\n"
            "    swaps = 0\n"
            "    for ch in s:\n"
            "        if ch == '[':\n"
            "            balance += 1\n"
            "        else:\n"
            "            balance -= 1\n"
            "            if balance < 0:\n"
            "                swaps += 1\n"
            "                balance = 1\n"
            "    return swaps\n"
            "\n"
            "def minSwaps(s):\n"
            "    return min_swaps_balanced(s)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1963\b|\bswaps to make the string balanced\b",
                    low,
                )
            ),
            (
                (("][][",), 1),
                (("]]][[[",), 2),
                (("[]",), 0),
            ),
        ),
        T(
            "minimum_length_after_ops",
            "def minimum_length_after_ops(s):\n"
            '    """Min length after deleting two of a char that appears >= 3 (LeetCode 3223)."""\n'
            "    from collections import Counter\n"
            "    ans = 0\n"
            "    for count in Counter(s).values():\n"
            "        ans += 1 if count % 2 else 2\n"
            "    return ans\n"
            "\n"
            "def minimumLength(s):\n"
            "    return minimum_length_after_ops(s)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3223\b|\bminimum length of string after operations\b",
                    low,
                )
            ),
            (
                (("abaacbcbb",), 5),
                (("aa",), 2),
            ),
        ),
        T(
            "can_sort_array",
            "def can_sort_array(nums):\n"
            '    """True if equal-popcount adjacent swaps can sort nums (LeetCode 3011)."""\n'
            "    prev_max = 0\n"
            "    i = 0\n"
            "    n = len(nums)\n"
            "    while i < n:\n"
            "        bits = nums[i].bit_count()\n"
            "        j = i\n"
            "        cur_min = cur_max = nums[i]\n"
            "        while j < n and nums[j].bit_count() == bits:\n"
            "            cur_min = min(cur_min, nums[j])\n"
            "            cur_max = max(cur_max, nums[j])\n"
            "            j += 1\n"
            "        if cur_min < prev_max:\n"
            "            return False\n"
            "        prev_max = cur_max\n"
            "        i = j\n"
            "    return True\n"
            "\n"
            "def canSortArray(nums):\n"
            "    return can_sort_array(nums)\n",
            lambda low: bool(
                re.search(r"\bleetcode 3011\b|\barray can be sorted\b", low)
            )
            and "sorted array" not in low,
            (
                (([8, 4, 2, 30, 15],), True),
                (([1, 2, 3, 4, 5],), True),
                (([3, 16, 8, 4, 2],), False),
            ),
        ),
    ]
