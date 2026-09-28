"""Cycle 273: additional verified Python templates (pack 15)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "number_of_steps",
            "def number_of_steps(num):\n"
            '    """Steps to reduce num to zero: even /2, odd -1."""\n'
            "    n = int(num)\n"
            "    steps = 0\n"
            "    while n > 0:\n"
            "        n = n // 2 if n % 2 == 0 else n - 1\n"
            "        steps += 1\n"
            "    return steps\n",
            lambda low: bool(
                re.search(
                    r"\bnumber of steps to reduce\b|"
                    r"\bnumber_of_steps\b|"
                    r"\breduce (?:a |the )?number to zero\b|"
                    r"\bsteps to reduce .{0,20}to zero\b",
                    low,
                )
            ),
            (((14,), 6), ((8,), 4), ((123,), 12)),
        ),
        T(
            "max_number_of_balloons",
            "def max_number_of_balloons(text):\n"
            '    """Max times the word balloon can be formed from text."""\n'
            "    from collections import Counter\n"
            "    c = Counter(str(text))\n"
            "    return min(c.get('b', 0), c.get('a', 0), c.get('l', 0) // 2, c.get('o', 0) // 2, c.get('n', 0))\n",
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)? number of balloons\b|"
                    r"\bmax_number_of_balloons\b|"
                    r"\bmaximum number of times you can form .{0,8}balloon\b",
                    low,
                )
            ),
            ((("nlaebolko",), 1), (("loonbalxballpoon",), 2), (("leetcode",), 0)),
        ),
        T(
            "check_if_n_and_double_exist",
            "def check_if_n_and_double_exist(arr):\n"
            '    """True if some i, j (i != j) satisfy arr[i] == 2 * arr[j]."""\n'
            "    seen = set()\n"
            "    for x in arr:\n"
            "        x = int(x)\n"
            "        if 2 * x in seen or (x % 2 == 0 and x // 2 in seen):\n"
            "            return True\n"
            "        seen.add(x)\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bcheck if n and (?:its )?double exist\b|"
                    r"\bcheck_if_n_and_double_exist\b|"
                    r"\bn and (?:its )?double exist\b",
                    low,
                )
            )
            and "smaller than" not in low,
            (([[10, 2, 5, 3],], True), ([[3, 1, 7, 11],], False), ([[7, 1, 14, 11],], True)),
        ),
        T(
            "kth_missing_positive",
            "def kth_missing_positive(arr, k):\n"
            '    """Return the k-th positive integer missing from a sorted unique array."""\n'
            "    a = [int(x) for x in arr]\n"
            "    k = int(k)\n"
            "    missing = 0\n"
            "    expect = 1\n"
            "    i = 0\n"
            "    while True:\n"
            "        if i < len(a) and a[i] == expect:\n"
            "            i += 1\n"
            "        else:\n"
            "            missing += 1\n"
            "            if missing == k:\n"
            "                return expect\n"
            "        expect += 1\n",
            lambda low: bool(
                re.search(
                    r"\bkth missing positive\b|"
                    r"\bk-?th missing positive\b|"
                    r"\bkth_missing_positive\b|"
                    r"\bk-?th positive integer missing\b",
                    low,
                )
            )
            and "first missing" not in low,
            (([[2, 3, 4, 7, 11], 5], 9), ([[1, 2, 3, 4], 2], 6)),
        ),
        T(
            "dest_city",
            "def dest_city(paths):\n"
            '    """Destination city: appears as dest never as origin."""\n'
            "    origins = {a for a, _b in paths}\n"
            "    for _a, b in paths:\n"
            "        if b not in origins:\n"
            "            return b\n"
            "    return ''\n",
            lambda low: bool(
                re.search(
                    r"\bdest(?:ination)? city\b|"
                    r"\bdest_city\b|"
                    r"\bdestination city of (?:the )?paths?\b",
                    low,
                )
            ),
            (
                (([["London", "New York"], ["New York", "Lima"], ["Lima", "Sao Paulo"]],), "Sao Paulo"),
                (([["B", "C"], ["D", "B"], ["C", "A"]],), "A"),
            ),
        ),
        T(
            "sum_odd_length_subarrays",
            "def sum_odd_length_subarrays(arr):\n"
            '    """Sum of all odd-length subarrays of arr."""\n'
            "    a = [int(x) for x in arr]\n"
            "    n = len(a)\n"
            "    total = 0\n"
            "    for i, v in enumerate(a):\n"
            "        left, right = i + 1, n - i\n"
            "        total += v * ((left * right + 1) // 2)\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bsum of (?:all )?odd[- ]length subarrays\b|"
                    r"\bsum_odd_length_subarrays\b|"
                    r"\bodd[- ]length subarrays\b",
                    low,
                )
            )
            and "max_product" not in low
            and "maximum product" not in low,
            (([[1, 4, 2, 5, 3],], 58), ([[1, 2],], 3), ([[10, 11, 12],], 66)),
        ),
    ]
