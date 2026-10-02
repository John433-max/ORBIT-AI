"""Cycle 370: array-zero ops, recolors, limited-sum subsequence, equal frequency, hardest worker, valid clocks.

2418 / 2341 / 2351 / 2367 / 2395 / 2399 / 2409 / 2413 / 2427 / 2441 already matched
earlier packs. These six phrases were unmatched stubs.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "minimum_operations_array_zero",
            "def minimum_operations_array_zero(nums):\n"
            '    """Ops to zero an array by subtracting a positive x (LeetCode 2357)."""\n'
            "    return len({x for x in nums if x})\n"
            "\n"
            "def minimumOperations(nums):\n"
            "    return minimum_operations_array_zero(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bmake array zero by subtracting\b|"
                    r"\bsubtracting equal amounts\b|"
                    r"\bleetcode 2357\b",
                    low,
                )
            ),
            (
                (([1, 5, 0, 3, 5],), 3),
                (([0],), 0),
                (([1, 2, 3, 4],), 4),
            ),
        ),
        T(
            "minimum_recolors",
            "def minimum_recolors(blocks, k):\n"
            '    """Min white recolors for k consecutive black blocks (LeetCode 2379)."""\n'
            "    window = blocks[:k].count('W')\n"
            "    best = window\n"
            "    for i in range(k, len(blocks)):\n"
            "        window += (blocks[i] == 'W') - (blocks[i - k] == 'W')\n"
            "        if window < best:\n"
            "            best = window\n"
            "    return best\n"
            "\n"
            "def minimumRecolors(blocks, k):\n"
            "    return minimum_recolors(blocks, k)\n",
            lambda low: bool(
                re.search(
                    r"\bminimum recolors\b|"
                    r"\bk consecutive black\b|"
                    r"\bleetcode 2379\b",
                    low,
                )
            ),
            (
                (("WBBWWBBWBW", 7), 3),
                (("WBWBBBW", 2), 0),
                (("B", 1), 0),
            ),
        ),
        T(
            "answer_queries_limited_sum",
            "def answer_queries_limited_sum(nums, queries):\n"
            '    """Longest subsequence size with sum <= each query (LeetCode 2389)."""\n'
            "    prefix = []\n"
            "    total = 0\n"
            "    for x in sorted(nums):\n"
            "        total += x\n"
            "        prefix.append(total)\n"
            "    out = []\n"
            "    for q in queries:\n"
            "        lo, hi = 0, len(prefix)\n"
            "        while lo < hi:\n"
            "            mid = (lo + hi) // 2\n"
            "            if prefix[mid] <= q:\n"
            "                lo = mid + 1\n"
            "            else:\n"
            "                hi = mid\n"
            "        out.append(lo)\n"
            "    return out\n"
            "\n"
            "def answerQueries(nums, queries):\n"
            "    return answer_queries_limited_sum(nums, queries)\n",
            lambda low: bool(
                re.search(
                    r"\blongest subsequence with limited sum\b|"
                    r"\blimited sum\b|"
                    r"\bleetcode 2389\b",
                    low,
                )
            ),
            (
                (([4, 5, 2, 1], [3, 10, 21]), [2, 3, 4]),
                (([2, 3, 4, 5], [1]), [0]),
            ),
        ),
        T(
            "equal_frequency",
            "def equal_frequency(word):\n"
            '    """True if deleting one letter equalizes remaining frequencies (LeetCode 2423)."""\n'
            "    from collections import Counter\n"
            "    base = Counter(word)\n"
            "    for ch in list(base):\n"
            "        cnt = base.copy()\n"
            "        cnt[ch] -= 1\n"
            "        if cnt[ch] == 0:\n"
            "            del cnt[ch]\n"
            "        if cnt and len(set(cnt.values())) == 1:\n"
            "            return True\n"
            "    return False\n"
            "\n"
            "def equalFrequency(word):\n"
            "    return equal_frequency(word)\n",
            lambda low: bool(
                re.search(
                    r"\bremove letter to equalize frequency\b|"
                    r"\bequalize frequency\b|"
                    r"\bleetcode 2423\b",
                    low,
                )
            ),
            (
                (("abcc",), True),
                (("aazz",), False),
                (("abbcc",), True),
            ),
        ),
        T(
            "hardest_worker",
            "def hardest_worker(n, logs):\n"
            '    """Employee id with the longest task; ties take the smaller id (LeetCode 2432)."""\n'
            "    best_id = logs[0][0]\n"
            "    best = logs[0][1]\n"
            "    prev = logs[0][1]\n"
            "    for i in range(1, len(logs)):\n"
            "        dur = logs[i][1] - prev\n"
            "        prev = logs[i][1]\n"
            "        eid = logs[i][0]\n"
            "        if dur > best or (dur == best and eid < best_id):\n"
            "            best = dur\n"
            "            best_id = eid\n"
            "    return best_id\n"
            "\n"
            "def hardestWorker(n, logs):\n"
            "    return hardest_worker(n, logs)\n",
            lambda low: bool(
                re.search(
                    r"\bworked on the longest task\b|"
                    r"\blongest task\b|"
                    r"\bleetcode 2432\b",
                    low,
                )
            ),
            (
                ((10, [[0, 3], [2, 5], [0, 9], [1, 15]]), 1),
                ((26, [[1, 1], [3, 7], [2, 12], [7, 17]]), 3),
                ((2, [[0, 10], [1, 20]]), 0),
            ),
        ),
        T(
            "count_valid_clock_times",
            "def count_valid_clock_times(time):\n"
            '    """Valid hh:mm fillings of ? digits (LeetCode 2437)."""\n'
            "    hh, mm = time.split(':')\n"
            "    def _ok(pattern, limit):\n"
            "        count = 0\n"
            "        for i in range(limit):\n"
            "            s = f'{i:02d}'\n"
            "            if (pattern[0] in ('?', s[0])) and (pattern[1] in ('?', s[1])):\n"
            "                count += 1\n"
            "        return count\n"
            "    return _ok(hh, 24) * _ok(mm, 60)\n"
            "\n"
            "def countTime(time):\n"
            "    return count_valid_clock_times(time)\n",
            lambda low: bool(
                re.search(
                    r"\bvalid clock times\b|"
                    r"\bnumber of valid clock\b|"
                    r"\bleetcode 2437\b",
                    low,
                )
            ),
            (
                (("?5:00",), 2),
                (("0?:0?",), 100),
                (("??:??",), 1440),
            ),
        ),
    ]
