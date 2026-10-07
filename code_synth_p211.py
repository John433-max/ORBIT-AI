"""Cycle 495: exclusive phrase templates that previously missed the router.

zip longest, truncate, all equal, frequency map, intersperse, ensure prefix.
Pad-left is an alias on left_pad (p196), not a second template.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "zip_longest",
            "def zip_longest(a, b, fill=None):\n"
            '    """Pair items, padding the shorter side with fill."""\n'
            "    a = list(a)\n"
            "    b = list(b)\n"
            "    n = max(len(a), len(b))\n"
            "    out = []\n"
            "    for i in range(n):\n"
            "        left = a[i] if i < len(a) else fill\n"
            "        right = b[i] if i < len(b) else fill\n"
            "        out.append((left, right))\n"
            "    return out\n",
            lambda low: "zip longest" in low or "ziplongest" in low,
            (
                (([1, 2], ["a"]), [(1, "a"), (2, None)]),
                (([1], ["a", "b"], "x"), [(1, "a"), ("x", "b")]),
                (([], []), []),
            ),
        ),
        T(
            "truncate_string",
            "def truncate_string(text, limit, ellipsis=\"...\"):\n"
            '    """Shorten text to limit characters, appending ellipsis if cut."""\n'
            "    text = str(text)\n"
            "    limit = int(limit)\n"
            "    if limit < 0 or len(text) <= limit:\n"
            "        return text\n"
            "    mark = str(ellipsis)\n"
            "    if limit <= len(mark):\n"
            "        return text[:limit]\n"
            "    return text[: limit - len(mark)] + mark\n",
            lambda low: "truncate" in low and "sql" not in low and "table" not in low,
            (
                (("hello", 10), "hello"),
                (("hello world", 8), "hello..."),
                (("", 3), ""),
            ),
        ),
        T(
            "all_equal",
            "def all_equal(items):\n"
            '    """True when every item equals the first (empty is True)."""\n'
            "    items = list(items)\n"
            "    if not items:\n"
            "        return True\n"
            "    head = items[0]\n"
            "    return all(item == head for item in items)\n",
            lambda low: (
                (
                    "all equal" in low
                    or "all the same" in low
                    or "all identical" in low
                    or "all items are equal" in low
                    or "all items equal" in low
                    or "all elements are equal" in low
                )
                and "unique" not in low
                and "leetcode" not in low
                and "transform" not in low
                and "make equal" not in low
                and "to all equal" not in low
            ),
            (
                (([1, 1, 1],), True),
                (([1, 2],), False),
                (([],), True),
            ),
        ),
        T(
            "frequency_map",
            "def frequency_map(items):\n"
            '    """Count how often each item appears."""\n'
            "    counts = {}\n"
            "    for item in items:\n"
            "        counts[item] = counts.get(item, 0) + 1\n"
            "    return counts\n",
            lambda low: (
                ("frequency map" in low or "count map" in low or "freq map" in low)
                and "most common" not in low
            ),
            (
                (([1, 1, 2],), {1: 2, 2: 1}),
                ((["a"],), {"a": 1}),
                (([],), {}),
            ),
        ),
        T(
            "intersperse",
            "def intersperse(items, sep):\n"
            '    """Insert sep between items."""\n'
            "    items = list(items)\n"
            "    if not items:\n"
            "        return []\n"
            "    out = [items[0]]\n"
            "    for item in items[1:]:\n"
            "        out.append(sep)\n"
            "        out.append(item)\n"
            "    return out\n",
            lambda low: "intersperse" in low,
            (
                (([1, 2, 3], 0), [1, 0, 2, 0, 3]),
                ((["a"], "-"), ["a"]),
                (([], "-"), []),
            ),
        ),
        T(
            "ensure_prefix",
            "def ensure_prefix(text, prefix):\n"
            '    """Return text starting with prefix, adding it when missing."""\n'
            "    text = str(text)\n"
            "    prefix = str(prefix)\n"
            "    if text.startswith(prefix):\n"
            "        return text\n"
            "    return prefix + text\n",
            lambda low: (
                ("ensure a prefix" in low or "ensure prefix" in low or "ensure the prefix" in low)
                and "suffix" not in low
                and "starts with" not in low
            ),
            (
                (("world", "pre-"), "pre-world"),
                (("pre-world", "pre-"), "pre-world"),
                (("", "x"), "x"),
            ),
        ),
    ]
