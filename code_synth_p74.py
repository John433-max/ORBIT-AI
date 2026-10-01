"""Cycle 338: unused Easy — perfect number / build array from permutation /
concatenation of array / final value after operations / double reversal /
minimum chairs in a waiting room."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "check_perfect_number",
            "def check_perfect_number(num):\n"
            '    """True if num equals the sum of its proper divisors (LeetCode 507)."""\n'
            "    if num <= 1:\n"
            "        return False\n"
            "    total = 1\n"
            "    i = 2\n"
            "    while i * i <= num:\n"
            "        if num % i == 0:\n"
            "            total += i\n"
            "            if i * i != num:\n"
            "                total += num // i\n"
            "        i += 1\n"
            "    return total == num\n",
            lambda low: bool(
                re.search(r"\bperfect[_ ]number\b|\bcheck[_ ]perfect[_ ]number\b", low)
            ),
            (
                ((28,), True),
                ((7,), False),
                ((6,), True),
            ),
        ),
        T(
            "build_array",
            "def build_array(nums):\n"
            '    """ans[i] = nums[nums[i]] for a zero-based permutation (LeetCode 1920)."""\n'
            "    return [nums[nums[i]] for i in range(len(nums))]\n",
            lambda low: bool(
                re.search(
                    r"\bbuild[_ ]array[_ ]from[_ ]permutation\b|"
                    r"\bbuild[_ ]array\b.*\bpermutation\b",
                    low,
                )
            ),
            (
                (([0, 2, 1, 5, 3, 4],), [0, 1, 2, 4, 5, 3]),
                (([5, 0, 1, 2, 3, 4],), [4, 5, 0, 1, 2, 3]),
            ),
        ),
        T(
            "added_integer",
            "def added_integer(nums1, nums2):\n"
            '    """Difference of maxima: the integer added to every nums1 element (LeetCode 3131)."""\n'
            "    return max(nums2) - max(nums1)\n",
            lambda low: bool(
                re.search(
                    r"\badded[_ ]integer\b|\binteger[_ ]added[_ ]to[_ ]array\b",
                    low,
                )
            ),
            (
                (([2, 6, 4], [9, 7, 9]), 3),
                (([10], [5]), -5),
                (([1, 1, 1, 1], [1, 1, 1, 1]), 0),
            ),
        ),
        T(
            "final_value_after_operations",
            "def final_value_after_operations(operations):\n"
            '    """X starts at 0; ++X/X++ increment, --X/X-- decrement (LeetCode 2011)."""\n'
            "    x = 0\n"
            "    for op in operations:\n"
            "        x += 1 if '+' in op else -1\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bfinal[_ ]value[_ ]of[_ ]variable\b|"
                    r"\bafter[_ ]performing[_ ]operations\b|"
                    r"\bfinal[_ ]value[_ ]after[_ ]operations\b",
                    low,
                )
            ),
            (
                ((["--X", "X++", "X++"],), 1),
                ((["++X", "++X", "X++"],), 3),
                ((["X++", "++X", "--X", "X--"],), 0),
            ),
        ),
        T(
            "is_same_after_reversals",
            "def is_same_after_reversals(num):\n"
            '    """Reversing twice keeps num iff it has no trailing zero (LeetCode 2119)."""\n'
            "    return num == 0 or num % 10 != 0\n",
            lambda low: bool(
                re.search(
                    r"\bdouble[_ ]reversal\b|\bsame[_ ]after[_ ]reversals\b|"
                    r"\bafter[_ ]a[_ ]double[_ ]reversal\b",
                    low,
                )
            ),
            (
                ((526,), True),
                ((1800,), False),
                ((0,), True),
            ),
        ),
        T(
            "minimum_chairs",
            "def minimum_chairs(s):\n"
            '    """Minimum chairs so a waiting room never goes negative (LeetCode 3168)."""\n'
            "    cur = need = 0\n"
            "    for ch in s:\n"
            "        cur += 1 if ch == 'E' else -1\n"
            "        if cur > need:\n"
            "            need = cur\n"
            "    return need\n",
            lambda low: bool(
                re.search(
                    r"\bminimum[_ ]number[_ ]of[_ ]chairs\b|"
                    r"\bchairs[_ ]in[_ ]a[_ ]waiting[_ ]room\b|"
                    r"\bminimum[_ ]chairs\b",
                    low,
                )
            ),
            (
                (("EEEEEEE",), 7),
                (("ELELEEL",), 2),
                (("ELEELEELLL",), 3),
            ),
        ),
    ]
