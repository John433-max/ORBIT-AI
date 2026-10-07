"""Cycle 500: natural-language coding misses.

LeetCode 1523 / 1859 / 1748 / 1662 / 1528 / 1502. Matchers stay off
three-consecutive-odds, unique-occurrences, and string rotations.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_odds",
            "def count_odds(low, high):\n"
            '    """Count odd integers in the inclusive range [low, high]."""\n'
            "    low, high = int(low), int(high)\n"
            "    if high < low:\n"
            "        return 0\n"
            "    return (high + 1) // 2 - low // 2\n",
            lambda low: (
                "odd" in low
                and ("range" in low or "between" in low or "interval" in low)
                and "consecutive" not in low
                and "product" not in low
            ),
            (
                ((3, 7), 3),
                ((8, 10), 1),
                ((1, 1), 1),
            ),
        ),
        T(
            "sort_sentence",
            "def sort_sentence(s):\n"
            '    """Reorder a shuffled sentence whose words end with 1-based indices."""\n'
            "    parts = str(s).split()\n"
            "    ordered = [None] * len(parts)\n"
            "    for word in parts:\n"
            "        ordered[int(word[-1]) - 1] = word[:-1]\n"
            "    return \" \".join(ordered)\n",
            lambda low: (
                "sentence" in low
                and ("numbered" in low or "shuffled sentence" in low or "sort" in low)
                and "anagram" not in low
            ),
            (
                (("is2 sentence4 This1 a3",), "This is a sentence"),
                (("Myself2 Me1 I4 and3",), "Me Myself and I"),
            ),
        ),
        T(
            "sum_of_unique",
            "def sum_of_unique(nums):\n"
            '    """Sum values that appear exactly once."""\n'
            "    from collections import Counter\n"
            "    counts = Counter(nums)\n"
            "    return sum(v for v, c in counts.items() if c == 1)\n",
            lambda low: (
                "unique" in low
                and "sum" in low
                and "occurrence" not in low
                and "zero" not in low
                and "character" not in low
            ),
            (
                (([1, 2, 3, 2],), 4),
                (([1, 1, 1, 1],), 0),
                (([1, 2, 3],), 6),
            ),
        ),
        T(
            "array_strings_are_equal",
            "def array_strings_are_equal(word1, word2):\n"
            '    """True when two string arrays concatenate to the same text."""\n'
            "    return \"\".join(word1) == \"\".join(word2)\n",
            lambda low: (
                "equivalent" in low
                and "string" in low
                and "array" in low
            ),
            (
                ((["ab", "c"], ["a", "bc"]), True),
                ((["a", "cb"], ["ab", "c"]), False),
            ),
        ),
        T(
            "restore_string",
            "def restore_string(s, indices):\n"
            '    """Place each character at the given index (LeetCode 1528)."""\n'
            "    out = [\"\"] * len(indices)\n"
            "    for ch, i in zip(s, indices):\n"
            "        out[i] = ch\n"
            "    return \"\".join(out)\n",
            lambda low: (
                (
                    "restore" in low and "string" in low
                )
                or (
                    "shuffle" in low
                    and "string" in low
                    and ("indic" in low or "index" in low)
                )
            ) and "ip" not in low,
            (
                (("codeleet", [4, 5, 6, 7, 0, 2, 1, 3]), "leetcode"),
                (("abc", [0, 1, 2]), "abc"),
            ),
        ),
        T(
            "can_make_arithmetic_progression",
            "def can_make_arithmetic_progression(arr):\n"
            '    """True when arr can be rearranged into an arithmetic progression."""\n'
            "    vals = sorted(arr)\n"
            "    if len(vals) < 2:\n"
            "        return True\n"
            "    step = vals[1] - vals[0]\n"
            "    return all(vals[i] - vals[i - 1] == step for i in range(2, len(vals)))\n",
            lambda low: (
                "arithmetic" in low
                and "progression" in low
            ),
            (
                (([3, 5, 1],), True),
                (([1, 2, 4],), False),
            ),
        ),
    ]
