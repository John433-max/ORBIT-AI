"""Cycle 399: unused Easy — exactly-k sum / split by separator / car points /
missing-and-repeated / encrypted integers / parity transform.

Official examples (doocs/leetcode README_EN):
- 2656 Maximum Sum With Exactly K Elements: always take current max.
  [1,2,3,4,5], k=3 -> 18; [5,5,5], k=2 -> 11.
- 2788 Split Strings by Separator: drop empty pieces.
  ["one.two.three","four.five","six"], "." -> six tokens; ["|||"], "|" -> [].
- 2848 Points That Intersect With Cars: inclusive coverage.
  [[3,6],[1,5],[4,7]] -> 7; [[1,3],[5,8]] -> 7.
- 2965 Find Missing and Repeated Values: n^2 grid of 1..n^2 with one dup.
  [[1,3],[2,2]] -> [2,4]; [[9,1,7],[8,9,2],[3,4,6]] -> [9,5].
- 3079 Sum of Encrypted Integers: each digit becomes the max digit.
  [1,2,3] -> 6; [10,21,31] -> 66.
- 3467 Transform Array by Parity: even->0, odd->1, then sort.
  [4,3,2,1] -> [0,0,1,1]; [1,5,1,4,2] -> [0,0,1,1,1].
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "maximize_sum",
            "def maximize_sum(nums, k):\n"
            '    """Score of taking the current max exactly k times (LeetCode 2656)."""\n'
            "    m = max(nums)\n"
            "    return k * m + k * (k - 1) // 2\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2656\b", low)
                or "exactly k elements" in low
                or "maximum sum with exactly" in low
            ),
            examples=(
                (([1, 2, 3, 4, 5], 3), 18),
                (([5, 5, 5], 2), 11),
            ),
        ),
        T(
            "split_words_by_separator",
            "def split_words_by_separator(words, separator):\n"
            '    """Split each word and drop empty pieces (LeetCode 2788)."""\n'
            "    out = []\n"
            "    for word in words:\n"
            "        out.extend(part for part in word.split(separator) if part)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2788\b", low)
                or "split strings by separator" in low
                or "split words by separator" in low
            ),
            examples=(
                ((["one.two.three", "four.five", "six"], "."), ["one", "two", "three", "four", "five", "six"]),
                ((["|||"], "|"), []),
            ),
        ),
        T(
            "number_of_points",
            "def number_of_points(nums):\n"
            '    """Count distinct points covered by inclusive car intervals (LeetCode 2848)."""\n'
            "    seen = set()\n"
            "    for start, end in nums:\n"
            "        seen.update(range(start, end + 1))\n"
            "    return len(seen)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2848\b", low)
                or "intersect with cars" in low
                or "points that intersect" in low
            ),
            examples=(
                (([[3, 6], [1, 5], [4, 7]],), 7),
                (([[1, 3], [5, 8]],), 7),
            ),
        ),
        T(
            "find_missing_and_repeated_values",
            "def find_missing_and_repeated_values(grid):\n"
            '    """Repeated and missing values in a 1..n^2 grid (LeetCode 2965)."""\n'
            "    n = len(grid)\n"
            "    count = [0] * (n * n + 1)\n"
            "    for row in grid:\n"
            "        for value in row:\n"
            "            count[value] += 1\n"
            "    repeated = missing = 0\n"
            "    for value in range(1, n * n + 1):\n"
            "        if count[value] == 2:\n"
            "            repeated = value\n"
            "        elif count[value] == 0:\n"
            "            missing = value\n"
            "    return [repeated, missing]\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2965\b", low)
                or "missing and repeated" in low
                or "repeated and missing values" in low
            ),
            examples=(
                (([[1, 3], [2, 2]],), [2, 4]),
                (([[9, 1, 7], [8, 9, 2], [3, 4, 6]],), [9, 5]),
            ),
        ),
        T(
            "sum_of_encrypted_int",
            "def sum_of_encrypted_int(nums):\n"
            '    """Sum after replacing each digit with the max digit (LeetCode 3079)."""\n'
            "    total = 0\n"
            "    for num in nums:\n"
            "        digits = str(num)\n"
            "        total += int(max(digits) * len(digits))\n"
            "    return total\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3079\b", low)
                or "encrypted integers" in low
                or "sum of encrypted" in low
            ),
            examples=(
                (([1, 2, 3],), 6),
                (([10, 21, 31],), 66),
            ),
        ),
        T(
            "transform_array",
            "def transform_array(nums):\n"
            '    """Even to 0, odd to 1, then sort (LeetCode 3467)."""\n'
            "    return sorted(value % 2 for value in nums)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3467\b", low)
                or "transform array by parity" in low
                or "array by parity" in low and "transform" in low
            ),
            examples=(
                (([4, 3, 2, 1],), [0, 0, 1, 1]),
                (([1, 5, 1, 4, 2],), [0, 0, 1, 1, 1]),
            ),
        ),
    ]
