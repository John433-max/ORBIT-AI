"""Cycle 336: unused Easy — array partition / three-parts equal sum /
cells distance order / string matching / min abs difference /
consecutive characters."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "array_partition",
            "def array_partition(nums):\n"
            '    """Max sum of min(ai, bi) over n pairs (LeetCode 561)."""\n'
            "    nums = sorted(nums)\n"
            "    return sum(nums[i] for i in range(0, len(nums), 2))\n",
            lambda low: bool(
                re.search(
                    r"\barray[_ ]partition(?:[_ ]i)?\b|"
                    r"\barray_pair_sum\b",
                    low,
                )
            ),
            (
                (([1, 4, 3, 2],), 4),
                (([6, 2, 6, 5, 1, 2],), 9),
            ),
        ),
        T(
            "can_three_parts_equal_sum",
            "def can_three_parts_equal_sum(arr):\n"
            '    """True if array splits into three equal-sum parts (LeetCode 1013)."""\n'
            "    total = sum(arr)\n"
            "    if total % 3:\n"
            "        return False\n"
            "    need, acc, parts = total // 3, 0, 0\n"
            "    for v in arr:\n"
            "        acc += v\n"
            "        if acc == need:\n"
            "            parts += 1\n"
            "            acc = 0\n"
            "    return parts >= 3\n",
            lambda low: bool(
                re.search(
                    r"\bpartition[_ ]array[_ ]into[_ ]three[_ ]parts\b|"
                    r"\bthree[_ ]parts[_ ]with[_ ]equal[_ ]sum\b|"
                    r"\bcan[_ ]three[_ ]parts[_ ]equal[_ ]sum\b",
                    low,
                )
            ),
            (
                (([0, 2, 1, -6, 6, -7, 9, 1, 2, 0, 1],), True),
                (([0, 2, 1, -6, 6, 7, 9, -1, 2, 0, 1],), False),
                (([3, 3, 6, 5, -2, 2, 5, 1, -9, 4],), True),
            ),
        ),
        T(
            "all_cells_dist_order",
            "def all_cells_dist_order(rows, cols, rCenter, cCenter):\n"
            '    """Matrix cells sorted by Manhattan distance (LeetCode 1030)."""\n'
            "    cells = [[r, c] for r in range(rows) for c in range(cols)]\n"
            "    cells.sort(key=lambda rc: abs(rc[0] - rCenter) + abs(rc[1] - cCenter))\n"
            "    return cells\n",
            lambda low: bool(
                re.search(
                    r"\bmatrix[_ ]cells[_ ]in[_ ]distance[_ ]order\b|"
                    r"\ball[_ ]cells[_ ]dist[_ ]order\b|"
                    r"\bcells[_ ]distance[_ ]order\b",
                    low,
                )
            ),
            (
                ((1, 2, 0, 0), [[0, 0], [0, 1]]),
                ((2, 2, 0, 1), [[0, 1], [0, 0], [1, 1], [1, 0]]),
            ),
        ),
        T(
            "string_matching",
            "def string_matching(words):\n"
            '    """Words that are substrings of another word (LeetCode 1408)."""\n'
            "    out = []\n"
            "    for w in words:\n"
            "        if any(w != other and w in other for other in words):\n"
            "            out.append(w)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bstring[_ ]matching[_ ]in[_ ]an[_ ]array\b|"
                    r"\bstring[_ ]matching\b",
                    low,
                )
            ) and not re.search(r"\bword[_ ]search\b", low),
            (
                ((["mass", "as", "hero", "superhero"],), ["as", "hero"]),
                ((["leetcode", "et", "code"],), ["et", "code"]),
                ((["blue", "green", "bu"],), []),
            ),
        ),
        T(
            "minimum_abs_difference",
            "def minimum_abs_difference(arr):\n"
            '    """All pairs with the minimum absolute difference (LeetCode 1200)."""\n'
            "    arr = sorted(arr)\n"
            "    best = min(arr[i + 1] - arr[i] for i in range(len(arr) - 1))\n"
            "    return [[arr[i], arr[i + 1]] for i in range(len(arr) - 1) if arr[i + 1] - arr[i] == best]\n",
            lambda low: bool(
                re.search(
                    r"\bminimum[_ ]absolute[_ ]difference\b|"
                    r"\bminimum[_ ]abs[_ ]difference\b|"
                    r"\bmin[_ ]abs[_ ]difference\b",
                    low,
                )
            ),
            (
                (([4, 2, 1, 3],), [[1, 2], [2, 3], [3, 4]]),
                (([1, 3, 6, 10, 15],), [[1, 3]]),
                (([3, 8, -10, 23, 19, -4, -14, 27],), [[-14, -10], [19, 23], [23, 27]]),
            ),
        ),
        T(
            "consecutive_characters",
            "def consecutive_characters(s):\n"
            '    """Longest substring of one repeated character (LeetCode 1446)."""\n'
            "    best = cur = 1\n"
            "    for i in range(1, len(s)):\n"
            "        if s[i] == s[i - 1]:\n"
            "            cur += 1\n"
            "            if cur > best:\n"
            "                best = cur\n"
            "        else:\n"
            "            cur = 1\n"
            "    return best if s else 0\n",
            lambda low: bool(
                re.search(
                    r"\bconsecutive[_ ]characters\b|"
                    r"\bmax[_ ]power\b|"
                    r"\blongest substring of one repeated\b",
                    low,
                )
            ),
            (
                (("leetcode",), 2),
                (("abbcccddddeeeeedcba",), 5),
                (("triplepillooooow",), 5),
            ),
        ),
    ]
