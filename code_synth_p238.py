"""Cycle 526: drop-n, elementwise squares, sort-by-length, symmetric difference, replace-all, acronym.

These returned NotImplemented drafts or were stolen by drop_first, sum_of_squares,
sort_list, or list_difference. This pack loads first so the specific phrases win.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "drop_n",
            "def drop_n(items, n):\n"
            '    """Drop the first n items. n <= 0 returns a copy."""\n'
            "    items = list(items)\n"
            "    n = int(n)\n"
            "    if n <= 0:\n"
            "        return items\n"
            "    return items[n:]\n",
            lambda low: "drop" in low and "first n" in low and "last" not in low,
            (
                (([1, 2, 3, 4], 2), [3, 4]),
                (([1, 2], 0), [1, 2]),
                (([1], 5), []),
            ),
        ),
        T(
            "square_elements",
            "def square_elements(nums):\n"
            '    """Square each number. Does not sum them."""\n'
            "    return [x * x for x in nums]\n",
            lambda low: (
                ("squares a list" in low or "square each" in low or "squares each" in low)
                and "sum" not in low
                and "magic" not in low
            ),
            (
                (([1, 2, 3],), [1, 4, 9]),
                (([],), []),
                (([-2],), [4]),
            ),
        ),
        T(
            "sort_by_length",
            "def sort_by_length(items):\n"
            '    """Sort strings by length, keeping the original order on ties."""\n'
            "    return sorted(items, key=len)\n",
            lambda low: (
                ("by length" in low or "string length" in low)
                and "sort" in low
                and "index" not in low
            ),
            (
                ((["bb", "a", "ccc"],), ["a", "bb", "ccc"]),
                ((["aa", "b"],), ["b", "aa"]),
                (([],), []),
            ),
        ),
        T(
            "symmetric_difference",
            "def symmetric_difference(a, b):\n"
            '    """Items in exactly one of the lists, a then b, order preserved."""\n'
            "    sb = set(b)\n"
            "    sa = set(a)\n"
            "    out = [x for x in a if x not in sb]\n"
            "    out.extend(x for x in b if x not in sa)\n"
            "    return out\n",
            lambda low: "symmetric" in low and "difference" in low,
            (
                (([1, 2, 3], [2, 3, 4]), [1, 4]),
                (([], []), []),
                (([1], [1]), []),
            ),
        ),
        T(
            "replace_all",
            "def replace_all(s, old, new):\n"
            '    """Replace every occurrence of old with new."""\n'
            "    return str(s).replace(old, new)\n",
            lambda low: (
                ("replace all" in low or "replaces all" in low or "replaces a substring" in low)
                and "tab" not in low
                and "question mark" not in low
                and "1576" not in low
            ),
            (
                (("a-b-a", "-", "_"), "a_b_a"),
                (("aaa", "a", "b"), "bbb"),
                (("hi", "x", "y"), "hi"),
            ),
        ),
        T(
            "acronym",
            "def acronym(phrase):\n"
            '    """Initials of each whitespace-separated word, uppercased."""\n'
            "    parts = str(phrase).split()\n"
            "    return \"\".join(p[0].upper() for p in parts if p)\n",
            lambda low: ("acronym" in low or "initials of a name" in low or "returns initials" in low)
            and "leetcode" not in low,
            (
                (("portable network graphics",), "PNG"),
                (("a",), "A"),
                (("",), ""),
            ),
        ),
    ]
