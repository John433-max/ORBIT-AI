"""Cycle 391: Easy prompts still absent from the template index.

LeetCode 459, 566, 598, 599, 717, and 3843 were not referenced by any pack.
Matchers stay ID- or title-specific so substring, reshape, and index-sum
prompts do not steal longest-common / matrix-search / two-sum templates.
Loaded before p111.

Sources:
- LeetCode 459 Repeated Substring Pattern (classic KMP/string doubling).
- LeetCode 566 Reshape the Matrix.
- LeetCode 598 Range Addition II (min-ops rectangle).
- LeetCode 599 Minimum Index Sum of Two Lists.
- LeetCode 717 1-bit and 2-bit Characters.
- LeetCode 3843 First Element with Unique Frequency (doocs wiki, 2026-09-12):
  leftmost value whose frequency is unique, else -1. Examples
  [20,10,30,30] -> 30, [20,20,10,30,30,30] -> 20, [10,10,20,20] -> -1.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "repeated_substring_pattern",
            "def repeated_substring_pattern(s):\n"
            '    """True if s is a repeated concatenation of a proper substring (LeetCode 459)."""\n'
            "    s = str(s)\n"
            "    return s in (s + s)[1:-1]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 459\b|"
                    r"\brepeated substring pattern\b",
                    low,
                )
            ),
            (
                (("abab",), True),
                (("aba",), False),
                (("abcabcabcabc",), True),
            ),
        ),
        T(
            "matrix_reshape",
            "def matrix_reshape(mat, r, c):\n"
            '    """Reshape mat to r x c, or return mat if the size differs (LeetCode 566)."""\n'
            "    flat = [x for row in mat for x in row]\n"
            "    r, c = int(r), int(c)\n"
            "    if r * c != len(flat):\n"
            "        return [list(row) for row in mat]\n"
            "    return [flat[i * c:(i + 1) * c] for i in range(r)]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 566\b|"
                    r"\breshape the matrix\b|"
                    r"\bmatrix reshape\b",
                    low,
                )
            ),
            (
                (([[1, 2], [3, 4]], 1, 4), [[1, 2, 3, 4]]),
                (([[1, 2], [3, 4]], 2, 4), [[1, 2], [3, 4]]),
                (([[1, 2, 3, 4]], 2, 2), [[1, 2], [3, 4]]),
            ),
        ),
        T(
            "range_addition_ii",
            "def range_addition_ii(m, n, ops):\n"
            '    """Count cells with the maximum value after range increments (LeetCode 598)."""\n'
            "    m, n = int(m), int(n)\n"
            "    if not ops:\n"
            "        return m * n\n"
            "    a = min(int(op[0]) for op in ops)\n"
            "    b = min(int(op[1]) for op in ops)\n"
            "    return a * b\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 598\b|"
                    r"\brange addition ii\b",
                    low,
                )
            ),
            (
                ((3, 3, [[2, 2], [3, 3]]), 4),
                ((3, 3, []), 9),
                ((2, 2, [[1, 2], [2, 1]]), 1),
            ),
        ),
        T(
            "find_restaurant",
            "def find_restaurant(list1, list2):\n"
            '    """Common strings with the minimum index sum (LeetCode 599)."""\n'
            "    idx = {s: i for i, s in enumerate(list1)}\n"
            "    best = 10 ** 9\n"
            "    out = []\n"
            "    for j, s in enumerate(list2):\n"
            "        if s not in idx:\n"
            "            continue\n"
            "        score = idx[s] + j\n"
            "        if score < best:\n"
            "            best = score\n"
            "            out = [s]\n"
            "        elif score == best:\n"
            "            out.append(s)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 599\b|"
                    r"\bminimum index sum\b|"
                    r"\bfind restaurant\b",
                    low,
                )
            ),
            (
                (
                    (
                        ["Shogun", "Tapioca Express", "Burger King", "KFC"],
                        ["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"],
                    ),
                    ["Shogun"],
                ),
                ((["happy", "sad", "good"], ["sad", "happy", "good"]), ["sad", "happy"]),
                ((["a", "b"], ["c"]), []),
            ),
        ),
        T(
            "is_one_bit_character",
            "def is_one_bit_character(bits):\n"
            '    """True if the last bit starts a 1-bit character (LeetCode 717)."""\n'
            "    i = 0\n"
            "    n = len(bits)\n"
            "    while i < n - 1:\n"
            "        i += 2 if bits[i] == 1 else 1\n"
            "    return i == n - 1\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 717\b|"
                    r"\b1-bit and 2-bit\b|"
                    r"\bone-bit character\b|"
                    r"\bis_one_bit_character\b",
                    low,
                )
            ),
            (
                (([1, 0, 0],), True),
                (([1, 1, 1, 0],), False),
                (([0],), True),
            ),
        ),
        T(
            "first_unique_frequency",
            "def first_unique_frequency(nums):\n"
            '    """Leftmost value whose frequency is unique, else -1 (LeetCode 3843)."""\n'
            "    from collections import Counter\n"
            "    freq = Counter(nums)\n"
            "    used = Counter(freq.values())\n"
            "    for x in nums:\n"
            "        if used[freq[x]] == 1:\n"
            "            return x\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3843\b|"
                    r"\bfirst element with unique frequency\b|"
                    r"\bunique frequency\b",
                    low,
                )
            ),
            (
                (([20, 10, 30, 30],), 30),
                (([20, 20, 10, 30, 30, 30],), 20),
                (([10, 10, 20, 20],), -1),
            ),
        ),
    ]
