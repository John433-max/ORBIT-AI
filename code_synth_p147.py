"""Cycle 425: interval DP, game, and weighted-interval asks still unmatched after p146.

Matchers stay phrase-specific so palindrome partitioning (all cuts) and stock
"best time to buy" stay on earlier packs.
- strange printer (LC 664)
- minimum cost to cut a stick (LC 1547)
- cat and mouse (LC 913)
- super egg drop (LC 887)
- palindrome partitioning II / min cuts (LC 132)
- maximum profit in job scheduling (LC 1235)
"""
from __future__ import annotations

from code_synth import Template


def _printer(low: str) -> bool:
    return "strange printer" in low


def _stick(low: str) -> bool:
    return "cut a stick" in low or "cost to cut a stick" in low or "cut stick" in low


def _cat(low: str) -> bool:
    return "cat and mouse" in low and "ii" not in low and "2" not in low.split()


def _egg(low: str) -> bool:
    return "egg drop" in low or "super egg" in low


def _min_cut(low: str) -> bool:
    return (
        "palindrome partitioning ii" in low
        or "palindrome partition ii" in low
        or "minimum cuts" in low and "palindrome" in low
        or "min cut" in low and "palindrome" in low
    )


def _jobs(low: str) -> bool:
    return "job scheduling" in low or ("maximum profit" in low and "job" in low)


def templates() -> list[Template]:
    return [
        Template(
            "strange_printer",
            "def strangePrinter(s):\n"
            '    """Fewest turns for the strange printer (LeetCode 664)."""\n'
            "    n = len(s)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    dp = [[n] * n for _ in range(n)]\n"
            "    for i in range(n):\n"
            "        dp[i][i] = 1\n"
            "    for j in range(n):\n"
            "        for i in range(j, -1, -1):\n"
            "            for k in range(i, j):\n"
            "                same = 1 if s[k] == s[j] else 0\n"
            "                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] - same)\n"
            "    return dp[0][n - 1]\n",
            _printer,
            (
                (("aaabbb",), 2),
                (("aba",), 2),
            ),
        ),
        Template(
            "min_cost_cut_stick",
            "def minCost(n, cuts):\n"
            '    """Min cost to cut a stick at the given positions (LeetCode 1547)."""\n'
            "    points = sorted(set(cuts) | {0, n})\n"
            "    m = len(points)\n"
            "    dp = [[0] * m for _ in range(m)]\n"
            "    for length in range(2, m):\n"
            "        for i in range(m - length):\n"
            "            j = i + length\n"
            "            best = min(dp[i][k] + dp[k][j] for k in range(i + 1, j))\n"
            "            dp[i][j] = best + points[j] - points[i]\n"
            "    return dp[0][m - 1]\n",
            _stick,
            (
                ((7, [1, 3, 4, 5]), 16),
                ((9, [5, 6, 1, 4, 2]), 22),
            ),
        ),
        Template(
            "cat_mouse_game",
            "def catMouseGame(graph):\n"
            '    """Cat and mouse on a graph; 1 mouse, 2 cat, 0 draw (LeetCode 913)."""\n'
            "    n = len(graph)\n"
            "    memo = {}\n"
            "\n"
            "    def dp(mouse, cat, turns):\n"
            "        key = (mouse, cat, turns)\n"
            "        if key in memo:\n"
            "            return memo[key]\n"
            "        if turns == 2 * n:\n"
            "            memo[key] = 0\n"
            "            return 0\n"
            "        if mouse == 0:\n"
            "            memo[key] = 1\n"
            "            return 1\n"
            "        if mouse == cat:\n"
            "            memo[key] = 2\n"
            "            return 2\n"
            "        if turns % 2 == 0:\n"
            "            draw = False\n"
            "            for nxt in graph[mouse]:\n"
            "                res = dp(nxt, cat, turns + 1)\n"
            "                if res == 1:\n"
            "                    memo[key] = 1\n"
            "                    return 1\n"
            "                if res == 0:\n"
            "                    draw = True\n"
            "            memo[key] = 0 if draw else 2\n"
            "            return memo[key]\n"
            "        draw = False\n"
            "        for nxt in graph[cat]:\n"
            "            if nxt == 0:\n"
            "                continue\n"
            "            res = dp(mouse, nxt, turns + 1)\n"
            "            if res == 2:\n"
            "                memo[key] = 2\n"
            "                return 2\n"
            "            if res == 0:\n"
            "                draw = True\n"
            "        memo[key] = 0 if draw else 1\n"
            "        return memo[key]\n"
            "\n"
            "    return dp(1, 2, 0)\n",
            _cat,
            (
                (([[2, 5], [3], [0, 4, 5], [1, 4, 5], [2, 3], [0, 2, 3]],), 0),
                (([[1, 3], [0], [3], [0, 2]],), 1),
            ),
        ),
        Template(
            "super_egg_drop",
            "def superEggDrop(k, n):\n"
            '    """Min worst-case drops with k eggs and n floors (LeetCode 887)."""\n'
            "    dp = [[0] * (k + 1) for _ in range(n + 1)]\n"
            "    for moves in range(1, n + 1):\n"
            "        for eggs in range(1, k + 1):\n"
            "            dp[moves][eggs] = dp[moves - 1][eggs - 1] + dp[moves - 1][eggs] + 1\n"
            "        if dp[moves][k] >= n:\n"
            "            return moves\n"
            "    return n\n",
            _egg,
            (
                ((1, 2), 2),
                ((2, 6), 3),
                ((3, 14), 4),
            ),
        ),
        Template(
            "palindrome_partition_ii",
            "def minCut(s):\n"
            '    """Minimum cuts so every piece is a palindrome (LeetCode 132)."""\n'
            "    n = len(s)\n"
            "    pal = [[False] * n for _ in range(n)]\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        for j in range(i, n):\n"
            "            if s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1]):\n"
            "                pal[i][j] = True\n"
            "    cut = [0] * n\n"
            "    for i in range(n):\n"
            "        if pal[0][i]:\n"
            "            continue\n"
            "        cut[i] = min(cut[j] + 1 for j in range(i) if pal[j + 1][i])\n"
            "    return cut[-1]\n",
            _min_cut,
            (
                (("aab",), 1),
                (("a",), 0),
                (("ab",), 1),
            ),
        ),
        Template(
            "job_scheduling_profit",
            "def jobScheduling(startTime, endTime, profit):\n"
            '    """Max profit of non-overlapping jobs (LeetCode 1235)."""\n'
            "    jobs = sorted(zip(endTime, startTime, profit))\n"
            "    ends = []\n"
            "    best = []\n"
            "    for end, start, pay in jobs:\n"
            "        lo, hi = 0, len(ends)\n"
            "        while lo < hi:\n"
            "            mid = (lo + hi) // 2\n"
            "            if ends[mid] <= start:\n"
            "                lo = mid + 1\n"
            "            else:\n"
            "                hi = mid\n"
            "        take = pay + (best[lo - 1] if lo else 0)\n"
            "        cur = max(take, best[-1] if best else 0)\n"
            "        ends.append(end)\n"
            "        best.append(cur)\n"
            "    return best[-1] if best else 0\n",
            _jobs,
            (
                (([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]), 120),
                (([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]), 150),
                (([1, 1, 1], [2, 3, 4], [5, 6, 4]), 6),
            ),
        ),
    ]
