"""Cycle 359: unmatched Easy — laser beams, append-to-subsequence,
strong password II, sort people, remove digit, truck units.

Official problem statements (algorithms only, not copied text):
LeetCode 2125, 2486, 2299, 2418, 2259, 1710.
"""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "number_of_beams",
            "def number_of_beams(bank):\n"
            '    """Beams between consecutive non-empty rows (LeetCode 2125)."""\n'
            "    prev = 0\n"
            "    total = 0\n"
            "    for row in bank:\n"
            "        cur = str(row).count('1')\n"
            "        if cur:\n"
            "            total += prev * cur\n"
            "            prev = cur\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]of[_ ]beams\b|"
                    r"\blaser beams in a bank\b|"
                    r"\bleetcode 2125\b",
                    low,
                )
            ),
            (
                ((["011001", "000000", "010100", "001000"],), 8),
                ((["000", "111", "000"],), 0),
                ((["010", "000", "101"],), 2),
            ),
        ),
        T(
            "append_characters",
            "def append_characters(s, t):\n"
            '    """Chars to append so t is a subsequence of s (LeetCode 2486)."""\n'
            "    j = 0\n"
            "    for ch in s:\n"
            "        if j < len(t) and ch == t[j]:\n"
            "            j += 1\n"
            "    return len(t) - j\n",
            lambda low: bool(
                re.search(
                    r"\bappend[_ ]characters\b|"
                    r"\bleetcode 2486\b|"
                    r"\bmake subsequence by appending\b",
                    low,
                )
            ),
            (
                (("coaching", "coding"), 4),
                (("abcde", "a"), 0),
                (("z", "abcde"), 5),
            ),
        ),
        T(
            "strong_password_checker_ii",
            "def strong_password_checker_ii(password):\n"
            '    """Strong password rules, no adjacent repeats (LeetCode 2299)."""\n'
            "    if len(password) < 8:\n"
            "        return False\n"
            "    special = set('!@#$%^&*()-+')\n"
            "    has_lo = has_up = has_digit = has_sp = False\n"
            "    prev = ''\n"
            "    for ch in password:\n"
            "        if ch == prev:\n"
            "            return False\n"
            "        prev = ch\n"
            "        if ch.islower():\n"
            "            has_lo = True\n"
            "        elif ch.isupper():\n"
            "            has_up = True\n"
            "        elif ch.isdigit():\n"
            "            has_digit = True\n"
            "        elif ch in special:\n"
            "            has_sp = True\n"
            "    return has_lo and has_up and has_digit and has_sp\n",
            lambda low: bool(
                re.search(
                    r"\bstrong[_ ]password[_ ]checker[_ ]ii\b|"
                    r"\bleetcode 2299\b|"
                    r"\bstrong password ii\b",
                    low,
                )
            ),
            (
                (("IloveLe3tcode!",), True),
                (("Me+You--IsMyDream",), False),
                (("1aB!",), False),
            ),
        ),
        T(
            "remove_digit",
            "def remove_digit(number, digit):\n"
            '    """Delete one digit occurrence to maximize the number (LeetCode 2259)."""\n'
            "    best = ''\n"
            "    digit = str(digit)\n"
            "    number = str(number)\n"
            "    for i, ch in enumerate(number):\n"
            "        if ch == digit:\n"
            "            cand = number[:i] + number[i + 1 :]\n"
            "            if cand > best:\n"
            "                best = cand\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bremove[_ ]digit\b|"
                    r"\bleetcode 2259\b|"
                    r"\bremove one digit to maximize\b",
                    low,
                )
            ),
            (
                (("123", "3"), "12"),
                (("1231", "1"), "231"),
                (("551", "5"), "51"),
            ),
        ),
        T(
            "add_spaces",
            "def add_spaces(s, spaces):\n"
            '    """Insert spaces at the given indices (LeetCode 2109)."""\n'
            "    parts = []\n"
            "    prev = 0\n"
            "    for i in spaces:\n"
            "        i = int(i)\n"
            "        parts.append(s[prev:i])\n"
            "        parts.append(' ')\n"
            "        prev = i\n"
            "    parts.append(s[prev:])\n"
            "    return ''.join(parts)\n",
            lambda low: bool(
                re.search(
                    r"\badding[_ ]spaces\b|"
                    r"\badd[_ ]spaces\b|"
                    r"\bleetcode 2109\b",
                    low,
                )
            ),
            (
                (("LeetcodeHelpsMeLearn", [8, 13, 15]), "Leetcode Helps Me Learn"),
                (("icodeinpython", [1, 5, 7, 9]), "i code in py thon"),
                (("spacing", [0, 1, 2, 3, 4, 5, 6]), " s p a c i n g"),
            ),
        ),
        T(
            "max_ice_cream",
            "def max_ice_cream(costs, coins):\n"
            '    """How many bars can be bought (LeetCode 1833)."""\n'
            "    ordered = sorted(int(c) for c in costs)\n"
            "    left = int(coins)\n"
            "    bought = 0\n"
            "    for cost in ordered:\n"
            "        if cost > left:\n"
            "            break\n"
            "        left -= cost\n"
            "        bought += 1\n"
            "    return bought\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum[_ ]ice[_ ]cream\b|"
                    r"\bice cream bars\b|"
                    r"\bleetcode 1833\b",
                    low,
                )
            ),
            (
                (([1, 3, 2, 4, 1], 7), 4),
                (([10, 6, 8, 7, 7, 8], 5), 0),
                (([1, 6, 3, 1, 2, 5], 20), 6),
            ),
        ),
    ]
