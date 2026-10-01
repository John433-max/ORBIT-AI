"""Cycle 331: unused Easy — key of numbers / missing+repeated /
digits that divide / concatenation value / encrypted ints / max-freq."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "generate_key",
            "def generate_key(num1, num2, num3):\n"
            '    """Min digit at each place of 3 ints, then form the number (LeetCode 3270)."""\n'
            "    key = 0\n"
            "    place = 1\n"
            "    for _ in range(4):\n"
            "        d = min(num1 % 10, num2 % 10, num3 % 10)\n"
            "        key += d * place\n"
            "        place *= 10\n"
            "        num1 //= 10\n"
            "        num2 //= 10\n"
            "        num3 //= 10\n"
            "    return key\n",
            lambda low: bool(
                re.search(
                    r"\bgenerate_key\b|"
                    r"\bfind[_ ]the[_ ]key[_ ]of[_ ]the[_ ]numbers\b|"
                    r"\bkey[_ ]of[_ ]the[_ ]numbers\b|"
                    r"\bleetcode[_ ]3270\b",
                    low,
                )
            ),
            (
                ((1, 10, 1000), 0),
                ((987, 879, 798), 777),
                ((1, 2, 3), 1),
            ),
        ),
        T(
            "find_missing_and_repeated_values",
            "def find_missing_and_repeated_values(grid):\n"
            '    """[repeated, missing] in n×n grid of 1..n² (LeetCode 2965)."""\n'
            "    n = len(grid)\n"
            "    seen = [0] * (n * n + 1)\n"
            "    for row in grid:\n"
            "        for x in row:\n"
            "            seen[x] += 1\n"
            "    a = b = 0\n"
            "    for i in range(1, n * n + 1):\n"
            "        if seen[i] == 2:\n"
            "            a = i\n"
            "        elif seen[i] == 0:\n"
            "            b = i\n"
            "    return [a, b]\n",
            lambda low: bool(
                re.search(
                    r"\bfind_missing_and_repeated_values\b|"
                    r"\bfind[_ ]missing[_ ]and[_ ]repeated[_ ]values\b|"
                    r"\bmissing[_ ]and[_ ]repeated[_ ]values\b|"
                    r"\bleetcode[_ ]2965\b",
                    low,
                )
            )
            and "first missing" not in low,
            (
                (([[1, 3], [2, 2]],), [2, 4]),
                (([[9, 1, 7], [8, 9, 2], [3, 4, 6]],), [9, 5]),
            ),
        ),
        T(
            "count_digits",
            "def count_digits(num):\n"
            '    """How many digits of num divide num (LeetCode 2520)."""\n'
            "    n = num\n"
            "    c = 0\n"
            "    while n:\n"
            "        d = n % 10\n"
            "        if d and num % d == 0:\n"
            "            c += 1\n"
            "        n //= 10\n"
            "    return c\n",
            lambda low: bool(
                re.search(
                    r"\bcount_digits\b|"
                    r"\bcount[_ ]the[_ ]digits[_ ]that[_ ]divide\b|"
                    r"\bdigits[_ ]that[_ ]divide[_ ]the[_ ]number\b|"
                    r"\bleetcode[_ ]2520\b",
                    low,
                )
            )
            and "count_and_say" not in low
            and "count bits" not in low,
            (
                ((7,), 1),
                ((121,), 2),
                ((1248,), 4),
            ),
        ),
        T(
            "find_the_array_conc_val",
            "def find_the_array_conc_val(nums):\n"
            '    """Sum concatenation of symmetric pairs (LeetCode 2562)."""\n'
            "    i, j = 0, len(nums) - 1\n"
            "    total = 0\n"
            "    while i < j:\n"
            "        total += int(str(nums[i]) + str(nums[j]))\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    if i == j:\n"
            "        total += nums[i]\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bfind_the_array_conc_val\b|"
                    r"\bfind[_ ]the[_ ]array[_ ]concatenation[_ ]value\b|"
                    r"\barray[_ ]concatenation[_ ]value\b|"
                    r"\bleetcode[_ ]2562\b",
                    low,
                )
            ),
            (
                (([7, 52, 2, 4],), 596),
                (([5, 14, 13, 8, 12],), 673),
            ),
        ),
        T(
            "sum_of_encrypted_int",
            "def sum_of_encrypted_int(nums):\n"
            '    """Replace each int by its max digit repeated, then sum (LeetCode 3079)."""\n'
            "    total = 0\n"
            "    for x in nums:\n"
            "        s = str(x)\n"
            "        total += int(max(s) * len(s))\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bsum_of_encrypted_int\b|"
                    r"\bsum[_ ]of[_ ]encrypted[_ ]integers\b|"
                    r"\bencrypt[_ ]and[_ ]sum\b|"
                    r"\bleetcode[_ ]3079\b",
                    low,
                )
            )
            and "get_encrypted_string" not in low
            and "encrypted string" not in low,
            (
                (([1, 2, 3],), 6),
                (([10, 21, 31],), 66),
            ),
        ),
        T(
            "max_frequency_elements",
            "def max_frequency_elements(nums):\n"
            '    """Total count of elements that share the maximum frequency (LeetCode 3005)."""\n'
            "    freq = {}\n"
            "    for x in nums:\n"
            "        freq[x] = freq.get(x, 0) + 1\n"
            "    m = max(freq.values())\n"
            "    return sum(v for v in freq.values() if v == m)\n",
            lambda low: bool(
                re.search(
                    r"\bmax_frequency_elements\b|"
                    r"\bcount[_ ]elements[_ ]with[_ ]maximum[_ ]frequency\b|"
                    r"\belements[_ ]with[_ ]maximum[_ ]frequency\b|"
                    r"\bleetcode[_ ]3005\b",
                    low,
                )
            )
            and "most_frequent_even" not in low,
            (
                (([1, 2, 2, 3, 1, 4],), 4),
                (([1, 2, 3, 4, 5],), 5),
            ),
        ),
    ]
