"""Cycle 275: additional verified Python templates (pack 17)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "relative_ranks",
            "def relative_ranks(score):\n"
            '    """Map scores to Gold/Silver/Bronze/rank strings."""\n'
            "    s = [int(x) for x in score]\n"
            "    order = sorted(range(len(s)), key=lambda i: -s[i])\n"
            "    medals = {0: 'Gold Medal', 1: 'Silver Medal', 2: 'Bronze Medal'}\n"
            "    out = [''] * len(s)\n"
            "    for rank, i in enumerate(order):\n"
            "        out[i] = medals.get(rank, str(rank + 1))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\brelative ranks\b|"
                    r"\brelative_ranks\b|"
                    r"\bgold silver bronze\b|"
                    r"\bathlete ranks?\b",
                    low,
                )
            )
            and "kth" not in low,
            (([[5, 4, 3, 2, 1],], ["Gold Medal", "Silver Medal", "Bronze Medal", "4", "5"]),),
        ),
        T(
            "can_three_parts_equal_sum",
            "def can_three_parts_equal_sum(arr):\n"
            '    """True if arr can be split into 3 contiguous parts of equal sum."""\n'
            "    a = [int(x) for x in arr]\n"
            "    total = sum(a)\n"
            "    if total % 3 != 0:\n"
            "        return False\n"
            "    target = total // 3\n"
            "    acc = parts = 0\n"
            "    for i, v in enumerate(a):\n"
            "        acc += v\n"
            "        if acc == target:\n"
            "            parts += 1\n"
            "            acc = 0\n"
            "            if parts == 2 and i < len(a) - 1:\n"
            "                return True\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bthree parts.{0,20}equal sum\b|"
                    r"\bcan_three_parts_equal_sum\b|"
                    r"\bsplit.{0,20}three equal\b|"
                    r"\b3 parts equal sum\b",
                    low,
                )
            ),
            (([[0, 2, 1, -6, 6, -7, 9, 1, 2, 0, 1],], True), ([[0, 2, 1, -6, 6, 7, 9, -1, 2, 0, 1],], False)),
        ),
        T(
            "image_smoother",
            "def image_smoother(img):\n"
            '    """3x3 average-filter smoother on a gray image (floor)."""\n'
            "    g = [list(map(int, row)) for row in img]\n"
            "    m, n = len(g), len(g[0]) if g else 0\n"
            "    out = [[0] * n for _ in range(m)]\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            s = c = 0\n"
            "            for di in (-1, 0, 1):\n"
            "                for dj in (-1, 0, 1):\n"
            "                    ni, nj = i + di, j + dj\n"
            "                    if 0 <= ni < m and 0 <= nj < n:\n"
            "                        s += g[ni][nj]\n"
            "                        c += 1\n"
            "            out[i][j] = s // c\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bimage smoother\b|"
                    r"\bimage_smoother\b|"
                    r"\bsmooth (?:an? |the )?image\b",
                    low,
                )
            ),
            (([[[1, 1, 1], [1, 0, 1], [1, 1, 1]],], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),),
        ),
        T(
            "smallest_range_i",
            "def smallest_range_i(nums, k):\n"
            '    """Min possible max-min after adding x in [-k,k] to each element."""\n'
            "    a = [int(x) for x in nums]\n"
            "    k = int(k)\n"
            "    return max(0, max(a) - min(a) - 2 * k)\n",
            lambda low: bool(
                re.search(
                    r"\bsmallest range i\b|"
                    r"\bsmallest_range_i\b|"
                    r"\bsmallest range 1\b",
                    low,
                )
            )
            and not re.search(r"\bsmallest range ii\b", low),
            (([[1], 0], 0), ([[0, 10], 2], 6), ([[1, 3, 6], 3], 0)),
        ),
        T(
            "largest_perimeter",
            "def largest_perimeter(nums):\n"
            '    """Largest perimeter of a non-degenerate triangle from nums, else 0."""\n'
            "    a = sorted((int(x) for x in nums), reverse=True)\n"
            "    for i in range(len(a) - 2):\n"
            "        if a[i] < a[i + 1] + a[i + 2]:\n"
            "            return a[i] + a[i + 1] + a[i + 2]\n"
            "    return 0\n",
            lambda low: bool(
                re.search(
                    r"\blargest perimeter\b|"
                    r"\blargest_perimeter\b|"
                    r"\blargest triangle perimeter\b",
                    low,
                )
            ),
            (([[2, 1, 2],], 5), ([[1, 2, 1, 10],], 0)),
        ),
        T(
            "surface_area",
            "def surface_area(grid):\n"
            '    """Surface area of stacked n x n cubes given height grid."""\n'
            "    g = [list(map(int, row)) for row in grid]\n"
            "    n = len(g)\n"
            "    area = 0\n"
            "    for i in range(n):\n"
            "        for j in range(n):\n"
            "            h = g[i][j]\n"
            "            if h:\n"
            "                area += 2 + 4 * h\n"
            "                if i > 0:\n"
            "                    area -= 2 * min(h, g[i - 1][j])\n"
            "                if j > 0:\n"
            "                    area -= 2 * min(h, g[i][j - 1])\n"
            "    return area\n",
            lambda low: bool(
                re.search(
                    r"\bsurface area of 3d\b|"
                    r"\bsurface_area\b|"
                    r"\b3d shapes surface\b|"
                    r"\bcubes surface area\b",
                    low,
                )
            ),
            (([[[1, 2], [3, 4]],], 34), ([[[1, 1, 1], [1, 0, 1], [1, 1, 1]],], 32)),
        ),
    ]
