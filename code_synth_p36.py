"""Cycle 296: shuffle string / max power / good rectangles / goal parser / busy student / visit points."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "shuffle_string",
            "def shuffle_string(s, indices):\n"
            '    """Restore shuffled string given target indices (LeetCode 1528)."""\n'
            "    out = [''] * len(s)\n"
            "    for ch, i in zip(s, indices):\n"
            "        out[i] = ch\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\bshuffle[_ ]string\b|"
                    r"\brestore (?:a )?shuffled string\b|"
                    r"\bshuffle a string given indices\b",
                    low,
                )
            ),
            (
                (("codeleet", [4, 5, 6, 7, 0, 2, 1, 3]), "leetcode"),
                (("abc", [0, 1, 2]), "abc"),
                (("aiohn", [3, 1, 4, 2, 0]), "nihao"),
            ),
        ),
        T(
            "max_power",
            "def max_power(s):\n"
            '    """Longest consecutive identical characters (LeetCode 1446)."""\n'
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
                    r"\bmax[_ ]power\b|"
                    r"\bconsecutive characters? power\b|"
                    r"\bmax power of a string\b",
                    low,
                )
            ),
            (
                (("leetcode",), 2),
                (("abbcccddddeeeeedcba",), 5),
                (("triple",), 1),
            ),
        ),
        T(
            "count_good_rectangles",
            "def count_good_rectangles(rectangles):\n"
            '    """Count rectangles that can form the largest square (LeetCode 1725)."""\n'
            "    sides = [min(l, w) for l, w in rectangles]\n"
            "    m = max(sides)\n"
            "    return sum(1 for s in sides if s == m)\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]good[_ ]rectangles\b|"
                    r"\bnumber of rectangles that can form the largest square\b|"
                    r"\bcount good rectangles\b",
                    low,
                )
            ),
            (
                (([[5, 8], [3, 9], [5, 12], [16, 5]],), 3),
                (([[2, 3], [3, 7], [4, 3], [3, 7]],), 3),
                (([[1, 1], [2, 2]],), 1),
            ),
        ),
        T(
            "interpret",
            "def interpret(command):\n"
            '    """Goal parser interpretation of G / () / (al) (LeetCode 1678)."""\n'
            "    return command.replace('(al)', 'al').replace('()', 'o')\n",
            lambda low: bool(
                re.search(
                    r"\bgoal[_ ]parser\b|"
                    r"\binterpret (?:a )?goal parser\b|"
                    r"\bgoal parser interpretation\b",
                    low,
                )
            ),
            (
                (("G()(al)",), "Goal"),
                (("G()()()()(al)",), "Gooooal"),
                (("(al)G(al)()()G",), "alGalooG"),
            ),
        ),
        T(
            "busy_student",
            "def busy_student(start_time, end_time, query_time):\n"
            '    """Students doing homework at query_time (LeetCode 1450)."""\n'
            "    return sum(1 for s, e in zip(start_time, end_time) if s <= query_time <= e)\n",
            lambda low: bool(
                re.search(
                    r"\bbusy[_ ]student\b|"
                    r"\bstudents doing homework at (?:a )?given time\b|"
                    r"\bnumber of students doing homework\b",
                    low,
                )
            ),
            (
                (([1, 2, 3], [3, 2, 7], 4), 1),
                (([4], [4], 4), 1),
                (([4], [4], 5), 0),
            ),
        ),
        T(
            "min_time_to_visit_all_points",
            "def min_time_to_visit_all_points(points):\n"
            '    """Min time visiting points with diagonal moves (LeetCode 1266)."""\n'
            "    t = 0\n"
            "    for (x1, y1), (x2, y2) in zip(points, points[1:]):\n"
            "        t += max(abs(x2 - x1), abs(y2 - y1))\n"
            "    return t\n",
            lambda low: bool(
                re.search(
                    r"\bmin[_ ]time[_ ]to[_ ]visit[_ ]all[_ ]points\b|"
                    r"\bminimum time visiting all points\b|"
                    r"\bmin time to visit all points\b",
                    low,
                )
            ),
            (
                (([[1, 1], [3, 4], [-1, 0]],), 7),
                (([[3, 2], [-2, 2]],), 5),
                (([[0, 0], [1, 0], [1, 1]],), 2),
            ),
        ),
    ]
