"""Cycle 371: reverse-distinct, distinct averages, unequal triplets, circle cuts, digit-sum string, latest hidden time.

2441 / 2446 / 2451 / 2455 / 2460 / 2469 / 2485 / 2490 / 2496 / 2500 already matched.
These six phrases were unmatched stubs.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_distinct_integers_reverse",
            "def count_distinct_integers_reverse(nums):\n"
            '    """Distinct values after adding each reverse (LeetCode 2442)."""\n'
            "    seen = set()\n"
            "    for n in nums:\n"
            "        seen.add(n)\n"
            "        seen.add(int(str(n)[::-1]))\n"
            "    return len(seen)\n"
            "\n"
            "def countDistinctIntegers(nums):\n"
            "    return count_distinct_integers_reverse(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bdistinct integers after reverse\b|"
                    r"\breverse operations\b|"
                    r"\bleetcode 2442\b",
                    low,
                )
            ),
            (
                (([1, 13, 10, 12, 31],), 6),
                (([2, 2, 2],), 1),
            ),
        ),
        T(
            "distinct_averages",
            "def distinct_averages(nums):\n"
            '    """Distinct min+max averages after sorting (LeetCode 2465)."""\n'
            "    vals = sorted(nums)\n"
            "    i, j = 0, len(vals) - 1\n"
            "    seen = set()\n"
            "    while i < j:\n"
            "        seen.add(vals[i] + vals[j])\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return len(seen)\n"
            "\n"
            "def distinctAverages(nums):\n"
            "    return distinct_averages(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bdistinct averages\b|"
                    r"\bleetcode 2465\b",
                    low,
                )
            ),
            (
                (([4, 1, 4, 0, 3, 5],), 2),
                (([1, 100],), 1),
            ),
        ),
        T(
            "unequal_triplets",
            "def unequal_triplets(nums):\n"
            '    """Index triples with three different values (LeetCode 2475)."""\n'
            "    n = len(nums)\n"
            "    count = 0\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            if nums[i] == nums[j]:\n"
            "                continue\n"
            "            for k in range(j + 1, n):\n"
            "                if nums[k] != nums[i] and nums[k] != nums[j]:\n"
            "                    count += 1\n"
            "    return count\n"
            "\n"
            "def unequalTriplets(nums):\n"
            "    return unequal_triplets(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bunequal triplets\b|"
                    r"\bleetcode 2475\b",
                    low,
                )
            ),
            (
                (([4, 4, 2, 4, 3],), 3),
                (([1, 1, 1, 1, 1],), 0),
            ),
        ),
        T(
            "minimum_cuts_circle",
            "def minimum_cuts_circle(n):\n"
            '    """Minimum cuts to split a circle into n parts (LeetCode 2481)."""\n'
            "    if n <= 1:\n"
            "        return 0\n"
            "    return n if n % 2 else n // 2\n"
            "\n"
            "def numberOfCuts(n):\n"
            "    return minimum_cuts_circle(n)\n",
            lambda low: bool(
                re.search(
                    r"\bminimum cuts to divide a circle\b|"
                    r"\bdivide a circle\b|"
                    r"\bleetcode 2481\b",
                    low,
                )
            ),
            (
                ((4,), 2),
                ((3,), 3),
                ((1,), 0),
            ),
        ),
        T(
            "digit_sum_string",
            "def digit_sum_string(s, k):\n"
            '    """Repeat k-group digit sums until length <= k (LeetCode 2243)."""\n'
            "    while len(s) > k:\n"
            "        parts = []\n"
            "        for i in range(0, len(s), k):\n"
            "            parts.append(str(sum(int(ch) for ch in s[i:i + k])))\n"
            "        s = ''.join(parts)\n"
            "    return s\n"
            "\n"
            "def digitSum(s, k):\n"
            "    return digit_sum_string(s, k)\n",
            lambda low: bool(
                re.search(
                    r"\bdigit sum of a string\b|"
                    r"\bcalculate digit sum\b|"
                    r"\bleetcode 2243\b",
                    low,
                )
            ),
            (
                (("11111222223", 3), "135"),
                (("00000000", 3), "000"),
            ),
        ),
        T(
            "latest_time_hidden",
            "def latest_time_hidden(time):\n"
            '    """Latest valid hh:mm replacing ? digits (LeetCode 1736)."""\n'
            "    t = list(time)\n"
            "    if t[0] == '?':\n"
            "        t[0] = '2' if t[1] in '?0123' else '1'\n"
            "    if t[1] == '?':\n"
            "        t[1] = '3' if t[0] == '2' else '9'\n"
            "    if t[3] == '?':\n"
            "        t[3] = '5'\n"
            "    if t[4] == '?':\n"
            "        t[4] = '9'\n"
            "    return ''.join(t)\n"
            "\n"
            "def maximumTime(time):\n"
            "    return latest_time_hidden(time)\n",
            lambda low: bool(
                re.search(
                    r"\blatest time by replacing hidden\b|"
                    r"\bhidden digits\b|"
                    r"\bleetcode 1736\b",
                    low,
                )
            ),
            (
                (("2?:?0",), "23:50"),
                (("0?:3?",), "09:39"),
                (("1?:22",), "19:22"),
            ),
        ),
    ]
