"""Cycle 490: phrase-specific matrix/string/list utilities that still fell through."""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "column_sums",
            "def column_sums(rows):\n"
            '    """Sum each column of a rectangular matrix. Empty input returns []."""\n'
            "    rows = list(rows)\n"
            "    if not rows:\n"
            "        return []\n"
            "    width = len(rows[0])\n"
            "    out = [0] * width\n"
            "    for row in rows:\n"
            "        for i, value in enumerate(row):\n"
            "            out[i] += value\n"
            "    return out\n",
            lambda low: "column" in low and "sum" in low and "row" not in low,
            (
                (([[1, 2], [3, 4]],), [4, 6]),
                (([[5]],), [5]),
                (([],), []),
            ),
        ),
        T(
            "zip_with_index",
            "def zip_with_index(items):\n"
            '    """Pair each item with its index as (index, item)."""\n'
            "    return [(i, item) for i, item in enumerate(items)]\n",
            lambda low: (
                "index" in low
                and ("pair" in low or "zip" in low)
                and "string" not in low
                and "search" not in low
            ),
            (
                ((["a", "b"],), [(0, "a"), (1, "b")]),
                (([],), []),
                (([9],), [(0, 9)]),
            ),
        ),
        T(
            "mask_email",
            "def mask_email(value):\n"
            '    """Mask an email local-part, keeping the first character and domain."""\n'
            "    s = str(value)\n"
            "    if '@' not in s:\n"
            "        return s\n"
            "    local, domain = s.split('@', 1)\n"
            "    if not local:\n"
            "        return s\n"
            "    return local[0] + ('*' * (len(local) - 1)) + '@' + domain\n",
            lambda low: "email" in low and "mask" in low,
            (
                (("ada@example.com",), "a**@example.com"),
                (("a@x.io",), "a@x.io"),
                (("no-at",), "no-at"),
            ),
        ),
        T(
            "running_diff",
            "def running_diff(nums):\n"
            '    """Differences between consecutive numbers. Fewer than 2 items returns []."""\n'
            "    nums = list(nums)\n"
            "    return [nums[i] - nums[i - 1] for i in range(1, len(nums))]\n",
            lambda low: (
                "consecutive" in low
                and "difference" in low
                and "list" in low
                and "duplicate" not in low
                and "group" not in low
            ),
            (
                (([3, 8, 6],), [5, -2]),
                (([4],), []),
                (([],), []),
            ),
        ),
        T(
            "strip_prefix",
            "def strip_prefix(s, prefix):\n"
            '    """Remove prefix from s once if present. Otherwise return s."""\n'
            "    s, prefix = str(s), str(prefix)\n"
            "    if prefix and s.startswith(prefix):\n"
            "        return s[len(prefix):]\n"
            "    return s\n",
            lambda low: "strip" in low and "prefix" in low and "suffix" not in low,
            (
                (("unhappy", "un"), "happy"),
                (("abc", "z"), "abc"),
                (("", "a"), ""),
            ),
        ),
        T(
            "repeat_each",
            "def repeat_each(items, n):\n"
            '    """Repeat each item n times. n < 1 returns []."""\n'
            "    n = int(n)\n"
            "    if n < 1:\n"
            "        return []\n"
            "    out = []\n"
            "    for item in items:\n"
            "        out.extend([item] * n)\n"
            "    return out\n",
            lambda low: ("repeat each" in low or "repeats each" in low) and "string" not in low,
            (
                ((["a", "b"], 2), ["a", "a", "b", "b"]),
                (([1], 0), []),
                (([], 3), []),
            ),
        ),
    ]
