"""Cycle 642 (p350 restore): six Easy prompts from smoke code_2021–code_2026.

is_power_of_three (326), trailing_zeroes (172), binary_watch (401),
count_sub_islands (1905), excel_sheet_column_title (168),
letter_case_permutation (784).

Previous p350 write was truncated mid-template (SyntaxError); pack never loaded.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "is_power_of_three",
            '''def is_power_of_three(n):
    """True if n is a power of three (LeetCode 326, educational)."""
    if n <= 0:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1
''',
            lambda low: bool(
                re.search(r"\bpower\s+of\s+three\b", low)
                or re.search(r"\bis[_ ]power[_ ]of[_ ]three\b", low)
            ),
            (
                ((27,), True),
                ((0,), False),
                ((9,), True),
                ((45,), False),
            ),
        ),
        T(
            "trailing_zeroes",
            '''def trailing_zeroes(n):
    """Number of trailing zeroes in n! (LeetCode 172, educational)."""
    count = 0
    while n >= 5:
        n //= 5
        count += n
    return count
''',
            lambda low: bool(
                re.search(r"\btrailing\s+zeroe?s?\b", low)
                and "factorial" not in low.replace(" ", "")
                or re.search(r"\btrailing\s+zeroe?s?\b", low)
            )
            and "binary" not in low,
            (
                ((3,), 0),
                ((5,), 1),
                ((10,), 2),
                ((25,), 6),
            ),
        ),
        T(
            "binary_watch",
            '''def binary_watch(turned_on):
    """All valid times with exactly turned_on LEDs (LeetCode 401, educational)."""
    out = []
    for h in range(12):
        for m in range(60):
            if bin(h).count("1") + bin(m).count("1") == turned_on:
                out.append("%d:%02d" % (h, m))
    return out
''',
            lambda low: bool(
                re.search(r"\bbinary\s+watch\b", low)
                or re.search(r"\bread\s+binary\s+watch\b", low)
            ),
            (
                ((1,), ["0:01", "0:02", "0:04", "0:08", "0:16", "0:32", "1:00", "2:00", "4:00", "8:00"]),
            ),
        ),
        T(
            "count_sub_islands",
            '''def count_sub_islands(grid1, grid2):
    """Count islands in grid2 that are subsets of grid1 (LeetCode 1905)."""
    if not grid2 or not grid2[0]:
        return 0
    rows, cols = len(grid2), len(grid2[0])

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid2[r][c] == 0:
            return True
        grid2[r][c] = 0
        ok = grid1[r][c] == 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if not dfs(r + dr, c + dc):
                ok = False
        return ok

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid2[r][c] == 1 and dfs(r, c):
                count += 1
    return count
''',
            lambda low: bool(
                re.search(r"\bsub[\s-]?islands?\b", low)
                or re.search(r"\bcount\s+sub\s+islands?\b", low)
            ),
            (
                (
                    (
                        [[1, 1, 1, 0, 0], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 0, 1, 1]],
                        [[1, 1, 1, 0, 0], [0, 0, 1, 1, 1], [0, 1, 0, 0, 0], [1, 0, 1, 1, 0], [0, 1, 0, 1, 0]],
                    ),
                    3,
                ),
                (([[1, 0, 1, 0, 1], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 0, 1, 0, 1]],
                  [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1]]), 2),
            ),
        ),
        T(
            "excel_sheet_column_title",
            '''def excel_sheet_column_title(column_number):
    """Convert 1-based column number to Excel title (LeetCode 168)."""
    letters = []
    n = column_number
    while n:
        n -= 1
        letters.append(chr(ord("A") + n % 26))
        n //= 26
    return "".join(reversed(letters))
''',
            lambda low: bool(
                re.search(r"\bexcel\s+(sheet\s+)?column\s+title\b", low)
                or re.search(r"\bcolumn\s+title\b", low)
                or re.search(r"\bconvert\s+to\s+title\b", low)
            )
            and "number" not in low,
            (
                ((1,), "A"),
                ((28,), "AB"),
                ((701,), "ZY"),
            ),
        ),
        T(
            "letter_case_permutation",
            '''def letter_case_permutation(s):
    """All letter-case permutations of s (LeetCode 784, educational)."""
    out = []
    n = len(s)

    def dfs(i, path):
        if i == n:
            out.append("".join(path))
            return
        ch = s[i]
        path.append(ch)
        dfs(i + 1, path)
        path.pop()
        if ch.isalpha():
            path.append(ch.swapcase())
            dfs(i + 1, path)
            path.pop()

    dfs(0, [])
    return out
''',
            lambda low: bool(
                re.search(r"\bletter\s+case\s+permutation\b", low)
                or re.search(r"\bletter[_ ]case[_ ]permutation\b", low)
            ),
            (
                (("a1b2",), ["a1b2", "a1B2", "A1b2", "A1B2"]),
                (("3z4",), ["3z4", "3Z4"]),
            ),
        ),
    ]
