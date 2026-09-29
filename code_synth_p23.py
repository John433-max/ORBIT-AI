"""Cycle 281: additional verified Python templates (pack 23)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "tictactoe_winner",
            "def tictactoe(moves):\n"
            '    """Winner of a tic-tac-toe game from move pairs, or Draw/Pending."""\n'
            "    board = [[''] * 3 for _ in range(3)]\n"
            "    for i, (r, c) in enumerate(moves):\n"
            "        board[r][c] = 'A' if i % 2 == 0 else 'B'\n"
            "\n"
            "    def winner(ch):\n"
            "        lines = board + [list(col) for col in zip(*board)]\n"
            "        lines.append([board[i][i] for i in range(3)])\n"
            "        lines.append([board[i][2 - i] for i in range(3)])\n"
            "        return any(all(cell == ch for cell in line) for line in lines)\n"
            "\n"
            "    if winner('A'):\n"
            "        return 'A'\n"
            "    if winner('B'):\n"
            "        return 'B'\n"
            "    return 'Draw' if len(moves) == 9 else 'Pending'\n",
            lambda low: bool(
                re.search(
                    r"\btic[\s-]?tac[\s-]?toe\b|"
                    r"\btictactoe\b|"
                    r"\bfind winner on a tic",
                    low,
                )
            ),
            (
                (([[0, 0], [2, 0], [1, 1], [2, 1], [2, 2]],), "A"),
                (([[0, 0], [1, 1], [0, 1], [0, 2], [1, 0], [2, 0]],), "B"),
            ),
        ),
        T(
            "num_equiv_domino_pairs",
            "def num_equiv_domino_pairs(dominoes):\n"
            '    """Count pairs of equivalent dominoes (order-invariant)."""\n'
            "    from collections import Counter\n"
            "    counts = Counter(tuple(sorted(d)) for d in dominoes)\n"
            "    return sum(n * (n - 1) // 2 for n in counts.values())\n",
            lambda low: bool(
                re.search(
                    r"\bequiv(alent)? domino\b|"
                    r"\bnum_equiv_domino_pairs\b|"
                    r"\bdomino pairs\b",
                    low,
                )
            ),
            (
                (([[1, 2], [2, 1], [3, 4], [5, 6]],), 1),
                (([[1, 2], [1, 2], [1, 1], [1, 2], [2, 2]],), 3),
            ),
        ),
        T(
            "distance_between_bus_stops",
            "def distance_between_bus_stops(distance, start, destination):\n"
            '    """Min clockwise/counterclockwise distance between bus stops."""\n'
            "    d = list(distance)\n"
            "    n = len(d)\n"
            "    a, b = start % n, destination % n\n"
            "    if a > b:\n"
            "        a, b = b, a\n"
            "    clockwise = sum(d[a:b])\n"
            "    return min(clockwise, sum(d) - clockwise)\n",
            lambda low: bool(
                re.search(
                    r"\bdistance between bus stops\b|"
                    r"\bdistance_between_bus_stops\b|"
                    r"\bbus stops\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4], 0, 1), 1),
                (([1, 2, 3, 4], 0, 2), 3),
                (([1, 2, 3, 4], 0, 3), 4),
            ),
        ),
        T(
            "day_of_the_year",
            "def day_of_the_year(date):\n"
            '    """Day-of-year number for YYYY-MM-DD (Gregorian leap years)."""\n'
            "    y, m, d = (int(p) for p in str(date).split('-'))\n"
            "    mdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]\n"
            "    if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0):\n"
            "        mdays[1] = 29\n"
            "    return sum(mdays[: m - 1]) + d\n",
            lambda low: bool(
                re.search(
                    r"\bday of the year\b|"
                    r"\bday_of_the_year\b|"
                    r"\bday of year\b",
                    low,
                )
            ),
            ((("2019-01-09",), 9), (("2019-02-10",), 41), (("2003-03-01",), 60)),
        ),
        T(
            "check_straight_line",
            "def check_straight_line(coordinates):\n"
            '    """True if all points lie on one straight line."""\n'
            "    pts = [tuple(p) for p in coordinates]\n"
            "    if len(pts) <= 2:\n"
            "        return True\n"
            "    x0, y0 = pts[0]\n"
            "    x1, y1 = pts[1]\n"
            "    dx, dy = x1 - x0, y1 - y0\n"
            "    for x, y in pts[2:]:\n"
            "        if dy * (x - x0) != dx * (y - y0):\n"
            "            return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bcheck(_| )?(if it is a )?straight line\b|"
                    r"\bcheck_straight_line\b|"
                    r"\bis straight line\b",
                    low,
                )
            ),
            (
                (([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]],), True),
                (([[1, 1], [2, 2], [3, 4], [4, 5], [5, 6], [7, 7]],), False),
            ),
        ),
        T(
            "count_negatives",
            "def count_negatives(grid):\n"
            '    """Count negatives in a row-and-column non-increasing matrix."""\n'
            "    return sum(1 for row in grid for v in row if v < 0)\n",
            lambda low: bool(
                re.search(
                    r"\bcount negatives\b|"
                    r"\bcount_negatives\b|"
                    r"\bnegative numbers in a sorted matrix\b",
                    low,
                )
            ),
            (
                (([[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]],), 8),
                (([[3, 2], [1, 0]],), 0),
            ),
        ),
    ]
