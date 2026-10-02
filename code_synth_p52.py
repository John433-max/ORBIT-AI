"""Cycle 314: date-to-binary / changing keys / symmetric integers /
patterns as substrings / pivot integer / ascending numbers in sentence."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "convert_date_to_binary",
            "def convert_date_to_binary(date):\n"
            '    """YYYY-MM-DD parts as binary without 0b prefix (LeetCode 3280)."""\n'
            "    return '-'.join(bin(int(p))[2:] for p in date.split('-'))\n"
            "\n"
            "def date_to_binary(date):\n"
            "    return convert_date_to_binary(date)\n",
            lambda low: bool(
                re.search(
                    r"\bconvert[_ ]date[_ ]to[_ ](?:the[_ ])?binary\b|"
                    r"\bconvert_date_to_binary\b",
                    low,
                )
            ),
            (
                (("2080-02-29",), "100000100000-10-11101"),
                (("1900-01-01",), "11101101100-1-1"),
                (("2000-12-31",), "11111010000-1100-11111"),
            ),
        ),
        T(
            "count_changing_keys",
            "def count_changing_keys(s):\n"
            '    """Count times consecutive letters change ignoring case (LeetCode 3019)."""\n'
            "    s = s.lower()\n"
            "    return sum(s[i] != s[i - 1] for i in range(1, len(s)))\n",
            lambda low: bool(
                re.search(
                    r"\b(?:count|number)[_ ](?:of[_ ])?changing[_ ]keys\b|"
                    r"\bcount_changing_keys\b",
                    low,
                )
            ),
            (
                (("aAbBcC",), 2),
                (("AaAaAaaA",), 0),
                (("aBc",), 2),
            ),
        ),
        T(
            "count_symmetric_integers",
            "def count_symmetric_integers(low, high):\n"
            '    """Count even-digit nums in [low, high] with equal half-sums (LeetCode 2843)."""\n'
            "    c = 0\n"
            "    for n in range(low, high + 1):\n"
            "        s = str(n)\n"
            "        m = len(s)\n"
            "        if m % 2:\n"
            "            continue\n"
            "        h = m // 2\n"
            "        if sum(map(int, s[:h])) == sum(map(int, s[h:])):\n"
            "            c += 1\n"
            "    return c\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]symmetric[_ ]integers\b|"
                    r"\bcount_symmetric_integers\b",
                    low,
                )
            ),
            (
                ((1, 100), 9),
                ((1200, 1230), 4),
                ((1, 1), 0),
            ),
        ),
        T(
            "num_of_strings",
            "def num_of_strings(patterns, word):\n"
            '    """Count patterns that occur as a substring of word (LeetCode 1967)."""\n'
            "    return sum(1 for p in patterns if p in word)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]of[_ ]strings[_ ](?:that[_ ])?appear[_ ]as[_ ]substrings?\b|"
                    r"\bnum_of_strings\b",
                    low,
                )
            ),
            (
                ((["a", "abc", "bc", "d"], "abc"), 3),
                ((["a", "b", "c"], "aaaaabbbbb"), 2),
                ((["a", "a", "a"], "ab"), 3),
            ),
        ),
        T(
            "pivot_integer",
            "def pivot_integer(n):\n"
            '    """x in 1..n with sum(1..x)==sum(x..n), else -1 (LeetCode 2485)."""\n'
            "    total = n * (n + 1) // 2\n"
            "    x = int(total ** 0.5)\n"
            "    if x * x == total:\n"
            "        return x\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\b(?:find[_ ])?(?:the[_ ])?pivot[_ ]integer\b|"
                    r"\bpivot_integer\b",
                    low,
                )
            ),
            (
                ((8,), 6),
                ((1,), 1),
                ((4,), -1),
            ),
        ),
        T(
            "are_numbers_ascending",
            "def are_numbers_ascending(s):\n"
            '    """True if space-separated integers in s are strictly increasing (LeetCode 2042)."""\n'
            "    nums = [int(t) for t in s.split() if t.isdigit()]\n"
            "    return all(nums[i] > nums[i - 1] for i in range(1, len(nums)))\n",
            lambda low: bool(
                re.search(
                    r"\b(?:check[_ ]if[_ ])?numbers[_ ]are[_ ]ascending(?:[_ ]in[_ ]a[_ ]sentence)?\b|"
                    r"\bare_numbers_ascending\b",
                    low,
                )
            ),
            (
                (("1 box has 3 blue 4 red 6 green and 12 yellow marbles",), True),
                (("hello world 5 x 5",), False),
                (("sunset is at 7 51 pm overnight lows will be in the low 50 and 60 s",), False),
            ),
        ),
    ]
