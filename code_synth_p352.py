"""Cycle 643 (p352): Hard/classic coding-smoke gaps code_2027–code_2032.

expression_add_operators (282), get_skyline (218), basic_calculator (224),
max_points_on_a_line (149), mincost_tickets (983), max_subarray_sum_circular (918).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "expression_add_operators",
            '''def add_operators(num, target):
    """Insert + - * so the expression equals target (LeetCode 282, educational).

    No leading zeros in operands. Results sorted for stable verify.
    """
    n = len(num)
    res = []

    def dfs(i, expr, val, last):
        if i == n:
            if val == target:
                res.append(expr)
            return
        for j in range(i, n):
            if j > i and num[i] == "0":
                break
            cur = int(num[i : j + 1])
            piece = num[i : j + 1]
            if i == 0:
                dfs(j + 1, piece, cur, cur)
            else:
                dfs(j + 1, expr + "+" + piece, val + cur, cur)
                dfs(j + 1, expr + "-" + piece, val - cur, -cur)
                dfs(j + 1, expr + "*" + piece, val - last + last * cur, last * cur)

    dfs(0, "", 0, 0)
    return sorted(res)
''',
            lambda low: bool(
                re.search(r"\b(expression\s+)?add\s+operators\b", low)
                or re.search(r"\boperators?\b.*\bexpression\b", low)
                or re.search(r"\badd[_ ]operators\b", low)
            ),
            (
                (("123", 6), ["1*2*3", "1+2+3"]),
                (("232", 8), ["2*3+2", "2+3*2"]),
                (("105", 5), ["1*0+5", "10-5"]),
            ),
        ),
        T(
            "get_skyline",
            '''def get_skyline(buildings):
    """Key points of the city skyline (LeetCode 218, educational sweep)."""
    import heapq

    events = []
    for left, right, height in buildings:
        events.append((left, -height, right))
        events.append((right, 0, 0))
    events.sort()
    live = [(0, float("inf"))]
    res = []
    prev = 0
    for x, neg_h, right in events:
        if neg_h < 0:
            heapq.heappush(live, (neg_h, right))
        while live and live[0][1] <= x:
            heapq.heappop(live)
        cur = -live[0][0] if live else 0
        if cur != prev:
            res.append([x, cur])
            prev = cur
    return res
''',
            lambda low: bool(
                re.search(r"\b(the\s+)?skyline\b", low)
                or re.search(r"\bget[_ ]skyline\b", low)
            ),
            (
                (
                    ([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],),
                    [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]],
                ),
                (
                    ([[0, 2, 3], [2, 5, 3]],),
                    [[0, 3], [5, 0]],
                ),
            ),
        ),
        T(
            "basic_calculator",
            '''def calculate(s):
    """Evaluate expression with +, -, (, ) (LeetCode 224, educational)."""
    stack = []
    num = 0
    sign = 1
    res = 0
    for ch in s + "+":
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            res += sign * num
            num = 0
            sign = 1 if ch == "+" else -1
        elif ch == "(":
            stack.append(res)
            stack.append(sign)
            res = 0
            sign = 1
        elif ch == ")":
            res += sign * num
            num = 0
            res *= stack.pop()
            res += stack.pop()
    return res
''',
            lambda low: bool(
                re.search(r"\bbasic[_\s-]?calculator\b", low)
                and not re.search(r"\bbasic[_\s-]?calculator[_\s-]?ii\b", low)
            ),
            (
                (("1 + 1",), 2),
                ((" 2-1 + 2 ",), 3),
                (("(1+(4+5+2)-3)+(6+8)",), 23),
            ),
        ),
        T(
            "max_points_on_a_line",
            '''def max_points(points):
    """Max points on a straight line (LeetCode 149, educational)."""
    from collections import defaultdict
    from math import gcd

    n = len(points)
    if n <= 2:
        return n
    ans = 0
    for i in range(n):
        slopes = defaultdict(int)
        same = 0
        local = 0
        x1, y1 = points[i]
        for j in range(n):
            if i == j:
                continue
            x2, y2 = points[j]
            dx, dy = x2 - x1, y2 - y1
            if dx == 0 and dy == 0:
                same += 1
                continue
            g = gcd(dx, dy)
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            slopes[(dx, dy)] += 1
            local = max(local, slopes[(dx, dy)])
        ans = max(ans, local + same + 1)
    return ans
''',
            lambda low: bool(
                re.search(r"\bmax[_\s-]?points\b", low)
                or re.search(r"\bpoints\s+on\s+a\s+line\b", low)
            ),
            (
                (([[1, 1], [2, 2], [3, 3]],), 3),
                (([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]],), 4),
            ),
        ),
        T(
            "mincost_tickets",
            '''def mincost_tickets(days, costs):
    """Min cost for tickets covering travel days (LeetCode 983)."""
    dayset = set(days)
    last = days[-1]
    dp = [0] * (last + 1)
    for d in range(1, last + 1):
        if d not in dayset:
            dp[d] = dp[d - 1]
            continue
        dp[d] = dp[d - 1] + costs[0]
        dp[d] = min(dp[d], dp[max(0, d - 7)] + costs[1])
        dp[d] = min(dp[d], dp[max(0, d - 30)] + costs[2])
    return dp[last]
''',
            lambda low: bool(
                re.search(r"\bmin(?:imum)?[_\s-]?cost[_\s-]?for[_\s-]?tickets?\b", low)
                or re.search(r"\bmincost[_ ]tickets\b", low)
            ),
            (
                (([1, 4, 6, 7, 8, 20], [2, 7, 15]), 11),
                (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15]), 17),
            ),
        ),
        T(
            "max_subarray_sum_circular",
            '''def max_subarray_sum_circular(nums):
    """Max sum of circular subarray (LeetCode 918, educational Kadane)."""
    def kadane(arr, find_max=True):
        best = cur = arr[0]
        for x in arr[1:]:
            if find_max:
                cur = max(x, cur + x)
                best = max(best, cur)
            else:
                cur = min(x, cur + x)
                best = min(best, cur)
        return best

    total = sum(nums)
    max_normal = kadane(nums, True)
    min_sub = kadane(nums, False)
    if total == min_sub:  # all negative
        return max_normal
    return max(max_normal, total - min_sub)
''',
            lambda low: bool(
                re.search(r"\bmax(?:imum)?[_\s-]?sum[_\s-]?circular[_\s-]?subarray\b", low)
                or re.search(r"\bcircular[_\s-]?subarray\b", low)
                or re.search(r"\bmax_subarray_sum_circular\b", low)
            ),
            (
                (([1, -2, 3, -2],), 3),
                (([5, -3, 5],), 10),
                (([-3, -2, -3],), -2),
            ),
        ),
    ]
