"""Cycle 318: common factors / distinct difference array / max-frequency
elements / find the peaks / X-matrix / distinct numbers on board."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "common_factors",
            "def common_factors(a, b):\n"
            '    """Count positive common factors of a and b (LeetCode 2427)."""\n'
            "    from math import gcd\n"
            "    g = gcd(a, b)\n"
            "    count = 0\n"
            "    i = 1\n"
            "    while i * i <= g:\n"
            "        if g % i == 0:\n"
            "            count += 1 if i * i == g else 2\n"
            "        i += 1\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]of[_ ]common[_ ]factors\b|"
                    r"\bcommon[_ ]factors\b|"
                    r"\bcommon_factors\b",
                    low,
                )
            )
            and "greatest" not in low
            and "gcd" not in low,
            (
                ((12, 6), 4),
                ((25, 30), 2),
                ((1, 1), 1),
            ),
        ),
        T(
            "distinct_difference_array",
            "def distinct_difference_array(nums):\n"
            '    """Prefix distinct minus suffix distinct (LeetCode 2670)."""\n'
            "    n = len(nums)\n"
            "    left = [0] * n\n"
            "    seen = set()\n"
            "    for i, x in enumerate(nums):\n"
            "        seen.add(x)\n"
            "        left[i] = len(seen)\n"
            "    right = [0] * n\n"
            "    seen = set()\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        right[i] = len(seen)\n"
            "        seen.add(nums[i])\n"
            "    return [left[i] - right[i] for i in range(n)]\n",
            lambda low: bool(
                re.search(
                    r"\bdistinct[_ ]difference[_ ]array\b|"
                    r"\bfind[_ ]the[_ ]distinct[_ ]difference\b|"
                    r"\bdistinct_difference_array\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4, 5],), [-3, -1, 1, 3, 5]),
                (([3, 2, 3, 4, 2],), [-2, -1, 0, 2, 3]),
            ),
        ),
        T(
            "max_frequency_elements",
            "def max_frequency_elements(nums):\n"
            '    """Total count of elements that share the max frequency (LeetCode 3005)."""\n'
            "    from collections import Counter\n"
            "    freq = Counter(nums)\n"
            "    mx = max(freq.values())\n"
            "    return sum(v for v in freq.values() if v == mx)\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]elements[_ ]with[_ ]maximum[_ ]frequency\b|"
                    r"\bmax[_ ]frequency[_ ]elements\b|"
                    r"\bmax_frequency_elements\b",
                    low,
                )
            )
            and "even" not in low
            and "subarray" not in low,
            (
                (([1, 2, 2, 3, 1, 4],), 4),
                (([1, 2, 3, 4, 5],), 5),
                (([10, 10, 10],), 3),
            ),
        ),
        T(
            "find_peaks",
            "def find_peaks(mountain):\n"
            '    """Indices of strict interior peaks (LeetCode 2951)."""\n'
            "    return [\n"
            "        i\n"
            "        for i in range(1, len(mountain) - 1)\n"
            "        if mountain[i] > mountain[i - 1] and mountain[i] > mountain[i + 1]\n"
            "    ]\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]the[_ ]peaks\b|"
                    r"\bfind[_ ]peaks\b|"
                    r"\bfind_peaks\b",
                    low,
                )
            )
            and "mountain array" not in low
            and "peak index" not in low
            and "bitonic" not in low,
            (
                (([2, 4, 4],), []),
                (([1, 4, 3, 8, 5],), [1, 3]),
                (([1, 2, 1],), [1]),
            ),
        ),
        T(
            "check_x_matrix",
            "def check_x_matrix(grid):\n"
            '    """True iff n x n grid is an X-matrix (LeetCode 2319)."""\n'
            "    n = len(grid)\n"
            "    for i in range(n):\n"
            "        for j in range(n):\n"
            "            on_diag = i == j or i + j == n - 1\n"
            "            if on_diag:\n"
            "                if grid[i][j] == 0:\n"
            "                    return False\n"
            "            elif grid[i][j] != 0:\n"
            "                return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bx[_ -]?matrix\b|"
                    r"\bcheck[_ ]if[_ ]matrix[_ ]is[_ ]x\b|"
                    r"\bcheck_x_matrix\b",
                    low,
                )
            )
            and "search" not in low
            and "spiral" not in low
            and "rotate" not in low,
            (
                (([[2, 0, 0, 1], [0, 3, 1, 0], [0, 5, 2, 0], [4, 0, 0, 2]],), True),
                (([[5, 7, 0], [0, 3, 1], [0, 5, 0]],), False),
                (([[1, 0, 1], [0, 1, 0], [1, 0, 1]],), True),
            ),
        ),
        T(
            "distinct_integers_on_board",
            "def distinct_integers_on_board(n):\n"
            '    """Distinct values obtainable from n via x % y == 1 (LeetCode 2549)."""\n'
            "    return 1 if n == 1 else n - 1\n",
            lambda low: bool(
                re.search(
                    r"\bdistinct[_ ](?:integers|numbers)[_ ]on[_ ](?:the[_ ])?board\b|"
                    r"\bcount[_ ]distinct[_ ]numbers[_ ]on[_ ]board\b|"
                    r"\bdistinct_integers_on_board\b",
                    low,
                )
            ),
            (
                ((5,), 4),
                ((3,), 2),
                ((1,), 1),
            ),
        ),
    ]
