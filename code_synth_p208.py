"""Cycle 492: phrase asks that still missed the template router.

digit_sum declines LeetCode siblings (even digit sum, alternating, base-k)
so earlier specific templates stay the winner.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "middle_element",
            "def middle_element(items):\n"
            '    """Return the lower-middle item. Empty list returns None."""\n'
            "    items = list(items)\n"
            "    if not items:\n"
            "        return None\n"
            "    return items[(len(items) - 1) // 2]\n",
            lambda low: (
                "middle" in low
                and "element" in low
                and "linked" not in low
                and "node" not in low
            ),
            (
                (([1, 2, 3, 4, 5],), 3),
                (([1, 2, 3, 4],), 2),
                (([],), None),
            ),
        ),
        T(
            "repeat_until_length",
            "def repeat_until_length(items, n):\n"
            '    """Cycle items until length n. Empty source stays empty."""\n'
            "    items = list(items)\n"
            "    n = int(n)\n"
            "    if n <= 0 or not items:\n"
            "        return []\n"
            "    out = []\n"
            "    i = 0\n"
            "    while len(out) < n:\n"
            "        out.append(items[i % len(items)])\n"
            "        i += 1\n"
            "    return out\n",
            lambda low: (
                "repeat" in low
                and "list" in low
                and "until" in low
                and "length" in low
            ),
            (
                (([1, 2], 5), [1, 2, 1, 2, 1]),
                ((["a"], 3), ["a", "a", "a"]),
                (([], 4), []),
            ),
        ),
        T(
            "swap_adjacent",
            "def swap_adjacent(items):\n"
            '    """Swap each pair of neighbors. An odd tail stays put."""\n'
            "    items = list(items)\n"
            "    out = items[:]\n"
            "    for i in range(0, len(out) - 1, 2):\n"
            "        out[i], out[i + 1] = out[i + 1], out[i]\n"
            "    return out\n",
            lambda low: "adjacent" in low and "swap" in low,
            (
                (([1, 2, 3, 4],), [2, 1, 4, 3]),
                (([1, 2, 3],), [2, 1, 3]),
                (([9],), [9]),
            ),
        ),
        T(
            "insert_at",
            "def insert_at(items, index, value):\n"
            '    """Insert value at index, clamping the index into range."""\n'
            "    items = list(items)\n"
            "    index = int(index)\n"
            "    if index < 0:\n"
            "        index = 0\n"
            "    if index > len(items):\n"
            "        index = len(items)\n"
            "    items.insert(index, value)\n"
            "    return items\n",
            lambda low: (
                "insert" in low
                and "index" in low
                and "binary" not in low
                and "search" not in low
            ),
            (
                (([1, 2, 3], 1, 9), [1, 9, 2, 3]),
                (([1], 5, 0), [1, 0]),
                (([], 0, "a"), ["a"]),
            ),
        ),
        T(
            "remove_at",
            "def remove_at(items, index):\n"
            '    """Drop the item at index. Out-of-range index leaves the list unchanged."""\n'
            "    items = list(items)\n"
            "    index = int(index)\n"
            "    if index < 0 or index >= len(items):\n"
            "        return items\n"
            "    del items[index]\n"
            "    return items\n",
            lambda low: (
                ("remove" in low or "removes" in low or "drop" in low)
                and "index" in low
                and "element" in low
                and "nth" not in low
            ),
            (
                (([1, 2, 3], 1), [1, 3]),
                (([1, 2], 9), [1, 2]),
                (([], 0), []),
            ),
        ),
        T(
            "digit_sum",
            "def digit_sum(n):\n"
            '    """Sum decimal digits of n, ignoring sign."""\n'
            "    n = abs(int(n))\n"
            "    total = 0\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    while n:\n"
            "        total += n % 10\n"
            "        n //= 10\n"
            "    return total\n",
            lambda low: (
                "digit" in low
                and "sum" in low
                and "product" not in low
                and "string" not in low
                and "alternat" not in low
                and "leetcode" not in low
                and "base" not in low
                and "even" not in low
                and "count" not in low
                and "convert" not in low
                and "element" not in low
                and "index" not in low
                and "divisib" not in low
            ),
            (
                ((123,), 6),
                ((-45,), 9),
                ((0,), 0),
            ),
        ),
    ]
