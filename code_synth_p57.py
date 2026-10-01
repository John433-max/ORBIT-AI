"""Cycle 319: equivalent string arrays / score of a string /
permutation difference / min ops divisible by three / sneaky numbers /
min element after digit-sum replace."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "array_strings_are_equal",
            "def array_strings_are_equal(word1, word2):\n"
            '    """True if concatenating word1 equals concatenating word2 (LeetCode 1662)."""\n'
            "    return ''.join(word1) == ''.join(word2)\n",
            lambda low: bool(
                re.search(
                    r"\b(check[_ ]if[_ ]two[_ ]string[_ ]arrays[_ ]are[_ ]equivalent|"
                    r"array[_ ]strings[_ ]are[_ ]equal|"
                    r"two[_ ]string[_ ]arrays[_ ]are[_ ]equivalent)\b",
                    low,
                )
            )
            and "anagram" not in low,
            (
                ((["ab", "c"], ["a", "bc"]), True),
                ((["a", "cb"], ["ab", "c"]), False),
                ((["abc", "d", "defg"], ["abcddefg"]), True),
            ),
        ),
        T(
            "score_of_string",
            "def score_of_string(s):\n"
            '    """Sum of abs ASCII diffs of adjacent chars (LeetCode 3110)."""\n'
            "    return sum(abs(ord(s[i]) - ord(s[i - 1])) for i in range(1, len(s)))\n",
            lambda low: bool(
                re.search(
                    r"\bscore[_ ]of[_ ](a[_ ])?string\b|"
                    r"\bscore_of_string\b",
                    low,
                )
            )
            and "parenthes" not in low,
            (
                (("hello",), 13),
                (("zaz",), 50),
            ),
        ),
        T(
            "permutation_difference",
            "def permutation_difference(s, t):\n"
            '    """Sum of index distances of each char in s vs permutation t (LeetCode 3146)."""\n'
            "    pos = {ch: i for i, ch in enumerate(t)}\n"
            "    return sum(abs(i - pos[ch]) for i, ch in enumerate(s))\n",
            lambda low: bool(
                re.search(
                    r"\bpermutation[_ ]difference\b|"
                    r"\bpermutation_difference\b",
                    low,
                )
            )
            and "next_permutation" not in low
            and "build_array" not in low,
            (
                (("abc", "bac"), 2),
                (("abcde", "edbac"), 12),
            ),
        ),
        T(
            "minimum_operations_divisible_by_three",
            "def minimum_operations_divisible_by_three(nums):\n"
            '    """Min increments/decrements so every value is divisible by 3 (LeetCode 3190)."""\n'
            "    return sum(1 for x in nums if x % 3 != 0)\n",
            lambda low: bool(
                re.search(
                    r"\bminimum[_ ]operations[_ ]to[_ ]make[_ ]all[_ ]elements[_ ]divisible[_ ]by[_ ]three\b|"
                    r"\bmin[_ ]operations[_ ]divisible[_ ]by[_ ]three\b|"
                    r"\bminimum_operations_divisible_by_three\b",
                    low,
                )
            )
            and "increasing" not in low,
            (
                (([1, 2, 3, 4],), 3),
                (([3, 6, 9],), 0),
            ),
        ),
        T(
            "get_sneaky_numbers",
            "def get_sneaky_numbers(nums):\n"
            '    """The two values that appear twice in 0..n-1 plus those two (LeetCode 3289)."""\n'
            "    seen = set()\n"
            "    out = []\n"
            "    for x in nums:\n"
            "        if x in seen:\n"
            "            out.append(x)\n"
            "        else:\n"
            "            seen.add(x)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\b(two[_ ]sneaky[_ ]numbers|get[_ ]sneaky[_ ]numbers|sneaky[_ ]numbers)\b",
                    low,
                )
            ),
            (
                (([0, 1, 1, 0],), [1, 0]),
                (([0, 3, 2, 1, 3, 2],), [3, 2]),
                (([7, 1, 5, 4, 3, 4, 6, 0, 9, 5, 8, 2],), [4, 5]),
            ),
        ),
        T(
            "min_element_after_digit_sum",
            "def min_element_after_digit_sum(nums):\n"
            '    """Replace each value with its digit sum; return the minimum (LeetCode 3300)."""\n'
            "    def digit_sum(x):\n"
            "        s = 0\n"
            "        while x:\n"
            "            s += x % 10\n"
            "            x //= 10\n"
            "        return s\n"
            "    return min(digit_sum(x) for x in nums)\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)?[_ ]element[_ ]after[_ ]replacement\b|"
                    r"\breplacement[_ ]with[_ ]digit[_ ]sum\b|"
                    r"\bmin_element_after_digit_sum\b",
                    low,
                )
            )
            and "difference_element" not in low,
            (
                (([10, 12, 13, 14],), 1),
                (([1, 2, 3, 4],), 1),
                (([999, 19, 199],), 10),
            ),
        ),
    ]
