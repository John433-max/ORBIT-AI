"""Cycle 325: highest unused Easy — find_max_k / delete greatest row /
changing keys / X-matrix / negative matrix count / equal-sum subarrays."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "find_max_k",
            "def find_max_k(nums):\n"
            '    """Largest k such that k and -k both exist (LeetCode 2441)."""\n'
            "    s = set(nums)\n"
            "    best = -1\n"
            "    for x in s:\n"
            "        if x > 0 and -x in s and x > best:\n"
            "            best = x\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bfind_max_k\b|"
                    r"\blargest[_ ]positive[_ ]integer[_ ]that[_ ]exists[_ ]with[_ ]its[_ ]negative\b|"
                    r"\bleetcode[_ ]2441\b",
                    low,
                )
            )
            and "kth" not in low
            and "find_max_average" not in low
            and "max_k_elements" not in low,
            (
                (([-1, 2, -3, 3],), 3),
                (([-1, 10, 6, 7, -7, 1],), 7),
                (([-10, 8, 6, 7, -2, -3],), -1),
            ),
        ),
        T(
            "delete_greatest_value",
            "def delete_greatest_value(grid):\n"
            '    """Repeatedly delete row maxima and add the global max (LeetCode 2500)."""\n'
            "    rows = [sorted(r) for r in grid]\n"
            "    ans = 0\n"
            "    while rows[0]:\n"
            "        mx = 0\n"
            "        for r in rows:\n"
            "            v = r.pop()\n"
            "            if v > mx:\n"
            "                mx = v\n"
            "        ans += mx\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bdelete_greatest_value\b|"
                    r"\bdelete[_ ]greatest[_ ]value[_ ]in[_ ]each[_ ]row\b|"
                    r"\bleetcode[_ ]2500\b",
                    low,
                )
            ),
            (
                (([[1, 2, 4], [3, 3, 1]],), 8),
                (([[10]],), 10),
            ),
        ),
        T(
            "count_changing_keys",
            "def count_changing_keys(s):\n"
            '    """How many times the typed key changes, case-insensitive (LeetCode 3019)."""\n'
            "    s = s.lower()\n"
            "    return sum(s[i] != s[i - 1] for i in range(1, len(s)))\n",
            lambda low: bool(
                re.search(
                    r"\bcount_changing_keys\b|"
                    r"\bnumber[_ ]of[_ ]changing[_ ]keys\b|"
                    r"\bchanging[_ ]keys\b|"
                    r"\bleetcode[_ ]3019\b",
                    low,
                )
            )
            and "keyboard" not in low,
            (
                (("aAbBcC",), 2),
                (("AaAaAaaA",), 0),
            ),
        ),
        T(
            "check_x_matrix",
            "def check_x_matrix(grid):\n"
            '    """True iff diagonals are non-zero and off-diagonals are 0 (LeetCode 2319)."""\n'
            "    n = len(grid)\n"
            "    for i in range(n):\n"
            "        for j in range(n):\n"
            "            diag = i == j or i + j == n - 1\n"
            "            if diag and grid[i][j] == 0:\n"
            "                return False\n"
            "            if not diag and grid[i][j] != 0:\n"
            "                return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bcheck_x_matrix\b|"
                    r"\bcheck[_ ]if[_ ]matrix[_ ]is[_ ]x[_ ]matrix\b|"
                    r"\bx[_ ]matrix\b|"
                    r"\bleetcode[_ ]2319\b",
                    low,
                )
            )
            and "spiral" not in low
            and "reshape" not in low,
            (
                (([[2, 0, 0, 1], [0, 3, 1, 0], [0, 5, 2, 0], [4, 0, 0, 2]],), True),
                (([[5, 7, 0], [0, 3, 1], [0, 5, 0]],), False),
            ),
        ),
        T(
            "count_negatives",
            "def count_negatives(grid):\n"
            '    """Count negatives in a row-and-column sorted matrix (LeetCode 1351)."""\n'
            "    return sum(1 for row in grid for v in row if v < 0)\n",
            lambda low: bool(
                re.search(
                    r"\bcount_negatives\b|"
                    r"\bcount[_ ]negative[_ ]numbers[_ ]in[_ ]a[_ ]sorted[_ ]matrix\b|"
                    r"\bcount[_ ]negative[_ ]numbers\b|"
                    r"\bleetcode[_ ]1351\b",
                    low,
                )
            )
            and "first_missing" not in low,
            (
                (([[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]],), 8),
                (([[3, 2], [1, 0]],), 0),
            ),
        ),
        T(
            "find_subarrays",
            "def find_subarrays(nums):\n"
            '    """True if two different-length-2+ subarrays share the same sum (LeetCode 2395)."""\n'
            "    seen = set()\n"
            "    for i in range(len(nums) - 1):\n"
            "        s = nums[i] + nums[i + 1]\n"
            "        if s in seen:\n"
            "            return True\n"
            "        seen.add(s)\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bfind_subarrays\b|"
                    r"\bfind[_ ]subarrays[_ ]with[_ ]equal[_ ]sum\b|"
                    r"\bsubarrays[_ ]with[_ ]equal[_ ]sum\b|"
                    r"\bleetcode[_ ]2395\b",
                    low,
                )
            )
            and "subarray_sum" not in low
            and "product_subarray" not in low,
            (
                (([4, 2, 4],), True),
                (([1, 2, 3, 4, 5],), False),
                (([0, 0, 0],), True),
            ),
        ),
    ]
