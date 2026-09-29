"""Cycle 280: additional verified Python templates (pack 22)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "toeplitz_matrix",
            "def is_toeplitz_matrix(matrix):\n"
            '    """True if every descending diagonal from left to right is constant."""\n'
            "    grid = [list(row) for row in matrix]\n"
            "    if not grid or not grid[0]:\n"
            "        return True\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    for i in range(1, rows):\n"
            "        for j in range(1, cols):\n"
            "            if grid[i][j] != grid[i - 1][j - 1]:\n"
            "                return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\btoeplitz\b|"
                    r"\bis_toeplitz_matrix\b|"
                    r"\btoeplitz matrix\b",
                    low,
                )
            ),
            (
                (([[1, 2, 3, 4], [5, 1, 2, 3], [9, 5, 1, 2]],), True),
                (([[1, 2], [2, 2]],), False),
            ),
        ),
        T(
            "rectangle_overlap",
            "def rectangle_overlap(rec1, rec2):\n"
            '    """True if two axis-aligned rectangles [x1,y1,x2,y2] overlap."""\n'
            "    a = list(rec1)\n"
            "    b = list(rec2)\n"
            "    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]\n",
            lambda low: bool(
                re.search(
                    r"\brectangle overlap\b|"
                    r"\brectangle_overlap\b|"
                    r"\brectangles overlap\b",
                    low,
                )
            ),
            (
                (([0, 0, 2, 2], [1, 1, 3, 3]), True),
                (([0, 0, 1, 1], [1, 0, 2, 1]), False),
            ),
        ),
        T(
            "long_pressed_name",
            "def is_long_pressed_name(name, typed):\n"
            '    """True if typed could be name with some letters long-pressed."""\n'
            "    name, typed = str(name), str(typed)\n"
            "    i = 0\n"
            "    for j, ch in enumerate(typed):\n"
            "        if i < len(name) and name[i] == ch:\n"
            "            i += 1\n"
            "        elif j == 0 or ch != typed[j - 1]:\n"
            "            return False\n"
            "    return i == len(name)\n",
            lambda low: bool(
                re.search(
                    r"\blong pressed name\b|"
                    r"\bis_long_pressed_name\b|"
                    r"\blong-pressed name\b|"
                    r"\blong pressed\b",
                    low,
                )
            ),
            ((("alex", "aaleex"), True), (("saeed", "ssaaedd"), False), (("leelee", "lleeelee"), True)),
        ),
        T(
            "delete_columns_to_make_sorted",
            "def min_deletion_size(strs):\n"
            '    """Count columns that are not lexicographically sorted top to bottom."""\n'
            "    rows = [str(s) for s in strs]\n"
            "    if not rows:\n"
            "        return 0\n"
            "    n = len(rows[0])\n"
            "    deleted = 0\n"
            "    for c in range(n):\n"
            "        col = [row[c] for row in rows]\n"
            "        if col != sorted(col):\n"
            "            deleted += 1\n"
            "    return deleted\n",
            lambda low: bool(
                re.search(
                    r"\bdelete columns to make sorted\b|"
                    r"\bmin_deletion_size\b|"
                    r"\bdelete_columns_to_make_sorted\b|"
                    r"\bmin deletion size\b",
                    low,
                )
            )
            and "sorted list" not in low,
            (
                ((["cba", "daf", "ghi"],), 1),
                ((["a", "b"],), 0),
                ((["zyx", "wvu", "tsr"],), 3),
            ),
        ),
        T(
            "verify_alien_dictionary",
            "def is_alien_sorted(words, order):\n"
            '    """True if words are sorted by the given alien alphabet order."""\n'
            "    rank = {ch: i for i, ch in enumerate(str(order))}\n"
            "    def key(w):\n"
            "        return tuple(rank[ch] for ch in str(w))\n"
            "    seq = [str(w) for w in words]\n"
            "    return all(key(seq[i]) <= key(seq[i + 1]) for i in range(len(seq) - 1))\n",
            lambda low: bool(
                re.search(
                    r"\bverify alien dictionary\b|"
                    r"\bis_alien_sorted\b|"
                    r"\bis alien sorted\b|"
                    r"\bverify_alien_dictionary\b",
                    low,
                )
            ),
            (
                ((["hello", "leetcode"], "hlabcdefgijkmnopqrstuvwxyz"), True),
                ((["word", "world", "row"], "worldabcefghijkmnpqstuvxyz"), False),
            ),
        ),
        T(
            "repeated_n_times",
            "def repeated_n_times(nums):\n"
            '    """Return the element that appears n times in a 2n-length array."""\n'
            "    seen = set()\n"
            "    for x in nums:\n"
            "        if x in seen:\n"
            "            return x\n"
            "        seen.add(x)\n"
            "    return nums[0]\n",
            lambda low: bool(
                re.search(
                    r"\brepeated n times\b|"
                    r"\brepeated_n_times\b|"
                    r"\bn-times repeated\b",
                    low,
                )
            )
            and "majority" not in low,
            (
                (([1, 2, 3, 3],), 3),
                (([2, 1, 2, 5, 3, 2],), 2),
                (([5, 1, 5, 2, 5, 3, 5, 4],), 5),
            ),
        ),
    ]
