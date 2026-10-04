"""Cycle 427: hard asks that still drafted or mis-routed after p147.

Matchers require the II / substring / supersequence / triangulation phrase so
cat-and-mouse (913), distinct subsequences (115), and longest palindromic
subsequence stay on earlier packs.
- cat and mouse II (LC 1728)
- minimum cost to merge stones (LC 1000)
- longest palindromic substring (LC 5)
- shortest common supersequence (LC 1092)
- distinct subsequences II (LC 940)
- minimum score triangulation (LC 1039)
"""
from __future__ import annotations

from code_synth import Template


def _cat_ii(low: str) -> bool:
    return (
        "1728" in low
        or "cat and mouse ii" in low
        or "cat and mouse 2" in low
        or ("cat and mouse" in low and " ii" in low)
    )


def _stones(low: str) -> bool:
    return "merge stones" in low or ("merge" in low and "stones" in low and "cost" in low)


def _substr(low: str) -> bool:
    return "palindromic substring" in low or "palindrome substring" in low


def _scs(low: str) -> bool:
    return "common supersequence" in low or "shortest common supersequence" in low


def _ds2(low: str) -> bool:
    return "940" in low or (
        "distinct subsequence" in low and (" ii" in low or "2" in low.split())
    )


def _tri(low: str) -> bool:
    return "triangulation" in low or ("minimum score" in low and "polygon" in low)


