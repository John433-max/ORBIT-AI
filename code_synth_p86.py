"""Cycle 360: unmatched Easy string templates.

Official problem statements (algorithms only, not copied text):
LeetCode 1047, 1544, 1592, 1624, 1796, 1961.
"""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "remove_all_adjacent_duplicates",
            "def remove_all_adjacent_duplicates(s):\n"
            '    """Stack-pop adjacent equal chars (LeetCode 1047)."""\n'
            "    stack = []\n"
            "    for ch in s:\n"
            "        if stack and stack[-1] == ch:\n"
            "            stack.pop()\n"
            "        else:\n"
            "            stack.append(ch)\n"
            "    return ''.join(stack)\n",
            lambda low: bool(
                re.search(
                    r"\bremove[_ ]all[_ ]adjacent[_ ]duplicates\b|"
                    r"\badjacent duplicates in (a )?string\b|"
                    r"\bleetcode 1047\b",
                    low,
                )
            ),
            (
                (("abbaca",), "ca"),
                (("azxxzy",), "ay"),
                (("a",), "a"),
            ),
        ),
        T(
            "make_good",
            "def make_good(s):\n"
            '    """Remove adjacent case-inverse pairs (LeetCode 1544)."""\n'
            "    stack = []\n"
            "    for ch in s:\n"
            "        if stack and stack[-1] != ch and stack[-1].lower() == ch.lower():\n"
            "            stack.pop()\n"
            "        else:\n"
            "            stack.append(ch)\n"
            "    return ''.join(stack)\n",
            lambda low: bool(
                re.search(
                    r"\bmake[_ ]the[_ ]string[_ ]great\b|"
                    r"\bmake[_ ]good\b|"
                    r"\bleetcode 1544\b",
                    low,
                )
            ),
            (
                (("leEeetcode",), "leetcode"),
                (("abBAcC",), ""),
                (("s",), "s"),
            ),
        ),
        T(
            "reorder_spaces",
            "def reorder_spaces(text):\n"
            '    """Evenly redistribute spaces between words (LeetCode 1592)."""\n'
            "    words = text.split()\n"
            "    spaces = text.count(' ')\n"
            "    if not words:\n"
            "        return ' ' * spaces\n"
            "    if len(words) == 1:\n"
            "        return words[0] + ' ' * spaces\n"
            "    gaps = len(words) - 1\n"
            "    each, extra = divmod(spaces, gaps)\n"
            "    return (' ' * each).join(words) + ' ' * extra\n",
            lambda low: bool(
                re.search(
                    r"\brearrange[_ ]spaces\b|"
                    r"\breorder[_ ]spaces\b|"
                    r"\bleetcode 1592\b",
                    low,
                )
            ),
            (
                (("  this   is  a sentence  ",), "this   is   a   sentence "),
                ((" practice   makes   perfect",), "practice   makes   perfect "),
                (("hello",), "hello"),
            ),
        ),
        T(
            "max_length_between_equal_characters",
            "def max_length_between_equal_characters(s):\n"
            '    """Largest gap between two equal chars (LeetCode 1624)."""\n'
            "    first = {}\n"
            "    best = -1\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch in first:\n"
            "            best = max(best, i - first[ch] - 1)\n"
            "        else:\n"
            "            first[ch] = i\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blargest substring between two equal\b|"
                    r"\bmax[_ ]length[_ ]between[_ ]equal\b|"
                    r"\bleetcode 1624\b",
                    low,
                )
            ),
            (
                (("aa",), 0),
                (("abca",), 2),
                (("cbzxy",), -1),
                (("cabbac",), 4),
            ),
        ),
        T(
            "second_highest",
            "def second_highest(s):\n"
            '    """Second-largest digit in a string, or -1 (LeetCode 1796)."""\n'
            "    digits = sorted({int(ch) for ch in s if ch.isdigit()}, reverse=True)\n"
            "    return digits[1] if len(digits) >= 2 else -1\n",
            lambda low: bool(
                re.search(
                    r"\bsecond[_ ]largest[_ ]digit\b|"
                    r"\bsecond[_ ]highest\b|"
                    r"\bleetcode 1796\b",
                    low,
                )
            ),
            (
                (("dfa12321afd",), 2),
                (("abc1111",), -1),
                (("ck077",), 0),
            ),
        ),
        T(
            "is_prefix_string",
            "def is_prefix_string(s, words):\n"
            '    """True if s is a concatenation prefix of words (LeetCode 1961)."""\n'
            "    built = ''\n"
            "    for w in words:\n"
            "        built += w\n"
            "        if built == s:\n"
            "            return True\n"
            "        if len(built) > len(s):\n"
            "            return False\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bprefix of array\b|"
                    r"\bis[_ ]prefix[_ ]string\b|"
                    r"\bleetcode 1961\b",
                    low,
                )
            ),
            (
                (("iloveleetcode", ["i", "love", "leetcode", "apples"]), True),
                (("iloveleetcode", ["apples", "i", "love", "leetcode"]), False),
                (("a", ["a"]), True),
            ),
        ),
    ]
