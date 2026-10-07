"""Cycle 496: exclusive phrase templates that previously missed the router.

sliding windows, take while, drop while, common prefix, sign, cumulative product.
Pad-right is an alias on right_pad (p197), not a second template.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "sliding_windows",
            "def sliding_windows(items, size):\n"
            '    """Contiguous windows of length size. Empty if size is invalid."""\n'
            "    items = list(items)\n"
            "    size = int(size)\n"
            "    if size <= 0 or size > len(items):\n"
            "        return []\n"
            "    return [items[i : i + size] for i in range(len(items) - size + 1)]\n",
            lambda low: (
                ("sliding window" in low or "sliding windows" in low)
                and "maximum" not in low
                and "minimum" not in low
            ),
            (
                (([1, 2, 3, 4], 2), [[1, 2], [2, 3], [3, 4]]),
                (([1, 2, 3], 3), [[1, 2, 3]]),
                (([1], 2), []),
            ),
        ),
        T(
            "take_while",
            "def take_while(items, limit):\n"
            '    """Prefix of items strictly less than limit."""\n'
            "    out = []\n"
            "    for item in items:\n"
            "        if not item < limit:\n"
            "            break\n"
            "        out.append(item)\n"
            "    return out\n",
            lambda low: "take while" in low and "drop" not in low,
            (
                (([1, 2, 5, 3], 5), [1, 2]),
                (([0, 1, 2], 0), []),
                (([], 3), []),
            ),
        ),
        T(
            "drop_while",
            "def drop_while(items, limit):\n"
            '    """Drop a prefix of items strictly less than limit."""\n'
            "    items = list(items)\n"
            "    i = 0\n"
            "    while i < len(items) and items[i] < limit:\n"
            "        i += 1\n"
            "    return items[i:]\n",
            lambda low: "drop while" in low and "take while" not in low,
            (
                (([1, 2, 5, 3], 5), [5, 3]),
                (([1, 2], 0), [1, 2]),
                (([], 3), []),
            ),
        ),
        T(
            "common_prefix",
            "def common_prefix(words):\n"
            '    """Longest string prefix shared by every word. Empty list is empty."""\n'
            "    words = [str(w) for w in words]\n"
            "    if not words:\n"
            "        return \"\"\n"
            "    prefix = words[0]\n"
            "    for word in words[1:]:\n"
            "        while not word.startswith(prefix):\n"
            "            prefix = prefix[:-1]\n"
            "            if not prefix:\n"
            "                return \"\"\n"
            "    return prefix\n",
            lambda low: "common prefix" in low and "suffix" not in low,
            (
                ((["flower", "flow", "flight"],), "fl"),
                ((["dog", "racecar"],), ""),
                (([],), ""),
            ),
        ),
        T(
            "sign",
            "def sign(n):\n"
            '    """Sign of a number: -1, 0, or 1."""\n'
            "    n = float(n)\n"
            "    if n > 0:\n"
            "        return 1\n"
            "    if n < 0:\n"
            "        return -1\n"
            "    return 0\n",
            lambda low: (
                ("sign of" in low or "signum" in low or low.strip().endswith(" sign"))
                and "assign" not in low
                and "design" not in low
                and "significant" not in low
            ),
            (
                ((5,), 1),
                ((-3.2,), -1),
                ((0,), 0),
            ),
        ),
        T(
            "cumulative_product",
            "def cumulative_product(nums):\n"
            '    """Running product. Empty input is an empty list."""\n'
            "    out = []\n"
            "    acc = 1\n"
            "    for n in nums:\n"
            "        acc *= n\n"
            "        out.append(acc)\n"
            "    return out\n",
            lambda low: (
                ("cumulative product" in low or "running product" in low)
                and "sum" not in low
            ),
            (
                (([1, 2, 3, 4],), [1, 2, 6, 24]),
                (([2, 0, 5],), [2, 0, 0]),
                (([],), []),
            ),
        ),
    ]
