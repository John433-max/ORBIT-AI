"""Cycle 405: implement-without-function stubs and a sandbox syntax miss.

Official examples:
- LeetCode 556 Next Greater Element III:
  12 -> 21; 21 -> -1; 101 -> 110. No greater permutation, or result
  above 2**31-1, returns -1.
- LeetCode 807 Max Increase to Keep City Skyline:
  [[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]] -> 35.
  Each cell may rise to min(row max, col max).
- LeetCode 299 Bulls and Cows:
  secret 1807 guess 7810 -> "1A3B"; 1123 / 0111 -> "1A1B".
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "next_greater_element_iii",
            "def nextGreaterElement(n):\n"
            '    """Smallest greater permutation of n, else -1 (LeetCode 556)."""\n'
            "    digits = list(str(int(n)))\n"
            "    i = len(digits) - 2\n"
            "    while i >= 0 and digits[i] >= digits[i + 1]:\n"
            "        i -= 1\n"
            "    if i < 0:\n"
            "        return -1\n"
            "    j = len(digits) - 1\n"
            "    while digits[j] <= digits[i]:\n"
            "        j -= 1\n"
            "    digits[i], digits[j] = digits[j], digits[i]\n"
            "    digits[i + 1 :] = reversed(digits[i + 1 :])\n"
            "    out = int(''.join(digits))\n"
            "    return out if out <= 2147483647 else -1\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*556\b", low)
                or "next greater element iii" in low
                or "next greater element 3" in low
            ),
            examples=(
                ((12,), 21),
                ((21,), -1),
                ((101,), 110),
            ),
        ),
        T(
            "max_increase_skyline",
            "def maxIncreaseKeepingSkyline(grid):\n"
            '    """Sum of raises that keep row and column skylines (LeetCode 807)."""\n'
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    rows = [max(int(v) for v in row) for row in grid]\n"
            "    cols = [max(int(grid[r][c]) for r in range(len(grid))) for c in range(len(grid[0]))]\n"
            "    total = 0\n"
            "    for r, row in enumerate(grid):\n"
            "        for c, val in enumerate(row):\n"
            "            total += min(rows[r], cols[c]) - int(val)\n"
            "    return total\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*807\b", low)
                or "city skyline" in low
                or "keep city skyline" in low
                or "max increase keeping skyline" in low
            ),
            examples=(
                (([[3, 0, 8, 4], [2, 4, 5, 7], [9, 2, 6, 3], [0, 3, 1, 0]],), 35),
                (([[1, 2], [3, 4]],), 1),
            ),
        ),
        T(
            "bulls_and_cows",
            "def getHint(secret, guess):\n"
            '    """Bulls (exact) and cows (wrong spot) hint (LeetCode 299)."""\n'
            "    secret, guess = str(secret), str(guess)\n"
            "    bulls = sum(a == b for a, b in zip(secret, guess))\n"
            "    counts = {}\n"
            "    for ch in secret:\n"
            "        counts[ch] = counts.get(ch, 0) + 1\n"
            "    overlap = 0\n"
            "    for ch in guess:\n"
            "        if counts.get(ch, 0):\n"
            "            overlap += 1\n"
            "            counts[ch] -= 1\n"
            "    cows = overlap - bulls\n"
            "    return f'{bulls}A{cows}B'\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*299\b", low)
                or "bulls and cows" in low
                or "bulls & cows" in low
            ),
            examples=(
                (("1807", "7810"), "1A3B"),
                (("1123", "0111"), "1A1B"),
            ),
        ),
    ]
