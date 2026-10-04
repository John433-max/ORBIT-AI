"""Cycle 406: LeetCode prompts stolen by generic reverse/add or a draft stub.

Official examples (not copied solutions):
- 344 Reverse String: in-place character list. ["h","e","l","l","o"] -> ["o","l","l","e","h"].
- 541 Reverse String II: reverse each 2k block's first k chars. "abcdefg", 2 -> "bacdfeg".
- 445 Add Two Numbers II: MSD-first [val, next] lists. 7->2->4->3 + 5->6->4 = 7->8->0->7.
- 420 Strong Password Checker: min edits. "a" -> 5; "aA1" -> 3; "1337C0d3" -> 0.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "reverse_string_leetcode_344",
            "def reverseString(s):\n"
            '    """Reverse a character list in place (LeetCode 344)."""\n'
            "    i, j = 0, len(s) - 1\n"
            "    while i < j:\n"
            "        s[i], s[j] = s[j], s[i]\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return s\n",
            lambda low: bool(
                re.search(r"\bleetcode 344\b", low)
                or (
                    re.search(r"\breverse\b.{0,24}\bstring\b", low)
                    and ("in-place" in low or "in place" in low or "characters" in low)
                    and " ii" not in low
                    and "541" not in low
                    and "2k" not in low
                )
            ),
            (
                ((["h", "e", "l", "l", "o"],), ["o", "l", "l", "e", "h"]),
                ((["H", "a", "n", "n", "a", "h"],), ["h", "a", "n", "n", "a", "H"]),
            ),
        ),
        T(
            "reverse_string_ii",
            "def reverseStr(s, k):\n"
            '    """Reverse the first k chars of every 2k block (LeetCode 541)."""\n'
            "    chars = list(s)\n"
            "    k = int(k)\n"
            "    for start in range(0, len(chars), 2 * k):\n"
            "        i, j = start, min(start + k - 1, len(chars) - 1)\n"
            "        while i < j:\n"
            "            chars[i], chars[j] = chars[j], chars[i]\n"
            "            i += 1\n"
            "            j -= 1\n"
            "    return ''.join(chars)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 541\b|"
                    r"\breverse string ii\b|"
                    r"\breverse_str\b|"
                    r"\breverse every 2k\b",
                    low,
                )
            ),
            (
                (("abcdefg", 2), "bacdfeg"),
                (("abcd", 2), "bacd"),
                (("abcdef", 3), "cbadef"),
            ),
        ),
        T(
            "add_two_numbers_ii",
            "def addTwoNumbers(l1, l2):\n"
            '    """Add MSD-first [val, next] digit lists (LeetCode 445)."""\n'
            "    def to_int(node):\n"
            "        n = 0\n"
            "        while node is not None:\n"
            "            n = n * 10 + int(node[0])\n"
            "            node = node[1] if len(node) > 1 else None\n"
            "        return n\n"
            "    total = to_int(l1) + to_int(l2)\n"
            "    digits = str(total)\n"
            "    head = None\n"
            "    for ch in reversed(digits):\n"
            "        head = [int(ch), head]\n"
            "    return head\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 445\b|"
                    r"\badd two numbers ii\b|"
                    r"\badd_two_numbers_ii\b",
                    low,
                )
            ),
            (
                (
                    ([7, [2, [4, [3, None]]]], [5, [6, [4, None]]]),
                    [7, [8, [0, [7, None]]]],
                ),
                (([0, None], [0, None]), [0, None]),
                (([5, None], [5, None]), [1, [0, None]]),
            ),
        ),
        T(
            "strong_password_checker",
            "def strongPasswordChecker(password):\n"
            '    """Minimum edits for a strong password (LeetCode 420)."""\n'
            "    n = len(password)\n"
            "    missing = 3\n"
            "    if any('a' <= c <= 'z' for c in password):\n"
            "        missing -= 1\n"
            "    if any('A' <= c <= 'Z' for c in password):\n"
            "        missing -= 1\n"
            "    if any(c.isdigit() for c in password):\n"
            "        missing -= 1\n"
            "    change = 0\n"
            "    one = two = 0\n"
            "    i = 2\n"
            "    while i < n:\n"
            "        if password[i] == password[i - 1] == password[i - 2]:\n"
            "            length = 2\n"
            "            while i < n and password[i] == password[i - 1]:\n"
            "                length += 1\n"
            "                i += 1\n"
            "            change += length // 3\n"
            "            if length % 3 == 0:\n"
            "                one += 1\n"
            "            elif length % 3 == 1:\n"
            "                two += 1\n"
            "        else:\n"
            "            i += 1\n"
            "    if n < 6:\n"
            "        return max(missing, 6 - n)\n"
            "    if n <= 20:\n"
            "        return max(missing, change)\n"
            "    delete = n - 20\n"
            "    change -= min(delete, one)\n"
            "    change -= min(max(delete - one, 0), two * 2) // 2\n"
            "    change -= max(delete - one - 2 * two, 0) // 3\n"
            "    return delete + max(missing, change)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 420\b|"
                    r"\bstrong password checker\b",
                    low,
                )
                and " ii" not in low
                and "2299" not in low
            ),
            (
                (("a",), 5),
                (("aA1",), 3),
                (("1337C0d3",), 0),
                (("aaa111",), 2),
                (("aaaaaaaaaaaaaaaaaaaaa",), 7),
            ),
        ),
    ]
