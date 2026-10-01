"""Cycle 324: split words by separator / odd string difference /
check letter distances / points covered by cars / digits that divide n /
grid column widths."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "split_words_by_separator",
            "def split_words_by_separator(words, separator):\n"
            '    """Split each word on separator and drop empties (LeetCode 2788)."""\n'
            "    out = []\n"
            "    for w in words:\n"
            "        for part in w.split(separator):\n"
            "            if part:\n"
            "                out.append(part)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsplit_words_by_separator\b|"
                    r"\bsplit[_ ]words[_ ]by[_ ]separator\b|"
                    r"\bleetcode[_ ]2788\b",
                    low,
                )
            )
            and "thousand_separator" not in low,
            (
                ((["one.two.three", "four.five", "six"], "."), ["one", "two", "three", "four", "five", "six"]),
                ((["$easy$", "$problem$"], "$"), ["easy", "problem"]),
            ),
        ),
        T(
            "odd_string_difference",
            "def odd_string_difference(words):\n"
            '    """Word whose consecutive-diff tuple is unique (LeetCode 2451)."""\n'
            "    def sig(w):\n"
            "        return tuple(ord(w[i + 1]) - ord(w[i]) for i in range(len(w) - 1))\n"
            "    sigs = [sig(w) for w in words]\n"
            "    for i, s in enumerate(sigs):\n"
            "        if sigs.count(s) == 1:\n"
            "            return words[i]\n"
            "    return words[0]\n",
            lambda low: bool(
                re.search(
                    r"\bodd_string_difference\b|"
                    r"\bodd[_ ]string[_ ]difference\b|"
                    r"\bleetcode[_ ]2451\b",
                    low,
                )
            ),
            (
                ((["adc", "wzy", "abc"],), "abc"),
                ((["aaa", "bob", "ccc", "ddd"],), "bob"),
            ),
        ),
        T(
            "check_distances",
            "def check_distances(s, distance):\n"
            '    """Each letter pair is distance[letter] apart (LeetCode 2399)."""\n'
            "    pos = {}\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch in pos:\n"
            "            if i - pos[ch] - 1 != distance[ord(ch) - 97]:\n"
            "                return False\n"
            "        else:\n"
            "            pos[ch] = i\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bcheck_distances\b|"
                    r"\bcheck[_ ]distances[_ ]between[_ ]same[_ ]letters\b|"
                    r"\bleetcode[_ ]2399\b",
                    low,
                )
            )
            and "bus_stop" not in low
            and "hamming" not in low,
            (
                (("abaccb", [1, 3, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), True),
                (("aa", [1] + [0] * 25), False),
            ),
        ),
        T(
            "number_of_points",
            "def number_of_points(nums):\n"
            '    """Count unique integers covered by car intervals (LeetCode 2848)."""\n'
            "    covered = set()\n"
            "    for a, b in nums:\n"
            "        for x in range(a, b + 1):\n"
            "            covered.add(x)\n"
            "    return len(covered)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber_of_points\b|"
                    r"\bpoints[_ ]that[_ ]intersect[_ ]with[_ ]cars\b|"
                    r"\bleetcode[_ ]2848\b",
                    low,
                )
            ),
            (
                (([[3, 6], [1, 5], [4, 7]],), 7),
                (([[1, 3], [5, 8]],), 7),
            ),
        ),
        T(
            "convert_time",
            "def convert_time(current, correct):\n"
            '    """Min ops 60/15/5/1 minutes to go current->correct (LeetCode 2224)."""\n'
            "    def mins(t):\n"
            "        h, m = t.split(':')\n"
            "        return int(h) * 60 + int(m)\n"
            "    diff = mins(correct) - mins(current)\n"
            "    ops = 0\n"
            "    for step in (60, 15, 5, 1):\n"
            "        ops += diff // step\n"
            "        diff %= step\n"
            "    return ops\n",
            lambda low: bool(
                re.search(
                    r"\bconvert_time\b|"
                    r"\bminimum[_ ]number[_ ]of[_ ]operations[_ ]to[_ ]convert[_ ]time\b|"
                    r"\bleetcode[_ ]2224\b",
                    low,
                )
            )
            and "convert_temperature" not in low,
            (
                (("02:30", "04:35"), 3),
                (("11:00", "11:01"), 1),
            ),
        ),
        T(
            "find_column_width",
            "def find_column_width(grid):\n"
            '    """Width of each column as max printed-integer length (LeetCode 2639)."""\n'
            "    cols = len(grid[0])\n"
            "    return [max(len(str(grid[r][c])) for r in range(len(grid))) for c in range(cols)]\n",
            lambda low: bool(
                re.search(
                    r"\bfind_column_width\b|"
                    r"\bfind[_ ]the[_ ]width[_ ]of[_ ]columns\b|"
                    r"\bwidth[_ ]of[_ ]columns[_ ]of[_ ]a[_ ]grid\b|"
                    r"\bleetcode[_ ]2639\b",
                    low,
                )
            )
            and "binary_tree" not in low,
            (
                (([[1], [22], [333]],), [3]),
                (([[-15, 1, 3], [15, 7, 12], [5, 6, -2]],), [3, 1, 2]),
            ),
        ),
    ]
