"""Cycle 396: unmatched LeetCode easies 1360 / 1403 / 1560 / 1582 / 2094 / 2231.

These titles previously fell through to the unverified draft stub.

Official examples:
- 1360 Number of Days Between Two Dates: absolute day difference.
  ("2019-06-29","2019-06-30")->1; ("2020-01-15","2019-12-31")->15.
- 1403 Minimum Subsequence in Non-Increasing Order: shortest non-increasing
  subsequence with sum strictly greater than the rest.
  [4,3,10,9,8]->[10,9]; [4,4,7,6,7]->[7,7,6]; [6]->[6].
- 1560 Most Visited Sector in a Circular Track: sectors visited most often.
  n=4 rounds=[1,3,1,2]->[1,2]; n=2 long alternate->[2];
  n=7 rounds=[1,3,5,7]->[1,2,3,4,5,6,7].
- 1582 Special Positions in a Binary Matrix: 1s that are alone in row and column.
  [[1,0,0],[0,0,1],[1,0,0]]->1; identity 3x3->3.
- 2094 Finding 3-Digit Even Numbers: unique even numbers formable from digits.
  [2,1,3,0]->[102,120,130,132,210,230,312,320]; [3,7,5]->[].
- 2231 Largest Number After Digit Swaps by Parity: reorder odd and even digits
  independently, largest first, keeping parity positions.
  1234->3412; 65875->87655.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "days_between_dates",
            "def days_between_dates(date1, date2):\n"
            '    """Absolute day difference between YYYY-MM-DD dates (LeetCode 1360)."""\n'
            "    import datetime\n"
            "    a = datetime.date.fromisoformat(date1)\n"
            "    b = datetime.date.fromisoformat(date2)\n"
            "    return abs((a - b).days)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1360\b", low)
                or "days between two dates" in low
                or "number of days between two dates" in low
            ),
            examples=(
                (("2019-06-29", "2019-06-30"), 1),
                (("2020-01-15", "2019-12-31"), 15),
            ),
        ),
        T(
            "min_subsequence",
            "def min_subsequence(nums):\n"
            '    """Shortest non-increasing subsequence summing over the rest (LeetCode 1403)."""\n'
            "    nums = sorted(nums, reverse=True)\n"
            "    total = sum(nums)\n"
            "    acc = 0\n"
            "    out = []\n"
            "    for x in nums:\n"
            "        acc += x\n"
            "        out.append(x)\n"
            "        if acc > total - acc:\n"
            "            break\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1403\b", low)
                or "minimum subsequence in non-increasing" in low
                or "min subsequence in non-increasing" in low
            ),
            examples=(
                (([4, 3, 10, 9, 8],), [10, 9]),
                (([4, 4, 7, 6, 7],), [7, 7, 6]),
                (([6],), [6]),
            ),
        ),
        T(
            "most_visited",
            "def most_visited(n, rounds):\n"
            '    """Sectors visited most on a circular track (LeetCode 1560)."""\n'
            "    start, end = rounds[0], rounds[-1]\n"
            "    if start <= end:\n"
            "        return list(range(start, end + 1))\n"
            "    return list(range(1, end + 1)) + list(range(start, n + 1))\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1560\b", low)
                or "most visited sector" in low
                or "circular track" in low and "visited" in low
            ),
            examples=(
                ((4, [1, 3, 1, 2]), [1, 2]),
                ((2, [2, 1, 2, 1, 2, 1, 2, 1, 2]), [2]),
                ((7, [1, 3, 5, 7]), [1, 2, 3, 4, 5, 6, 7]),
            ),
        ),
        T(
            "num_special",
            "def num_special(mat):\n"
            '    """Count 1s alone in their row and column (LeetCode 1582)."""\n'
            "    rows = [sum(r) for r in mat]\n"
            "    cols = [sum(mat[i][j] for i in range(len(mat))) for j in range(len(mat[0]))]\n"
            "    ans = 0\n"
            "    for i, row in enumerate(mat):\n"
            "        for j, val in enumerate(row):\n"
            "            if val == 1 and rows[i] == 1 and cols[j] == 1:\n"
            "                ans += 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1582\b", low)
                or "special positions in a binary matrix" in low
                or "special position in a binary matrix" in low
            ),
            examples=(
                (([[1, 0, 0], [0, 0, 1], [1, 0, 0]],), 1),
                (([[1, 0, 0], [0, 1, 0], [0, 0, 1]],), 3),
            ),
        ),
        T(
            "find_even_numbers",
            "def find_even_numbers(digits):\n"
            '    """Unique 3-digit even numbers formable from digits (LeetCode 2094)."""\n'
            "    from collections import Counter\n"
            "    cnt = Counter(digits)\n"
            "    out = []\n"
            "    for n in range(100, 1000, 2):\n"
            "        need = Counter(int(c) for c in str(n))\n"
            "        if all(cnt[d] >= need[d] for d in need):\n"
            "            out.append(n)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2094\b", low)
                or "finding 3-digit even" in low
                or "find 3-digit even numbers" in low
            ),
            examples=(
                (([2, 1, 3, 0],), [102, 120, 130, 132, 210, 230, 302, 310, 312, 320]),
                (([2, 2, 8, 8, 2],), [222, 228, 282, 288, 822, 828, 882]),
                (([3, 7, 5],), []),
            ),
        ),
        T(
            "largest_integer",
            "def largest_integer(num):\n"
            '    """Largest number after same-parity digit swaps (LeetCode 2231)."""\n'
            "    chars = list(str(num))\n"
            "    odds = sorted((c for c in chars if int(c) % 2), reverse=True)\n"
            "    evens = sorted((c for c in chars if int(c) % 2 == 0), reverse=True)\n"
            "    oi = ei = 0\n"
            "    out = []\n"
            "    for c in chars:\n"
            "        if int(c) % 2:\n"
            "            out.append(odds[oi])\n"
            "            oi += 1\n"
            "        else:\n"
            "            out.append(evens[ei])\n"
            "            ei += 1\n"
            "    return int(''.join(out))\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2231\b", low)
                or "digit swaps by parity" in low
                or "largest number after digit swaps" in low
            ),
            examples=(
                ((1234,), 3412),
                ((65875,), 87655),
            ),
        ),
    ]
