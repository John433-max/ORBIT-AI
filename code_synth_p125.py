"""Cycle 403: interval asks that stubbed or hit the wrong template.

Official examples:
- LeetCode 1288 Remove Covered Intervals: [[1,4],[3,6],[2,8]] -> 2; [[1,4],[2,3]] -> 1.
- LeetCode 3169 Count Days Without Meetings: days=10 meetings=[[5,7],[1,3],[9,10]] -> 2;
  days=5 meetings=[[2,4],[1,3]] -> 1; days=6 meetings=[[1,6]] -> 0.
- LeetCode 452 Minimum Number of Arrows to Burst Balloons:
  [[10,16],[2,8],[1,6],[7,12]] -> 2; [[1,2],[3,4],[5,6],[7,8]] -> 4;
  [[1,2],[2,3],[3,4],[4,5]] -> 2.
- LeetCode 57 Insert Interval: [[1,3],[6,9]] + [2,5] -> [[1,5],[6,9]];
  [[1,2],[3,5],[6,7],[8,10],[12,16]] + [4,8] -> [[1,2],[3,10],[12,16]].
- LeetCode 986 Interval List Intersections:
  [[0,2],[5,10],[13,23],[24,25]] x [[1,5],[8,12],[15,24],[25,26]]
  -> [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]].
- LeetCode 435 Non-overlapping / Erase Overlap Intervals:
  [[1,2],[2,3],[3,4],[1,3]] -> 1; [[1,2],[1,2],[1,2]] -> 2; [[1,2],[2,3]] -> 0.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "remove_covered_intervals",
            "def remove_covered_intervals(intervals):\n"
            '    """Count intervals not covered by another (LeetCode 1288)."""\n'
            "    items = sorted(((int(a), int(b)) for a, b in intervals), key=lambda x: (x[0], -x[1]))\n"
            "    remain = 0\n"
            "    end = -1\n"
            "    for _lo, hi in items:\n"
            "        if hi > end:\n"
            "            remain += 1\n"
            "            end = hi\n"
            "    return remain\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1288\b", low)
                or "remove covered intervals" in low
                or "covered intervals" in low
            ),
            examples=(
                (([[1, 4], [3, 6], [2, 8]],), 2),
                (([[1, 4], [2, 3]],), 1),
            ),
        ),
        T(
            "count_days",
            "def count_days(days, meetings):\n"
            '    """Days with no meeting, inclusive ranges (LeetCode 3169)."""\n'
            "    days = int(days)\n"
            "    items = sorted((int(a), int(b)) for a, b in meetings)\n"
            "    busy = 0\n"
            "    cur_lo = cur_hi = None\n"
            "    for lo, hi in items:\n"
            "        if cur_lo is None:\n"
            "            cur_lo, cur_hi = lo, hi\n"
            "        elif lo <= cur_hi + 1:\n"
            "            cur_hi = max(cur_hi, hi)\n"
            "        else:\n"
            "            busy += cur_hi - cur_lo + 1\n"
            "            cur_lo, cur_hi = lo, hi\n"
            "    if cur_lo is not None:\n"
            "        busy += cur_hi - cur_lo + 1\n"
            "    return days - busy\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3169\b", low)
                or "days without meetings" in low
                or "count days without" in low
            ),
            examples=(
                ((10, [[5, 7], [1, 3], [9, 10]]), 2),
                ((5, [[2, 4], [1, 3]]), 1),
                ((6, [[1, 6]]), 0),
            ),
        ),
        T(
            "find_min_arrow_shots",
            "def find_min_arrow_shots(points):\n"
            '    """Minimum arrows to burst all balloons (LeetCode 452)."""\n'
            "    items = sorted(((int(a), int(b)) for a, b in points), key=lambda x: x[1])\n"
            "    if not items:\n"
            "        return 0\n"
            "    arrows = 1\n"
            "    end = items[0][1]\n"
            "    for lo, hi in items[1:]:\n"
            "        if lo > end:\n"
            "            arrows += 1\n"
            "            end = hi\n"
            "    return arrows\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*452\b", low)
                or "minimum number of arrows" in low
                or "min arrow" in low
                or ("arrow" in low and "balloon" in low)
            ),
            examples=(
                (([[10, 16], [2, 8], [1, 6], [7, 12]],), 2),
                (([[1, 2], [3, 4], [5, 6], [7, 8]],), 4),
                (([[1, 2], [2, 3], [3, 4], [4, 5]],), 2),
            ),
        ),
        T(
            "insert_interval",
            "def insert_interval(intervals, newInterval):\n"
            '    """Insert and merge one interval (LeetCode 57)."""\n'
            "    lo, hi = int(newInterval[0]), int(newInterval[1])\n"
            "    out = []\n"
            "    placed = False\n"
            "    for a, b in intervals:\n"
            "        a, b = int(a), int(b)\n"
            "        if b < lo:\n"
            "            out.append([a, b])\n"
            "        elif a > hi:\n"
            "            if not placed:\n"
            "                out.append([lo, hi])\n"
            "                placed = True\n"
            "            out.append([a, b])\n"
            "        else:\n"
            "            lo = min(lo, a)\n"
            "            hi = max(hi, b)\n"
            "    if not placed:\n"
            "        out.append([lo, hi])\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*57\b", low)
                or "insert interval" in low
                or "insert a new interval" in low
            ),
            examples=(
                (([[1, 3], [6, 9]], [2, 5]), [[1, 5], [6, 9]]),
                (([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]), [[1, 2], [3, 10], [12, 16]]),
            ),
        ),
        T(
            "interval_intersection",
            "def interval_intersection(firstList, secondList):\n"
            '    """Intersection of two interval lists (LeetCode 986)."""\n'
            "    i = j = 0\n"
            "    out = []\n"
            "    a = [[int(x), int(y)] for x, y in firstList]\n"
            "    b = [[int(x), int(y)] for x, y in secondList]\n"
            "    while i < len(a) and j < len(b):\n"
            "        lo = max(a[i][0], b[j][0])\n"
            "        hi = min(a[i][1], b[j][1])\n"
            "        if lo <= hi:\n"
            "            out.append([lo, hi])\n"
            "        if a[i][1] < b[j][1]:\n"
            "            i += 1\n"
            "        else:\n"
            "            j += 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*986\b", low)
                or "interval list intersection" in low
                or "interval intersections" in low
            ),
            examples=(
                (
                    (
                        [[0, 2], [5, 10], [13, 23], [24, 25]],
                        [[1, 5], [8, 12], [15, 24], [25, 26]],
                    ),
                    [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]],
                ),
                (([], [[1, 5]]), []),
            ),
        ),
        T(
            "erase_overlap_intervals",
            "def erase_overlap_intervals(intervals):\n"
            '    """Minimum removals so intervals do not overlap (LeetCode 435)."""\n'
            "    items = sorted(((int(a), int(b)) for a, b in intervals), key=lambda x: x[1])\n"
            "    if not items:\n"
            "        return 0\n"
            "    end = items[0][1]\n"
            "    keep = 1\n"
            "    for lo, hi in items[1:]:\n"
            "        if lo >= end:\n"
            "            keep += 1\n"
            "            end = hi\n"
            "    return len(items) - keep\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*435\b", low)
                or "erase overlap" in low
                or "non-overlapping intervals" in low
                or "non overlapping intervals" in low
            ),
            examples=(
                (([[1, 2], [2, 3], [3, 4], [1, 3]],), 1),
                (([[1, 2], [1, 2], [1, 2]],), 2),
                (([[1, 2], [2, 3]],), 0),
            ),
        ),
    ]
