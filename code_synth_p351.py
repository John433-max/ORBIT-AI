"""Cycle 642 (p351): fill remaining Easy/Medium coding-smoke gaps.

is_power_of_three (326), trailing_zeroes (172), binary_watch (401),
count_sub_islands (1905), excel_sheet_column_title (168), letter_case_permutation (784).

Also widens convert_to_title / title_to_number matchers so "excel sheet column title"
and similar phrases route correctly (higher pack wins).
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
    """Return True if n is a power of three (LeetCode 326)."""
    if n <= 0:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1
''',
            lambda low: bool(
                re.search(r"\bis[_\s-]?power[_\s-]?of[_\s-]?three\b", low)
                or re.search(r"\bpower\s+of\s+3\b", low)
                or re.search(r"\b3\^k\b", low)
            ),
            (
                ((1,), True),
                ((3,), True),
                ((9,), True),
                ((27,), True),
                ((0,), False),
                ((2,), False),
                ((45,), False),
            ),
        ),
        T(
            "trailing_zeroes",
            '''def trailing_zeroes(n):
    """Number of trailing zeroes in n! (LeetCode 172)."""
    if n < 0:
        return 0
    count = 0
    while n:
        n //= 5
        count += n
    return count
''',
            lambda low: bool(
                re.search(r"\btrailing[_\s-]?zeroe?s\b", low)
                or re.search(r"\bfactorial\s+trailing\b", low)
                or re.search(r"\btrailing\s+zeros?\s+in\s+n?!\b", low)
            ),
            (
                ((0,), 0),
                ((5,), 1),
                ((10,), 2),
                ((25,), 6),
                ((3,), 0),
            ),
        ),
        T(
            "binary_watch",
            '''def binary_watch(turned_on):
    """All possible times a binary watch can show with turned_on LEDs (LeetCode 401)."""
    res = []
    for h in range(12):
        for m in range(60):
            if bin(h).count("1") + bin(m).count("1") == turned_on:
                res.append(f"{h}:{m:02d}")
    return res
''',
            lambda low: bool(
                re.search(r"\bbinary[_\s-]?watch\b", low)
                or re.search(r"\bread\s+binary\s+watch\b", low)
            ),
            (
                ((1,), ["0:01", "0:02", "0:04", "0:08", "0:16", "0:32", "1:00", "2:00", "4:00", "8:00"]),
                ((0,), ["0:00"]),
            ),
        ),
        T(
            "count_sub_islands",
            '''def count_sub_islands(grid1, grid2):
    """Count sub-islands of grid2 that are contained in grid1 (LeetCode 1905)."""
    if not grid1 or not grid2:
        return 0
    rows, cols = len(grid2), len(grid2[0])

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid2[r][c] != 1:
            return True
        grid2[r][c] = 0
        ok = grid1[r][c] == 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if not dfs(r + dr, c + dc):
                ok = False
        return ok

    count = 0
    for i in range(rows):
        for j in range(cols):
            if grid2[i][j] == 1 and dfs(i, j):
                count += 1
    return count
''',
            lambda low: bool(
                re.search(r"\bcount[_\s-]?sub[_\s-]?islands?\b", low)
                or re.search(r"\bsub-?islands?\b", low)
            ),
            (
                (
                    (
                        [[1, 1, 1, 0, 0], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 0, 1, 1]],
                        [[1, 1, 1, 0, 0], [0, 0, 1, 1, 1], [0, 1, 0, 0, 0], [1, 0, 1, 1, 0], [0, 1, 0, 1, 0]],
                    ),
                    3,
                ),
                (
                    (
                        [[1, 0, 1, 0, 1], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 0, 1, 0, 1]],
                        [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1]],
                    ),
                    2,
                ),
            ),
        ),
        T(
            "excel_sheet_column_title",
            '''def excel_sheet_column_title(column_number):
    """Convert column number to Excel title (LeetCode 168)."""
    res = []
    n = column_number
    while n:
        n, rem = divmod(n - 1, 26)
        res.append(chr(ord("A") + rem))
    return "".join(reversed(res))
''',
            lambda low: bool(
                re.search(r"\bexcel[_\s-]?sheet[_\s-]?column[_\s-]?title\b", low)
                or re.search(r"\bexcel\s+column\s+title\b", low)
                or re.search(r"\bcolumn\s+(?:number\s+)?to\s+title\b", low)
                or re.search(r"\bconvert[_\s-]?to[_\s-]?title\b", low)
                or re.search(r"\bexcel\s+title\s+from\b", low)
            ),
            (
                ((1,), "A"),
                ((28,), "AB"),
                ((701,), "ZY"),
                ((52,), "AZ"),
            ),
        ),
        T(
            "letter_case_permutation",
            '''def letter_case_permutation(s):
    """All letter-case permutations of a string (LeetCode 784)."""
    res = [""]
    for ch in s:
        if ch.isalpha():
            nxt = []
            for prefix in res:
                nxt.append(prefix + ch.lower())
                nxt.append(prefix + ch.upper())
            res = nxt
        else:
            res = [prefix + ch for prefix in res]
    return res
''',
            lambda low: bool(
                re.search(r"\bletter[_\s-]?case[_\s-]?permutation\b", low)
                or re.search(r"\bcase\s+permutation\b", low)
                or re.search(r"\bletter\s+case\s+perm", low)
            ),
            (
                (("a1b2",), ["a1b2", "a1B2", "A1b2", "A1B2"]),
                (("3z4",), ["3z4", "3Z4"]),
                (("12345",), ["12345"]),
            ),
        ),
        # Widen existing convert_to_title / title_to_number so common phrases hit.
        T(
            "convert_to_title",
            '''def convert_to_title(column_number):
    """Convert column number to Excel title (LeetCode 168)."""
    res = []
    n = column_number
    while n:
        n, rem = divmod(n - 1, 26)
        res.append(chr(ord("A") + rem))
    return "".join(reversed(res))
''',
            lambda low: bool(
                re.search(r"\bexcel[_\s-]?sheet[_\s-]?column[_\s-]?title\b", low)
                or re.search(r"\bexcel\s+column\s+title\b", low)
                or re.search(r"\bcolumn\s+(?:number\s+)?to\s+title\b", low)
                or re.search(r"\bconvert[_\s-]?to[_\s-]?title\b", low)
                or re.search(r"\bexcel\s+title\s+from\b", low)
                or re.search(r"\bcolumn\s+title\b", low)
            ),
            (
                ((1,), "A"),
                ((28,), "AB"),
                ((701,), "ZY"),
            ),
        ),
        T(
            "title_to_number",
            '''def title_to_number(column_title):
    """Convert Excel column title to number (LeetCode 171)."""
    n = 0
    for ch in column_title:
        n = n * 26 + (ord(ch.upper()) - ord("A") + 1)
    return n
''',
            lambda low: bool(
                re.search(r"\bexcel[_\s-]?sheet[_\s-]?column[_\s-]?number\b", low)
                or re.search(r"\bexcel\s+column\s+number\b", low)
                or re.search(r"\bcolumn\s+title\s+to\s+number\b", low)
                or re.search(r"\btitle[_\s-]?to[_\s-]?number\b", low)
                or re.search(r"\bexcel\s+number\s+from\b", low)
            ),
            (
                (("A",), 1),
                (("AB",), 28),
                (("ZY",), 701),
            ),
        ),
    ]
