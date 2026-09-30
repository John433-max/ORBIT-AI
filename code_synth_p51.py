"""Cycle 313: largest odd substring / count ops to zero / keep-multiply-by-two /
count prefixes / digits that divide n / separate digits."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "largest_odd_number",
            "def largest_odd_number(num):\n"
            '    """Largest-valued odd-digit prefix of num, else empty (LeetCode 1903)."""\n'
            "    for i in range(len(num) - 1, -1, -1):\n"
            "        if int(num[i]) % 2 == 1:\n"
            "            return num[: i + 1]\n"
            "    return ''\n",
            lambda low: bool(
                re.search(
                    r"\blargest[_ ]odd[_ ]number(?:[_ ]in[_ ](?:the[_ ])?string)?\b|"
                    r"\blargest_odd_number\b",
                    low,
                )
            ),
            (
                (("52",), "5"),
                (("4206",), ""),
                (("35427",), "35427"),
            ),
        ),
        T(
            "count_operations",
            "def count_operations(num1, num2):\n"
            '    """Ops of subtracting min from max until a value is 0 (LeetCode 2169)."""\n'
            "    ops = 0\n"
            "    while num1 and num2:\n"
            "        if num1 >= num2:\n"
            "            ops += num1 // num2\n"
            "            num1 %= num2\n"
            "        else:\n"
            "            ops += num2 // num1\n"
            "            num2 %= num1\n"
            "    return ops\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]operations[_ ]to[_ ]obtain[_ ]zero\b|"
                    r"\bcount_operations\b",
                    low,
                )
            ),
            (
                ((2, 3), 3),
                ((10, 10), 1),
                ((1, 0), 0),
            ),
        ),
        T(
            "find_final_value",
            "def find_final_value(nums, original):\n"
            '    """Keep multiplying original by 2 while it is in nums (LeetCode 2154)."""\n'
            "    seen = set(nums)\n"
            "    while original in seen:\n"
            "        original *= 2\n"
            "    return original\n",
            lambda low: bool(
                re.search(
                    r"\bkeep[_ ]multiplying[_ ]found[_ ]values[_ ]by[_ ]two\b|"
                    r"\bfind[_ ]final[_ ]value\b|"
                    r"\bfind_final_value\b",
                    low,
                )
            ),
            (
                (([5, 3, 6, 1, 12], 3), 24),
                (([2, 7, 9], 4), 4),
                (([8, 4, 2], 2), 16),
            ),
        ),
        T(
            "count_prefixes",
            "def count_prefixes(words, s):\n"
            '    """Count words that are prefixes of s (LeetCode 2255)."""\n'
            "    return sum(1 for w in words if s.startswith(w))\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]prefixes[_ ]of[_ ]a[_ ]given[_ ]string\b|"
                    r"\bcount_prefixes\b",
                    low,
                )
            ),
            (
                ((["a", "b", "c", "ab", "bc", "abc"], "abc"), 3),
                ((["a", "a"], "aa"), 2),
                ((["xyz"], "abc"), 0),
            ),
        ),
        T(
            "count_digits",
            "def count_digits(num):\n"
            '    """Count digits of num that divide num (LeetCode 2520)."""\n'
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
                    r"\bcount[_ ]the[_ ]digits[_ ]that[_ ]divide[_ ](?:a[_ ])?number\b|"
                    r"\bcount_digits\b",
                    low,
                )
            ),
            (
                ((7,), 1),
                ((121,), 2),
                ((1248,), 4),
            ),
        ),
        T(
            "separate_digits",
            "def separate_digits(nums):\n"
            '    """Concatenate decimal digits of each integer (LeetCode 2553)."""\n'
            "    out = []\n"
            "    for n in nums:\n"
            "        for ch in str(n):\n"
            "            out.append(int(ch))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bseparate[_ ]the[_ ]digits[_ ]in[_ ]an[_ ]array\b|"
                    r"\bseparate_digits\b",
                    low,
                )
            ),
            (
                (([13, 25, 83, 77],), [1, 3, 2, 5, 8, 3, 7, 7]),
                (([7, 1, 3, 9],), [7, 1, 3, 9]),
                (([10],), [1, 0]),
            ),
        ),
    ]
