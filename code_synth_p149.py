"""Cycle 428: coding asks that still returned NotImplementedError stubs.

Matchers stay specific so kids-with-candies (1431), distribute candies (2928),
and minimum-cost candies (2144) keep their packs. Candy 135 only matches the
rating/leetcode-135 phrasing.
- candy (LC 135) alias for "leetcode 135"
- paint house (LC 256)
- out of boundary paths (LC 576)
- champagne tower (LC 799)
- new 21 game (LC 837)
- predict the winner (LC 486)
"""
from __future__ import annotations

import re

from code_synth import Template


def _id(low: str, num: str) -> bool:
    return bool(re.search(rf"(?<!\d){num}(?!\d)", low))


def _candy(low: str) -> bool:
    # "135" is a substring of 1351/1356; only the exact problem id counts.
    if re.search(r"\bleetcode 135\d", low):
        return False
    if any(
        s in low
        for s in (
            "greatest number of candies",
            "kids with",
            "2928",
            "2144",
            "discount",
            "distribute candies",
            "negative",
            "1 bits",
            "one bits",
        )
    ):
        return False
    if "limit" in low and "children" in low:
        return False
    return bool(re.search(r"\bleetcode 135\b", low)) or (
        "candy" in low and ("rating" in low or "neighbor" in low)
    )


def _paint(low: str) -> bool:
    return _id(low, "256") or "paint house" in low or "paint houses" in low


def _oob(low: str) -> bool:
    return _id(low, "576") or "out of boundary" in low or "out-of-boundary" in low


def _champ(low: str) -> bool:
    return _id(low, "799") or "champagne tower" in low


def _n21(low: str) -> bool:
    return _id(low, "837") or "new 21" in low or "new21" in low


def _pred(low: str) -> bool:
    return _id(low, "486") or "predict the winner" in low


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "candy",
            "def candy(ratings):\n"
            '    """Min candies so a higher rating gets more than its neighbors (LeetCode 135)."""\n'
            "    ratings = list(ratings)\n"
            "    n = len(ratings)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    give = [1] * n\n"
            "    for i in range(1, n):\n"
            "        if ratings[i] > ratings[i - 1]:\n"
            "            give[i] = give[i - 1] + 1\n"
            "    for i in range(n - 2, -1, -1):\n"
            "        if ratings[i] > ratings[i + 1]:\n"
            "            give[i] = max(give[i], give[i + 1] + 1)\n"
            "    return sum(give)\n",
            _candy,
            [
                (([1, 0, 2],), 5),
                (([1, 2, 2],), 4),
                (([1, 3, 2, 2, 1],), 7),
            ],
        ),
        T(
            "min_cost_paint_house",
            "def minCost(costs):\n"
            '    """Min cost to paint houses with no two adjacent the same color (LeetCode 256)."""\n'
            "    if not costs:\n"
            "        return 0\n"
            "    a = b = c = 0\n"
            "    for cost in costs:\n"
            "        x, y, z = int(cost[0]), int(cost[1]), int(cost[2])\n"
            "        a, b, c = x + min(b, c), y + min(a, c), z + min(a, b)\n"
            "    return min(a, b, c)\n",
            _paint,
            [
                (([[17, 2, 17], [16, 16, 5], [14, 3, 19]],), 10),
                (([[7, 6, 2]],), 2),
                (([],), 0),
            ],
        ),
        T(
            "find_paths",
            "def findPaths(m, n, maxMove, startRow, startColumn):\n"
            '    """Paths that leave an m x n grid within maxMove steps (LeetCode 576)."""\n'
            "    mod = 10 ** 9 + 7\n"
            "    m, n = int(m), int(n)\n"
            "    dp = [[0] * n for _ in range(m)]\n"
            "    dp[int(startRow)][int(startColumn)] = 1\n"
            "    ans = 0\n"
            "    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))\n"
            "    for _ in range(int(maxMove)):\n"
            "        nxt = [[0] * n for _ in range(m)]\n"
            "        for i in range(m):\n"
            "            for j in range(n):\n"
            "                if not dp[i][j]:\n"
            "                    continue\n"
            "                for di, dj in dirs:\n"
            "                    ni, nj = i + di, j + dj\n"
            "                    if ni < 0 or ni >= m or nj < 0 or nj >= n:\n"
            "                        ans = (ans + dp[i][j]) % mod\n"
            "                    else:\n"
            "                        nxt[ni][nj] = (nxt[ni][nj] + dp[i][j]) % mod\n"
            "        dp = nxt\n"
            "    return ans\n",
            _oob,
            [
                ((2, 2, 2, 0, 0), 6),
                ((1, 3, 3, 0, 1), 12),
                ((1, 1, 0, 0, 0), 0),
            ],
        ),
        T(
            "champagne_tower",
            "def champagneTower(poured, query_row, query_glass):\n"
            '    """Fraction of the query glass that is full (LeetCode 799)."""\n'
            "    row = [float(poured)]\n"
            "    for r in range(int(query_row)):\n"
            "        nxt = [0.0] * (r + 2)\n"
            "        for j, vol in enumerate(row):\n"
            "            excess = vol - 1.0\n"
            "            if excess > 0:\n"
            "                nxt[j] += excess / 2.0\n"
            "                nxt[j + 1] += excess / 2.0\n"
            "        row = nxt\n"
            "    return min(1.0, row[int(query_glass)])\n",
            _champ,
            [
                ((1, 1, 1), 0.0),
                ((2, 1, 1), 0.5),
                ((100000009, 33, 17), 1.0),
            ],
        ),
        T(
            "new21_game",
            "def new21Game(n, k, maxPts):\n"
            '    """Probability of stopping at or below n (LeetCode 837)."""\n'
            "    n, k, maxPts = int(n), int(k), int(maxPts)\n"
            "    if k == 0 or n >= k - 1 + maxPts:\n"
            "        return 1.0\n"
            "    dp = [0.0] * (n + 1)\n"
            "    dp[0] = 1.0\n"
            "    window = 1.0\n"
            "    ans = 0.0\n"
            "    for i in range(1, n + 1):\n"
            "        dp[i] = window / maxPts\n"
            "        if i < k:\n"
            "            window += dp[i]\n"
            "        else:\n"
            "            ans += dp[i]\n"
            "        if i >= maxPts:\n"
            "            window -= dp[i - maxPts]\n"
            "    return ans\n",
            _n21,
            [
                ((10, 1, 10), 1.0),
                ((6, 1, 10), 0.6),
                ((21, 17, 10), 0.7327777870686082),
            ],
        ),
        T(
            "predict_the_winner",
            "def predictTheWinner(nums):\n"
            '    """True if player 1 score >= player 2 with optimal play (LeetCode 486)."""\n'
            "    nums = [int(x) for x in nums]\n"
            "    n = len(nums)\n"
            "    dp = [0] * n\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        dp[i] = nums[i]\n"
            "        for j in range(i + 1, n):\n"
            "            dp[j] = max(nums[i] - dp[j], nums[j] - dp[j - 1])\n"
            "    return dp[-1] >= 0\n",
            _pred,
            [
                (([1, 5, 2],), False),
                (([1, 5, 233, 7],), True),
                (([1],), True),
            ],
        ),
    ]
