"""Cycle 307: even-digit numbers / restore string / halves alike / water bottles / thousand sep / avg salary."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "numbers_with_even_digits",
            "def numbers_with_even_digits(nums):\n"
            '    """Count integers with an even number of digits (LeetCode 1295)."""\n'
            "    return sum(1 for x in nums if len(str(abs(int(x)))) % 2 == 0)\n",
            lambda low: bool(
                re.search(
                    r"\bnumbers[_ ]with[_ ]even[_ ]digits\b|"
                    r"\bnumbers_with_even_digits\b",
                    low,
                )
            ),
            (
                (([12, 345, 2, 6, 7896],), 2),
                (([555, 901, 482, 1771],), 1),
                (([1, 22, 333, 4444],), 2),
            ),
        ),
        T(
            "restore_string",
            "def restore_string(s, indices):\n"
            '    """Shuffle s so char i moves to indices[i] (LeetCode 1528)."""\n'
            "    out = [''] * len(s)\n"
            "    for ch, i in zip(s, indices):\n"
            "        out[i] = ch\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\brestore[_ ]string\b|"
                    r"\bshuffle string by indices\b|"
                    r"\brestore the string from indices\b",
                    low,
                )
            ),
            (
                (("codeleet", [4, 5, 6, 7, 0, 2, 1, 3]), "leetcode"),
                (("abc", [0, 1, 2]), "abc"),
                (("aiohn", [3, 1, 4, 2, 0]), "nihao"),
            ),
        ),
        T(
            "halves_are_alike",
            "def halves_are_alike(s):\n"
            '    """True if both halves have the same vowel count (LeetCode 1704)."""\n'
            "    vowels = set('aeiouAEIOU')\n"
            "    n = len(s) // 2\n"
            "    return sum(c in vowels for c in s[:n]) == sum(c in vowels for c in s[n:])\n",
            lambda low: bool(
                re.search(
                    r"\bhalves[_ ]are[_ ]alike\b|"
                    r"\bboth halves have the same number of vowels\b|"
                    r"\bdetermine if string halves are alike\b",
                    low,
                )
            ),
            (
                (("book",), True),
                (("textbook",), False),
                (("AbCdEfGh",), True),
            ),
        ),
        T(
            "num_water_bottles",
            "def num_water_bottles(num_bottles, num_exchange):\n"
            '    """Bottles drunk after exchanging empties (LeetCode 1518)."""\n'
            "    drunk = int(num_bottles)\n"
            "    empty = drunk\n"
            "    k = int(num_exchange)\n"
            "    while empty >= k:\n"
            "        extra = empty // k\n"
            "        drunk += extra\n"
            "        empty = empty % k + extra\n"
            "    return drunk\n",
            lambda low: bool(
                re.search(
                    r"\bnum[_ ]water[_ ]bottles\b|"
                    r"\bwater bottles\b|"
                    r"\bexchange empty bottles\b",
                    low,
                )
            ),
            (
                ((9, 3), 13),
                ((15, 4), 19),
                ((5, 5), 6),
            ),
        ),
        T(
            "thousand_separator",
            "def thousand_separator(n):\n"
            '    """Insert dots as thousand separators (LeetCode 1556)."""\n'
            "    s = str(int(n))\n"
            "    parts = []\n"
            "    while s:\n"
            "        parts.append(s[-3:])\n"
            "        s = s[:-3]\n"
            "    return '.'.join(reversed(parts))\n",
            lambda low: bool(
                re.search(
                    r"\bthousand[_ ]separator\b|"
                    r"\bthousand-separator\b|"
                    r"\binsert thousand separators\b",
                    low,
                )
            ),
            (
                ((987,), "987"),
                ((1234,), "1.234"),
                ((123456789,), "123.456.789"),
            ),
        ),
        T(
            "average_salary_excluding",
            "def average_salary_excluding(salary):\n"
            '    """Average salary excluding min and max (LeetCode 1491)."""\n'
            "    return (sum(salary) - min(salary) - max(salary)) / (len(salary) - 2)\n",
            lambda low: bool(
                re.search(
                    r"\baverage[_ ]salary[_ ]excluding\b|"
                    r"\baverage salary excluding the minimum and maximum\b|"
                    r"\baverage salary excluding min and max\b",
                    low,
                )
            ),
            (
                (([4000, 3000, 1000, 2000],), 2500.0),
                (([1000, 2000, 3000],), 2000.0),
                (([8000, 9000, 2000, 3000, 6000, 1000],), 4750.0),
            ),
        ),
    ]
