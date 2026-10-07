"""Cycle 330: unused Easy — max pos/neg count / event conflict /
bit flips / two-array difference / hills+valleys / 3-same-digit."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "maximum_count",
            "def maximum_count(nums):\n"
            '    """Max of (#positives, #negatives); zeros count for neither (LeetCode 2529)."""\n'
            "    pos = neg = 0\n"
            "    for x in nums:\n"
            "        if x > 0:\n"
            "            pos += 1\n"
            "        elif x < 0:\n"
            "            neg += 1\n"
            "    return pos if pos >= neg else neg\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum_count\b|"
                    r"\bmaximum[_ ]count[_ ]of[_ ]positive\b|"
                    r"\bpositive[_ ]integer[_ ]and[_ ]negative\b|"
                    r"\bleetcode[_ ]2529\b",
                    low,
                )
            ),
            (
                (([-2, -1, -1, 1, 2, 3],), 3),
                (([-3, -2, -1, 0, 0, 1, 2],), 3),
                (([5, 20, 66, 1314],), 4),
            ),
        ),
        T(
            "have_conflict",
            "def have_conflict(event1, event2):\n"
            '    """True if two inclusive HH:MM events overlap (LeetCode 2446)."""\n'
            "    return event1[0] <= event2[1] and event2[0] <= event1[1]\n",
            lambda low: bool(
                re.search(
                    r"\bhave_conflict\b|"
                    r"\btwo[_ ]events[_ ]have[_ ]conflict\b|"
                    r"\bevents have conflict\b|"
                    r"\bdetermine[_ ]if[_ ]two[_ ]events[_ ]have[_ ]conflict\b|"
                    r"\bleetcode[_ ]2446\b",
                    low,
                )
            ),
            (
                ((["01:15", "02:00"], ["02:00", "03:00"]), True),
                ((["01:00", "02:00"], ["01:20", "03:00"]), True),
                ((["10:00", "11:00"], ["14:00", "15:00"]), False),
            ),
        ),
        T(
            "min_bit_flips",
            "def min_bit_flips(start, goal):\n"
            '    """Hamming distance between start and goal bit patterns (LeetCode 2220)."""\n'
            "    x = start ^ goal\n"
            "    n = 0\n"
            "    while x:\n"
            "        n += x & 1\n"
            "        x >>= 1\n"
            "    return n\n",
            lambda low: bool(
                re.search(
                    r"\bmin_bit_flips\b|"
                    r"\bminimum[_ ]bit[_ ]flips[_ ]to[_ ]convert\b|"
                    r"\bbit[_ ]flips[_ ]to[_ ]convert[_ ]number\b|"
                    r"\bleetcode[_ ]2220\b",
                    low,
                )
            ),
            (
                ((10, 7), 3),
                ((3, 4), 3),
            ),
        ),
        T(
            "find_difference",
            "def find_difference(nums1, nums2):\n"
            '    """[nums1-only values, nums2-only values] as unique lists (LeetCode 2215)."""\n'
            "    a, b = set(nums1), set(nums2)\n"
            "    return [sorted(a - b), sorted(b - a)]\n",
            lambda low: bool(
                re.search(
                    r"\bfind_difference\b|"
                    r"\bfind[_ ]the[_ ]difference[_ ]of[_ ]two[_ ]arrays\b|"
                    r"\bdifference[_ ]of[_ ]two[_ ]arrays\b|"
                    r"\bleetcode[_ ]2215\b",
                    low,
                )
            ),
            (
                (([1, 2, 3], [2, 4, 6]), [[1, 3], [4, 6]]),
                (([1, 2, 3, 3], [1, 1, 2, 2]), [[3], []]),
            ),
        ),
        T(
            "count_hill_valley",
            "def count_hill_valley(nums):\n"
            '    """Count hills and valleys after collapsing equal neighbors (LeetCode 2210)."""\n'
            "    compact = [nums[0]]\n"
            "    for x in nums[1:]:\n"
            "        if x != compact[-1]:\n"
            "            compact.append(x)\n"
            "    n = 0\n"
            "    for i in range(1, len(compact) - 1):\n"
            "        left, mid, right = compact[i - 1], compact[i], compact[i + 1]\n"
            "        if (mid > left and mid > right) or (mid < left and mid < right):\n"
            "            n += 1\n"
            "    return n\n",
            lambda low: bool(
                re.search(
                    r"\bcount_hill_valley\b|"
                    r"\bcount[_ ]hills[_ ]and[_ ]valleys\b|"
                    r"\bhills[_ ]and[_ ]valleys[_ ]in[_ ]an[_ ]array\b|"
                    r"\bleetcode[_ ]2210\b",
                    low,
                )
            ),
            (
                (([2, 4, 1, 1, 6, 5],), 3),
                (([6, 6, 5, 5, 4, 1],), 0),
            ),
        ),
        T(
            "largest_good_integer",
            "def largest_good_integer(num):\n"
            '    """Largest 3-same-digit substring in num, else empty (LeetCode 2264)."""\n'
            "    best = ''\n"
            "    for i in range(len(num) - 2):\n"
            "        if num[i] == num[i + 1] == num[i + 2]:\n"
            "            trip = num[i : i + 3]\n"
            "            if trip > best:\n"
            "                best = trip\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blargest_good_integer\b|"
                    r"\blargest[_ ]3[_ ]same[_ ]digit\b|"
                    r"\blargest[_ ]good[_ ]integer\b|"
                    r"\bleetcode[_ ]2264\b",
                    low,
                )
            ),
            (
                (("6777133339",), "777"),
                (("2300019",), "000"),
                (("42352338",), ""),
            ),
        ),
    ]
