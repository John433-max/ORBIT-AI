"""Cycle 373: furthest origin, common elements, date-to-binary, special array I, complete-day pairs, min average.

2833 / 2956 / 3280 / 3151 / 3184 / 3194 were unmatched stubs.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "furthest_point_from_origin",
            "def furthest_point_from_origin(moves):\n"
            '    """Furthest origin distance; blanks all go one way (LeetCode 2833)."""\n'
            "    left = moves.count('L')\n"
            "    right = moves.count('R')\n"
            "    blank = moves.count('_')\n"
            "    return abs(left - right) + blank\n"
            "\n"
            "def furthestDistanceFromOrigin(moves):\n"
            "    return furthest_point_from_origin(moves)\n"
            "\n"
            "def furthest_distance_from_origin(moves):\n"
            "    return furthest_point_from_origin(moves)\n",
            lambda low: bool(
                re.search(
                    r"\bfurthest point from origin\b|"
                    r"\bleetcode 2833\b",
                    low,
                )
            ),
            (
                (("L_RL__R",), 3),
                (("_R__LL_",), 5),
                (("_______",), 7),
            ),
        ),
        T(
            "common_elements_two_arrays",
            "def common_elements_two_arrays(nums1, nums2):\n"
            '    """Counts of values present in the other array (LeetCode 2956)."""\n'
            "    set1, set2 = set(nums1), set(nums2)\n"
            "    a = sum(1 for x in nums1 if x in set2)\n"
            "    b = sum(1 for x in nums2 if x in set1)\n"
            "    return [a, b]\n"
            "\n"
            "def findIntersectionValues(nums1, nums2):\n"
            "    return common_elements_two_arrays(nums1, nums2)\n"
            "\n"
            "def find_intersection_values(nums1, nums2):\n"
            "    return common_elements_two_arrays(nums1, nums2)\n",
            lambda low: bool(
                re.search(
                    r"\bcommon elements between two arrays\b|"
                    r"\bleetcode 2956\b",
                    low,
                )
            ),
            (
                (([4, 3, 2, 3, 1], [2, 2, 5, 2, 3, 6]), [3, 4]),
                (([3, 4, 2, 3], [1, 5]), [0, 0]),
                (([2, 3, 2], [1, 2]), [2, 1]),
            ),
        ),
        T(
            "date_to_binary",
            "def date_to_binary(date):\n"
            '    """yyyy-mm-dd with each part in binary, no leading zeros (LeetCode 3280)."""\n'
            "    return '-'.join(format(int(part), 'b') for part in date.split('-'))\n"
            "\n"
            "def convertDateToBinary(date):\n"
            "    return date_to_binary(date)\n",
            lambda low: bool(
                re.search(
                    r"\bdate to binary\b|"
                    r"\bconvert date to binary\b|"
                    r"\bleetcode 3280\b",
                    low,
                )
            ),
            (
                (("2080-02-29",), "100000100000-10-11101"),
                (("1900-01-01",), "11101101100-1-1"),
            ),
        ),
        T(
            "special_array_i",
            "def special_array_i(nums):\n"
            '    """Adjacent elements have different parity (LeetCode 3151)."""\n'
            "    for a, b in zip(nums, nums[1:]):\n"
            "        if (a % 2) == (b % 2):\n"
            "            return False\n"
            "    return True\n"
            "\n"
            "def isArraySpecial(nums):\n"
            "    return special_array_i(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bspecial array i\b|"
                    r"\bleetcode 3151\b",
                    low,
                )
            )
            and "greater than or equal" not in low,
            (
                (([1],), True),
                (([2, 1, 4],), True),
                (([4, 3, 1, 6],), False),
            ),
        ),
        T(
            "complete_day_pairs",
            "def complete_day_pairs(hours):\n"
            '    """Pairs whose hours sum to a multiple of 24 (LeetCode 3184)."""\n'
            "    ans = 0\n"
            "    count = [0] * 24\n"
            "    for hour in hours:\n"
            "        ans += count[(24 - hour % 24) % 24]\n"
            "        count[hour % 24] += 1\n"
            "    return ans\n"
            "\n"
            "def countCompleteDayPairs(hours):\n"
            "    return complete_day_pairs(hours)\n",
            lambda low: bool(
                re.search(
                    r"\bcomplete day\b|"
                    r"\bleetcode 3184\b",
                    low,
                )
            ),
            (
                (([12, 12, 30, 24, 24],), 2),
                (([72, 48, 24, 3],), 3),
            ),
        ),
        T(
            "minimum_average",
            "def minimum_average(nums):\n"
            '    """Min average of smallest+largest pairs (LeetCode 3194)."""\n'
            "    vals = sorted(nums)\n"
            "    i, j = 0, len(vals) - 1\n"
            "    best = float('inf')\n"
            "    while i < j:\n"
            "        best = min(best, (vals[i] + vals[j]) / 2)\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return best\n"
            "\n"
            "def minimumAverage(nums):\n"
            "    return minimum_average(nums)\n"
            "\n"
            "def find_minimum_average(nums):\n"
            "    return minimum_average(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bminimum average of smallest and largest\b|"
                    r"\bleetcode 3194\b",
                    low,
                )
            ),
            (
                (([7, 8, 3, 4, 15, 13, 4, 1],), 5.5),
                (([1, 9, 8, 3, 10, 5],), 5.5),
                (([1, 2, 3, 7, 8, 9],), 5.0),
            ),
        ),
    ]
