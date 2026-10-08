"""Cycle 504: unmatched write-a-function asks.

LeetCode 2418 / 2570 / 2614 / 2609 / 2711 / 2856 / 2523 / 2455.
Specific phrases only so sort_list and average do not steal them.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "sort_people",
            "def sort_people(names, heights):\n"
            '    """Sort names by descending height (LeetCode 2418)."""\n'
            "    order = sorted(range(len(names)), key=lambda i: -heights[i])\n"
            "    return [names[i] for i in order]\n",
            lambda low: "people" in low and "height" in low and "sort" in low,
            (
                ((["Mary", "John", "Emma"], [180, 165, 170]), ["Mary", "Emma", "John"]),
                ((["Alice", "Bob", "Bob"], [155, 185, 150]), ["Bob", "Alice", "Bob"]),
            ),
        ),
        T(
            "merge_arrays",
            "def merge_arrays(nums1, nums2):\n"
            '    """Merge two id-value arrays by summing values (LeetCode 2570)."""\n'
            "    totals = {}\n"
            "    for row in list(nums1) + list(nums2):\n"
            "        key, val = int(row[0]), int(row[1])\n"
            "        totals[key] = totals.get(key, 0) + val\n"
            "    return [[k, totals[k]] for k in sorted(totals)]\n",
            lambda low: (
                "2d" in low
                and "sum" in low
                and "merge" in low
                and "interval" not in low
            ),
            (
                (([[1, 2], [2, 3], [4, 5]], [[1, 4], [3, 2], [4, 1]]), [[1, 6], [2, 3], [3, 2], [4, 6]]),
                (([[2, 4], [3, 6], [5, 5]], [[1, 3], [4, 3]]), [[1, 3], [2, 4], [3, 6], [4, 3], [5, 5]]),
            ),
        ),
        T(
            "diagonal_prime",
            "def diagonal_prime(nums):\n"
            '    """Largest prime on either diagonal, else 0 (LeetCode 2614)."""\n'
            "    def is_prime(n):\n"
            "        if n < 2:\n"
            "            return False\n"
            "        if n % 2 == 0:\n"
            "            return n == 2\n"
            "        i = 3\n"
            "        while i * i <= n:\n"
            "            if n % i == 0:\n"
            "                return False\n"
            "            i += 2\n"
            "        return True\n"
            "    n = len(nums)\n"
            "    best = 0\n"
            "    for i in range(n):\n"
            "        for v in (nums[i][i], nums[i][n - 1 - i]):\n"
            "            v = int(v)\n"
            "            if is_prime(v) and v > best:\n"
            "                best = v\n"
            "    return best\n",
            lambda low: "prime" in low and "diagonal" in low and "distinct" not in low,
            (
                (([[1, 2, 3], [5, 6, 7], [9, 10, 11]],), 11),
                (([[1, 2, 3], [5, 17, 7], [9, 11, 10]],), 17),
            ),
        ),
        T(
            "longest_balanced_substring",
            "def longest_balanced_substring(s):\n"
            '    """Longest 0*1* binary substring with equal counts (LeetCode 2609)."""\n'
            "    s = str(s)\n"
            "    best = 0\n"
            "    i = 0\n"
            "    n = len(s)\n"
            "    while i < n:\n"
            "        zeros = 0\n"
            "        while i < n and s[i] == '0':\n"
            "            zeros += 1\n"
            "            i += 1\n"
            "        ones = 0\n"
            "        while i < n and s[i] == '1':\n"
            "            ones += 1\n"
            "            i += 1\n"
            "        best = max(best, 2 * min(zeros, ones))\n"
            "    return best\n",
            lambda low: "balanced" in low and "substring" in low,
            (
                (("01000111",), 6),
                (("00111",), 4),
                (("111",), 0),
            ),
        ),
        T(
            "difference_of_distinct",
            "def difference_of_distinct(grid):\n"
            '    """|distinct above-left minus below-right| on each diagonal (LeetCode 2711)."""\n'
            "    m = len(grid)\n"
            "    n = len(grid[0]) if m else 0\n"
            "    ans = [[0] * n for _ in range(m)]\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            top = set()\n"
            "            x, y = i - 1, j - 1\n"
            "            while x >= 0 and y >= 0:\n"
            "                top.add(grid[x][y])\n"
            "                x -= 1\n"
            "                y -= 1\n"
            "            bot = set()\n"
            "            x, y = i + 1, j + 1\n"
            "            while x < m and y < n:\n"
            "                bot.add(grid[x][y])\n"
            "                x += 1\n"
            "                y += 1\n"
            "            ans[i][j] = abs(len(top) - len(bot))\n"
            "    return ans\n",
            lambda low: "distinct" in low and "diagonal" in low,
            (
                (([[1, 2, 3], [3, 1, 5], [3, 2, 1]],), [[1, 1, 0], [1, 0, 1], [0, 1, 1]]),
            ),
        ),
        T(
            "minimum_length_after_removals",
            "def minimum_length_after_removals(nums):\n"
            '    """Length after removing different-value pairs (LeetCode 2856)."""\n'
            "    counts = {}\n"
            "    for x in nums:\n"
            "        counts[x] = counts.get(x, 0) + 1\n"
            "    n = len(nums)\n"
            "    freq = max(counts.values()) if counts else 0\n"
            "    if freq * 2 > n:\n"
            "        return freq * 2 - n\n"
            "    return n % 2\n",
            lambda low: "minimum length" in low and "removal" in low,
            (
                (([1, 2, 3, 4],), 0),
                (([1, 1, 2, 2, 3, 3],), 0),
                (([1, 1, 1, 1],), 4),
                (([1, 1, 2],), 1),
            ),
        ),
        T(
            "closest_primes",
            "def closest_primes(left, right):\n"
            '    """Closest prime pair in [left, right], else [-1, -1] (LeetCode 2523)."""\n'
            "    left, right = int(left), int(right)\n"
            "    if right < 2:\n"
            "        return [-1, -1]\n"
            "    prime = [True] * (right + 1)\n"
            "    prime[0] = prime[1] = False\n"
            "    i = 2\n"
            "    while i * i <= right:\n"
            "        if prime[i]:\n"
            "            for j in range(i * i, right + 1, i):\n"
            "                prime[j] = False\n"
            "        i += 1\n"
            "    vals = [k for k in range(max(left, 2), right + 1) if prime[k]]\n"
            "    if len(vals) < 2:\n"
            "        return [-1, -1]\n"
            "    best = (vals[1] - vals[0], vals[0], vals[1])\n"
            "    for a, b in zip(vals, vals[1:]):\n"
            "        if b - a < best[0]:\n"
            "            best = (b - a, a, b)\n"
            "    return [best[1], best[2]]\n",
            lambda low: "closest" in low and "prime" in low,
            (
                ((10, 19), [11, 13]),
                ((4, 6), [-1, -1]),
            ),
        ),
        T(
            "average_value",
            "def average_value(nums):\n"
            '    """Floor average of evens divisible by three (LeetCode 2455)."""\n'
            "    vals = [int(x) for x in nums if int(x) % 6 == 0]\n"
            "    if not vals:\n"
            "        return 0\n"
            "    return sum(vals) // len(vals)\n",
            lambda low: (
                "average" in low
                and "divisible" in low
                and ("three" in low or "3" in low)
            ),
            (
                (([1, 3, 6, 10, 12, 15],), 9),
                (([1, 2, 4, 7, 10],), 0),
            ),
        ),
    ]
