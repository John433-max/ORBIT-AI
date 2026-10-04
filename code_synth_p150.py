"""Cycle 429: asks stolen by broad matchers or still unmatched.

- 1005 largest sum after K negations was stolen by sum_list ("sum of array").
- 1351 / 1356 were stolen by candy because "135" is a substring of those ids.
- 953 / 1103 / 1317 had no template.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "largest_sum_after_k_negations",
            "def largestSumAfterKNegations(nums, k):\n"
            '    """Max sum after flipping the sign of k elements (LeetCode 1005)."""\n'
            "    nums = sorted(int(x) for x in nums)\n"
            "    k = int(k)\n"
            "    i = 0\n"
            "    while k and i < len(nums) and nums[i] < 0:\n"
            "        nums[i] = -nums[i]\n"
            "        i += 1\n"
            "        k -= 1\n"
            "    if k % 2:\n"
            "        j = min(range(len(nums)), key=lambda t: nums[t])\n"
            "        nums[j] = -nums[j]\n"
            "    return sum(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1005\b|\bk negations\b|\bafter k negations\b",
                    low,
                )
            ),
            (
                (([4, 2, 3], 1), 5),
                (([3, -1, 0, 2], 3), 6),
                (([2, -3, -1, 5, -4], 2), 13),
            ),
        ),
        T(
            "count_negatives_1351",
            "def countNegatives(grid):\n"
            '    """Count negative cells in a matrix (LeetCode 1351)."""\n'
            "    return sum(1 for row in grid for x in row if int(x) < 0)\n",
            lambda low: bool(re.search(r"\bleetcode 1351\b|\bcountnegatives\b", low)),
            (
                (([[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]],), 8),
                (([[3, 2], [1, 0]],), 0),
            ),
        ),
        T(
            "sort_by_bits",
            "def sortByBits(arr):\n"
            '    """Sort by popcount, then value (LeetCode 1356)."""\n'
            "    return sorted(arr, key=lambda x: (bin(int(x)).count('1'), int(x)))\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1356\b|\bsort integers by the number of 1 bits\b|\bsort by bits\b",
                    low,
                )
            ),
            (
                (([0, 1, 2, 3, 4, 5, 6, 7, 8],), [0, 1, 2, 4, 8, 3, 5, 6, 7]),
                (([1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1],), [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]),
            ),
        ),
        T(
            "is_alien_sorted",
            "def isAlienSorted(words, order):\n"
            '    """True if words are sorted in the alien alphabet (LeetCode 953)."""\n'
            "    rank = {c: i for i, c in enumerate(order)}\n"
            "    def key(word):\n"
            "        return [rank.get(c, -1) for c in word]\n"
            "    return all(key(words[i]) <= key(words[i + 1]) for i in range(len(words) - 1))\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 953\b|\balien dictionary\b|\bis_alien_sorted\b",
                    low,
                )
            ),
            (
                ((["hello", "leetcode"], "hlabcdefgijkmnopqrstuvwxyz"), True),
                ((["word", "world", "row"], "worldabcefghijkmnpqstuvxyz"), False),
                ((["apple", "app"], "abcdefghijklmnopqrstuvwxyz"), False),
            ),
        ),
        T(
            "distribute_candies_people",
            "def distributeCandies(candies, num_people):\n"
            '    """Give 1,2,3,... candies around the table (LeetCode 1103)."""\n'
            "    left = int(candies)\n"
            "    n = int(num_people)\n"
            "    out = [0] * n\n"
            "    give = 1\n"
            "    i = 0\n"
            "    while left > 0:\n"
            "        take = give if give < left else left\n"
            "        out[i % n] += take\n"
            "        left -= take\n"
            "        give += 1\n"
            "        i += 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1103\b|\bdistribute candies to people\b",
                    low,
                )
            ),
            (
                ((7, 4), [1, 2, 3, 1]),
                ((10, 3), [5, 2, 3]),
            ),
        ),
        T(
            "get_no_zero_integers",
            "def getNoZeroIntegers(n):\n"
            '    """Two positive integers without digit 0 that sum to n (LeetCode 1317)."""\n'
            "    n = int(n)\n"
            "    for a in range(1, n):\n"
            "        b = n - a\n"
            "        if '0' not in str(a) and '0' not in str(b):\n"
            "            return [a, b]\n"
            "    return [1, n - 1]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1317\b|\bno-zero integers\b|\bno zero integers\b",
                    low,
                )
            ),
            (
                ((2,), [1, 1]),
                ((11,), [2, 9]),
            ),
        ),
    ]
