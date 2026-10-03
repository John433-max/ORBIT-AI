"""Cycle 378: special-chars II, almost-equivalent, reformat, prefix-xor, beautiful binary, equal-one.

3121 / 2068 / 1417 / 2433 / 2914 / 3191 were unmatched stubs.
Examples follow published LeetCode samples (any valid reformat is accepted; this pack is deterministic).
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "number_of_special_chars_ii",
            "def number_of_special_chars_ii(word):\n"
            '    """Special letters whose every lowercase is before the first uppercase (LeetCode 3121)."""\n'
            "    first_upper = {}\n"
            "    last_lower = {}\n"
            "    for i, ch in enumerate(word):\n"
            "        if ch.islower():\n"
            "            last_lower[ch] = i\n"
            "        elif ch.isupper() and ch not in first_upper:\n"
            "            first_upper[ch] = i\n"
            "    ans = 0\n"
            "    for c in 'abcdefghijklmnopqrstuvwxyz':\n"
            "        up = c.upper()\n"
            "        if c in last_lower and up in first_upper and last_lower[c] < first_upper[up]:\n"
            "            ans += 1\n"
            "    return ans\n"
            "\n"
            "def numberOfSpecialChars(word):\n"
            "    return number_of_special_chars_ii(word)\n",
            lambda low: bool(re.search(r"\bleetcode 3121\b|\bspecial characters ii\b", low))
            and "special characters i " not in low
            and not re.search(r"\bspecial characters i\b", low),
            (
                (("aaAbcBC",), 3),
                (("abc",), 0),
                (("AbBCab",), 0),
            ),
        ),
        T(
            "check_almost_equivalent",
            "def check_almost_equivalent(word1, word2):\n"
            '    """True if every letter frequency differs by at most 3 (LeetCode 2068)."""\n'
            "    from collections import Counter\n"
            "    c1, c2 = Counter(word1), Counter(word2)\n"
            "    letters = set(c1) | set(c2)\n"
            "    return all(abs(c1[ch] - c2[ch]) <= 3 for ch in letters)\n"
            "\n"
            "def checkAlmostEquivalent(word1, word2):\n"
            "    return check_almost_equivalent(word1, word2)\n",
            lambda low: bool(
                re.search(r"\bleetcode 2068\b|\balmost equivalent\b", low)
            ),
            (
                (("aaaa", "bccb"), False),
                (("abcdeef", "abaaacc"), True),
                (("cccddabba", "babababab"), True),
            ),
        ),
        T(
            "reformat_string",
            "def reformat_string(s):\n"
            '    """Alternate letters and digits; empty if impossible (LeetCode 1417)."""\n'
            "    letters = [c for c in s if c.isalpha()]\n"
            "    digits = [c for c in s if c.isdigit()]\n"
            "    if abs(len(letters) - len(digits)) > 1:\n"
            "        return ''\n"
            "    if len(letters) < len(digits):\n"
            "        letters, digits = digits, letters\n"
            "    out = []\n"
            "    for a, b in zip(letters, digits):\n"
            "        out.append(a + b)\n"
            "    if len(letters) > len(digits):\n"
            "        out.append(letters[-1])\n"
            "    return ''.join(out)\n"
            "\n"
            "def reformat(s):\n"
            "    return reformat_string(s)\n",
            lambda low: bool(re.search(r"\bleetcode 1417\b|\breformat the string\b", low))
            and "phone" not in low,
            (
                (("a0b1c2",), "a0b1c2"),
                (("leetcode",), ""),
                (("1229857369",), ""),
                (("covid2019",), "c2o0v1i9d"),
                (("ab123",), "1a2b3"),
            ),
        ),
        T(
            "find_array_prefix_xor",
            "def find_array_prefix_xor(pref):\n"
            '    """Recover arr where pref[i] is the XOR of arr[0..i] (LeetCode 2433)."""\n'
            "    arr = [pref[0]]\n"
            "    for i in range(1, len(pref)):\n"
            "        arr.append(pref[i - 1] ^ pref[i])\n"
            "    return arr\n"
            "\n"
            "def findArray(pref):\n"
            "    return find_array_prefix_xor(pref)\n",
            lambda low: bool(
                re.search(r"\bleetcode 2433\b|\boriginal array of prefix xor\b", low)
            )
            and "decode" not in low,
            (
                (([5, 2, 0, 3, 1],), [5, 7, 2, 3, 2]),
                (([13],), [13]),
            ),
        ),
        T(
            "min_changes_beautiful",
            "def min_changes_beautiful(s):\n"
            '    """Min flips so even-length binary pairs match (LeetCode 2914)."""\n'
            "    return sum(a != b for a, b in zip(s[::2], s[1::2]))\n"
            "\n"
            "def minChanges(s):\n"
            "    return min_changes_beautiful(s)\n",
            lambda low: bool(
                re.search(r"\bleetcode 2914\b|\bbinary string beautiful\b", low)
            )
            and "alternating" not in low,
            (
                (("1001",), 2),
                (("10",), 1),
                (("0000",), 0),
            ),
        ),
        T(
            "min_operations_equal_one",
            "def min_operations_equal_one(nums):\n"
            '    """Min length-3 flips to make a binary array all ones, or -1 (LeetCode 3191)."""\n'
            "    a = list(nums)\n"
            "    ops = 0\n"
            "    for i in range(len(a) - 2):\n"
            "        if a[i] == 0:\n"
            "            a[i] ^= 1\n"
            "            a[i + 1] ^= 1\n"
            "            a[i + 2] ^= 1\n"
            "            ops += 1\n"
            "    if any(x == 0 for x in a):\n"
            "        return -1\n"
            "    return ops\n"
            "\n"
            "def minOperations(nums):\n"
            "    return min_operations_equal_one(nums)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 3191\b|\bequal to one i\b|\belements equal to one i\b",
                    low,
                )
            ),
            (
                (([0, 1, 1, 1, 0, 0],), 3),
                (([0, 1, 1, 1],), -1),
            ),
        ),
    ]
