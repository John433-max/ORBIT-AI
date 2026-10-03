"""Cycle 398: unmatched LeetCode easies 2566 / 2739 / 2815 / 2899 / 2937 / 3114.

These titles previously fell through to the unverified draft stub.

Official examples (doocs/leetcode README_EN):
- 2566 Maximum Difference by Remapping a Digit:
  11891 -> 99009; 90 -> 99.
- 2739 Total Distance Traveled: 10 km/L; every 5 L from main injects 1 L
  from additional. (5, 10) -> 60; (1, 2) -> 10.
- 2815 Max Pair Sum in an Array: pair sharing the same largest digit.
  [51,71,17,24,42] -> 88; [112,131,411] -> -1.
- 2899 Last Visited Integers: consecutive -1s look up k-th last positive.
  [1,2,-1,-1,-1] -> [2,1,-1]; [1,-1,2,-1,-1] -> [1,2,1].
- 2937 Make Three Strings Equal: delete rightmost chars to a common prefix.
  ("abc","abb","ab") -> 2; ("dac","bac","cac") -> -1.
- 3114 Latest Time You Can Obtain After Replacing Characters (12-hour):
  "1?:?4" -> "11:54"; "0?:5?" -> "09:59".
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "min_max_difference",
            "def min_max_difference(num):\n"
            '    """Max-min after remapping one digit everywhere (LeetCode 2566)."""\n'
            "    s = str(num)\n"
            "    lo = int(s.replace(s[0], '0'))\n"
            "    for ch in s:\n"
            "        if ch != '9':\n"
            "            return int(s.replace(ch, '9')) - lo\n"
            "    return num - lo\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2566\b", low)
                or "remapping a digit" in low
                or "remap a digit" in low
            ),
            examples=(
                ((11891,), 99009),
                ((90,), 99),
            ),
        ),
        T(
            "distance_traveled",
            "def distance_traveled(main_tank, additional_tank):\n"
            '    """Km traveled at 10 km/L with 1 L inject every 5 L (LeetCode 2739)."""\n'
            "    ans = used = 0\n"
            "    while main_tank:\n"
            "        used += 1\n"
            "        ans += 10\n"
            "        main_tank -= 1\n"
            "        if used % 5 == 0 and additional_tank:\n"
            "            additional_tank -= 1\n"
            "            main_tank += 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2739\b", low)
                or "total distance traveled" in low
                or "distance traveled" in low and "tank" in low
            ),
            examples=(
                ((5, 10), 60),
                ((1, 2), 10),
            ),
        ),
        T(
            "max_pair_sum",
            "def max_pair_sum(nums):\n"
            '    """Max pair sum sharing the same largest digit (LeetCode 2815)."""\n'
            "    ans = -1\n"
            "    best = [0] * 10\n"
            "    for num in nums:\n"
            "        digit = max(int(ch) for ch in str(num))\n"
            "        if best[digit]:\n"
            "            ans = max(ans, num + best[digit])\n"
            "        best[digit] = max(best[digit], num)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2815\b", low)
                or "max pair sum" in low
                or ("largest digit" in low and "pair" in low)
            ),
            examples=(
                (([51, 71, 17, 24, 42],), 88),
                (([112, 131, 411],), -1),
            ),
        ),
        T(
            "last_visited_integers",
            "def last_visited_integers(nums):\n"
            '    """Answers for each -1: k-th last positive seen (LeetCode 2899)."""\n'
            "    seen = []\n"
            "    ans = []\n"
            "    k = 0\n"
            "    for x in nums:\n"
            "        if x == -1:\n"
            "            k += 1\n"
            "            ans.append(-1 if k > len(seen) else seen[-k])\n"
            "        else:\n"
            "            k = 0\n"
            "            seen.append(x)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2899\b", low)
                or "last visited integers" in low
            ),
            examples=(
                (([1, 2, -1, -1, -1],), [2, 1, -1]),
                (([1, -1, 2, -1, -1],), [1, 2, 1]),
            ),
        ),
        T(
            "find_minimum_operations",
            "def find_minimum_operations(s1, s2, s3):\n"
            '    """Deletes to a shared nonempty prefix, else -1 (LeetCode 2937)."""\n'
            "    total = len(s1) + len(s2) + len(s3)\n"
            "    n = min(len(s1), len(s2), len(s3))\n"
            "    for i in range(n):\n"
            "        if not (s1[i] == s2[i] == s3[i]):\n"
            "            return -1 if i == 0 else total - 3 * i\n"
            "    return total - 3 * n\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2937\b", low)
                or "make three strings equal" in low
            ),
            examples=(
                (("abc", "abb", "ab"), 2),
                (("dac", "bac", "cac"), -1),
            ),
        ),
        T(
            "find_latest_time",
            "def find_latest_time(s):\n"
            '    """Latest valid 12-hour time replacing ? (LeetCode 3114)."""\n'
            "    chars = list(s)\n"
            "    if chars[0] == '?':\n"
            "        chars[0] = '1' if chars[1] == '?' or chars[1] < '2' else '0'\n"
            "    if chars[1] == '?':\n"
            "        chars[1] = '1' if chars[0] == '1' else '9'\n"
            "    if chars[3] == '?':\n"
            "        chars[3] = '5'\n"
            "    if chars[4] == '?':\n"
            "        chars[4] = '9'\n"
            "    return ''.join(chars)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3114\b", low)
                or "latest time you can obtain" in low
                or ("replacing characters" in low and "time" in low)
            ),
            examples=(
                (("1?:?4",), "11:54"),
                (("0?:5?",), "09:59"),
            ),
        ),
    ]
