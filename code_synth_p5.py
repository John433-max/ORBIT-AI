"""Cycle 262: additional verified Python templates (pack 5)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "valid_sudoku",
            "def valid_sudoku(board):\n"
            '    """Return True if a 9x9 Sudoku board is valid (empty as \'.\')."""\n'
            "    rows = [set() for _ in range(9)]\n"
            "    cols = [set() for _ in range(9)]\n"
            "    boxes = [set() for _ in range(9)]\n"
            "    for i, row in enumerate(board):\n"
            "        for j, cell in enumerate(row):\n"
            "            if cell in ('.', 0, None, ''):\n"
            "                continue\n"
            "            val = str(cell)\n"
            "            b = (i // 3) * 3 + j // 3\n"
            "            if val in rows[i] or val in cols[j] or val in boxes[b]:\n"
            "                return False\n"
            "            rows[i].add(val)\n"
            "            cols[j].add(val)\n"
            "            boxes[b].add(val)\n"
            "    return True\n",
            lambda low: bool(
                re.search(r"\bvalid(?:ate)? sudoku\b|\bsudoku board\b|\bis_valid_sudoku\b", low)
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
                    True,
                ),
                (
                    (
                        [["5", "5", ".", ".", ".", ".", ".", ".", "."]]
                        + [["."] * 9 for _ in range(8)],
                    ),
                    False,
                ),
            ),
        ),
        T(
            "game_of_life",
            "def game_of_life(board):\n"
            '    """Return the next Game of Life board (0 dead, 1 live)."""\n'
            "    if not board or not board[0]:\n"
            "        return board\n"
            "    m, n = len(board), len(board[0])\n"
            "    nxt = [[0] * n for _ in range(m)]\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            live = 0\n"
            "            for di in (-1, 0, 1):\n"
            "                for dj in (-1, 0, 1):\n"
            "                    if di == 0 and dj == 0:\n"
            "                        continue\n"
            "                    ni, nj = i + di, j + dj\n"
            "                    if 0 <= ni < m and 0 <= nj < n and board[ni][nj] == 1:\n"
            "                        live += 1\n"
            "            if board[i][j] == 1:\n"
            "                nxt[i][j] = 1 if live in (2, 3) else 0\n"
            "            else:\n"
            "                nxt[i][j] = 1 if live == 3 else 0\n"
            "    return nxt\n",
            lambda low: bool(
                re.search(r"\bgame of life\b|\bnext board state\b|\bconway\b", low)
            ),
            (
                (([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]],), [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]),
            ),
        ),
        T(
            "count_and_say",
            "def count_and_say(n):\n"
            '    """nth term of the count-and-say sequence (1-indexed)."""\n'
            "    s = '1'\n"
            "    for _ in range(max(0, int(n) - 1)):\n"
            "        out = []\n"
            "        i = 0\n"
            "        while i < len(s):\n"
            "            j = i\n"
            "            while j < len(s) and s[j] == s[i]:\n"
            "                j += 1\n"
            "            out.append(str(j - i))\n"
            "            out.append(s[i])\n"
            "            i = j\n"
            "        s = ''.join(out)\n"
            "    return s\n",
            lambda low: bool(re.search(r"\bcount and say\b|\bcount_and_say\b", low)),
            (((1,), "1"), ((4,), "1211")),
        ),
        T(
            "majority_element_ii",
            "def majority_element_ii(nums):\n"
            '    """Elements appearing more than n/3 times (Boyer-Moore)."""\n'
            "    nums = list(nums)\n"
            "    a = b = None\n"
            "    ca = cb = 0\n"
            "    for x in nums:\n"
            "        if a == x:\n"
            "            ca += 1\n"
            "        elif b == x:\n"
            "            cb += 1\n"
            "        elif ca == 0:\n"
            "            a, ca = x, 1\n"
            "        elif cb == 0:\n"
            "            b, cb = x, 1\n"
            "        else:\n"
            "            ca -= 1\n"
            "            cb -= 1\n"
            "    out = []\n"
            "    n = len(nums)\n"
            "    for cand in (a, b):\n"
            "        if cand is not None and nums.count(cand) > n // 3 and cand not in out:\n"
            "            out.append(cand)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bmajority element\s*(ii|2)\b|"
                    r"\bmajority_element_ii\b|"
                    r"\bmore than n/?3\b",
                    low,
                )
            ),
            ((([3, 2, 3],), [3]), (([1, 1, 1, 3, 3, 2, 2, 2],), [1, 2])),
        ),
        T(
            "my_pow",
            "def my_pow(x, n):\n"
            '    """Compute x**n with binary exponentiation (n may be negative)."""\n'
            "    n = int(n)\n"
            "    if n == 0:\n"
            "        return 1.0\n"
            "    if n < 0:\n"
            "        x = 1.0 / x\n"
            "        n = -n\n"
            "    acc = 1.0\n"
            "    base = float(x)\n"
            "    while n:\n"
            "        if n & 1:\n"
            "            acc *= base\n"
            "        base *= base\n"
            "        n >>= 1\n"
            "    return acc\n",
            lambda low: bool(
                re.search(
                    r"\bpow\s*\(\s*x|"
                    r"\bpow x n\b|"
                    r"\bmy_pow\b|"
                    r"\bnegative exponent\b|"
                    r"\bbinary exponentiation\b",
                    low,
                )
            ),
            (((2.0, 10), 1024.0), ((2.0, -2), 0.25)),
        ),
        T(
            "remove_duplicates_ii",
            "def remove_duplicates_ii(nums):\n"
            '    """Keep at most two copies of each value in a sorted list."""\n'
            "    nums = list(nums)\n"
            "    out = []\n"
            "    for n in nums:\n"
            "        if len(out) < 2 or out[-1] != n or out[-2] != n:\n"
            "            out.append(n)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bat most two\b|"
                    r"\bkeep(?:s|ing)? at most 2\b|"
                    r"\bremove_duplicates_ii\b|"
                    r"\bduplicates from sorted array ii\b|"
                    r"\bsorted array(?: ii| 2)\b",
                    low,
                )
            ),
            ((([1, 1, 1, 2, 2, 3],), [1, 1, 2, 2, 3]), (([0, 0, 1, 1, 1, 1, 2, 3, 3],), [0, 0, 1, 1, 2, 3, 3])),
        ),
    ]
