"""Cycle 438: fix broad steals and cover six unmatched Easy/Medium asks.

is_even was matching "bitwise or of even numbers" (3688) and "maximum even split".
running_sum was matching "smallest missing integer greater than sequential prefix sum".
Matchers here are phrase- or id-gated. Groups subsequence I does not steal II.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "even_numbers_bitwise_or",
            "def even_numbers_bitwise_or(nums):\n"
            '    """Bitwise OR of even values, or 0 if none (LeetCode 3688)."""\n'
            "    acc = 0\n"
            "    found = False\n"
            "    for x in nums:\n"
            "        if int(x) % 2 == 0:\n"
            "            acc |= int(x)\n"
            "            found = True\n"
            "    return acc if found else 0\n",
            lambda low: bool(
                re.search(r"\bleetcode 3688\b", low)
                or "bitwise or of even" in low
                or "or of even numbers" in low
            ),
            (
                (([1, 2, 4, 6],), 6),
                (([1, 3, 5],), 0),
                (([8, 2],), 10),
            ),
        ),
        T(
            "missing_integer",
            "def missing_integer(nums):\n"
            '    """Smallest missing integer >= sequential prefix sum (LeetCode 2996)."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    score = int(nums[0])\n"
            "    for i in range(1, len(nums)):\n"
            "        if int(nums[i]) == int(nums[i - 1]) + 1:\n"
            "            score += int(nums[i])\n"
            "        else:\n"
            "            break\n"
            "    have = set(int(x) for x in nums)\n"
            "    while score in have:\n"
            "        score += 1\n"
            "    return score\n",
            lambda low: bool(
                re.search(r"\bleetcode 2996\b", low)
                or "sequential prefix sum" in low
                or (
                    "smallest missing integer" in low
                    and "prefix" in low
                )
            ),
            (
                (([1, 2, 3, 2, 5],), 6),
                (([3, 4, 5, 1, 12, 14, 13],), 15),
                (([1, 2, 0],), 3),
            ),
        ),
        T(
            "can_be_equal_ops",
            "def can_be_equal(s1, s2):\n"
            '    """Swap i with i+2 until s1 equals s2 (LeetCode 2839)."""\n'
            "    if len(s1) != len(s2):\n"
            "        return False\n"
            "    return sorted(s1[0::2]) == sorted(s2[0::2]) and sorted(s1[1::2]) == sorted(s2[1::2])\n",
            lambda low: bool(
                re.search(r"\bleetcode 2839\b", low)
                or "made equal with operations i" in low
                or "strings can be made equal" in low
            )
            and "ii" not in low.split("operations")[-1][:4],
            (
                (("abcd", "cdab"), True),
                (("abcd", "dacb"), False),
                (("bnxw", "bwxn"), True),
            ),
        ),
        T(
            "maximum_triplet_value",
            "def maximum_triplet_value(nums):\n"
            '    """Max (nums[i] - nums[j]) * nums[k] for i < j < k (LeetCode 2873)."""\n'
            "    nums = [int(x) for x in nums]\n"
            "    n = len(nums)\n"
            "    best = 0\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            diff = nums[i] - nums[j]\n"
            "            if diff <= 0:\n"
            "                continue\n"
            "            for k in range(j + 1, n):\n"
            "                best = max(best, diff * nums[k])\n"
            "    return best\n",
            lambda low: bool(
                re.search(r"\bleetcode 2873\b", low)
                or "ordered triplet i" in low
                or "maximum value of an ordered triplet" in low
            )
            and "ii" not in low,
            (
                (([12, 6, 1, 2, 7],), 77),
                (([1, 10, 3, 4, 19],), 133),
                (([1, 2, 3],), 0),
            ),
        ),
        T(
            "unequal_adjacent_groups",
            "def get_longest_subsequence(words, groups):\n"
            '    """Longest subsequence with unequal adjacent groups (LeetCode 2900)."""\n'
            "    if not words:\n"
            "        return []\n"
            "    out = [words[0]]\n"
            "    prev = groups[0]\n"
            "    for w, g in zip(words[1:], groups[1:]):\n"
            "        if g != prev:\n"
            "            out.append(w)\n"
            "            prev = g\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode 2900\b", low)
                or "unequal adjacent groups subsequence i" in low
                or "unequal adjacent groups" in low
            )
            and " ii" not in low
            and "subsequence ii" not in low,
            (
                ((["e", "a", "b"], [0, 0, 1]), ["e", "b"]),
                ((["a", "b", "c", "d"], [1, 0, 1, 1]), ["a", "b", "c"]),
            ),
        ),
        T(
            "matrix_similarity_shifts",
            "def are_similar(mat, k):\n"
            '    """True if each row equals itself after a left cyclic shift of k (LeetCode 2946)."""\n'
            "    if not mat or not mat[0]:\n"
            "        return True\n"
            "    n = len(mat[0])\n"
            "    k = int(k) % n\n"
            "    for row in mat:\n"
            "        for j in range(n):\n"
            "            if row[j] != row[(j + k) % n]:\n"
            "                return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(r"\bleetcode 2946\b", low)
                or "matrix similarity after cyclic" in low
                or "cyclic shifts" in low and "matrix" in low
            ),
            (
                (([[1, 2, 1, 2], [5, 5, 5, 5], [6, 3, 6, 3]], 2), True),
                (([[1, 2, 3], [1, 2, 3]], 1), False),
                (([[2, 2], [2, 2]], 3), True),
            ),
        ),

        T(
            "maximum_even_split",
            "def maximum_even_split(final_sum):\n"
            '    """Split into the most distinct positive evens that sum to final_sum (LeetCode 2178)."""\n'
            "    n = int(final_sum)\n"
            "    if n % 2:\n"
            "        return []\n"
            "    out = []\n"
            "    cur = 2\n"
            "    while n - cur >= cur + 2:\n"
            "        out.append(cur)\n"
            "        n -= cur\n"
            "        cur += 2\n"
            "    out.append(n)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode 2178\b", low)
                or "maximum even split" in low
            ),
            (
                ((12,), [2, 4, 6]),
                ((7,), []),
                ((28,), [2, 4, 6, 16]),
            ),
        ),
    ]
