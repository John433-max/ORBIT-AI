"""Cycle 544: sudoku solver (LeetCode 37 style, in-place or return board)."""
from __future__ import annotations

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "sudoku_solver",
            "def sudoku_solver(board):\n"
            '    """Fill a 9x9 Sudoku board in place. Empty cells are \'.\' or 0. Returns the board."""\n'
            "    rows = [set() for _ in range(9)]\n"
            "    cols = [set() for _ in range(9)]\n"
            "    boxes = [set() for _ in range(9)]\n"
            "    empties = []\n"
            "    for r in range(9):\n"
            "        for c in range(9):\n"
            "            v = board[r][c]\n"
            "            if v in ('.', '0', 0, None):\n"
            "                empties.append((r, c))\n"
            "                continue\n"
            "            v = str(v)\n"
            "            board[r][c] = v\n"
            "            rows[r].add(v)\n"
            "            cols[c].add(v)\n"
            "            boxes[(r // 3) * 3 + c // 3].add(v)\n"
            "\n"
            "    def place(k):\n"
            "        if k == len(empties):\n"
            "            return True\n"
            "        r, c = empties[k]\n"
            "        b = (r // 3) * 3 + c // 3\n"
            "        for d in '123456789':\n"
            "            if d not in rows[r] and d not in cols[c] and d not in boxes[b]:\n"
            "                board[r][c] = d\n"
            "                rows[r].add(d)\n"
            "                cols[c].add(d)\n"
            "                boxes[b].add(d)\n"
            "                if place(k + 1):\n"
            "                    return True\n"
            "                rows[r].remove(d)\n"
            "                cols[c].remove(d)\n"
            "                boxes[b].remove(d)\n"
            "                board[r][c] = '.'\n"
            "        return False\n"
            "\n"
            "    place(0)\n"
            "    return board\n",
            lambda low: (
                ("sudoku" in low)
                and ("solve" in low or "solver" in low or "fill" in low)
                and "valid" not in low
            ),
            (
                (
                    (
                        [
                            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
                            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
                            [".", "9", "8", ".", ".", ".", ".", "6", "."],
                            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
                            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
                            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                            [".", "6", ".", ".", ".", ".", "2", "8", "."],
                            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
                            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
                        ],
                    ),
                    [
                        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
                        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
                        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
                        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
                        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
                        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
                        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
                        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
                        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
                    ],
                ),
            ),
        ),
    ]
