"""Cycle 269: additional verified Python templates (pack 12)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "matrix_reshape",
            "def matrix_reshape(mat, r, c):\n"
            '    """Reshape mat into r x c if element count matches; else return mat."""\n'
            "    rows = [list(row) for row in mat]\n"
            "    flat = [int(x) for row in rows for x in row]\n"
            "    if r * c != len(flat):\n"
            "        return rows\n"
            "    return [flat[i * c:(i + 1) * c] for i in range(r)]\n",
            lambda low: bool(
                re.search(
                    r"\breshape (?:the )?matrix\b|"
                    r"\bmatrix_reshape\b|"
                    r"\breshape.?mat(?:rix)?\b|"
                    r"\bmatrix reshape\b",
                    low,
                )
            )
            and "rotate" not in low
            and "spiral" not in low,
            (([[[1, 2], [3, 4]], 1, 4], [[1, 2, 3, 4]]), ([[[1, 2], [3, 4]], 2, 4], [[1, 2], [3, 4]])),
        ),
        T(
            "di_string_match",
            "def di_string_match(s):\n"
            '    """Permutation of 0..n matching I/D pattern in s."""\n'
            "    s = str(s)\n"
            "    lo, hi = 0, len(s)\n"
            "    out = []\n"
            "    for ch in s:\n"
            "        if ch == 'I':\n"
            "            out.append(lo)\n"
            "            lo += 1\n"
            "        else:\n"
            "            out.append(hi)\n"
            "            hi -= 1\n"
            "    out.append(lo)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bdi string match\b|"
                    r"\bdi_string_match\b|"
                    r"\bDI string match\b|"
                    r"\bmatch increase decrease string\b",
                    low,
                )
            )
            and "isomorphic" not in low
            and "word pattern" not in low,
            ((("IDID",), [0, 4, 1, 3, 2]), (("III",), [0, 1, 2, 3]), (("DDI",), [3, 2, 0, 1])),
        ),
        T(
            "relative_sort_array",
            "def relative_sort_array(arr1, arr2):\n"
            '    """Sort arr1 by arr2 order; leftovers ascending."""\n'
            "    a = [int(x) for x in arr1]\n"
            "    order = {int(x): i for i, x in enumerate(arr2)}\n"
            "    a.sort(key=lambda x: (0, order[x]) if x in order else (1, x))\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\brelative sort array\b|"
                    r"\brelative_sort_array\b|"
                    r"\bsort arr1 (?:by|according to) arr2\b|"
                    r"\brelative sort\b",
                    low,
                )
            )
            and "parity" not in low
            and "colors" not in low,
            (([[2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]], [2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19]),),
        ),
        T(
            "add_to_array_form",
            "def add_to_array_form(num, k):\n"
            '    """Add integer k to the array-form of num."""\n'
            "    digits = [int(x) for x in num]\n"
            "    i = len(digits) - 1\n"
            "    carry = int(k)\n"
            "    while i >= 0 or carry:\n"
            "        if i >= 0:\n"
            "            carry += digits[i]\n"
            "            digits[i] = carry % 10\n"
            "            i -= 1\n"
            "        else:\n"
            "            digits.insert(0, carry % 10)\n"
            "        carry //= 10\n"
            "    return digits\n",
            lambda low: bool(
                re.search(
                    r"\badd to array.?form\b|"
                    r"\badd_to_array_form\b|"
                    r"\barray.?form of (?:an? )?integer\b|"
                    r"\badd k to array form\b",
                    low,
                )
            )
            and "two numbers" not in low
            and "strings" not in low
            and "linked" not in low,
            (([[1, 2, 0, 0], 34], [1, 2, 3, 4]), ([[2, 7, 4], 181], [4, 5, 5]), ([[9, 9, 9], 1], [1, 0, 0, 0])),
        ),
        T(
            "common_chars",
            "def common_chars(words):\n"
            '    """Chars that appear in every word, with multiplicity."""\n'
            "    if not words:\n"
            "        return []\n"
            "    from collections import Counter\n"
            "    acc = Counter(str(words[0]))\n"
            "    for w in words[1:]:\n"
            "        acc &= Counter(str(w))\n"
            "    out = []\n"
            "    for ch, n in sorted(acc.items()):\n"
            "        out.extend([ch] * n)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bfind common characters\b|"
                    r"\bcommon_chars\b|"
                    r"\bcommon characters\b|"
                    r"\bchars? in every (?:word|string)\b",
                    low,
                )
            )
            and "anagram" not in low
            and "jewels" not in low,
            (([["bella", "label", "roller"]], ["e", "l", "l"]), ([["cool", "lock", "cook"]], ["c", "o"])),
        ),
        T(
            "projection_area",
            "def projection_area(grid):\n"
            '    """Sum of xy, yz, and zx projections of n x n stacked cubes."""\n'
            "    n = len(grid)\n"
            "    xy = yz = zx = 0\n"
            "    for i in range(n):\n"
            "        row_max = col_max = 0\n"
            "        for j in range(n):\n"
            "            v = int(grid[i][j])\n"
            "            if v > 0:\n"
            "                xy += 1\n"
            "            if v > row_max:\n"
            "                row_max = v\n"
            "            c = int(grid[j][i])\n"
            "            if c > col_max:\n"
            "                col_max = c\n"
            "        yz += row_max\n"
            "        zx += col_max\n"
            "    return xy + yz + zx\n",
            lambda low: bool(
                re.search(
                    r"\bprojection area\b|"
                    r"\bprojection_area\b|"
                    r"\b3d (?:shape )?projection\b|"
                    r"\bprojection area of 3d\b",
                    low,
                )
            )
            and "island" not in low
            and "perimeter" not in low,
            (([[[1, 2], [3, 4]]], 17), ([[[2]]], 5), ([[[1, 0], [0, 2]]], 8)),
        ),
    ]
