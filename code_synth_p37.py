"""Cycle 298: maximum 69 / equivalent string arrays / odds in interval / decode XOR / sum unique / max units."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "maximum_69_number",
            "def maximum_69_number(num):\n"
            '    """Change the first 6 to 9 for the max number (LeetCode 1323)."""\n'
            "    s = list(str(num))\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch == '6':\n"
            "            s[i] = '9'\n"
            "            break\n"
            "    return int(''.join(s))\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum[_ ]69[_ ]number\b|"
                    r"\bmaximum 69 number\b|"
                    r"\bchange (?:the )?first 6 to 9\b",
                    low,
                )
            ),
            (
                ((9669,), 9969),
                ((9996,), 9999),
                ((9999,), 9999),
            ),
        ),
        T(
            "array_strings_are_equal",
            "def array_strings_are_equal(word1, word2):\n"
            '    """Whether two string arrays concatenate to the same string (LeetCode 1662)."""\n'
            "    return ''.join(word1) == ''.join(word2)\n",
            lambda low: bool(
                re.search(
                    r"\barray[_ ]strings[_ ]are[_ ]equal\b|"
                    r"\bcheck if two string arrays are equivalent\b|"
                    r"\btwo string arrays are equivalent\b",
                    low,
                )
            ),
            (
                ((["ab", "c"], ["a", "bc"]), True),
                ((["a", "cb"], ["ab", "c"]), False),
                ((["abc", "d", "defg"], ["abcddefg"]), True),
            ),
        ),
        T(
            "count_odds",
            "def count_odds(low, high):\n"
            '    """Count odd integers in the closed interval (LeetCode 1523)."""\n'
            "    return (high + 1) // 2 - low // 2\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]odds\b|"
                    r"\bcount odd numbers? in (?:an? )?(?:interval|range)\b|"
                    r"\bodds? in (?:a )?closed interval\b",
                    low,
                )
            ),
            (
                ((3, 7), 3),
                ((8, 10), 1),
                ((1, 1), 1),
            ),
        ),
        T(
            "decode_xored_array",
            "def decode_xored_array(encoded, first):\n"
            '    """Decode XOR-encoded array given first value (LeetCode 1720)."""\n'
            "    out = [first]\n"
            "    for x in encoded:\n"
            "        out.append(out[-1] ^ x)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bdecode[_ ]xored[_ ]array\b|"
                    r"\bdecode (?:an? )?xor(?:ed)? array\b|"
                    r"\bxor encoded array\b",
                    low,
                )
            ),
            (
                (([1, 2, 3], 1), [1, 0, 2, 1]),
                (([6, 2, 7, 3], 4), [4, 2, 0, 7, 4]),
                (([0], 1), [1, 1]),
            ),
        ),
        T(
            "sum_of_unique",
            "def sum_of_unique(nums):\n"
            '    """Sum of elements that appear exactly once (LeetCode 1748)."""\n'
            "    from collections import Counter\n"
            "    c = Counter(nums)\n"
            "    return sum(n for n, k in c.items() if k == 1)\n",
            lambda low: bool(
                re.search(
                    r"\bsum[_ ]of[_ ]unique\b|"
                    r"\bsum of unique elements\b|"
                    r"\bsum elements that appear exactly once\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 2],), 4),
                (([1, 1, 1, 1, 1],), 0),
                (([1, 2, 3, 4, 5],), 15),
            ),
        ),
        T(
            "max_units_on_truck",
            "def max_units_on_truck(box_types, truck_size):\n"
            '    """Max units that fit on a truck (LeetCode 1710)."""\n'
            "    box_types = sorted(box_types, key=lambda b: -b[1])\n"
            "    units = 0\n"
            "    left = truck_size\n"
            "    for count, per in box_types:\n"
            "        take = count if count < left else left\n"
            "        units += take * per\n"
            "        left -= take\n"
            "        if left == 0:\n"
            "            break\n"
            "    return units\n",
            lambda low: bool(
                re.search(
                    r"\bmax[_ ]units[_ ]on[_ ]truck\b|"
                    r"\bmaximum units on a truck\b|"
                    r"\bmax units that fit on a truck\b",
                    low,
                )
            ),
            (
                (([[1, 3], [2, 2], [3, 1]], 4), 8),
                (([[5, 10], [2, 5], [4, 7], [3, 9]], 10), 91),
                (([[1, 3]], 1), 3),
            ),
        ),
    ]
