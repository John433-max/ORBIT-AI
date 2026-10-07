"""Cycle 502: unmatched write-a-function asks.

LeetCode 1392 / 413 / 1800 / 1790 / 1823 / 1678. Destination city,
pangram, and array-sign already exist as dest_city, check_pangram,
and sign_of_product — this pack does not rematch those phrases.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "longest_happy_prefix",
            "def longest_happy_prefix(s):\n"
            '    """Longest proper prefix that is also a suffix (LeetCode 1392)."""\n'
            "    s = str(s)\n"
            "    n = len(s)\n"
            "    if n == 0:\n"
            "        return ''\n"
            "    pi = [0] * n\n"
            "    j = 0\n"
            "    for i in range(1, n):\n"
            "        while j and s[i] != s[j]:\n"
            "            j = pi[j - 1]\n"
            "        if s[i] == s[j]:\n"
            "            j += 1\n"
            "            pi[i] = j\n"
            "    return s[:pi[-1]]\n",
            lambda low: (
                "happy prefix" in low
                or ("proper prefix" in low and "suffix" in low)
            )
            and "common prefix" not in low,
            (
                (("level",), "l"),
                (("ababab",), "abab"),
                (("leetcode",), ""),
            ),
        ),
        T(
            "number_of_arithmetic_slices",
            "def number_of_arithmetic_slices(nums):\n"
            '    """Count of contiguous arithmetic slices of length >= 3 (LeetCode 413)."""\n'
            "    total = 0\n"
            "    run = 0\n"
            "    for i in range(2, len(nums)):\n"
            "        if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]:\n"
            "            run += 1\n"
            "            total += run\n"
            "        else:\n"
            "            run = 0\n"
            "    return total\n",
            lambda low: ("arithmetic slice" in low or "arithmetic slices" in low)
            and "progression" not in low,
            (
                (([1, 2, 3, 4],), 3),
                (([1],), 0),
                (([1, 2, 3, 4, 5],), 6),
            ),
        ),
        T(
            "max_ascending_sum",
            "def max_ascending_sum(nums):\n"
            '    """Maximum sum of a strictly ascending contiguous subarray (LeetCode 1800)."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    best = cur = nums[0]\n"
            "    for i in range(1, len(nums)):\n"
            "        if nums[i] > nums[i - 1]:\n"
            "            cur += nums[i]\n"
            "        else:\n"
            "            cur = nums[i]\n"
            "        if cur > best:\n"
            "            best = cur\n"
            "    return best\n",
            lambda low: (
                "ascending sum" in low
                or ("maximum sum" in low and "ascending" in low and "kadane" not in low)
            ),
            (
                (([10, 20, 30, 5, 10, 50],), 65),
                (([10, 20, 30, 40, 50],), 150),
                (([12, 17, 15, 13, 10, 11, 12],), 33),
            ),
        ),
        T(
            "are_almost_equal",
            "def are_almost_equal(s1, s2):\n"
            '    """True if s1 equals s2 after at most one swap (LeetCode 1790)."""\n'
            "    s1, s2 = str(s1), str(s2)\n"
            "    if len(s1) != len(s2):\n"
            "        return False\n"
            "    if s1 == s2:\n"
            "        return True\n"
            "    diff = [i for i in range(len(s1)) if s1[i] != s2[i]]\n"
            "    return (\n"
            "        len(diff) == 2\n"
            "        and s1[diff[0]] == s2[diff[1]]\n"
            "        and s1[diff[1]] == s2[diff[0]]\n"
            "    )\n",
            lambda low: (
                "almost equal" in low
                and ("swap" in low or "string" in low)
                and "pangram" not in low
            ),
            (
                (("bank", "kanb"), True),
                (("attack", "defend"), False),
                (("kelb", "kelb"), True),
            ),
        ),
        T(
            "find_the_winner",
            "def find_the_winner(n, k):\n"
            '    """Winner of the circle count-out game (LeetCode 1823)."""\n'
            "    winner = 0\n"
            "    n, k = int(n), int(k)\n"
            "    for i in range(1, n + 1):\n"
            "        winner = (winner + k) % i\n"
            "    return winner + 1\n",
            lambda low: (
                "find the winner" in low
                or ("winner" in low and ("circle" in low or "josephus" in low or "count out" in low))
            )
            and "game of life" not in low,
            (
                ((5, 2), 3),
                ((6, 5), 1),
                ((1, 1), 1),
            ),
        ),
        T(
            "interpret",
            "def interpret(command):\n"
            '    """Goal parser: () -> o and (al) -> al (LeetCode 1678)."""\n'
            "    return str(command).replace('()', 'o').replace('(al)', 'al')\n",
            lambda low: (
                "goal parser" in low
                or ("interpret" in low and "command" in low and "goal" in low)
            ),
            (
                (("G()(al)",), "Goal"),
                (("G()()()()(al)",), "Gooooal"),
                (("(al)G(al)()()G",), "alGalooG"),
            ),
        ),
    ]
