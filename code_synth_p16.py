"""Cycle 274: additional verified Python templates (pack 16)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "degree_of_array",
            "def degree_of_array(nums):\n"
            '    """Shortest subarray that has the same degree as nums."""\n'
            "    a = [int(x) for x in nums]\n"
            "    first, last, count = {}, {}, {}\n"
            "    for i, v in enumerate(a):\n"
            "        count[v] = count.get(v, 0) + 1\n"
            "        if v not in first:\n"
            "            first[v] = i\n"
            "        last[v] = i\n"
            "    deg = max(count.values()) if count else 0\n"
            "    return min(last[v] - first[v] + 1 for v, c in count.items() if c == deg)\n",
            lambda low: bool(
                re.search(
                    r"\bdegree of (?:an? |the )?array\b|"
                    r"\bdegree_of_array\b|"
                    r"\bshortest subarray.{0,30}degree\b",
                    low,
                )
            ),
            (([[1, 2, 2, 3, 1],], 2), ([[1, 2, 2, 3, 1, 4, 2],], 6)),
        ),
        T(
            "pivot_index",
            "def pivot_index(nums):\n"
            '    """Index where left sum equals right sum, else -1."""\n'
            "    a = [int(x) for x in nums]\n"
            "    total = sum(a)\n"
            "    left = 0\n"
            "    for i, v in enumerate(a):\n"
            "        if left == total - left - v:\n"
            "            return i\n"
            "        left += v\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bpivot index\b|"
                    r"\bfind (?:the )?pivot index\b|"
                    r"\bpivot_index\b|"
                    r"\bequilibrium index\b",
                    low,
                )
            )
            and "peak" not in low
            and "rotated" not in low,
            (([[1, 7, 3, 6, 5, 6],], 3), ([[1, 2, 3],], -1), ([[2, 1, -1],], 0)),
        ),
        T(
            "assign_cookies",
            "def assign_cookies(g, s):\n"
            '    """Max content children given greed g and cookie sizes s."""\n'
            "    kids = sorted(int(x) for x in g)\n"
            "    cookies = sorted(int(x) for x in s)\n"
            "    i = j = 0\n"
            "    while i < len(kids) and j < len(cookies):\n"
            "        if cookies[j] >= kids[i]:\n"
            "            i += 1\n"
            "        j += 1\n"
            "    return i\n",
            lambda low: bool(
                re.search(
                    r"\bassign cookies\b|"
                    r"\bassign_cookies\b|"
                    r"\bcontent children\b|"
                    r"\bcookie assignment\b",
                    low,
                )
            )
            and "candy" not in low
            and "kids with" not in low,
            (([[1, 2, 3], [1, 1]], 1), ([[1, 2], [1, 2, 3]], 2)),
        ),
        T(
            "duplicate_zeros",
            "def duplicate_zeros(arr):\n"
            '    """In-place: duplicate each zero, shifting right and dropping overflow."""\n'
            "    a = [int(x) for x in arr]\n"
            "    n = len(a)\n"
            "    zeros = a.count(0)\n"
            "    i = n - 1\n"
            "    j = n + zeros - 1\n"
            "    while i >= 0 and j >= 0:\n"
            "        if j < n:\n"
            "            a[j] = a[i]\n"
            "        if a[i] == 0:\n"
            "            j -= 1\n"
            "            if j < n:\n"
            "                a[j] = 0\n"
            "        i -= 1\n"
            "        j -= 1\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\bduplicate zeros\b|"
                    r"\bduplicate_zeros\b|"
                    r"\bduplicate each zero\b",
                    low,
                )
            )
            and "move zero" not in low,
            (([[1, 0, 2, 3, 0, 4, 5, 0],], [1, 0, 0, 2, 3, 0, 0, 4]), ([[1, 2, 3],], [1, 2, 3])),
        ),
        T(
            "lucky_numbers",
            "def lucky_numbers(matrix):\n"
            '    """Lucky numbers: min of their row and max of their column."""\n'
            "    m = [list(row) for row in matrix]\n"
            "    if not m or not m[0]:\n"
            "        return []\n"
            "    row_min = [min(row) for row in m]\n"
            "    col_max = [max(m[i][j] for i in range(len(m))) for j in range(len(m[0]))]\n"
            "    out = []\n"
            "    for i, row in enumerate(m):\n"
            "        for j, v in enumerate(row):\n"
            "            if v == row_min[i] and v == col_max[j]:\n"
            "                out.append(v)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\blucky numbers?\b|"
                    r"\blucky_numbers\b|"
                    r"\blucky numbers? in (?:a )?matrix\b",
                    low,
                )
            )
            and "lucky integer" not in low
            and "find lucky" not in low,
            (
                (([[3, 7, 8], [9, 11, 13], [15, 16, 17]],), [15]),
                (([[1, 10, 4, 2], [9, 3, 8, 7], [15, 16, 17, 12]],), [12]),
            ),
        ),
        T(
            "find_lucky",
            "def find_lucky(arr):\n"
            '    """Largest lucky integer: value equals its frequency, else -1."""\n'
            "    from collections import Counter\n"
            "    c = Counter(int(x) for x in arr)\n"
            "    lucky = [v for v, n in c.items() if v == n]\n"
            "    return max(lucky) if lucky else -1\n",
            lambda low: bool(
                re.search(
                    r"\bfind (?:the )?lucky integer\b|"
                    r"\bfind_lucky\b|"
                    r"\blucky integer in (?:an? )?array\b",
                    low,
                )
            )
            and "matrix" not in low
            and "lucky numbers" not in low,
            (([[2, 2, 3, 4],], 2), ([[1, 2, 2, 3, 3, 3],], 3), ([[2, 2, 2, 3, 3],], -1)),
        ),
    ]
