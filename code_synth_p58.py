"""Cycle 320: min-number game / separate digits / beautiful pairs /
same-color chessboard squares / find champion / complete-day pairs."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "minimum_number_game",
            "def minimum_number_game(nums):\n"
            '    """Alice/Bob min-number game result array (LeetCode 2974)."""\n'
            "    nums = sorted(nums)\n"
            "    out = []\n"
            "    for i in range(0, len(nums), 2):\n"
            "        out.append(nums[i + 1])\n"
            "        out.append(nums[i])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bminimum_number_game\b|"
                    r"\balice[_ ]bob[_ ]minimum[_ ]number[_ ]game\b|"
                    r"\bleetcode[_ ]2974\b",
                    low,
                )
            )
            and "min_max_game" not in low,
            (
                (([5, 4, 2, 3],), [3, 2, 5, 4]),
                (([2, 5],), [5, 2]),
            ),
        ),
        T(
            "separate_digits_in_array",
            "def separate_digits_in_array(nums):\n"
            '    """Concatenate decimal digits of each value (LeetCode 2553)."""\n'
            "    out = []\n"
            "    for x in nums:\n"
            "        s = str(x)\n"
            "        out.extend(int(ch) for ch in s)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bseparate[_ ]the[_ ]digits[_ ]in[_ ]an[_ ]array\b|"
                    r"\bseparate[_ ]the[_ ]digits\b|"
                    r"\bseparate_digits_in_array\b",
                    low,
                )
            )
            and "add_digits" not in low
            and "count_digits" not in low,
            (
                (([13, 25, 83, 77],), [1, 3, 2, 5, 8, 3, 7, 7]),
                (([7, 1, 3, 9],), [7, 1, 3, 9]),
            ),
        ),
        T(
            "beautiful_pairs",
            "def beautiful_pairs(nums):\n"
            '    """Count pairs whose first-digit(i) and last-digit(j) are coprime (LeetCode 2748)."""\n'
            "    from math import gcd\n"
            "    def first_digit(x):\n"
            "        while x >= 10:\n"
            "            x //= 10\n"
            "        return x\n"
            "    n = len(nums)\n"
            "    return sum(\n"
            "        1\n"
            "        for i in range(n)\n"
            "        for j in range(i + 1, n)\n"
            "        if gcd(first_digit(nums[i]), nums[j] % 10) == 1\n"
            "    )\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]of[_ ]beautiful[_ ]pairs\b|"
                    r"\bbeautiful[_ ]pairs\b|"
                    r"\bbeautiful_pairs\b",
                    low,
                )
            )
            and "palindrome" not in low,
            (
                (([2, 5, 1, 4],), 5),
                (([11, 21, 12],), 2),
            ),
        ),
        T(
            "same_color_chessboard",
            "def same_color_chessboard(coordinate1, coordinate2):\n"
            '    """True iff two chess squares have the same color (LeetCode 3274)."""\n'
            "    def color(c):\n"
            "        return (ord(c[0]) - ord('a') + int(c[1])) % 2\n"
            "    return color(coordinate1) == color(coordinate2)\n",
            lambda low: bool(
                re.search(
                    r"\bcheck[_ ]if[_ ]two[_ ]chessboard[_ ]squares[_ ]have[_ ]the[_ ]same[_ ]color\b|"
                    r"\bsame[_ ]color[_ ]chessboard\b|"
                    r"\bsame_color_chessboard\b",
                    low,
                )
            ),
            (
                (("a1", "c3"), True),
                (("a1", "h3"), False),
            ),
        ),
        T(
            "find_champion",
            "def find_champion(grid):\n"
            '    """Team that is not weaker than any other (LeetCode 2923)."""\n'
            "    n = len(grid)\n"
            "    for i in range(n):\n"
            "        if sum(grid[i]) == n - 1:\n"
            "            return i\n"
            "    return 0\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]champion[_ ]i\b|"
                    r"\bfind[_ ]the[_ ]champion\b|"
                    r"\bfind_champion\b",
                    low,
                )
            )
            and "ii" not in low
            and "center" not in low,
            (
                (([[0, 1], [0, 0]],), 0),
                (([[0, 0, 1], [1, 0, 1], [0, 0, 0]],), 1),
            ),
        ),
        T(
            "count_complete_day_pairs",
            "def count_complete_day_pairs(hours):\n"
            '    """Pairs whose hours sum to a multiple of 24 (LeetCode 3184)."""\n'
            "    n = len(hours)\n"
            "    return sum(\n"
            "        1\n"
            "        for i in range(n)\n"
            "        for j in range(i + 1, n)\n"
            "        if (hours[i] + hours[j]) % 24 == 0\n"
            "    )\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]pairs[_ ]that[_ ]form[_ ]a[_ ]complete[_ ]day\b|"
                    r"\bcount[_ ]complete[_ ]day[_ ]pairs\b|"
                    r"\bcount_complete_day_pairs\b",
                    low,
                )
            ),
            (
                (([12, 12, 30, 24, 24],), 2),
                (([72, 48, 24, 3],), 3),
            ),
        ),
    ]
