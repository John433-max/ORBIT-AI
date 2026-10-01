"""Cycle 340: unused Easy — circular sentence / apply operations /
prefix common array / exceed threshold / divisible by three / twice XOR."""

from __future__ import annotations

import re
from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "is_circular_sentence",
            "def is_circular_sentence(sentence):\n"
            '    """True if each word ends with the next word\'s start, wrapping (LeetCode 2490)."""\n'
            "    words = sentence.split()\n"
            "    for i, word in enumerate(words):\n"
            "        nxt = words[(i + 1) % len(words)]\n"
            "        if word[-1] != nxt[0]:\n"
            "            return False\n"
            "    return True\n",
            lambda low: bool(re.search(r"circular sentence", low)),
            (
                (("leetcode exercises sound delightful",), True),
                (("eetcode",), True),
                (("Leetcode is cool",), False),
            ),
        ),
        T(
            "apply_operations",
            "def apply_operations(nums):\n"
            '    """Double equal neighbors, then shift zeros right (LeetCode 2460)."""\n'
            "    nums = list(nums)\n"
            "    for i in range(len(nums) - 1):\n"
            "        if nums[i] == nums[i + 1]:\n"
            "            nums[i] *= 2\n"
            "            nums[i + 1] = 0\n"
            "    nonzero = [value for value in nums if value]\n"
            "    nonzero.extend([0] * (len(nums) - len(nonzero)))\n"
            "    return nonzero\n",
            lambda low: bool(re.search(r"apply operations to an array", low)),
            (
                (([1, 2, 2, 1, 1, 0],), [1, 4, 2, 0, 0, 0]),
                (([0, 1],), [1, 0]),
            ),
        ),
        T(
            "find_the_prefix_common_array",
            "def find_the_prefix_common_array(a, b):\n"
            '    """Prefix intersection sizes of two permutations (LeetCode 2657)."""\n'
            "    seen = set()\n"
            "    common = 0\n"
            "    out = []\n"
            "    for left, right in zip(a, b):\n"
            "        if left in seen:\n"
            "            common += 1\n"
            "        else:\n"
            "            seen.add(left)\n"
            "        if right in seen:\n"
            "            common += 1\n"
            "        else:\n"
            "            seen.add(right)\n"
            "        out.append(common)\n"
            "    return out\n",
            lambda low: bool(re.search(r"prefix common array", low)),
            (
                (([1, 3, 2, 4], [3, 1, 2, 4]), [0, 2, 3, 4]),
                (([2, 3, 1], [3, 1, 2]), [0, 1, 3]),
            ),
        ),
        T(
            "min_operations_exceed_threshold",
            "def min_operations(nums, k):\n"
            '    """Remove values strictly below k (LeetCode 3065)."""\n'
            "    return sum(value < k for value in nums)\n",
            lambda low: bool(
                re.search(r"exceed threshold value|operations to exceed threshold", low)
            ),
            (
                (([2, 11, 10, 1, 3], 10), 3),
                (([1, 1, 2, 4, 9], 1), 0),
                (([1, 1, 2, 4, 9], 9), 4),
            ),
        ),
        T(
            "minimum_operations_div_by_three",
            "def minimum_operations(nums):\n"
            '    """Ops to make every value divisible by 3 (LeetCode 3190)."""\n'
            "    return sum(value % 3 != 0 for value in nums)\n",
            lambda low: bool(
                re.search(r"divisible by three|divisible by 3", low)
                and "array" in low
            ),
            (
                (([1, 2, 3, 4],), 3),
                (([3, 6, 9],), 0),
            ),
        ),
        T(
            "duplicate_numbers_xor",
            "def duplicate_numbers_xor(nums):\n"
            '    """XOR of values that appear exactly twice (LeetCode 3158)."""\n'
            "    counts = {}\n"
            "    for value in nums:\n"
            "        counts[value] = counts.get(value, 0) + 1\n"
            "    ans = 0\n"
            "    for value, count in counts.items():\n"
            "        if count == 2:\n"
            "            ans ^= value\n"
            "    return ans\n",
            lambda low: bool(re.search(r"appear twice|numbers which appear twice", low)),
            (
                (([1, 2, 1, 3],), 1),
                (([1, 2, 3],), 0),
                (([1, 2, 2, 1],), 3),
            ),
        ),
    ]
