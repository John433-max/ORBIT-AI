"""Cycle 362: unmatched Easy array/string templates.

Official problem statements (algorithms only, not copied text):
LeetCode 2586, 3033, 3162, 3206, 3536, 3541.
"""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "vowel_strings_in_range",
            "def vowel_strings_in_range(words, queries):\n"
            '    """Count words in each [l, r] that start and end with a vowel (LeetCode 2586)."""\n'
            "    vowels = set('aeiou')\n"
            "    good = [1 if w and w[0] in vowels and w[-1] in vowels else 0 for w in words]\n"
            "    prefix = [0]\n"
            "    for bit in good:\n"
            "        prefix.append(prefix[-1] + bit)\n"
            "    return [prefix[r + 1] - prefix[l] for l, r in queries]\n",
            lambda low: bool(
                re.search(
                    r"\bvowel strings in range\b|"
                    r"\bcount the number of vowel strings\b|"
                    r"\bleetcode 2586\b",
                    low,
                )
            ),
            (
                ((["aba", "bcb", "ece", "aa", "e"], [[0, 2], [1, 4], [1, 1]]), [2, 3, 0]),
                ((["a", "e", "i"], [[0, 2]]), [3]),
                ((["xyz"], [[0, 0]]), [0]),
            ),
        ),
        T(
            "modified_matrix",
            "def modified_matrix(matrix):\n"
            '    """Replace each -1 with the max of its column (LeetCode 3033)."""\n'
            "    if not matrix or not matrix[0]:\n"
            "        return matrix\n"
            "    rows, cols = len(matrix), len(matrix[0])\n"
            "    out = [row[:] for row in matrix]\n"
            "    for c in range(cols):\n"
            "        col_max = max(matrix[r][c] for r in range(rows))\n"
            "        for r in range(rows):\n"
            "            if out[r][c] == -1:\n"
            "                out[r][c] = col_max\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bmodify the matrix\b|"
                    r"\bmodified matrix\b|"
                    r"\bleetcode 3033\b",
                    low,
                )
            ),
            (
                (([[1, 2, -1], [4, -1, 6], [7, 8, 9]],), [[1, 2, 9], [4, 8, 6], [7, 8, 9]]),
                (([[3, -1], [5, 2]],), [[3, 2], [5, 2]]),
                (([[-1]],), [[-1]]),
            ),
        ),
        T(
            "number_of_good_pairs_i",
            "def number_of_good_pairs_i(nums1, nums2, k):\n"
            '    """Pairs where nums1[i] is divisible by nums2[j] * k (LeetCode 3162)."""\n'
            "    count = 0\n"
            "    for a in nums1:\n"
            "        for b in nums2:\n"
            "            div = b * k\n"
            "            if div and a % div == 0:\n"
            "                count += 1\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\bnumber of good pairs i\b|"
                    r"\bgood pairs i\b|"
                    r"\bleetcode 3162\b",
                    low,
                )
            ),
            (
                (([1, 3, 4], [1, 3, 4], 1), 5),
                (([1, 2, 4, 12], [2, 4], 3), 2),
                (([1], [1], 1), 1),
            ),
        ),
        T(
            "alternating_groups_i",
            "def alternating_groups_i(colors):\n"
            '    """Circular length-3 groups whose neighbors differ from the middle (LeetCode 3206)."""\n'
            "    n = len(colors)\n"
            "    if n < 3:\n"
            "        return 0\n"
            "    count = 0\n"
            "    for i in range(n):\n"
            "        if colors[i] != colors[(i - 1) % n] and colors[i] != colors[(i + 1) % n]:\n"
            "            count += 1\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\balternating groups i\b|"
                    r"\balternating groups\b|"
                    r"\bleetcode 3206\b",
                    low,
                )
                and "ii" not in low
            ),
            (
                (([1, 1, 1],), 0),
                (([0, 1, 0, 0, 1],), 3),
                (([0, 1, 0],), 1),
            ),
        ),
        T(
            "max_product_two_digits",
            "def max_product_two_digits(n):\n"
            '    """Largest product of two distinct digits of n (LeetCode 3536)."""\n'
            "    digits = []\n"
            "    x = n\n"
            "    while x:\n"
            "        digits.append(x % 10)\n"
            "        x //= 10\n"
            "    if len(digits) < 2:\n"
            "        return 0\n"
            "    digits.sort(reverse=True)\n"
            "    return digits[0] * digits[1]\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum product of two digits\b|"
                    r"\bmax product of two digits\b|"
                    r"\bleetcode 3536\b",
                    low,
                )
            ),
            (
                ((31,), 3),
                ((22,), 4),
                ((124,), 8),
            ),
        ),
        T(
            "most_frequent_vowel_consonant",
            "def most_frequent_vowel_consonant(s):\n"
            '    """Sum of the max vowel frequency and max consonant frequency (LeetCode 3541)."""\n'
            "    vowels = set('aeiou')\n"
            "    freq = {}\n"
            "    for ch in s:\n"
            "        if ch.isalpha():\n"
            "            freq[ch] = freq.get(ch, 0) + 1\n"
            "    max_v = max((c for ch, c in freq.items() if ch in vowels), default=0)\n"
            "    max_c = max((c for ch, c in freq.items() if ch not in vowels), default=0)\n"
            "    return max_v + max_c\n",
            lambda low: bool(
                re.search(
                    r"\bmost frequent vowel and consonant\b|"
                    r"\bfrequent vowel and consonant\b|"
                    r"\bleetcode 3541\b",
                    low,
                )
            ),
            (
                (("successes",), 6),
                (("aeiaeia",), 3),
                (("a",), 1),
            ),
        ),
    ]
