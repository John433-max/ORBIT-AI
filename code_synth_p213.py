"""Cycle 497: exclusive phrase templates that previously missed the router.

matrix diagonal, last index, replace value, all unique, alternating case, row sums.
group_consecutive (p203) no longer requires the word list.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "matrix_diagonal",
            "def matrix_diagonal(matrix):\n"
            '    """Main diagonal of a matrix. Empty if a row is too short."""\n'
            "    if not matrix or not matrix[0]:\n"
            "        return []\n"
            "    out = []\n"
            "    for i, row in enumerate(matrix):\n"
            "        if i >= len(row):\n"
            "            break\n"
            "        out.append(row[i])\n"
            "    return out\n",
            lambda low: (
                ("main diagonal" in low or "matrix diagonal" in low or "diagonal of a matrix" in low)
                and "anti" not in low
                and "secondary" not in low
            ),
            (
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 5, 9]),
                (([[1, 2], [3, 4]],), [1, 4]),
                (([],), []),
            ),
        ),
        T(
            "last_index",
            "def last_index(items, value):\n"
            '    """Last index of value, or -1 if it is absent."""\n'
            "    for i in range(len(items) - 1, -1, -1):\n"
            "        if items[i] == value:\n"
            "            return i\n"
            "    return -1\n",
            lambda low: "last index" in low and "first" not in low,
            (
                (([1, 2, 1, 3], 1), 2),
                (([4, 5], 9), -1),
                (([], 1), -1),
            ),
        ),
        T(
            "replace_value",
            "def replace_value(items, old, new):\n"
            '    """Replace every equal occurrence of old with new."""\n'
            "    return [new if item == old else item for item in items]\n",
            lambda low: (
                ("replace every" in low or "replaces every" in low or "replace all occurrences" in low)
                and "digit" not in low
                and "string" not in low
            ),
            (
                (([1, 2, 1, 3], 1, 9), [9, 2, 9, 3]),
                ((["a", "b"], "a", "z"), ["z", "b"]),
                (([], 1, 2), []),
            ),
        ),
        T(
            "all_unique",
            "def all_unique(items):\n"
            '    """True when every item appears once. Unhashable items compare by equality."""\n'
            "    seen = []\n"
            "    for item in items:\n"
            "        if item in seen:\n"
            "            return False\n"
            "        seen.append(item)\n"
            "    return True\n",
            lambda low: (
                ("all unique" in low or "all items are unique" in low or "all elements are unique" in low)
                and "preserve" not in low
            ),
            (
                (([1, 2, 3],), True),
                (([1, 2, 1],), False),
                (([],), True),
            ),
        ),
        T(
            "alternating_case",
            "def alternating_case(text):\n"
            '    """Alternate upper and lower on letters; other characters stay put."""\n'
            "    out = []\n"
            "    upper = True\n"
            "    for ch in str(text):\n"
            "        if ch.isalpha():\n"
            "            out.append(ch.upper() if upper else ch.lower())\n"
            "            upper = not upper\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n",
            lambda low: "alternating case" in low and "swap" not in low,
            (
                (("hello",), "HeLlO"),
                (("a b",), "A b"),
                (("",), ""),
            ),
        ),
        T(
            "row_sums",
            "def row_sums(matrix):\n"
            '    """Sum of each row. Empty matrix is an empty list."""\n'
            "    return [sum(row) for row in matrix]\n",
            lambda low: "row sum" in low and "column" not in low,
            (
                (([[1, 2], [3, 4]],), [3, 7]),
                (([[5]],), [5]),
                (([],), []),
            ),
        ),
    ]
