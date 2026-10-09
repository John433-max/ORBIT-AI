"""Cycle 527: coding prompts stolen by generic factors/acronym/replace_all.

LeetCode 1952 Three Divisors, 2828 Acronym of Words, 1576 Modify String.
Loaded before p237/p238 so the specific names win. Official examples only.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "is_three",
            "def is_three(n):\n"
            '    """True if n has exactly three positive divisors (square of a prime)."""\n'
            "    n = int(n)\n"
            "    if n < 4:\n"
            "        return False\n"
            "    root = int(n ** 0.5)\n"
            "    if root * root != n:\n"
            "        return False\n"
            "    if root < 2:\n"
            "        return False\n"
            "    i = 2\n"
            "    while i * i <= root:\n"
            "        if root % i == 0:\n"
            "            return False\n"
            "        i += 1\n"
            "    return True\n",
            lambda low: bool(
                re.search(r"\bthree divisors\b|\bleetcode 1952\b", low)
            ),
            (
                ((4,), True),
                ((2,), False),
                ((9,), True),
            ),
        ),
        T(
            "is_acronym",
            "def is_acronym(words, s):\n"
            '    """True if s is the acronym formed by words (LeetCode 2828)."""\n'
            "    return \"\".join(w[0] for w in words if w) == s\n",
            lambda low: (
                "acronym of words" in low
                or "is an acronym" in low
                or "leetcode 2828" in low
            )
            and "builds an acronym" not in low
            and "build an acronym" not in low,
            (
                ((["alice", "bob", "charlie"], "abc"), True),
                ((["an", "apple"], "a"), False),
                ((["never", "gonna", "give", "up", "on", "you"], "ngguoy"), True),
            ),
        ),
        T(
            "modify_string",
            "def modify_string(s):\n"
            '    """Replace \'?\' so no two adjacent letters match (LeetCode 1576)."""\n'
            "    chars = list(s)\n"
            "    for i, ch in enumerate(chars):\n"
            "        if ch != \'?\':\n"
            "            continue\n"
            "        prev = chars[i - 1] if i else \"\"\n"
            "        nxt = chars[i + 1] if i + 1 < len(chars) else \"\"\n"
            "        for cand in \"abc\":\n"
            "            if cand != prev and cand != nxt:\n"
            "                chars[i] = cand\n"
            "                break\n"
            "    return \"\".join(chars)\n",
            lambda low: (
                "leetcode 1576" in low
                or (
                    "question mark" in low
                    and ("consecutive" in low or "repeating" in low)
                )
            ),
            (
                (("?zs",), "azs"),
                (("ubv?w",), "ubvaw"),
                (("???",), "aba"),
            ),
        ),
    ]
