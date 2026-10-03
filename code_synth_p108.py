"""Cycle 387: Easy prompts still absent from the template index.

LeetCode 3127, 3345, 3360, 3396, 3402, and 3417 were not referenced by any
pack. Matchers stay ID- or phrase-specific so existing "minimum operations",
Alice-win, and square/color templates keep their prompts.
Loaded before p107.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "can_make_square",
            "def can_make_square(grid):\n"
            '    """True if some 2x2 can be one color with at most one change (LeetCode 3127)."""\n'
            "    rows = len(grid)\n"
            "    cols = len(grid[0]) if rows else 0\n"
            "    for i in range(rows - 1):\n"
            "        for j in range(cols - 1):\n"
            "            cells = (\n"
            "                grid[i][j],\n"
            "                grid[i][j + 1],\n"
            "                grid[i + 1][j],\n"
            "                grid[i + 1][j + 1],\n"
            "            )\n"
            "            black = sum(c == 'B' for c in cells)\n"
            "            if black != 2:\n"
            "                return True\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3127\b|"
                    r"\bmake a square with the same color\b|"
                    r"\bsquare with the same color\b",
                    low,
                )
            ),
            (
                (([["B", "W", "B"], ["B", "W", "W"], ["B", "W", "B"]],), True),
                (([["B", "W", "B"], ["W", "B", "W"], ["B", "W", "B"]],), False),
                (([["B", "B"], ["B", "W"]],), True),
            ),
        ),
        T(
            "smallest_divisible_digit_product",
            "def smallest_divisible_digit_product(n, t):\n"
            '    """Smallest integer >= n whose digit product is divisible by t (LeetCode 3345)."""\n'
            "    x = int(n)\n"
            "    t = int(t)\n"
            "    while True:\n"
            "        prod = 1\n"
            "        for ch in str(x):\n"
            "            prod *= int(ch)\n"
            "            if prod == 0:\n"
            "                break\n"
            "        if prod % t == 0:\n"
            "            return x\n"
            "        x += 1\n"
            "\n"
            "def smallestNumber(n, t):\n"
            "    return smallest_divisible_digit_product(n, t)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3345\b|"
                    r"\bsmallest divisible digit product\b|"
                    r"\bdigit product i\b",
                    low,
                )
            ),
            (
                ((10, 2), 10),
                ((15, 3), 16),
                ((19, 4), 20),
            ),
        ),
        T(
            "stone_removal_game",
            "def stone_removal_game(n):\n"
            '    """Alice starts removing 10, then 9, ...; True if she takes the last (LeetCode 3360)."""\n'
            "    n = int(n)\n"
            "    take = 10\n"
            "    alice = False\n"
            "    while take > 0 and n >= take:\n"
            "        n -= take\n"
            "        alice = not alice\n"
            "        take -= 1\n"
            "    return alice\n"
            "\n"
            "def canAliceWin(n):\n"
            "    return stone_removal_game(n)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3360\b|"
                    r"\bstone removal game\b|"
                    r"\bremove stones game\b",
                    low,
                )
            ),
            (
                ((12,), True),
                ((1,), False),
                ((21,), False),
            ),
        ),
        T(
            "minimum_operations_distinct",
            "def minimum_operations_distinct(nums):\n"
            '    """Ops deleting a prefix of length 3 to make nums distinct (LeetCode 3396)."""\n'
            "    seen = set()\n"
            "    for i in range(len(nums) - 1, -1, -1):\n"
            "        if nums[i] in seen:\n"
            "            return (i + 1 + 2) // 3\n"
            "        seen.add(nums[i])\n"
            "    return 0\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3396\b|"
                    r"\boperations to make elements? (?:in (?:the )?array )?distinct\b|"
                    r"\bmake elements distinct\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4, 2, 3, 3, 5, 7],), 2),
                (([4, 5, 6, 4, 4],), 2),
                (([6, 7, 8, 9],), 0),
            ),
        ),
        T(
            "minimum_operations_columns",
            "def minimum_operations_columns(grid):\n"
            '    """Increments so each column is strictly increasing downward (LeetCode 3402)."""\n'
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    ans = 0\n"
            "    for c in range(cols):\n"
            "        prev = grid[0][c]\n"
            "        for r in range(1, rows):\n"
            "            if grid[r][c] <= prev:\n"
            "                prev = prev + 1\n"
            "                ans += prev - grid[r][c]\n"
            "            else:\n"
            "                prev = grid[r][c]\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3402\b|"
                    r"\bcolumns strictly increasing\b|"
                    r"\bmake columns strictly increasing\b",
                    low,
                )
            ),
            (
                (([[3, 2], [1, 3], [3, 4], [0, 1]],), 15),
                (([[3, 2, 1], [2, 1, 0], [1, 2, 3]],), 12),
            ),
        ),
        T(
            "zigzag_traversal",
            "def zigzag_traversal(grid):\n"
            '    """Zigzag row order, then every other cell (LeetCode 3417)."""\n'
            "    if not grid or not grid[0]:\n"
            "        return []\n"
            "    cells = []\n"
            "    cols = len(grid[0])\n"
            "    for r, row in enumerate(grid):\n"
            "        seq = row if r % 2 == 0 else row[::-1]\n"
            "        cells.extend(seq)\n"
            "    return cells[::2]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3417\b|"
                    r"\bzigzag grid traversal\b|"
                    r"\bzigzag traversal with skip\b",
                    low,
                )
            ),
            (
                (([[1, 2], [3, 4]],), [1, 4]),
                (([[2, 1], [2, 1], [2, 1]],), [2, 1, 2]),
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 3, 5, 7, 9]),
            ),
        ),
    ]