def templates() -> list[Template]:
    return [
        Template(
            "cat_mouse_ii",
            "def canMouseWin(grid, catJump, mouseJump):\n"
            '    """Mouse win under optimal play (LeetCode 1728)."""\n'
            "    import sys\n"
            "    sys.setrecursionlimit(8000)\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "\n"
            "    def locate(ch):\n"
            "        for i, row in enumerate(grid):\n"
            "            j = row.find(ch)\n"
            "            if j >= 0:\n"
            "                return i * cols + j\n"
            "        return -1\n"
            "\n"
            "    start_m, start_c, food = locate('M'), locate('C'), locate('F')\n"
            "    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))\n"
            "\n"
            "    def jumps(pos, limit):\n"
            "        r, c = divmod(pos, cols)\n"
            "        out = [pos]\n"
            "        for dr, dc in dirs:\n"
            "            for step in range(1, limit + 1):\n"
            "                nr, nc = r + dr * step, c + dc * step\n"
            "                if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == '#':\n"
            "                    break\n"
            "                out.append(nr * cols + nc)\n"
            "        return out\n"
            "\n"
            "    memo = {}\n"
            "\n"
            "    def mouse_wins(m, c, turn):\n"
            "        if turn >= 1000:\n"
            "            return False\n"
            "        key = (m, c, turn)\n"
            "        if key in memo:\n"
            "            return memo[key]\n"
            "        if turn % 2 == 0:\n"
            "            ans = False\n"
            "            for nm in jumps(m, mouseJump):\n"
            "                if nm == food:\n"
            "                    ans = True\n"
            "                    break\n"
            "                if nm == c:\n"
            "                    continue\n"
            "                if mouse_wins(nm, c, turn + 1):\n"
            "                    ans = True\n"
            "                    break\n"
            "        else:\n"
            "            ans = True\n"
            "            for nc in jumps(c, catJump):\n"
            "                if nc == food or nc == m or not mouse_wins(m, nc, turn + 1):\n"
            "                    ans = False\n"
            "                    break\n"
            "        memo[key] = ans\n"
            "        return ans\n"
            "\n"
            "    return mouse_wins(start_m, start_c, 0)\n",
            _cat_ii,
            [
                ((["####F", "#C...", "M...."], 1, 2), True),
                ((["M.C...F"], 1, 4), True),
                ((["M.C...F"], 1, 3), False),
            ],
        ),
        Template(
            "merge_stones",
            "def mergeStones(stones, k):\n"
            '    """Min cost to merge piles k at a time (LeetCode 1000)."""\n'
            "    n = len(stones)\n"
            "    if (n - 1) % (k - 1):\n"
            "        return -1\n"
            "    prefix = [0] * (n + 1)\n"
            "    for i, v in enumerate(stones):\n"
            "        prefix[i + 1] = prefix[i] + v\n"
            "    inf = 10 ** 9\n"
            "    dp = [[0] * n for _ in range(n)]\n"
            "    for length in range(k, n + 1):\n"
            "        for i in range(n - length + 1):\n"
            "            j = i + length - 1\n"
            "            best = inf\n"
            "            for mid in range(i, j, k - 1):\n"
            "                best = min(best, dp[i][mid] + dp[mid + 1][j])\n"
            "            if (j - i) % (k - 1) == 0:\n"
            "                best += prefix[j + 1] - prefix[i]\n"
            "            dp[i][j] = best\n"
            "    return dp[0][n - 1]\n",
            _stones,
            [
                (([3, 2, 4, 1], 2), 20),
                (([3, 2, 4, 1], 3), -1),
                (([3, 5, 1, 2, 6], 3), 25),
            ],
        ),
        Template(
            "longest_palindromic_substring",
            "def longestPalindrome(s):\n"
            '    """Longest palindromic substring (LeetCode 5)."""\n'
            "    if not s:\n"
            "        return ''\n"
            "    start = end = 0\n"
            "\n"
            "    def expand(left, right):\n"
            "        while left >= 0 and right < len(s) and s[left] == s[right]:\n"
            "            left -= 1\n"
            "            right += 1\n"
            "        return left + 1, right - 1\n"
            "\n"
            "    for i in range(len(s)):\n"
            "        l1, r1 = expand(i, i)\n"
            "        l2, r2 = expand(i, i + 1)\n"
            "        if r1 - l1 > end - start:\n"
            "            start, end = l1, r1\n"
            "        if r2 - l2 > end - start:\n"
            "            start, end = l2, r2\n"
            "    return s[start:end + 1]\n",
            _substr,
            [
                (("babad",), "bab"),
                (("cbbd",), "bb"),
            ],
        ),
        Template(
            "shortest_common_supersequence",
            "def shortestCommonSupersequence(str1, str2):\n"
            '    """Shortest string that has both inputs as subsequences (LeetCode 1092)."""\n'
            "    m, n = len(str1), len(str2)\n"
            "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
            "    for i in range(1, m + 1):\n"
            "        for j in range(1, n + 1):\n"
            "            if str1[i - 1] == str2[j - 1]:\n"
            "                dp[i][j] = dp[i - 1][j - 1] + 1\n"
            "            else:\n"
            "                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n"
            "    i, j = m, n\n"
            "    out = []\n"
            "    while i and j:\n"
            "        if str1[i - 1] == str2[j - 1]:\n"
            "            out.append(str1[i - 1])\n"
            "            i -= 1\n"
            "            j -= 1\n"
            "        elif dp[i - 1][j] >= dp[i][j - 1]:\n"
            "            out.append(str1[i - 1])\n"
            "            i -= 1\n"
            "        else:\n"
            "            out.append(str2[j - 1])\n"
            "            j -= 1\n"
            "    while i:\n"
            "        out.append(str1[i - 1])\n"
            "        i -= 1\n"
            "    while j:\n"
            "        out.append(str2[j - 1])\n"
            "        j -= 1\n"
            "    return ''.join(reversed(out))\n",
            _scs,
            [
                (("abac", "cab"), "cabac"),
                (("aaaaaaaa", "aaaaaaaa"), "aaaaaaaa"),
            ],
        ),
        Template(
            "distinct_subsequences_ii",
            "def distinctSubseqII(s):\n"
            '    """Count distinct non-empty subsequences (LeetCode 940)."""\n'
            "    mod = 10 ** 9 + 7\n"
            "    last = {}\n"
            "    dp = 1\n"
            "    for ch in s:\n"
            "        add = dp\n"
            "        if ch in last:\n"
            "            add = (add - last[ch]) % mod\n"
            "        last[ch] = dp\n"
            "        dp = (dp + add) % mod\n"
            "    return (dp - 1) % mod\n",
            _ds2,
            [
                (("abc",), 7),
                (("aba",), 6),
                (("aaa",), 3),
            ],
        ),
        Template(
            "min_score_triangulation",
            "def minScoreTriangulation(values):\n"
            '    """Minimum score triangulation of a polygon (LeetCode 1039)."""\n'
            "    n = len(values)\n"
            "    dp = [[0] * n for _ in range(n)]\n"
            "    for length in range(3, n + 1):\n"
            "        for i in range(n - length + 1):\n"
            "            j = i + length - 1\n"
            "            best = 10 ** 18\n"
            "            for k in range(i + 1, j):\n"
            "                score = dp[i][k] + dp[k][j] + values[i] * values[k] * values[j]\n"
            "                if score < best:\n"
            "                    best = score\n"
            "            dp[i][j] = best\n"
            "    return dp[0][n - 1]\n",
            _tri,
            [
                (([1, 2, 3],), 6),
                (([3, 7, 4, 5],), 144),
                (([1, 3, 1, 4, 1, 5],), 13),
            ],
        ),
    ]
