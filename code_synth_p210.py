"""Cycle 494: join words, enumerate, dedupe, pairwise, numbered lines, ensure suffix.

join_words requires word so list joins stay free. dedupe does not use
"remove duplicates" (remove_duplicates). enumerate excludes tree/graph.
ensure_suffix requires suffix and declines prefix asks.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "join_words",
            "def join_words(words, sep=\" \"):\n"
            '    """Join words with a separator."""\n'
            "    return sep.join(str(w) for w in words)\n",
            lambda low: (
                "join" in low
                and "word" in low
                and "sql" not in low
            ),
            (
                ((["a", "b"], "-"), "a-b"),
                ((["a", "b"],), "a b"),
                (([], ","), ""),
            ),
        ),
        T(
            "enumerate_list",
            "def enumerate_list(items, start=0):\n"
            '    """Return (index, item) pairs."""\n'
            "    return list(enumerate(items, start))\n",
            lambda low: "enumerate" in low and "tree" not in low and "graph" not in low,
            (
                ((["a", "b"],), [(0, "a"), (1, "b")]),
                ((["a"], 1), [(1, "a")]),
                (([],), []),
            ),
        ),
        T(
            "dedupe_list",
            "def dedupe_list(items):\n"
            '    """Drop later duplicates, preserving order."""\n'
            "    seen = set()\n"
            "    out = []\n"
            "    for item in items:\n"
            "        if item in seen:\n"
            "            continue\n"
            "        seen.add(item)\n"
            "        out.append(item)\n"
            "    return out\n",
            lambda low: "dedupe" in low or "de-duplicate" in low or "deduplicate" in low,
            (
                (([1, 2, 1, 3],), [1, 2, 3]),
                ((["a", "a"],), ["a"]),
                (([],), []),
            ),
        ),
        T(
            "pairwise",
            "def pairwise(items):\n"
            '    """Adjacent overlapping pairs."""\n'
            "    items = list(items)\n"
            "    return [(items[i], items[i + 1]) for i in range(len(items) - 1)]\n",
            lambda low: "pairwise" in low or "adjacent pair" in low,
            (
                (([1, 2, 3, 4],), [(1, 2), (2, 3), (3, 4)]),
                (([1],), []),
                (([],), []),
            ),
        ),
        T(
            "number_lines",
            "def number_lines(text, start=1):\n"
            '    """Prefix each line with its number."""\n'
            "    lines = str(text).splitlines()\n"
            "    return \"\\n\".join(f\"{start + i} {line}\" for i, line in enumerate(lines))\n",
            lambda low: (
                bool(re.search(r"\blines?\b", low))
                and ("number" in low or "prefix" in low)
                and "leetcode" not in low
                and "linked" not in low
                and "interpolat" not in low
                and "number of lines" not in low
                and "widths" not in low
            ),
            (
                (("a\nb",), "1 a\n2 b"),
                (("a", 3), "3 a"),
                (("",), ""),
            ),
        ),
        T(
            "ensure_suffix",
            "def ensure_suffix(text, suffix):\n"
            '    """Append suffix when it is missing."""\n'
            "    text = str(text)\n"
            "    suffix = str(suffix)\n"
            "    if text.endswith(suffix):\n"
            "        return text\n"
            "    return text + suffix\n",
            lambda low: "suffix" in low and "prefix" not in low,
            (
                (("file", ".txt"), "file.txt"),
                (("file.txt", ".txt"), "file.txt"),
                (("", ".txt"), ".txt"),
            ),
        ),
    ]
