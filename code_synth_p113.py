"""Cycle 392: Easy prompts still absent from the template index.

LeetCode 788, 811, 849, 867, 874, and 977 were not referenced by any pack.
Matchers stay ID- or title-specific so rotated-array, robot, and sort
prompts do not steal search-rotated / shortest-distance / sort-list templates.
Loaded before p112.

Sources:
- LeetCode 788 Rotated Digits: a number is good if it contains 2/5/6/9 and
  no 3/4/7 (0/1/8 stay valid under 180-degree rotation).
- LeetCode 811 Subdomain Visit Count: accumulate counts over every suffix.
- LeetCode 849 Maximize Distance to Closest Person: max of edge gaps and
  half the interior gaps between seated people.
- LeetCode 867 Transpose Matrix.
- LeetCode 874 Walking Robot Simulation: north/east/south/west, -1/-2 turns,
  stop before obstacles; return max squared Euclidean distance.
- LeetCode 977 Squares of a Sorted Array: square then sort (two-pointer equivalent).
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "rotated_digits",
            "def rotated_digits(n):\n"
            '    """Count 1..n that stay valid and change under 180 rotation (LeetCode 788)."""\n'
            "    good = 0\n"
            "    for i in range(1, int(n) + 1):\n"
            "        s = str(i)\n"
            "        if any(ch in '347' for ch in s):\n"
            "            continue\n"
            "        if any(ch in '2569' for ch in s):\n"
            "            good += 1\n"
            "    return good\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 788\b|"
                    r"\brotated digits\b",
                    low,
                )
            ),
            (
                ((10,), 4),
                ((1,), 0),
                ((20,), 9),
            ),
        ),
        T(
            "subdomain_visits",
            "def subdomain_visits(cpdomains):\n"
            '    """Count visits for every subdomain suffix (LeetCode 811)."""\n'
            "    from collections import Counter\n"
            "    counts = Counter()\n"
            "    for item in cpdomains:\n"
            "        count_s, domain = str(item).split()\n"
            "        count = int(count_s)\n"
            "        parts = domain.split('.')\n"
            "        for i in range(len(parts)):\n"
            "            counts['.'.join(parts[i:])] += count\n"
            "    return [f'{counts[dom]} {dom}' for dom in sorted(counts)]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 811\b|"
                    r"\bsubdomain visit count\b|"
                    r"\bsubdomain visits\b",
                    low,
                )
            ),
            (
                (
                    (["9001 discuss.leetcode.com"],),
                    ["9001 com", "9001 discuss.leetcode.com", "9001 leetcode.com"],
                ),
                (
                    (["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"],),
                    [
                        "951 com",
                        "900 google.mail.com",
                        "1 intel.mail.com",
                        "901 mail.com",
                        "5 org",
                        "5 wiki.org",
                        "50 yahoo.com",
                    ],
                ),
            ),
        ),
        T(
            "max_dist_to_closest",
            "def max_dist_to_closest(seats):\n"
            '    """Max distance to the closest seated person (LeetCode 849)."""\n'
            "    seats = list(seats)\n"
            "    n = len(seats)\n"
            "    prev = -1\n"
            "    best = 0\n"
            "    for i, seat in enumerate(seats):\n"
            "        if seat == 1:\n"
            "            best = i if prev < 0 else max(best, (i - prev) // 2)\n"
            "            prev = i\n"
            "    return max(best, n - 1 - prev)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 849\b|"
                    r"\bmaximize distance to closest person\b|"
                    r"\bmax dist to closest\b",
                    low,
                )
            ),
            (
                (([1, 0, 0, 0, 1, 0, 1],), 2),
                (([1, 0, 0, 0],), 3),
                (([0, 1],), 1),
            ),
        ),
        T(
            "transpose_matrix",
            "def transpose(matrix):\n"
            '    """Return the transpose of a matrix (LeetCode 867)."""\n'
            "    return [list(col) for col in zip(*matrix)]\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 867\b|"
                    r"\btranspose the matrix\b|"
                    r"\btranspose matrix\b",
                    low,
                )
            ),
            (
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
                (([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]]),
            ),
        ),
        T(
            "robot_sim",
            "def robot_sim(commands, obstacles):\n"
            '    """Walking robot simulation; max squared distance (LeetCode 874)."""\n'
            "    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))\n"
            "    blocked = {tuple(ob) for ob in (obstacles or [])}\n"
            "    x = y = d = 0\n"
            "    best = 0\n"
            "    for cmd in commands:\n"
            "        cmd = int(cmd)\n"
            "        if cmd == -1:\n"
            "            d = (d + 1) % 4\n"
            "        elif cmd == -2:\n"
            "            d = (d + 3) % 4\n"
            "        else:\n"
            "            dx, dy = dirs[d]\n"
            "            for _ in range(cmd):\n"
            "                nx, ny = x + dx, y + dy\n"
            "                if (nx, ny) in blocked:\n"
            "                    break\n"
            "                x, y = nx, ny\n"
            "                best = max(best, x * x + y * y)\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 874\b|"
                    r"\bwalking robot simulation\b|"
                    r"\brobot sim\b",
                    low,
                )
            ),
            (
                (([4, -1, 3], []), 25),
                (([4, -1, 4, -2, 4], [[2, 4]]), 65),
                (([6, -1, -1, 6], []), 36),
            ),
        ),
        T(
            "sorted_squares",
            "def sorted_squares(nums):\n"
            '    """Squares of a sorted array, returned sorted (LeetCode 977)."""\n'
            "    return sorted(int(x) * int(x) for x in nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 977\b|"
                    r"\bsquares of a sorted array\b|"
                    r"\bsorted squares\b",
                    low,
                )
            ),
            (
                (([-4, -1, 0, 3, 10],), [0, 1, 9, 16, 100]),
                (([-7, -3, 2, 3, 11],), [4, 9, 9, 49, 121]),
            ),
        ),
    ]
