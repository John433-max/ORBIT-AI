"""Cycle 517: zero-pad, even/odd split, adjacent collapse, spaces→underscores, list XOR, digits→int.

Matchers stay narrower than pad/string, sum-of-evens, digit-sum, and generic XOR.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "zero_pad",
            "def zero_pad(n, width):\n"
            '    """Left-pad the absolute value with zeros; keep a leading minus."""\n'
            "    sign = '-' if int(n) < 0 else ''\n"
            "    return sign + str(abs(int(n))).zfill(int(width))\n",
            lambda low: (
                "zero" in low
                and "pad" in low
                and "string" not in low
                and "left pad" not in low
                and "pad left" not in low
                and "right pad" not in low
            ),
            (
                ((42, 5), "00042"),
                ((-7, 3), "-007"),
                ((0, 2), "00"),
            ),
        ),
        T(
            "split_evens_odds",
            "def split_evens_odds(nums):\n"
            '    """Partition into even and odd values, preserving order."""\n'
            "    evens, odds = [], []\n"
            "    for x in nums:\n"
            "        (evens if int(x) % 2 == 0 else odds).append(x)\n"
            "    return evens, odds\n",
            lambda low: (
                "split" in low
                and "even" in low
                and "odd" in low
                and "sum" not in low
                and "product" not in low
                and "count" not in low
            ),
            (
                (([1, 2, 3, 4],), ([2, 4], [1, 3])),
                (([2, 4],), ([2, 4], [])),
                (([],), ([], [])),
            ),
        ),
        T(
            "remove_adjacent_duplicates",
            "def remove_adjacent_duplicates(s):\n"
            '    """Collapse runs of the same character to a single copy."""\n'
            "    out = []\n"
            "    for ch in s:\n"
            "        if not out or out[-1] != ch:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n",
            lambda low: (
                "adjacent" in low
                and "duplicate" in low
                and "list" not in low
                and "linked" not in low
            ),
            (
                (("aabbcca",), "abca"),
                (("abc",), "abc"),
                (("",), ""),
            ),
        ),
        T(
            "spaces_to_underscores",
            "def spaces_to_underscores(s):\n"
            '    """Replace each space with an underscore."""\n'
            "    return s.replace(' ', '_')\n",
            lambda low: (
                "space" in low
                and "underscore" in low
                and "snake" not in low
                and "camel" not in low
            ),
            (
                (("a b c",), "a_b_c"),
                (("nospace",), "nospace"),
                (("  ",), "__"),
            ),
        ),
        T(
            "xor_list",
            "def xor_list(nums):\n"
            '    """Bitwise XOR of every integer in the list."""\n'
            "    acc = 0\n"
            "    for x in nums:\n"
            "        acc ^= int(x)\n"
            "    return acc\n",
            lambda low: (
                "xor" in low
                and "list" in low
                and "string" not in low
                and "operation" not in low
            ),
            (
                (([1, 2, 3],), 0),
                (([7],), 7),
                (([],), 0),
            ),
        ),
        T(
            "digits_to_int",
            "def digits_to_int(digits):\n"
            '    """Interpret a digit sequence as a base-10 integer."""\n'
            "    n = 0\n"
            "    for d in digits:\n"
            "        n = n * 10 + int(d)\n"
            "    return n\n",
            lambda low: (
                "digit" in low
                and ("integer" in low or "int" in low)
                and "sum" not in low
                and "split" not in low
                and "count" not in low
                and "remove" not in low
                and "product" not in low
            ),
            (
                (([1, 2, 3],), 123),
                (([0, 4],), 4),
                (([],), 0),
            ),
        ),
    ]
