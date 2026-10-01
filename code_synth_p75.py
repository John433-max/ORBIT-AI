"""Cycle 339: unused Easy — smallest equal index / minimize string length /
equal-and-divisible pairs / multi-array intersection / largest good integer /
account balance after rounded purchase."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "smallest_equal",
            "def smallest_equal(nums):\n"
            '    """Smallest index i with nums[i] == i, else -1 (LeetCode 2057)."""\n'
            "    for i, value in enumerate(nums):\n"
            "        if value == i:\n"
            "            return i\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"smallest index with equal value|smallest[_ ]equal", low)
            ),
            (
                (([0, 1, 2],), 0),
                (([4, 3, 2, 1],), 2),
                (([1, 2, 3],), -1),
            ),
        ),
        T(
            "minimized_string_length",
            "def minimized_string_length(s):\n"
            '    """Length after minimizing by deleting one of a duplicate pair (LeetCode 2716)."""\n'
            "    return len(set(s))\n",
            lambda low: bool(
                re.search(r"minimize string length|minimized string length", low)
            ),
            (
                (("aaabc",), 3),
                (("cbbd",), 3),
                (("dddaaa",), 2),
            ),
        ),
        T(
            "count_equal_divisible_pairs",
            "def count_equal_divisible_pairs(nums, k):\n"
            '    """Pairs i < j with nums[i] == nums[j] and i*j divisible by k (LeetCode 2176)."""\n'
            "    count = 0\n"
            "    n = len(nums)\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            if nums[i] == nums[j] and (i * j) % k == 0:\n"
            "                count += 1\n"
            "    return count\n",
            lambda low: bool(
                re.search(r"equal and divisible pairs|count equal and divisible", low)
            ),
            (
                (([3, 1, 2, 2, 2, 1, 3], 2), 4),
                (([1, 2, 3, 4], 1), 0),
            ),
        ),
        T(
            "intersection_multiple_arrays",
            "def intersection_multiple_arrays(nums):\n"
            '    """Sorted values present in every array (LeetCode 2248)."""\n'
            "    if not nums:\n"
            "        return []\n"
            "    common = set(nums[0])\n"
            "    for row in nums[1:]:\n"
            "        common &= set(row)\n"
            "    return sorted(common)\n",
            lambda low: bool(
                re.search(r"intersection of multiple arrays", low)
            ),
            (
                (([[3, 1, 2, 4, 5], [1, 2, 3, 4], [3, 4, 5, 6]],), [3, 4]),
                (([[1, 2, 3], [4, 5, 6]],), []),
            ),
        ),
        T(
            "largest_good_integer",
            "def largest_good_integer(num):\n"
            '    """Largest 3-same-digit substring, or empty (LeetCode 2264)."""\n'
            "    best = \"\"\n"
            "    for i in range(len(num) - 2):\n"
            "        if num[i] == num[i + 1] == num[i + 2]:\n"
            "            chunk = num[i:i + 3]\n"
            "            if chunk > best:\n"
            "                best = chunk\n"
            "    return best\n",
            lambda low: bool(
                re.search(r"largest 3-same-digit|largest good integer", low)
            ),
            (
                (("6777133339",), "777"),
                (("2300019",), "000"),
                (("42352338",), ""),
            ),
        ),
        T(
            "account_balance_after_purchase",
            "def account_balance_after_purchase(purchase_amount):\n"
            '    """Balance after rounding purchase to nearest 10 (LeetCode 2806)."""\n'
            "    rounded = ((purchase_amount + 5) // 10) * 10\n"
            "    return 100 - rounded\n",
            lambda low: bool(
                re.search(
                    r"account balance after rounded purchase|rounded purchase",
                    low,
                )
            ),
            (
                ((9,), 90),
                ((15,), 80),
                ((10,), 90),
            ),
        ),
    ]
