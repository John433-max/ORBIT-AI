"""Cycle 365: unmatched Easy array/string templates.

Official problem statements (algorithms only, not copied text):
LeetCode 3674, 3683, 3697, 3707, 3712, 3718.
"""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "min_operations_equalize_array",
            "def min_operations_equalize_array(nums):\n"
            '    """AND-subarray ops to equalize: 0 if already equal else 1 (LeetCode 3674)."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    first = nums[0]\n"
            "    return 0 if all(x == first for x in nums) else 1\n"
            "\n"
            "def minOperations(nums):\n"
            "    return min_operations_equalize_array(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bequalize array\b|"
                    r"\bminimum operations to equalize\b|"
                    r"\bleetcode 3674\b",
                    low,
                )
            ),
            (
                (((1, 2),), 1),
                (((5, 5, 5),), 0),
                (((7,),), 0),
            ),
        ),
        T(
            "earliest_time_to_finish_one_task",
            "def earliest_time_to_finish_one_task(tasks):\n"
            '    """Earliest finish among independent [start, duration] tasks (LeetCode 3683)."""\n'
            "    return min(s + t for s, t in tasks)\n"
            "\n"
            "def earliestTime(tasks):\n"
            "    return earliest_time_to_finish_one_task(tasks)\n",
            lambda low: bool(
                re.search(
                    r"\bearliest time to finish one task\b|"
                    r"\bleetcode 3683\b",
                    low,
                )
            ),
            (
                ((((1, 6), (2, 3)),), 5),
                ((((100, 100), (100, 100), (100, 100)),), 200),
            ),
        ),
        T(
            "decimal_representation",
            "def decimal_representation(n):\n"
            '    """Base-10 components of n, descending (LeetCode 3697)."""\n'
            "    parts = []\n"
            "    place = 1\n"
            "    x = int(n)\n"
            "    while x:\n"
            "        digit = x % 10\n"
            "        if digit:\n"
            "            parts.append(digit * place)\n"
            "        x //= 10\n"
            "        place *= 10\n"
            "    parts.reverse()\n"
            "    return parts\n"
            "\n"
            "def decimalRepresentation(n):\n"
            "    return decimal_representation(n)\n",
            lambda low: bool(
                re.search(
                    r"\bdecimal representation\b|"
                    r"\bleetcode 3697\b",
                    low,
                )
            ),
            (
                ((537,), [500, 30, 7]),
                ((102,), [100, 2]),
                ((6,), [6]),
            ),
        ),
        T(
            "equal_score_substrings",
            "def equal_score_substrings(s):\n"
            '    """True if a split has equal alphabet scores, a=1..z=26 (LeetCode 3707)."""\n'
            "    if len(s) < 2:\n"
            "        return False\n"
            "    scores = [ord(ch) - 96 for ch in s]\n"
            "    total = sum(scores)\n"
            "    left = 0\n"
            "    for i, sc in enumerate(scores[:-1]):\n"
            "        left += sc\n"
            "        if left == total - left:\n"
            "            return True\n"
            "    return False\n"
            "\n"
            "def scoreBalance(s):\n"
            "    return equal_score_substrings(s)\n",
            lambda low: bool(
                re.search(
                    r"\bequal score substrings\b|"
                    r"\bleetcode 3707\b",
                    low,
                )
            ),
            (
                (("adcb",), True),
                (("bace",), False),
            ),
        ),
        T(
            "sum_freq_divisible_by_k",
            "def sum_freq_divisible_by_k(nums, k):\n"
            '    """Sum of values whose frequency is divisible by k (LeetCode 3712)."""\n'
            "    counts = {}\n"
            "    for x in nums:\n"
            "        counts[x] = counts.get(x, 0) + 1\n"
            "    total = 0\n"
            "    for x, c in counts.items():\n"
            "        if k and c % k == 0:\n"
            "            total += x * c\n"
            "    return total\n"
            "\n"
            "def sumDivisibleByK(nums, k):\n"
            "    return sum_freq_divisible_by_k(nums, k)\n",
            lambda low: bool(
                re.search(
                    r"\bfrequency divisible by k\b|"
                    r"\bleetcode 3712\b",
                    low,
                )
            ),
            (
                (((1, 2, 2, 3, 3, 3, 3, 4), 2), 16),
                (((1, 2, 3, 4, 5), 2), 0),
                (((4, 4, 4, 1, 2, 3), 3), 12),
            ),
        ),
        T(
            "missing_multiple",
            "def missing_multiple(nums, k):\n"
            '    """Smallest positive multiple of k absent from nums (LeetCode 3718)."""\n'
            "    seen = set(nums)\n"
            "    m = k\n"
            "    while m in seen:\n"
            "        m += k\n"
            "    return m\n"
            "\n"
            "def missingMultiple(nums, k):\n"
            "    return missing_multiple(nums, k)\n",
            lambda low: bool(
                re.search(
                    r"\bmissing multiple\b|"
                    r"\bsmallest missing multiple\b|"
                    r"\bleetcode 3718\b",
                    low,
                )
            ),
            (
                (((8, 2, 3, 4, 6), 2), 10),
                (((1, 4, 7, 10, 15), 5), 5),
            ),
        ),
    ]
