"""Cycle 403: prompts that still returned draft stubs.

Official examples (leetcode.doocs.org / LeetCode statements):
- 3200 Maximum Height of a Triangle: (2,4)->3; (2,1)->2; (1,1)->1; (10,1)->2.
- 3582 Generate Tag for Video Caption:
  "Leetcode daily streak achieved" -> "#leetcodeDailyStreakAchieved";
  "can I Go There" -> "#canIGoThere".
- 3242 Neighbor Sum: grid [[0,1,2],[3,4,5],[6,7,8]]
  adjacent(1)=6, adjacent(4)=16, diagonal(4)=16, diagonal(8)=4.
- 1578 Minimum Time to Make Rope Colorful:
  "abaac",[1,2,3,4,5] -> 3; "abc",[1,2,3] -> 0; "aabaa",[1,2,3,4,1] -> 2.
- 1277 Count Square Submatrices with All Ones:
  [[0,1,1,1],[1,1,1,1],[0,1,1,1]] -> 15; [[1,0,1],[1,1,0],[1,1,0]] -> 7.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "max_height_of_triangle",
            "def max_height_of_triangle(red, blue):\n"
            '    """Tallest alternating-color triangle (LeetCode 3200)."""\n'
            "    ans = 0\n"
            "    for start in (0, 1):\n"
            "        colors = [red, blue]\n"
            "        row, color = 1, start\n"
            "        while row <= colors[color]:\n"
            "            colors[color] -= row\n"
            "            ans = max(ans, row)\n"
            "            row += 1\n"
            "            color ^= 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3200\b", low)
                or "maximum height of a triangle" in low
                or "max height of a triangle" in low
            ),
            examples=(((2, 4), 3), ((2, 1), 2), ((1, 1), 1), ((10, 1), 2)),
        ),
        T(
            "generate_tag",
            "def generate_tag(caption):\n"
            '    """Camel-case video tag, truncated to 100 chars (LeetCode 3582)."""\n'
            "    words = [part.capitalize() for part in caption.split()]\n"
            "    if words:\n"
            "        words[0] = words[0].lower()\n"
            "    return '#' + ''.join(words)[:99]\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3582\b", low)
                or "generate tag for video caption" in low
                or ("video caption" in low and "tag" in low)
            ),
            examples=(
                (("Leetcode daily streak achieved",), "#leetcodeDailyStreakAchieved"),
                (("can I Go There",), "#canIGoThere"),
                (("h" * 101,), "#" + "h" * 99),
            ),
        ),
        T(
            "neighbor_adjacent_sum",
            "def neighbor_adjacent_sum(grid, value):\n"
            '    """Sum of orthogonal neighbors of value (LeetCode 3242)."""\n'
            "    pos = {cell: (r, c) for r, row in enumerate(grid) for c, cell in enumerate(row)}\n"
            "    r, c = pos[value]\n"
            "    total = 0\n"
            "    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):\n"
            "        nr, nc = r + dr, c + dc\n"
            "        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):\n"
            "            total += grid[nr][nc]\n"
            "    return total\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3242\b", low)
                or "neighbor sum" in low
                or "adjacent sum" in low and "neighbor" in low
            ),
            examples=(
                (([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 1), 6),
                (([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 4), 16),
            ),
        ),
        T(
            "neighbor_diagonal_sum",
            "def neighbor_diagonal_sum(grid, value):\n"
            '    """Sum of diagonal neighbors of value (LeetCode 3242)."""\n'
            "    pos = {cell: (r, c) for r, row in enumerate(grid) for c, cell in enumerate(row)}\n"
            "    r, c = pos[value]\n"
            "    total = 0\n"
            "    for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):\n"
            "        nr, nc = r + dr, c + dc\n"
            "        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):\n"
            "            total += grid[nr][nc]\n"
            "    return total\n",
            lambda low: bool(
                re.search(r"\bdiagonal sum\b", low)
                and ("neighbor" in low or re.search(r"\bleetcode\s*3242\b", low))
            )
            and "adjacent" not in low,
            examples=(
                (([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 4), 16),
                (([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 8), 4),
            ),
        ),
        T(
            "min_cost_rope_colorful",
            "def min_cost_rope_colorful(colors, needed_time):\n"
            '    """Min time to remove so no two adjacent balloons match (LeetCode 1578)."""\n'
            "    ans = group = 0\n"
            "    peak = 0\n"
            "    for i, color in enumerate(colors):\n"
            "        if i and color != colors[i - 1]:\n"
            "            ans += group - peak\n"
            "            group = peak = 0\n"
            "        group += needed_time[i]\n"
            "        peak = max(peak, needed_time[i])\n"
            "    return ans + group - peak\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1578\b", low)
                or "make rope colorful" in low
                or "time to make rope colorful" in low
            ),
            examples=(
                (("abaac", [1, 2, 3, 4, 5]), 3),
                (("abc", [1, 2, 3]), 0),
                (("aabaa", [1, 2, 3, 4, 1]), 2),
            ),
        ),
        T(
            "count_squares",
            "def count_squares(matrix):\n"
            '    """Count square submatrices of all ones (LeetCode 1277)."""\n'
            "    if not matrix or not matrix[0]:\n"
            "        return 0\n"
            "    rows, cols = len(matrix), len(matrix[0])\n"
            "    dp = [[0] * cols for _ in range(rows)]\n"
            "    ans = 0\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if matrix[r][c] != 1:\n"
            "                continue\n"
            "            if r == 0 or c == 0:\n"
            "                dp[r][c] = 1\n"
            "            else:\n"
            "                dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])\n"
            "            ans += dp[r][c]\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1277\b", low)
                or "count square submatrices" in low
                or "square submatrices with all ones" in low
            ),
            examples=(
                (([[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]],), 15),
                (([[1, 0, 1], [1, 1, 0], [1, 1, 0]],), 7),
            ),
        ),
    ]
