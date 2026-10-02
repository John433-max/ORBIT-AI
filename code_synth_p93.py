"""Cycle 368: different integers, min distance to target, redistribute chars, typed words, fancy string, convert XXX."""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "num_different_integers",
            "def num_different_integers(word):\n"
            '    """Count distinct integers in word, ignoring leading zeros (LeetCode 1805)."""\n'
            "    seen = set()\n"
            "    cur = []\n"
            "    for ch in word + \"a\":\n"
            "        if ch.isdigit():\n"
            "            cur.append(ch)\n"
            "        elif cur:\n"
            "            seen.add(int(\"\".join(cur)))\n"
            "            cur = []\n"
            "    return len(seen)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber of different integers\b|"
                    r"\bdifferent integers in a string\b|"
                    r"\bleetcode 1805\b",
                    low,
                )
            ),
            (
                (("a123bc34d8ef34",), 3),
                (("leet1234code234",), 2),
                (("a1b01c001",), 1),
            ),
        ),
        T(
            "min_distance_target",
            "def min_distance_target(nums, target, start):\n"
            '    """Min |i-start| with nums[i]==target (LeetCode 1848)."""\n'
            "    best = None\n"
            "    for i, value in enumerate(nums):\n"
            "        if value == target:\n"
            "            dist = abs(i - start)\n"
            "            if best is None or dist < best:\n"
            "                best = dist\n"
            "    return 0 if best is None else best\n"
            "\n"
            "def getMinDistance(nums, target, start):\n"
            "    return min_distance_target(nums, target, start)\n",
            lambda low: bool(
                re.search(
                    r"\bminimum distance to the target element\b|"
                    r"\bmin distance to the target\b|"
                    r"\bleetcode 1848\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4, 5], 5, 3), 1),
                (([1], 1, 0), 0),
                (([1, 2, 3, 4, 5], 2, 4), 3),
            ),
        ),
        T(
            "make_equal_strings",
            "def make_equal_strings(words):\n"
            '    """True if chars can be redistributed so every word is equal (LeetCode 1897)."""\n'
            "    from collections import Counter\n"
            "    counts = Counter()\n"
            "    for word in words:\n"
            "        counts.update(word)\n"
            "    n = len(words)\n"
            "    return all(c % n == 0 for c in counts.values())\n"
            "\n"
            "def makeEqual(words):\n"
            "    return make_equal_strings(words)\n",
            lambda low: bool(
                re.search(
                    r"\bredistribute characters\b|"
                    r"\bmake all strings equal\b|"
                    r"\bleetcode 1897\b",
                    low,
                )
            ),
            (
                ((["abc", "aabc", "bc"],), True),
                ((["ab", "a"],), False),
            ),
        ),
        T(
            "can_be_typed_words",
            "def can_be_typed_words(text, broken_letters):\n"
            '    """Words typeable without broken letters (LeetCode 1935)."""\n'
            "    broken = set(broken_letters)\n"
            "    return sum(1 for word in text.split() if broken.isdisjoint(word))\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum number of words you can type\b|"
                    r"\bwords you can type\b|"
                    r"\bbroken letters\b|"
                    r"\bleetcode 1935\b",
                    low,
                )
            ),
            (
                (("hello world", "ad"), 1),
                (("leet code", "lt"), 1),
                (("leet code", "e"), 0),
            ),
        ),
        T(
            "make_fancy_string",
            "def make_fancy_string(s):\n"
            '    """Delete chars so no three identical letters are consecutive (LeetCode 1957)."""\n'
            "    out = []\n"
            "    for ch in s:\n"
            "        if len(out) >= 2 and out[-1] == ch and out[-2] == ch:\n"
            "            continue\n"
            "        out.append(ch)\n"
            "    return \"\".join(out)\n",
            lambda low: bool(
                re.search(
                    r"\bfancy string\b|"
                    r"\bdelete characters to make fancy\b|"
                    r"\bleetcode 1957\b",
                    low,
                )
            ),
            (
                (("leeetcode",), "leetcode"),
                (("aaabaaaa",), "aabaa"),
                (("aab",), "aab"),
            ),
        ),
        T(
            "minimum_moves_convert_string",
            "def minimum_moves_convert_string(s):\n"
            '    """Min moves to turn s into all O; a move covers 3 indices (LeetCode 2027)."""\n'
            "    moves = 0\n"
            "    i = 0\n"
            "    n = len(s)\n"
            "    while i < n:\n"
            "        if s[i] == \"X\":\n"
            "            moves += 1\n"
            "            i += 3\n"
            "        else:\n"
            "            i += 1\n"
            "    return moves\n",
            lambda low: bool(
                re.search(
                    r"\bminimum moves to convert string\b|"
                    r"\bconvert string to all o\b|"
                    r"\bleetcode 2027\b",
                    low,
                )
            ),
            (
                (("XXX",), 1),
                (("XXOX",), 2),
                (("OOOO",), 0),
            ),
        ),
    ]
