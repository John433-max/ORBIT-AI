"""Cycle 489: phrase-specific string/list utilities that still fell through."""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "squeeze_spaces",
            "def squeeze_spaces(s):\n"
            '    """Collapse runs of spaces or tabs to a single space and strip ends."""\n'
            "    out = []\n"
            "    prev_space = False\n"
            "    for ch in str(s).replace('\\t', ' '):\n"
            "        if ch == ' ':\n"
            "            if not prev_space:\n"
            "                out.append(' ')\n"
            "            prev_space = True\n"
            "        else:\n"
            "            out.append(ch)\n"
            "            prev_space = False\n"
            "    return ''.join(out).strip()\n",
            lambda low: (
                "string" in low
                and "newline" not in low
                and (
                    "multiple spaces" in low
                    or "extra spaces" in low
                    or "collapse spaces" in low
                    or "squeeze spaces" in low
                )
            ),
            (
                (("a  b\tc",), "a b c"),
                (("  hi   ",), "hi"),
                (("",), ""),
            ),
        ),
        T(
            "center_text",
            "def center_text(s, width, fill=' '):\n"
            '    """Center s in width using fill. Wider strings are unchanged."""\n'
            "    s = str(s)\n"
            "    fill = (str(fill) or ' ')[:1]\n"
            "    width = int(width)\n"
            "    if width <= len(s):\n"
            "        return s\n"
            "    pad = width - len(s)\n"
            "    left = pad // 2\n"
            "    return fill * left + s + fill * (pad - left)\n",
            lambda low: (
                "center" in low
                and "string" in low
                and "pad" not in low
                and "matrix" not in low
                and "window" not in low
            ),
            (
                (("ab", 6, "*"), "**ab**"),
                (("ab", 5, "-"), "-ab--"),
                (("hello", 3, " "), "hello"),
            ),
        ),
        T(
            "drop_consecutive",
            "def drop_consecutive(items):\n"
            '    """Drop adjacent duplicates, keeping the first of each run."""\n'
            "    out = []\n"
            "    for x in items:\n"
            "        if not out or out[-1] != x:\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: (
                "consecutive" in low
                and "duplicate" in low
                and "list" in low
                and "group" not in low
            ),
            (
                (([1, 1, 2, 2, 2, 1],), [1, 2, 1]),
                (([1],), [1]),
                (([],), []),
            ),
        ),
        T(
            "sliding_windows",
            "def sliding_windows(items, k):\n"
            '    """Consecutive overlapping windows of length k. k<=0 yields []."""\n'
            "    xs = list(items)\n"
            "    k = int(k)\n"
            "    if k <= 0:\n"
            "        return []\n"
            "    return [xs[i:i + k] for i in range(0, max(0, len(xs) - k + 1))]\n",
            lambda low: "sliding" in low and "window" in low and ("list" in low or "sequence" in low),
            (
                (([1, 2, 3, 4], 2), [[1, 2], [2, 3], [3, 4]]),
                (([1, 2], 3), []),
                (([], 2), []),
            ),
        ),
        T(
            "split_half",
            "def split_half(items):\n"
            '    """Split a list into (left, right). Left gets the floor half."""\n'
            "    xs = list(items)\n"
            "    mid = len(xs) // 2\n"
            "    return xs[:mid], xs[mid:]\n",
            lambda low: (
                "half" in low
                and "split" in low
                and "list" in low
                and "chunk" not in low
                and "pair" not in low
            ),
            (
                (([1, 2, 3, 4],), ([1, 2], [3, 4])),
                (([1, 2, 3],), ([1], [2, 3])),
                (([],), ([], [])),
            ),
        ),
        T(
            "unzip_pairs",
            "def unzip_pairs(pairs):\n"
            '    """Unzip (a, b) pairs into two lists. Empty input yields two empty lists."""\n'
            "    left, right = [], []\n"
            "    for pair in pairs:\n"
            "        a, b = pair\n"
            "        left.append(a)\n"
            "        right.append(b)\n"
            "    return left, right\n",
            lambda low: "unzip" in low and ("pair" in low or "pairs" in low),
            (
                (([(1, "a"), (2, "b")],), ([1, 2], ["a", "b"])),
                (([],), ([], [])),
                (([(0, 1)],), ([0], [1])),
            ),
        ),
    ]
