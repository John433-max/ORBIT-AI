"""Cycle 403: restore bare-phrase LC names expected by smoke code_2037-2056.

excel_sheet_column_number, nim_game, is_ugly, valid_perfect_square,
search_insert_position, multiply_strings — educational pure-Python.
"""
from __future__ import annotations

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "multiply_strings",
            '''def multiply_strings(num1, num2):
    """Multiply two non-negative integers given as decimal strings.

    Educational LeetCode 43. Leading zeros are stripped; "0" stays "0".
    """
    if num1 == "0" or num2 == "0" or not num1 or not num2:
        return "0"
    m, n = len(num1), len(num2)
    pos = [0] * (m + n)
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            mul = (ord(num1[i]) - 48) * (ord(num2[j]) - 48)
            p1, p2 = i + j, i + j + 1
            total = mul + pos[p2]
            pos[p2] = total % 10
            pos[p1] += total // 10
    out = "".join(str(d) for d in pos).lstrip("0")
    return out or "0"
''',
            lambda low: ("multiply" in low and "string" in low and "complex" not in low),
            examples=[(("2", "3"), "6"), (("123", "456"), "56088"), (("0", "0"), "0")],
        ),
        T(
            "excel_sheet_column_number",
            '''def excel_sheet_column_number(columnTitle: str) -> int:
    """Convert Excel column title to number (LeetCode 171).

    A -> 1, Z -> 26, AA -> 27, AB -> 28.
    """
    n = 0
    for ch in columnTitle:
        n = n * 26 + (ord(ch.upper()) - ord("A") + 1)
    return n
''',
            lambda low: (
                "excel sheet column number" in low
                or "column title to number" in low
                # Exact LC 171; avoid 1716 (leetcode bank / total_money)
                or ("leetcode 171" in low and "leetcode 1716" not in low)
            ),
            examples=[(("A",), 1), (("AB",), 28), (("ZY",), 701)],
        ),
        T(
            "nim_game",
            '''def nim_game(n: int) -> bool:
    """Can I win the Nim game if I start with n stones (LeetCode 292)?

    Remove 1, 2, or 3 stones. Opponent plays optimally.
    Win iff n is not divisible by 4.
    """
    return n % 4 != 0
''',
            lambda low: ("nim game" in low or "leetcode 292" in low),
            examples=[((1,), True), ((2,), True), ((4,), False)],
        ),
        T(
            "is_ugly",
            '''def is_ugly(n: int) -> bool:
    """True if n is an ugly number (only prime factors 2, 3, 5) (LeetCode 263).

    n <= 0 is not ugly.
    """
    if n <= 0:
        return False
    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
    return n == 1
''',
            lambda low: (
                "is ugly" in low
                or "leetcode 263" in low
                or ("ugly number" in low and "nth" not in low and "n-th" not in low)
            ),
            examples=[((6,), True), ((1,), True), ((14,), False)],
        ),
        T(
            "valid_perfect_square",
            '''def valid_perfect_square(num: int) -> bool:
    """True if num is a perfect square without using sqrt (LeetCode 367).

    Binary search for an integer root.
    """
    if num < 1:
        return False
    lo, hi = 1, num
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
''',
            lambda low: ("valid perfect square" in low or "leetcode 367" in low),
            examples=[((16,), True), ((14,), False), ((1,), True)],
        ),
        T(
            "search_insert_position",
            '''def search_insert_position(nums, target: int) -> int:
    """Index where target is or should be inserted in a sorted array (LeetCode 35).

    Lower-bound binary search.
    """
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
''',
            lambda low: (
                "search insert position" in low
                # Exact LC 35 only (word boundary — not 354/357/3576/…)
                or bool(__import__("re").search(r"\\bleetcode\\s*35\\b", low))
            ),
            examples=[
                (([1, 3, 5, 6], 5), 2),
                (([1, 3, 5, 6], 2), 1),
                (([1, 3, 5, 6], 7), 4),
            ],
        ),
    ]
