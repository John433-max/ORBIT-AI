"""Cycle 393: Easy/Medium prompts still absent from the template index.

LeetCode 893, 937, 858, 949, 985, and 991 were not referenced by any pack.
Matchers stay ID- or title-specific so calculator, time, even-sum, and
reorder prompts do not steal basic-calculator / largest-number / even-count
templates. Loaded before p113.

Sources:
- LeetCode 893 Groups of Special-Equivalent Strings: even-index and odd-index
  character multisets identify a group. Examples return 3 and 3.
- LeetCode 937 Reorder Data in Log Files: letter-logs sorted by content then
  identifier; digit-logs keep relative order.
- LeetCode 858 Mirror Reflection: reduce p,q by gcd; both odd -> 1, odd p
  and even q -> 0, even p and odd q -> 2. Examples (2,1)->2 and (3,1)->1.
- LeetCode 949 Largest Time for Given Digits: max valid HH:MM or "".
- LeetCode 985 Sum of Even Numbers After Queries: maintain the running even sum.
- LeetCode 991 Broken Calculator: walk target down to start (halve if even,
  else add 1), then add the leftover subtracts.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "num_special_equiv_groups",
            "def num_special_equiv_groups(words):\n"
            '    """Count special-equivalent groups by even/odd multisets (LeetCode 893)."""\n'
            "    groups = set()\n"
            "    for word in words:\n"
            "        even = ''.join(sorted(word[0::2]))\n"
            "        odd = ''.join(sorted(word[1::2]))\n"
            "        groups.add((even, odd))\n"
            "    return len(groups)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 893\b|"
                    r"\bspecial[- ]equivalent\b",
                    low,
                )
            ),
            (
                ((["abcd", "cdab", "cbad", "xyzz", "zzxy", "zzyx"],), 3),
                ((["abc", "acb", "bac", "bca", "cab", "cba"],), 3),
            ),
        ),
        T(
            "reorder_log_files",
            "def reorder_log_files(logs):\n"
            '    """Letter-logs before digit-logs; letters by content then id (LeetCode 937)."""\n'
            "    letters = []\n"
            "    digits = []\n"
            "    for log in logs:\n"
            "        ident, rest = log.split(' ', 1)\n"
            "        if rest[:1].isdigit():\n"
            "            digits.append(log)\n"
            "        else:\n"
            "            letters.append((rest, ident, log))\n"
            "    letters.sort()\n"
            "    return [log for _, _, log in letters] + digits\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 937\b|"
                    r"\breorder data in log files\b|"
                    r"\breorder log files\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            "dig1 8 1 5 1",
                            "let1 art can",
                            "dig2 3 6",
                            "let2 own kit dig",
                            "let3 art zero",
                        ],
                    ),
                    [
                        "let1 art can",
                        "let3 art zero",
                        "let2 own kit dig",
                        "dig1 8 1 5 1",
                        "dig2 3 6",
                    ],
                ),
                (
                    (
                        [
                            "a1 9 2 3 1",
                            "g1 act car",
                            "zo4 4 7",
                            "ab1 off key dog",
                            "a8 act zoo",
                        ],
                    ),
                    [
                        "g1 act car",
                        "a8 act zoo",
                        "ab1 off key dog",
                        "a1 9 2 3 1",
                        "zo4 4 7",
                    ],
                ),
            ),
        ),
        T(
            "mirror_reflection",
            "def mirror_reflection(p, q):\n"
            '    """Receptor hit by a corner laser in a mirrored room (LeetCode 858)."""\n'
            "    from math import gcd\n"
            "    g = gcd(int(p), int(q)) or 1\n"
            "    p //= g\n"
            "    q //= g\n"
            "    if p % 2 == 0:\n"
            "        return 2\n"
            "    if q % 2 == 0:\n"
            "        return 0\n"
            "    return 1\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 858\b|"
                    r"\bmirror reflection\b",
                    low,
                )
            ),
            (
                ((2, 1), 2),
                ((3, 1), 1),
            ),
        ),
        T(
            "largest_time_from_digits",
            "def largest_time_from_digits(arr):\n"
            '    """Largest valid HH:MM from four digits, or empty (LeetCode 949)."""\n'
            "    from itertools import permutations\n"
            "    best = ''\n"
            "    for perm in set(permutations(int(x) for x in arr)):\n"
            "        hh = perm[0] * 10 + perm[1]\n"
            "        mm = perm[2] * 10 + perm[3]\n"
            "        if hh < 24 and mm < 60:\n"
            "            cand = f'{hh:02d}:{mm:02d}'\n"
            "            if cand > best:\n"
            "                best = cand\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 949\b|"
                    r"\blargest time for given digits\b|"
                    r"\blargest time from digits\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4],), "23:41"),
                (([5, 5, 5, 5],), ""),
                (([0, 0, 0, 0],), "00:00"),
            ),
        ),
        T(
            "sum_even_after_queries",
            "def sum_even_after_queries(nums, queries):\n"
            '    """Even sum after each value update (LeetCode 985)."""\n'
            "    nums = list(nums)\n"
            "    even = sum(x for x in nums if x % 2 == 0)\n"
            "    out = []\n"
            "    for val, idx in queries:\n"
            "        if nums[idx] % 2 == 0:\n"
            "            even -= nums[idx]\n"
            "        nums[idx] += val\n"
            "        if nums[idx] % 2 == 0:\n"
            "            even += nums[idx]\n"
            "        out.append(even)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 985\b|"
                    r"\bsum of even numbers after queries\b|"
                    r"\beven numbers after queries\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4], [[1, 0], [-3, 1], [-4, 0], [2, 3]]), [8, 6, 2, 4]),
                (([1], [[4, 0]]), [0]),
            ),
        ),
        T(
            "broken_calc",
            "def broken_calc(start_value, target):\n"
            '    """Min *2 and -1 ops from start to target (LeetCode 991)."""\n'
            "    ops = 0\n"
            "    start_value = int(start_value)\n"
            "    target = int(target)\n"
            "    while target > start_value:\n"
            "        ops += 1\n"
            "        if target % 2 == 0:\n"
            "            target //= 2\n"
            "        else:\n"
            "            target += 1\n"
            "    return ops + start_value - target\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 991\b|"
                    r"\bbroken calculator\b",
                    low,
                )
            ),
            (
                ((2, 3), 2),
                ((5, 8), 2),
                ((3, 10), 3),
            ),
        ),
    ]
