"""Cycle 559: weighted interval scheduling + heapify natural-language coverage.

Closes probes that still fell through to fallback after Cycle 558 matcher
widening:
- weighted interval scheduling (classic DP / activity selection with weights)
- max-heapify / heapify array in-place

Matchers stay phrase-specific so job-scheduling (LC 1235) and heap_sort stay
on earlier packs.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "weighted_interval_scheduling",
            "def weighted_interval_scheduling(intervals):\n"
            '    """Max total weight of non-overlapping intervals.\n'
            "\n"
            "    intervals: list of (start, end, weight). Returns optimal weight.\n"
            '    """\n'
            "    if not intervals:\n"
            "        return 0\n"
            "    jobs = sorted(intervals, key=lambda x: x[1])\n"
            "    n = len(jobs)\n"
            "    ends = [j[1] for j in jobs]\n"
            "\n"
            "    def latest_non_conflict(i):\n"
            "        # rightmost j < i with ends[j] <= jobs[i].start\n"
            "        lo, hi = 0, i - 1\n"
            "        ans = -1\n"
            "        while lo <= hi:\n"
            "            mid = (lo + hi) // 2\n"
            "            if ends[mid] <= jobs[i][0]:\n"
            "                ans = mid\n"
            "                lo = mid + 1\n"
            "            else:\n"
            "                hi = mid - 1\n"
            "        return ans\n"
            "\n"
            "    dp = [0] * n\n"
            "    dp[0] = jobs[0][2]\n"
            "    for i in range(1, n):\n"
            "        incl = jobs[i][2]\n"
            "        j = latest_non_conflict(i)\n"
            "        if j >= 0:\n"
            "            incl += dp[j]\n"
            "        dp[i] = max(incl, dp[i - 1])\n"
            "    return dp[-1]\n",
            lambda low: bool(
                re.search(
                    r"\bweighted[-_ ]?interval[-_ ]?scheduling\b|"
                    r"\bweighted[-_ ]?activity[-_ ]?selection\b|"
                    r"\binterval[-_ ]?scheduling\b.{0,24}\bweight\b|"
                    r"\bweight(?:ed)?\b.{0,24}\binterval[-_ ]?scheduling\b|"
                    r"\bmax(?:imum)? (?:total )?weight\b.{0,40}\bnon[-_ ]?overlapping intervals?\b|"
                    r"\bweighted intervals?\b.{0,24}\b(?:schedule|select|dp)\b",
                    low,
                )
            )
            and "job" not in low
            and "stock" not in low,
            (
                (([(1, 3, 5), (2, 5, 6), (4, 6, 5), (6, 7, 4), (5, 8, 11), (7, 9, 2)],), 17),
                (([(1, 2, 1), (2, 3, 1), (3, 4, 1)],), 3),
                (([(1, 10, 100), (2, 3, 10), (4, 5, 10)],), 100),
                (([],), 0),
            ),
        ),
        T(
            "heapify",
            "def heapify(arr, heap_type=\"min\"):\n"
            '    """In-place binary heapify. heap_type is \"min\" or \"max\". Returns arr."""\n'
            "    a = list(arr)\n"
            "    n = len(a)\n"
            "    is_min = str(heap_type).lower() != \"max\"\n"
            "\n"
            "    def sift_down(i):\n"
            "        while True:\n"
            "            l, r = 2 * i + 1, 2 * i + 2\n"
            "            best = i\n"
            "            if is_min:\n"
            "                if l < n and a[l] < a[best]:\n"
            "                    best = l\n"
            "                if r < n and a[r] < a[best]:\n"
            "                    best = r\n"
            "            else:\n"
            "                if l < n and a[l] > a[best]:\n"
            "                    best = l\n"
            "                if r < n and a[r] > a[best]:\n"
            "                    best = r\n"
            "            if best == i:\n"
            "                break\n"
            "            a[i], a[best] = a[best], a[i]\n"
            "            i = best\n"
            "\n"
            "    for i in range(n // 2 - 1, -1, -1):\n"
            "        sift_down(i)\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\b(?:max[-_ ]?)?heapify\b|"
                    r"\bheapify (?:an? )?(?:array|list)\b|"
                    r"\bbuild (?:a )?(?:max[-_ ]?|min[-_ ]?)?heap (?:from|on|in)(?: an?)? (?:array|list)\b|"
                    r"\bin[-_ ]?place (?:max[-_ ]?|min[-_ ]?)?heap\b",
                    low,
                )
            )
            and "sort" not in low
            and "priority" not in low
            and not re.search(r"\bmax[-_ ]?heapify\b", low),
            (
                (([3, 1, 4, 2], "min"), [1, 2, 4, 3]),
                (([3, 1, 4, 2], "max"), [4, 2, 3, 1]),
                (([5], "min"), [5]),
                (([], "max"), []),
            ),
        ),
        T(
            "max_heapify",
            "def max_heapify(arr):\n"
            '    """In-place max-heapify of a list; returns the heapified list."""\n'
            "    a = list(arr)\n"
            "    n = len(a)\n"
            "\n"
            "    def sift_down(i):\n"
            "        while True:\n"
            "            l, r = 2 * i + 1, 2 * i + 2\n"
            "            largest = i\n"
            "            if l < n and a[l] > a[largest]:\n"
            "                largest = l\n"
            "            if r < n and a[r] > a[largest]:\n"
            "                largest = r\n"
            "            if largest == i:\n"
            "                break\n"
            "            a[i], a[largest] = a[largest], a[i]\n"
            "            i = largest\n"
            "\n"
            "    for i in range(n // 2 - 1, -1, -1):\n"
            "        sift_down(i)\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\bmax[-_ ]?heapify\b|"
                    r"\bheapify\b.{0,16}\bmax\b|"
                    r"\bmax[-_ ]?heapify (?:an? )?(?:array|list)\b",
                    low,
                )
            )
            and "sort" not in low,
            (
                (([3, 1, 4, 2],), [4, 2, 3, 1]),
                (([5, 3, 7, 1],), [7, 3, 5, 1]),
                (([10],), [10]),
            ),
        ),
    ]
