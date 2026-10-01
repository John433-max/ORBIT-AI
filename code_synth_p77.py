"""Cycle 341: unused Easy — rings and rods / all bits set /
grid conditions / string-game kth / length-three subarrays / coin game."""

from __future__ import annotations

import re
from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_points",
            "def count_points(rings):\n"
            '    """Rods that have red, green, and blue rings (LeetCode 2103)."""\n'
            "    rods = [set() for _ in range(10)]\n"
            "    for i in range(0, len(rings), 2):\n"
            "        rods[int(rings[i + 1])].add(rings[i])\n"
            "    return sum(len(colors) == 3 for colors in rods)\n",
            lambda low: bool(re.search(r"rings and rods", low)),
            (
                (("B0B6G0R6R0R6G9",), 1),
                (("B0R0G0R9R0B0G0",), 1),
                (("G4",), 0),
            ),
        ),
        T(
            "smallest_number",
            "def smallest_number(n):\n"
            '    """Smallest number >= n whose binary is all ones (LeetCode 3370)."""\n'
            "    value = 1\n"
            "    while value < n:\n"
            "        value = value * 2 + 1\n"
            "    return value\n",
            lambda low: bool(re.search(r"all bits set", low))
            and "set bits" not in low,
            (
                ((5,), 7),
                ((10,), 15),
                ((3,), 3),
            ),
        ),
        T(
            "satisfies_conditions",
            "def satisfies_conditions(grid):\n"
            '    """Columns equal, adjacent row cells differ (LeetCode 3142)."""\n'
            "    if not grid or not grid[0]:\n"
            "        return True\n"
            "    rows = len(grid)\n"
            "    cols = len(grid[0])\n"
            "    for i in range(rows - 1):\n"
            "        for j in range(cols):\n"
            "            if grid[i][j] != grid[i + 1][j]:\n"
            "                return False\n"
            "    for j in range(cols - 1):\n"
            "        if grid[0][j] == grid[0][j + 1]:\n"
            "            return False\n"
            "    return True\n",
            lambda low: bool(re.search(r"grid satisfies conditions", low)),
            (
                (([[1, 0, 2], [1, 0, 2]],), True),
                (([[1, 1, 1], [0, 0, 0]],), False),
                (([[1], [2], [3]],), False),
            ),
        ),
        T(
            "kth_character",
            "def kth_character(k):\n"
            '    """K-th char after appending incremented copies (LeetCode 3304)."""\n'
            "    return chr(ord('a') + bin(k - 1).count('1'))\n",
            lambda low: bool(re.search(r"k-th character in string game|kth character in string game", low)),
            (
                ((5,), "b"),
                ((10,), "c"),
                ((1,), "a"),
            ),
        ),
        T(
            "count_subarrays",
            "def count_subarrays(nums):\n"
            '    """Length-3 windows where middle is twice the ends (LeetCode 3392)."""\n'
            "    return sum(\n"
            "        (nums[i - 1] + nums[i + 1]) * 2 == nums[i]\n"
            "        for i in range(1, len(nums) - 1)\n"
            "    )\n",
            lambda low: bool(
                re.search(r"subarrays of length three with a condition", low)
            ),
            (
                (([1, 2, 1, 4, 1],), 1),
                (([1, 1, 1],), 0),
            ),
        ),
        T(
            "losing_player",
            "def losing_player(x, y):\n"
            '    """Winner of the 75+10 coin game (LeetCode 3222)."""\n'
            "    return 'Alice' if min(x, y // 4) % 2 else 'Bob'\n",
            lambda low: bool(re.search(r"winning player in coin game", low)),
            (
                ((2, 7), "Alice"),
                ((4, 11), "Bob"),
            ),
        ),
    ]
