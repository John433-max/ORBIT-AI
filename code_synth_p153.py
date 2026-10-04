"""Cycle 431: course schedule III, last stone II, max vowels window, split ways, hand of straights, stock span.

These prompts were unmatched or stolen by broader matchers (course schedule, last stone, count vowels).
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "course_schedule_iii",
            "def course_schedule_iii(courses):\n"
            '    """Max courses you can take (LeetCode 630). courses[i] = [duration, lastDay]."""\n'
            "    import heapq\n"
            "    courses = sorted((int(d), int(end)) for d, end in courses)\n"
            "    heap = []\n"
            "    time = 0\n"
            "    for dur, end in courses:\n"
            "        heapq.heappush(heap, -dur)\n"
            "        time += dur\n"
            "        if time > end:\n"
            "            time += heapq.heappop(heap)\n"
            "    return len(heap)\n",
            lambda low: bool(
                re.search(r"\bleetcode 630\b", low)
                or (
                    "course schedule iii" in low
                    or "course schedule 3" in low
                )
            ),
            (
                (([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]],), 3),
                (([[1, 2]],), 1),
                (([[3, 2], [4, 3]],), 0),
            ),
        ),
        T(
            "last_stone_weight_ii",
            "def last_stone_weight_ii(stones):\n"
            '    """Min leftover after smashing into two partitions (LeetCode 1049)."""\n'
            "    stones = [int(s) for s in stones]\n"
            "    total = sum(stones)\n"
            "    target = total // 2\n"
            "    dp = [False] * (target + 1)\n"
            "    dp[0] = True\n"
            "    for s in stones:\n"
            "        for j in range(target, s - 1, -1):\n"
            "            if dp[j - s]:\n"
            "                dp[j] = True\n"
            "    best = 0\n"
            "    for j in range(target, -1, -1):\n"
            "        if dp[j]:\n"
            "            best = j\n"
            "            break\n"
            "    return total - 2 * best\n",
            lambda low: bool(
                re.search(r"\bleetcode 1049\b", low)
                or "last stone weight ii" in low
                or "last stone weight 2" in low
            ),
            (
                (([2, 7, 4, 1, 8, 1],), 1),
                (([31, 26, 33, 21, 40],), 5),
            ),
        ),
        T(
            "max_vowels",
            "def max_vowels(s, k):\n"
            '    """Max vowels in any window of length k (LeetCode 1456)."""\n'
            "    vowels = set('aeiou')\n"
            "    s = str(s).lower()\n"
            "    k = int(k)\n"
            "    if k <= 0 or not s:\n"
            "        return 0\n"
            "    k = min(k, len(s))\n"
            "    cur = sum(ch in vowels for ch in s[:k])\n"
            "    best = cur\n"
            "    for i in range(k, len(s)):\n"
            "        cur += (s[i] in vowels) - (s[i - k] in vowels)\n"
            "        if cur > best:\n"
            "            best = cur\n"
            "    return best\n"
            "\n"
            "def maxVowels(s, k):\n"
            "    return max_vowels(s, k)\n",
            lambda low: bool(
                re.search(r"\bleetcode 1456\b", low)
                or (
                    "vowels" in low
                    and ("substring" in low or "given length" in low)
                )
            ),
            (
                (("abciiidef", 3), 3),
                (("aeiou", 2), 2),
                (("leetcode", 3), 2),
            ),
        ),
        T(
            "num_ways_split",
            "def num_ways_split(s):\n"
            '    """Ways to split s into 3 parts with equal 1-counts (LeetCode 1573)."""\n'
            "    MOD = 10 ** 9 + 7\n"
            "    s = str(s)\n"
            "    ones = [i for i, ch in enumerate(s) if ch == '1']\n"
            "    n = len(ones)\n"
            "    if n % 3:\n"
            "        return 0\n"
            "    if n == 0:\n"
            "        m = len(s)\n"
            "        return ((m - 1) * (m - 2) // 2) % MOD\n"
            "    k = n // 3\n"
            "    return ((ones[k] - ones[k - 1]) * (ones[2 * k] - ones[2 * k - 1])) % MOD\n"
            "\n"
            "def numWays(s):\n"
            "    return num_ways_split(s)\n",
            lambda low: bool(
                re.search(r"\bleetcode 1573\b", low)
                or "ways to split a string" in low
                or "number of ways to split a string" in low
            ),
            (
                (("10101",), 4),
                (("1001",), 0),
                (("0000",), 3),
            ),
        ),
        T(
            "hand_of_straights",
            "def hand_of_straights(hand, groupSize):\n"
            '    """True if hand can be rearranged into consecutive groups (LeetCode 846)."""\n'
            "    from collections import Counter\n"
            "    hand = [int(x) for x in hand]\n"
            "    groupSize = int(groupSize)\n"
            "    if groupSize <= 0 or len(hand) % groupSize:\n"
            "        return False\n"
            "    cnt = Counter(hand)\n"
            "    for start in sorted(cnt):\n"
            "        need = cnt[start]\n"
            "        if need == 0:\n"
            "            continue\n"
            "        for x in range(start, start + groupSize):\n"
            "            if cnt[x] < need:\n"
            "                return False\n"
            "            cnt[x] -= need\n"
            "    return True\n"
            "\n"
            "def isNStraightHand(hand, groupSize):\n"
            "    return hand_of_straights(hand, groupSize)\n",
            lambda low: bool(
                re.search(r"\bleetcode 846\b", low)
                or "hand of straights" in low
                or "straight hand" in low
            ),
            (
                (([1, 2, 3, 6, 2, 3, 4, 7, 8], 3), True),
                (([1, 2, 3, 4, 5], 4), False),
            ),
        ),
        T(
            "online_stock_span",
            "def online_stock_span(prices):\n"
            '    """Span of consecutive days price was <= today (LeetCode 901)."""\n'
            "    stack = []\n"
            "    out = []\n"
            "    for p in prices:\n"
            "        p = int(p)\n"
            "        span = 1\n"
            "        while stack and stack[-1][0] <= p:\n"
            "            span += stack.pop()[1]\n"
            "        stack.append((p, span))\n"
            "        out.append(span)\n"
            "    return out\n"
            "\n"
            "def stock_span(prices):\n"
            "    return online_stock_span(prices)\n",
            lambda low: bool(
                re.search(r"\bleetcode 901\b", low)
                or "online stock span" in low
                or "stock span" in low
            ),
            (
                (([100, 80, 60, 70, 60, 75, 85],), [1, 1, 1, 2, 1, 4, 6]),
                (([31, 41, 48, 59, 79],), [1, 2, 3, 4, 5]),
            ),
        ),
    ]
