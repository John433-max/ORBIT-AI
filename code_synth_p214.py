"""Cycle 498: exclusive phrase templates that previously missed the router.

first duplicate, drop None, list subset, remove at index, anti-diagonal, column means.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "first_duplicate",
            "def first_duplicate(items):\n"
            '    """First value that appears again, or None if every item is unique."""\n'
            "    seen = set()\n"
            "    for item in items:\n"
            "        if item in seen:\n"
            "            return item\n"
            "        seen.add(item)\n"
            "    return None\n",
            lambda low: (
                ("first duplicate" in low or "first repeated" in low)
                and "character" not in low
                and "non-repeating" not in low
                and "non repeating" not in low
            ),
            (
                (([1, 2, 3, 2, 1],), 2),
                (([4, 5, 6],), None),
                (([],), None),
            ),
        ),
        T(
            "drop_none",
            "def drop_none(items):\n"
            '    """Drop None values. Keep 0, False, and empty strings."""\n'
            "    return [item for item in items if item is not None]\n",
            lambda low: (
                ("none" in low or "null" in low)
                and any(w in low for w in ("remove", "drop", "filter", "strip"))
                and "index" not in low
            ),
            (
                (([1, None, 0, None, False],), [1, 0, False]),
                (([None, None],), []),
                (([],), []),
            ),
        ),
        T(
            "is_subset",
            "def is_subset(left, right):\n"
            '    """True when every item in left also appears in right (set semantics)."""\n'
            "    return set(left).issubset(right)\n",
            lambda low: (
                ("is subset" in low or "is a subset" in low or "is_subset" in low)
                and "superset" not in low
                and "all subsets" not in low
                and "subsets of" not in low
                and "power set" not in low
                and "with dup" not in low
                and "duplicate" not in low
            ) or (
                "subset of" in low
                and "all" not in low
                and "power" not in low
                and "subsets" not in low
            ),
            (
                (([1, 2], [2, 1, 3]), True),
                (([1, 4], [1, 2]), False),
                (([], [1]), True),
            ),
        ),
        T(
            "remove_at",
            "def remove_at(items, index):\n"
            '    """Return a new list without the item at index. Out of range returns a copy."""\n'
            "    if index < 0 or index >= len(items):\n"
            "        return list(items)\n"
            "    return list(items[:index]) + list(items[index + 1 :])\n",
            lambda low: (
                ("at an index" in low or "at index" in low)
                and any(w in low for w in ("remove", "delete", "drop"))
                and "none" not in low
            ),
            (
                (([10, 20, 30], 1), [10, 30]),
                (([1], 0), []),
                (([1, 2], 5), [1, 2]),
            ),
        ),
        T(
            "anti_diagonal",
            "def anti_diagonal(matrix):\n"
            '    """Secondary diagonal from the top-right toward the bottom-left."""\n'
            "    if not matrix or not matrix[0]:\n"
            "        return []\n"
            "    width = len(matrix[0])\n"
            "    out = []\n"
            "    for i, row in enumerate(matrix):\n"
            "        j = width - 1 - i\n"
            "        if j < 0 or j >= len(row):\n"
            "            break\n"
            "        out.append(row[j])\n"
            "    return out\n",
            lambda low: (
                "anti diagonal" in low
                or "anti-diagonal" in low
                or "secondary diagonal" in low
            ),
            (
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [3, 5, 7]),
                (([[1, 2], [3, 4]],), [2, 3]),
                (([],), []),
            ),
        ),
        T(
            "column_means",
            "def column_means(matrix):\n"
            '    """Arithmetic mean of each column. Uneven rows skip missing cells."""\n'
            "    if not matrix:\n"
            "        return []\n"
            "    width = max(len(row) for row in matrix)\n"
            "    out = []\n"
            "    for j in range(width):\n"
            "        vals = [row[j] for row in matrix if j < len(row)]\n"
            "        out.append(sum(vals) / len(vals) if vals else 0)\n"
            "    return out\n",
            lambda low: "column mean" in low or "mean of each column" in low,
            (
                (([[1, 2], [3, 4]],), [2.0, 3.0]),
                (([[1, 3, 5]],), [1.0, 3.0, 5.0]),
                (([],), []),
            ),
        ),
    ]
