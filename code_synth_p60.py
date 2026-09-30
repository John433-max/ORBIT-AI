"""Cycle 322: faulty keyboard / take gifts / min common value /
remove trailing zeros / row with max ones / alternating digit sum."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "final_string",
            "def final_string(s):\n"
            '    """Type s; i reverses the current buffer (LeetCode 2810)."""\n'
            "    buf = []\n"
            "    for ch in s:\n"
            "        if ch == 'i':\n"
            "            buf.reverse()\n"
            "        else:\n"
            "            buf.append(ch)\n"
            "    return ''.join(buf)\n",
            lambda low: bool(
                re.search(
                    r"\bfinal_string\b|"
                    r"\bfaulty[_ ]keyboard\b|"
                    r"\bleetcode[_ ]2810\b",
                    low,
                )
            ),
            (
                (("string",), "rtsng"),
                (("poi",), "op"),
            ),
        ),
        T(
            "pick_gifts",
            "def pick_gifts(gifts, k):\n"
            '    """k times replace max pile with floor(sqrt) then sum (LeetCode 2558)."""\n'
            "    import math\n"
            "    gifts = list(gifts)\n"
            "    for _ in range(k):\n"
            "        i = max(range(len(gifts)), key=lambda j: gifts[j])\n"
            "        gifts[i] = int(math.isqrt(gifts[i]))\n"
            "    return sum(gifts)\n",
            lambda low: bool(
                re.search(
                    r"\bpick_gifts\b|"
                    r"\btake[_ ]gifts[_ ]from[_ ]the[_ ]richest[_ ]pile\b|"
                    r"\bleetcode[_ ]2558\b",
                    low,
                )
            ),
            (
                (([25, 64, 9, 4, 100], 4), 29),
                (([1, 1, 1, 1], 4), 4),
            ),
        ),
        T(
            "get_common",
            "def get_common(nums1, nums2):\n"
            '    """Minimum common value of two sorted arrays, else -1 (LeetCode 2540)."""\n'
            "    i = j = 0\n"
            "    while i < len(nums1) and j < len(nums2):\n"
            "        a, b = nums1[i], nums2[j]\n"
            "        if a == b:\n"
            "            return a\n"
            "        if a < b:\n"
            "            i += 1\n"
            "        else:\n"
            "            j += 1\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bget_common\b|"
                    r"\bminimum[_ ]common[_ ]value\b|"
                    r"\bleetcode[_ ]2540\b",
                    low,
                )
            )
            and "common_words" not in low,
            (
                (([1, 2, 3], [2, 4]), 2),
                (([1, 2, 3, 6], [2, 3, 4, 5]), 2),
            ),
        ),
        T(
            "remove_trailing_zeros",
            "def remove_trailing_zeros(num):\n"
            '    """Strip trailing zeros from a numeric string (LeetCode 2710)."""\n'
            "    return num.rstrip('0') or '0'\n",
            lambda low: bool(
                re.search(
                    r"\bremove_trailing_zeros\b|"
                    r"\bremove[_ ]trailing[_ ]zeros[_ ]from[_ ]a[_ ]string\b|"
                    r"\bleetcode[_ ]2710\b",
                    low,
                )
            )
            and "trailing_zeroes" not in low
            and "factorial" not in low,
            (
                (("51230100",), "512301"),
                (("123",), "123"),
            ),
        ),
        T(
            "row_and_maximum_ones",
            "def row_and_maximum_ones(mat):\n"
            '    """[row index, ones count] of the row with most 1s (LeetCode 2643)."""\n'
            "    best_i, best_c = 0, -1\n"
            "    for i, row in enumerate(mat):\n"
            "        c = sum(row)\n"
            "        if c > best_c:\n"
            "            best_i, best_c = i, c\n"
            "    return [best_i, best_c]\n",
            lambda low: bool(
                re.search(
                    r"\brow_and_maximum_ones\b|"
                    r"\brow[_ ]with[_ ]maximum[_ ]ones\b|"
                    r"\bleetcode[_ ]2643\b",
                    low,
                )
            ),
            (
                (([[0, 1], [1, 0]],), [0, 1]),
                (([[0, 0, 0], [0, 1, 1]],), [1, 2]),
            ),
        ),
        T(
            "alternate_digit_sum",
            "def alternate_digit_sum(n):\n"
            '    """Alternating + - digit sum from the left (LeetCode 2544)."""\n'
            "    s = str(n)\n"
            "    total = 0\n"
            "    sign = 1\n"
            "    for ch in s:\n"
            "        total += sign * int(ch)\n"
            "        sign = -sign\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\balternate_digit_sum\b|"
                    r"\balternating[_ ]digit[_ ]sum\b|"
                    r"\bleetcode[_ ]2544\b",
                    low,
                )
            )
            and "subtract_product" not in low,
            (
                ((521,), 4),
                ((111,), 1),
            ),
        ),
    ]
