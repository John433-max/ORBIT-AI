"""Cycle 264: additional verified Python templates (pack 7)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "missing_ranges",
            "def missing_ranges(nums, lower, upper):\n"
            '    """Inclusive missing ranges of nums inside [lower, upper]."""\n'
            "    nums = [int(x) for x in nums]\n"
            "    lower, upper = int(lower), int(upper)\n"
            "    out = []\n"
            "    prev = lower - 1\n"
            "    seq = nums + [upper + 1]\n"
            "    for x in seq:\n"
            "        if x - prev >= 2:\n"
            "            a, b = prev + 1, x - 1\n"
            "            out.append(str(a) if a == b else f'{a}->{b}')\n"
            "        prev = x\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bmissing ranges\b|"
                    r"\bmissing_ranges\b|"
                    r"\bmissing inclusive ranges\b",
                    low,
                )
            ),
            (
                (([0, 1, 3, 50, 75], 0, 99), ["2", "4->49", "51->74", "76->99"]),
                (([], 1, 1), ["1"]),
            ),
        ),
        T(
            "third_max",
            "def third_max(nums):\n"
            '    """Third distinct maximum, or the maximum if fewer than three."""\n'
            "    uniq = sorted(set(int(x) for x in nums), reverse=True)\n"
            "    return uniq[2] if len(uniq) >= 3 else uniq[0]\n",
            lambda low: bool(
                re.search(
                    r"\bthird (?:distinct )?max(?:imum)?\b|"
                    r"\bthird_max\b|"
                    r"\b3rd (?:distinct )?max(?:imum)?\b",
                    low,
                )
            ),
            ((([3, 2, 1],), 1), (([1, 2],), 2), (([2, 2, 3, 1],), 1)),
        ),
        T(
            "add_digits",
            "def add_digits(num):\n"
            '    """Digital root: repeatedly sum digits until a single digit remains."""\n'
            "    n = int(num)\n"
            "    if n <= 0:\n"
            "        return 0\n"
            "    return 1 + (n - 1) % 9\n",
            lambda low: bool(
                re.search(
                    r"\badd digits\b|"
                    r"\badd_digits\b|"
                    r"\bdigital root\b|"
                    r"\brepeatedly add(?: the)? digits\b",
                    low,
                )
            ),
            (((38,), 2), ((0,), 0), ((9,), 9), ((10,), 1)),
        ),
        T(
            "is_perfect_square",
            "def is_perfect_square(num):\n"
            '    """True if num is a perfect square (integer root)."""\n'
            "    n = int(num)\n"
            "    if n < 0:\n"
            "        return False\n"
            "    lo, hi = 0, n\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        sq = mid * mid\n"
            "        if sq == n:\n"
            "            return True\n"
            "        if sq < n:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bperfect square\b|"
                    r"\bis_perfect_square\b|"
                    r"\bperfect-square\b",
                    low,
                )
            ),
            (((16,), True), ((14,), False), ((1,), True), ((0,), True)),
        ),
        T(
            "can_win_nim",
            "def can_win_nim(n):\n"
            '    """True if the first player wins Nim with n stones (remove 1..3)."""\n'
            "    return int(n) % 4 != 0\n",
            lambda low: bool(
                re.search(
                    r"\bcan win nim\b|"
                    r"\bwin nim\b|"
                    r"\bnim game\b|"
                    r"\bcan_win_nim\b",
                    low,
                )
            ),
            (((4,), False), ((1,), True), ((2,), True), ((8,), False)),
        ),
        T(
            "to_hex",
            "def to_hex(num):\n"
            '    """Convert a 32-bit two\'s-complement integer to lowercase hex."""\n'
            "    n = int(num) & 0xFFFFFFFF\n"
            "    if n == 0:\n"
            "        return '0'\n"
            "    digits = '0123456789abcdef'\n"
            "    out = []\n"
            "    while n:\n"
            "        out.append(digits[n & 15])\n"
            "        n >>= 4\n"
            "    return ''.join(reversed(out))\n",
            lambda low: bool(
                re.search(
                    r"\bto hex\b|"
                    r"\bto_hex\b|"
                    r"\binteger to hex(?:adecimal)?\b|"
                    r"\bconvert.{0,20}hexadecimal\b",
                    low,
                )
            ),
            (((26,), "1a"), ((-1,), "ffffffff"), ((0,), "0")),
        ),
    ]
