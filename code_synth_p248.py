"""Cycle 551: Aho-Corasick multi-pattern string matching.

Loaded first so 'aho corasick' beats generic string search templates.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "aho_corasick",
            "def aho_corasick(text, patterns):\n"
            '    """All (start, pattern) matches via Aho-Corasick. Sorted by start then pattern."""\n'
            "    from collections import deque\n"
            "    class Node:\n"
            "        def __init__(self):\n"
            "            self.children = {}\n"
            "            self.fail = None\n"
            "            self.output = []\n"
            "    root = Node()\n"
            "    for pat in patterns:\n"
            "        node = root\n"
            "        for ch in pat:\n"
            "            node = node.children.setdefault(ch, Node())\n"
            "        node.output.append(pat)\n"
            "    q = deque()\n"
            "    for child in root.children.values():\n"
            "        child.fail = root\n"
            "        q.append(child)\n"
            "    while q:\n"
            "        cur = q.popleft()\n"
            "        for ch, nxt in cur.children.items():\n"
            "            fail = cur.fail\n"
            "            while fail is not None and ch not in fail.children:\n"
            "                fail = fail.fail\n"
            "            nxt.fail = fail.children[ch] if fail is not None else root\n"
            "            nxt.output = nxt.output + nxt.fail.output\n"
            "            q.append(nxt)\n"
            "    matches = []\n"
            "    node = root\n"
            "    for i, ch in enumerate(text):\n"
            "        while node is not root and ch not in node.children:\n"
            "            node = node.fail\n"
            "        node = node.children.get(ch, root)\n"
            "        for pat in node.output:\n"
            "            matches.append((i - len(pat) + 1, pat))\n"
            "    return sorted(matches)\n",
            lambda low: bool(
                re.search(
                    r"\baho[- ]?corasick\b|"
                    r"\bmulti[- ]pattern (?:string )?(?:matching|search)\b|"
                    r"\bmultiple pattern (?:string )?matching\b",
                    low,
                )
            ),
            (
                (("ushers", ["he", "she", "his", "hers"]), [(1, "she"), (2, "he"), (2, "hers")]),
                (("abcab", ["ab", "bc", "cab"]), [(0, "ab"), (1, "bc"), (2, "cab"), (3, "ab")]),
            ),
        ),
    ]
