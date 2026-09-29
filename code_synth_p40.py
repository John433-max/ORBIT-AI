"""Cycle 301: first palindrome / smallest even multiple / count asterisks / decode message / arithmetic triplets / reverse prefix."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "first_palindrome",
            "def first_palindrome(words):\n"
            '    """First palindromic string in words, or empty (LeetCode 2108)."""\n'
            "    for w in words:\n"
            "        if w == w[::-1]:\n"
            "            return w\n"
            "    return ''\n",
            lambda low: bool(
                re.search(
                    r"\bfirst[_ ]palindrome\b|"
                    r"\bfirst palindromic string\b|"
                    r"\bfind first palindromic\b",
                    low,
                )
            ),
            (
                ((["abc", "car", "ada", "racecar", "cool"],), "ada"),
                ((["notapalindrome", "racecar"],), "racecar"),
                ((["def", "ghi"],), ""),
            ),
        ),
        T(
            "smallest_even_multiple",
            "def smallest_even_multiple(n):\n"
            '    """Smallest positive even multiple of n (LeetCode 2413)."""\n'
            "    return n if n % 2 == 0 else 2 * n\n",
            lambda low: bool(
                re.search(
                    r"\bsmallest[_ ]even[_ ]multiple\b|"
                    r"\bsmallest even multiple of n\b|"
                    r"\bsmallest even multiple\b",
                    low,
                )
            ),
            (
                ((5,), 10),
                ((6,), 6),
                ((1,), 2),
            ),
        ),
        T(
            "count_asterisks",
            "def count_asterisks(s):\n"
            '    """Count * outside |pairs| (LeetCode 2315)."""\n'
            "    out = 0\n"
            "    inside = False\n"
            "    for ch in s:\n"
            "        if ch == '|':\n"
            "            inside = not inside\n"
            "        elif ch == '*' and not inside:\n"
            "            out += 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]asterisks\b|"
                    r"\bcount asterisks\b|"
                    r"\bcount the asterisks\b",
                    low,
                )
            ),
            (
                (("l|*e*et|c**o|*de|",), 2),
                (("iamprogrammer",), 0),
                (("yo|uar|e**|b|e***au|tifu|l",), 5),
            ),
        ),
        T(
            "decode_message",
            "def decode_message(key, message):\n"
            '    """Decode substitution cipher from key (LeetCode 2325)."""\n'
            "    mapping = {}\n"
            "    letter = ord('a')\n"
            "    for ch in key:\n"
            "        if ch != ' ' and ch not in mapping:\n"
            "            mapping[ch] = chr(letter)\n"
            "            letter += 1\n"
            "    return ''.join(' ' if ch == ' ' else mapping[ch] for ch in message)\n",
            lambda low: bool(
                re.search(
                    r"\bdecode[_ ]message\b|"
                    r"\bdecode the message\b|"
                    r"\bdecode substitution (?:cipher )?message\b",
                    low,
                )
            ),
            (
                (("the quick brown fox jumps over the lazy dog", "vkbs bs t suepuv"), "this is a secret"),
                (("eljuxhpwnyrdgtqkviszcfmabo", "zwx hnfx lqantp mnoeius ycgk vcnjrdb"), "the five boxing wizards jump quickly"),
            ),
        ),
        T(
            "arithmetic_triplets",
            "def arithmetic_triplets(nums, diff):\n"
            '    """Count i<j<k with nums[j]-nums[i]==nums[k]-nums[j]==diff (LeetCode 2367)."""\n'
            "    s = set(nums)\n"
            "    return sum(1 for x in nums if (x + diff) in s and (x + 2 * diff) in s)\n",
            lambda low: bool(
                re.search(
                    r"\barithmetic[_ ]triplets\b|"
                    r"\bnumber of arithmetic triplets\b|"
                    r"\bcount arithmetic triplets\b",
                    low,
                )
            ),
            (
                (([0, 1, 4, 6, 7, 10], 3), 2),
                (([4, 5, 6, 7, 8, 9], 2), 2),
            ),
        ),
        T(
            "reverse_prefix",
            "def reverse_prefix(word, ch):\n"
            '    """Reverse the prefix of word through first ch (LeetCode 2000)."""\n'
            "    i = word.find(ch)\n"
            "    if i < 0:\n"
            "        return word\n"
            "    return word[: i + 1][::-1] + word[i + 1 :]\n",
            lambda low: bool(
                re.search(
                    r"\breverse[_ ]prefix\b|"
                    r"\breverse prefix of word\b|"
                    r"\breverse the prefix of (?:a |the )?word\b",
                    low,
                )
            ),
            (
                (("abcdefd", "d"), "dcbaefd"),
                (("xyxzxe", "z"), "zxyxxe"),
                (("abcd", "z"), "abcd"),
            ),
        ),
    ]
