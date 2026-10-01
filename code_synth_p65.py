"""Cycle 327: unused Easy — balanced string / parity transform /
reverse degree / closest person / number key / same digits after ops."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "is_balanced_digit_string",
            "def is_balanced_digit_string(num):\n"
            '    """Even-index digit sum equals odd-index digit sum (LeetCode 3340)."""\n'
            "    ev = od = 0\n"
            "    for i, ch in enumerate(num):\n"
            "        if i % 2 == 0:\n"
            "            ev += int(ch)\n"
            "        else:\n"
            "            od += int(ch)\n"
            "    return ev == od\n",
            lambda low: bool(
                re.search(
                    r"\bis_balanced_digit_string\b|"
                    r"\bcheck[_ ]balanced[_ ]string\b|"
                    r"\bbalanced[_ ]string\b|"
                    r"\bleetcode[_ ]3340\b",
                    low,
                )
            )
            and "parentheses" not in low
            and "valid_parentheses" not in low
            and "mountain" not in low,
            (
                (("1234",), False),
                (("24123",), True),
            ),
        ),
        T(
            "transform_array_by_parity",
            "def transform_array_by_parity(nums):\n"
            '    """Replace evens with 0 and odds with 1, then sort (LeetCode 3467)."""\n'
            "    return sorted(0 if x % 2 == 0 else 1 for x in nums)\n",
            lambda low: bool(
                re.search(
                    r"\btransform_array_by_parity\b|"
                    r"\btransform[_ ]array[_ ]by[_ ]parity\b|"
                    r"\bleetcode[_ ]3467\b",
                    low,
                )
            )
            and "sort_array_by_parity" not in low
            and "by_parity_ii" not in low,
            (
                (([4, 3, 2, 1],), [0, 0, 1, 1]),
                (([1, 5, 1, 4, 2],), [0, 0, 1, 1, 1]),
            ),
        ),
        T(
            "reverse_degree",
            "def reverse_degree(s):\n"
            '    """Sum (26 - (c - a)) * 1-based index over letters (LeetCode 3498)."""\n'
            "    total = 0\n"
            "    for i, ch in enumerate(s, 1):\n"
            "        total += (26 - (ord(ch) - 97)) * i\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\breverse_degree\b|"
                    r"\breverse[_ ]degree\b|"
                    r"\breverse[_ ]degree[_ ]of[_ ]a[_ ]string\b|"
                    r"\bleetcode[_ ]3498\b",
                    low,
                )
            )
            and "reverse_string" not in low
            and "reverse_vowels" not in low
            and "reverse_words" not in low,
            (
                (("abc",), 148),
                (("zaza",), 160),
            ),
        ),
        T(
            "find_closest_person",
            "def find_closest_person(x, y, z):\n"
            '    """Who reaches z first: person 1 at x or person 2 at y (LeetCode 3516)."""\n'
            "    d1 = abs(x - z)\n"
            "    d2 = abs(y - z)\n"
            "    if d1 < d2:\n"
            "        return 1\n"
            "    if d2 < d1:\n"
            "        return 2\n"
            "    return 0\n",
            lambda low: bool(
                re.search(
                    r"\bfind_closest_person\b|"
                    r"\bfind[_ ]closest[_ ]person\b|"
                    r"\bclosest[_ ]person\b|"
                    r"\bleetcode[_ ]3516\b",
                    low,
                )
            )
            and "closest_value" not in low
            and "bst" not in low,
            (
                ((2, 7, 4), 1),
                ((2, 5, 6), 2),
                ((1, 5, 3), 0),
            ),
        ),
        T(
            "generate_key",
            "def generate_key(num1, num2, num3):\n"
            '    """Digit-wise min of three 1–4 digit numbers, no leading zeros kept except 0 (LeetCode 3270)."""\n'
            "    a = f'{num1:04d}'\n"
            "    b = f'{num2:04d}'\n"
            "    c = f'{num3:04d}'\n"
            "    key = ''.join(min(x, y, z) for x, y, z in zip(a, b, c))\n"
            "    return int(key)\n",
            lambda low: bool(
                re.search(
                    r"\bgenerate_key\b|"
                    r"\bfind[_ ]the[_ ]key[_ ]of[_ ]the[_ ]numbers\b|"
                    r"\bkey[_ ]of[_ ]the[_ ]numbers\b|"
                    r"\bleetcode[_ ]3270\b",
                    low,
                )
            )
            and "ransom" not in low,
            (
                ((1, 10, 1000), 0),
                ((987, 879, 798), 777),
                ((1, 2, 3), 1),
            ),
        ),
        T(
            "has_same_digits",
            "def has_same_digits(s):\n"
            '    """Repeatedly replace with pairwise digit sums mod 10 until length 2 (LeetCode 3461)."""\n'
            "    digits = [int(ch) for ch in s]\n"
            "    while len(digits) > 2:\n"
            "        digits = [(digits[i] + digits[i + 1]) % 10 for i in range(len(digits) - 1)]\n"
            "    return digits[0] == digits[1]\n",
            lambda low: bool(
                re.search(
                    r"\bhas_same_digits\b|"
                    r"\bcheck[_ ]if[_ ]digits[_ ]are[_ ]equal\b|"
                    r"\bdigits[_ ]are[_ ]equal[_ ]in[_ ]string[_ ]after[_ ]operations\b|"
                    r"\bleetcode[_ ]3461\b",
                    low,
                )
            )
            and "add_digits" not in low
            and "clear_digits" not in low,
            (
                (("3902",), True),
                (("34789",), False),
            ),
        ),
    ]
