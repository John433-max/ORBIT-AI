"""Cycle 295: matching items / max product diff / good triplets / star center / three odds / special array."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_items_matching",
            "def count_items_matching(items, rule_key, rule_value):\n"
            '    """Count items matching a type/color/name rule (LeetCode 1773)."""\n'
            "    idx = {'type': 0, 'color': 1, 'name': 2}[rule_key]\n"
            "    return sum(1 for it in items if it[idx] == rule_value)\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]items[_ ]matching\b|"
                    r"\bcount (?:the )?items matching (?:a )?rule\b|"
                    r"\bcount matches of (?:a )?rule in items\b",
                    low,
                )
            ),
            (
                (([["phone", "blue", "pixel"], ["computer", "silver", "lenovo"], ["phone", "gold", "iphone"]], "color", "silver"), 1),
                (([["phone", "blue", "pixel"], ["computer", "silver", "phone"], ["phone", "gold", "iphone"]], "type", "phone"), 2),
                (([["phone", "blue", "pixel"], ["computer", "silver", "lenovo"], ["phone", "gold", "iphone"]], "name", "pixel"), 1),
            ),
        ),
        T(
            "max_product_difference",
            "def max_product_difference(nums):\n"
            '    """Max (a*b) - (c*d) over distinct pairs (LeetCode 1913)."""\n'
            "    s = sorted(nums)\n"
            "    return s[-1] * s[-2] - s[0] * s[1]\n",
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)?[_ ]product[_ ]difference\b|"
                    r"\bmaximum product difference between two pairs\b|"
                    r"\bmax product difference\b",
                    low,
                )
            ),
            (
                (([5, 6, 2, 7, 4],), 34),
                (([4, 2, 5, 9, 7, 4, 8],), 64),
                (([1, 6, 7],), 36),
            ),
        ),
        T(
            "count_good_triplets",
            "def count_good_triplets(arr, a, b, c):\n"
            '    """Count i<j<k triplets within |diff| bounds (LeetCode 1534)."""\n'
            "    n = len(arr)\n"
            "    count = 0\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            if abs(arr[i] - arr[j]) > a:\n"
            "                continue\n"
            "            for k in range(j + 1, n):\n"
            "                if abs(arr[j] - arr[k]) <= b and abs(arr[i] - arr[k]) <= c:\n"
            "                    count += 1\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]good[_ ]triplets\b|"
                    r"\bcount (?:the )?good triplets\b|"
                    r"\bnumber of good triplets\b",
                    low,
                )
            ),
            (
                (([3, 0, 1, 1, 9, 7], 7, 2, 3), 4),
                (([1, 1, 2, 2, 3], 0, 0, 1), 0),
                (([7, 3, 7, 3, 7], 5, 5, 5), 10),
            ),
        ),
        T(
            "find_center",
            "def find_center(edges):\n"
            '    """Center of a star graph given n-1 edges (LeetCode 1791)."""\n'
            "    a, b = edges[0]\n"
            "    return a if a in edges[1] else b\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]center\b|"
                    r"\bfind (?:the )?center of (?:the |a )?star graph\b|"
                    r"\bcenter of star graph\b",
                    low,
                )
            ),
            (
                (([[1, 2], [2, 3], [4, 2]],), 2),
                (([[1, 2], [5, 1], [1, 3], [1, 4]],), 1),
                (([[2, 1], [3, 1]],), 1),
            ),
        ),
        T(
            "three_consecutive_odds",
            "def three_consecutive_odds(arr):\n"
            '    """True if three consecutive odd numbers exist (LeetCode 1550)."""\n'
            "    run = 0\n"
            "    for n in arr:\n"
            "        if n % 2:\n"
            "            run += 1\n"
            "            if run == 3:\n"
            "                return True\n"
            "        else:\n"
            "            run = 0\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bthree[_ ]consecutive[_ ]odds\b|"
                    r"\bthree consecutive odd numbers\b|"
                    r"\bthree consecutive odds\b",
                    low,
                )
            ),
            (
                (([2, 6, 4, 1],), False),
                (([1, 2, 34, 3, 4, 5, 7, 23, 12],), True),
                (([1, 3, 5],), True),
            ),
        ),
        T(
            "special_array",
            "def special_array(nums):\n"
            '    """x such that exactly x values are >= x, else -1 (LeetCode 1608)."""\n'
            "    nums = sorted(nums, reverse=True)\n"
            "    n = len(nums)\n"
            "    for x in range(1, n + 1):\n"
            "        if nums[x - 1] >= x and (x == n or nums[x] < x):\n"
            "            return x\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bspecial[_ ]array\b|"
                    r"\bspecial array with x elements greater than or equal x\b|"
                    r"\bspecial array x greater\b",
                    low,
                )
            ),
            (
                (([3, 5],), 2),
                (([0, 0],), -1),
                (([0, 4, 3, 0, 4],), 3),
            ),
        ),
    ]
