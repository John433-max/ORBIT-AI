"""Cycle 397: unmatched LeetCode easies 1290 / 1893 / 1995 / 2303 / 2347 / 2511.

These titles previously fell through to the unverified draft stub.

Official examples (doocs/leetcode README_EN, matching LeetCode statements):
- 1290 Convert Binary Number in a Linked List to Integer: MSB at head.
  [1,0,1]->5; [0]->0.
- 1893 Check if All the Integers in a Range Are Covered:
  ranges=[[1,2],[3,4],[5,6]], left=2, right=5 -> True;
  [[1,10],[10,20]], 21, 21 -> False.
- 1995 Count Special Quadruplets: a<b<c<d and nums[a]+nums[b]+nums[c]==nums[d].
  [1,2,3,6]->1; [3,3,6,4,5]->0; [1,1,1,3,5]->4.
- 2303 Calculate Amount Paid in Taxes:
  brackets=[[3,50],[7,10],[12,25]], income=10 -> 2.65;
  [[1,0],[4,25],[5,50]], 2 -> 0.25; [[2,50]], 0 -> 0.0.
- 2347 Best Poker Hand: Flush > Three of a Kind > Pair > High Card.
  ranks=[13,2,3,1,9], suits=aaaaa -> "Flush";
  [4,4,2,4,4] / daabc -> "Three of a Kind";
  [10,10,2,12,9] / abcad -> "Pair".
- 2511 Maximum Enemy Forts That Can Be Captured: max empty span between
  opposite forts (1 and -1). [1,0,0,-1,0,0,0,0,1]->4; [0,0,1,-1]->0.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "get_decimal_value",
            "def get_decimal_value(head):\n"
            '    """Decimal value of a 0/1 list, MSB first (LeetCode 1290)."""\n'
            "    ans = 0\n"
            "    for bit in head:\n"
            "        ans = (ans << 1) | int(bit)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1290\b", low)
                or "binary number in a linked list" in low
                or "convert binary number in a linked" in low
            ),
            examples=(
                (([1, 0, 1],), 5),
                (([0],), 0),
            ),
        ),
        T(
            "is_covered",
            "def is_covered(ranges, left, right):\n"
            '    """True if every integer in [left, right] is covered (LeetCode 1893)."""\n'
            "    diff = [0] * 52\n"
            "    for start, end in ranges:\n"
            "        diff[start] += 1\n"
            "        diff[end + 1] -= 1\n"
            "    covered = 0\n"
            "    for i, delta in enumerate(diff):\n"
            "        covered += delta\n"
            "        if covered <= 0 and left <= i <= right:\n"
            "            return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1893\b", low)
                or "integers in a range are covered" in low
                or "all the integers in a range are covered" in low
            ),
            examples=(
                (([[1, 2], [3, 4], [5, 6]], 2, 5), True),
                (([[1, 10], [10, 20]], 21, 21), False),
            ),
        ),
        T(
            "count_quadruplets",
            "def count_quadruplets(nums):\n"
            '    """Count a<b<c<d with nums[a]+nums[b]+nums[c]==nums[d] (LeetCode 1995)."""\n'
            "    ans = 0\n"
            "    n = len(nums)\n"
            "    for a in range(n - 3):\n"
            "        for b in range(a + 1, n - 2):\n"
            "            for c in range(b + 1, n - 1):\n"
            "                s = nums[a] + nums[b] + nums[c]\n"
            "                for d in range(c + 1, n):\n"
            "                    if s == nums[d]:\n"
            "                        ans += 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1995\b", low)
                or "special quadruplets" in low
                or "count special quadruplet" in low
            ),
            examples=(
                (([1, 2, 3, 6],), 1),
                (([3, 3, 6, 4, 5],), 0),
                (([1, 1, 1, 3, 5],), 4),
            ),
        ),
        T(
            "calculate_tax",
            "def calculate_tax(brackets, income):\n"
            '    """Tax from inclusive upper brackets (LeetCode 2303)."""\n'
            "    prev = 0\n"
            "    tax = 0.0\n"
            "    for upper, percent in brackets:\n"
            "        if income <= prev:\n"
            "            break\n"
            "        amount = min(income, upper) - prev\n"
            "        tax += amount * percent / 100.0\n"
            "        prev = upper\n"
            "        if income <= upper:\n"
            "            break\n"
            "    return round(tax, 5)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2303\b", low)
                or "amount paid in taxes" in low
                or "calculate amount paid in taxes" in low
            ),
            examples=(
                (([[3, 50], [7, 10], [12, 25]], 10), 2.65),
                (([[1, 0], [4, 25], [5, 50]], 2), 0.25),
                (([[2, 50]], 0), 0.0),
            ),
        ),
        T(
            "best_hand",
            "def best_hand(ranks, suits):\n"
            '    """Best poker hand among flush / three / pair / high card (LeetCode 2347)."""\n'
            "    if len(set(suits)) == 1:\n"
            '        return "Flush"\n'
            "    counts = {}\n"
            "    for rank in ranks:\n"
            "        counts[rank] = counts.get(rank, 0) + 1\n"
            "    best = max(counts.values()) if counts else 0\n"
            "    if best >= 3:\n"
            '        return "Three of a Kind"\n'
            "    if best == 2:\n"
            '        return "Pair"\n'
            '    return "High Card"\n',
            lambda low: bool(
                re.search(r"\bleetcode\s*2347\b", low)
                or "best poker hand" in low
            ),
            examples=(
                (([13, 2, 3, 1, 9], ["a", "a", "a", "a", "a"]), "Flush"),
                (([4, 4, 2, 4, 4], ["d", "a", "a", "b", "c"]), "Three of a Kind"),
                (([10, 10, 2, 12, 9], ["a", "b", "c", "a", "d"]), "Pair"),
            ),
        ),
        T(
            "capture_forts",
            "def capture_forts(forts):\n"
            '    """Max empty cells between opposite forts (LeetCode 2511)."""\n'
            "    ans = 0\n"
            "    prev = -1\n"
            "    for i, fort in enumerate(forts):\n"
            "        if fort == 0:\n"
            "            continue\n"
            "        if prev >= 0 and forts[prev] == -fort:\n"
            "            ans = max(ans, i - prev - 1)\n"
            "        prev = i\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2511\b", low)
                or "enemy forts that can be captured" in low
                or "maximum enemy forts" in low
            ),
            examples=(
                (([1, 0, 0, -1, 0, 0, 0, 0, 1],), 4),
                (([0, 0, 1, -1],), 0),
            ),
        ),
    ]
