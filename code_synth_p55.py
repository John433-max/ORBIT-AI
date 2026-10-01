"""Cycle 317: min ops to make array increasing / decrypt alphabet mapping /
maximum odd binary number / k-or of an array / neither min nor max /
closest number to zero."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "min_operations_increasing",
            "def min_operations_increasing(nums):\n"
            '    """Min increments so nums is strictly increasing (LeetCode 1827)."""\n'
            "    ops = 0\n"
            "    prev = nums[0]\n"
            "    for x in nums[1:]:\n"
            "        if x <= prev:\n"
            "            need = prev + 1\n"
            "            ops += need - x\n"
            "            prev = need\n"
            "        else:\n"
            "            prev = x\n"
            "    return ops\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)?[_ ]operations[_ ](?:to[_ ]make[_ ](?:the[_ ])?array[_ ])?increasing\b|"
                    r"\bmin_operations_increasing\b|"
                    r"\bmake[_ ](?:the[_ ])?array[_ ](?:strictly[_ ])?increasing\b",
                    low,
                )
            )
            and "longest" not in low
            and "path" not in low,
            (
                (([1, 1, 1],), 3),
                (([1, 5, 2, 4, 1],), 14),
                (([8],), 0),
            ),
        ),
        T(
            "freq_alphabets",
            "def freq_alphabets(s):\n"
            '    """Decrypt digit mapping 1->a .. 26#->z (LeetCode 1309)."""\n'
            "    out = []\n"
            "    i = len(s) - 1\n"
            "    while i >= 0:\n"
            "        if s[i] == '#':\n"
            "            out.append(chr(ord('a') + int(s[i - 2:i]) - 1))\n"
            "            i -= 3\n"
            "        else:\n"
            "            out.append(chr(ord('a') + int(s[i]) - 1))\n"
            "            i -= 1\n"
            "    return ''.join(reversed(out))\n",
            lambda low: bool(
                re.search(
                    r"\bfreq_alphabets\b|"
                    r"\bdecrypt[_ ](?:string[_ ])?(?:from[_ ])?alphabet[_ ](?:to[_ ]integer[_ ])?mapping\b|"
                    r"\balphabet[_ ]to[_ ]integer[_ ]mapping\b",
                    low,
                )
            ),
            (
                (("10#11#12",), "jkab"),
                (("1326#",), "acz"),
                (("25#",), "y"),
            ),
        ),
        T(
            "maximum_odd_binary_number",
            "def maximum_odd_binary_number(s):\n"
            '    """Rearrange bits of s to the maximum odd binary number (LeetCode 2864)."""\n'
            "    ones = s.count('1')\n"
            "    zeros = len(s) - ones\n"
            "    if ones == 0:\n"
            "        return s\n"
            "    return '1' * (ones - 1) + '0' * zeros + '1'\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum[_ ]odd[_ ]binary[_ ](?:number)?\b|"
                    r"\bmaximum_odd_binary_number\b",
                    low,
                )
            ),
            (
                (("010",), "001"),
                (("0101",), "1001"),
                (("1",), "1"),
            ),
        ),
        T(
            "find_k_or",
            "def find_k_or(nums, k):\n"
            '    """K-OR: bits set in at least k elements (LeetCode 2917)."""\n'
            "    ans = 0\n"
            "    for b in range(31):\n"
            "        bit = 1 << b\n"
            "        if sum(1 for x in nums if x & bit) >= k:\n"
            "            ans |= bit\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ](?:the[_ ])?k[-_ ]?or\b|"
                    r"\bk[-_ ]?or[_ ]of[_ ](?:an[_ ])?array\b|"
                    r"\bfind_k_or\b",
                    low,
                )
            ),
            (
                (([7, 12, 9, 8, 9, 15], 4), 9),
                (([2, 12, 1, 11, 4, 5], 6), 0),
                (([10, 8, 5, 9, 11, 6, 8], 1), 15),
            ),
        ),
        T(
            "neither_minimum_nor_maximum",
            "def neither_minimum_nor_maximum(nums):\n"
            '    """Any element that is neither min nor max, else -1 (LeetCode 2733)."""\n'
            "    lo, hi = min(nums), max(nums)\n"
            "    for x in nums:\n"
            "        if x != lo and x != hi:\n"
            "            return x\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bneither[_ ](?:the[_ ])?(?:min(?:imum)?[_ ]nor[_ ]max(?:imum)?|minimum[_ ]nor[_ ]maximum)\b|"
                    r"\bneither_minimum_nor_maximum\b",
                    low,
                )
            ),
            (
                (([3, 2, 1, 4],), 3),
                (([1, 2],), -1),
                (([2, 1, 3],), 2),
            ),
        ),
        T(
            "find_closest_number",
            "def find_closest_number(nums):\n"
            '    """Number closest to 0; ties pick the larger value (LeetCode 2239)."""\n'
            "    best = nums[0]\n"
            "    for x in nums[1:]:\n"
            "        ax, ab = abs(x), abs(best)\n"
            "        if ax < ab or (ax == ab and x > best):\n"
            "            best = x\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ](?:the[_ ])?closest[_ ]number[_ ]to[_ ]zero\b|"
                    r"\bclosest[_ ]number[_ ]to[_ ]zero\b|"
                    r"\bfind_closest_number\b",
                    low,
                )
            ),
            (
                (([-4, -2, 1, 4, 8],), 1),
                (([2, -1, 1],), 1),
                (([-100, -1],), -1),
            ),
        ),
    ]
