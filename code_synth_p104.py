"""Cycle 382: Easy coding prompts that still miss the template matcher.

917 / 1189 / 1629 / 1299 were unmatched. 806 and 830 already live in p19/p18;
do not redeclare those names here (loader keeps the first name, which would
shadow the broader smoke phrases).
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "reverse_only_letters",
            "def reverse_only_letters(s):\n"
            '    """Reverse letters, keep other characters in place (LeetCode 917)."""\n'
            "    chars = list(s)\n"
            "    i, j = 0, len(chars) - 1\n"
            "    while i < j:\n"
            "        if not chars[i].isalpha():\n"
            "            i += 1\n"
            "        elif not chars[j].isalpha():\n"
            "            j -= 1\n"
            "        else:\n"
            "            chars[i], chars[j] = chars[j], chars[i]\n"
            "            i += 1\n"
            "            j -= 1\n"
            "    return ''.join(chars)\n"
            "\n"
            "def reverseOnlyLetters(s):\n"
            "    return reverse_only_letters(s)\n",
            lambda low: bool(
                re.search(r"\bleetcode 917\b|\breverse only letters\b", low)
            ),
            (
                (("ab-cd",), "dc-ba"),
                (("a-bC-dEf-ghIj",), "j-Ih-gfE-dCba"),
                (("Test1ng-Leet=code-Q!",), "Qedo1ct-eeLg=ntse-T!"),
            ),
        ),
        T(
            "max_number_of_balloons",
            "def max_number_of_balloons(text):\n"
            '    """How many times balloon can be formed (LeetCode 1189)."""\n'
            "    need = {'b': 1, 'a': 1, 'l': 2, 'o': 2, 'n': 1}\n"
            "    have = {ch: 0 for ch in need}\n"
            "    for ch in text:\n"
            "        if ch in have:\n"
            "            have[ch] += 1\n"
            "    return min(have[ch] // need[ch] for ch in need)\n"
            "\n"
            "def maxNumberOfBalloons(text):\n"
            "    return max_number_of_balloons(text)\n",
            lambda low: bool(
                re.search(r"\bleetcode 1189\b|\bnumber of balloons\b", low)
            ),
            (
                (("nlaebolko",), 1),
                (("loonbalxballpoon",), 2),
                (("leetcode",), 0),
            ),
        ),
        T(
            "slowest_key",
            "def slowest_key(release_times, keys_pressed):\n"
            '    """Key with the longest press duration (LeetCode 1629)."""\n'
            "    best_key = keys_pressed[0]\n"
            "    best = release_times[0]\n"
            "    for i in range(1, len(release_times)):\n"
            "        duration = release_times[i] - release_times[i - 1]\n"
            "        key = keys_pressed[i]\n"
            "        if duration > best or (duration == best and key > best_key):\n"
            "            best = duration\n"
            "            best_key = key\n"
            "    return best_key\n"
            "\n"
            "def slowestKey(releaseTimes, keysPressed):\n"
            "    return slowest_key(releaseTimes, keysPressed)\n",
            lambda low: bool(
                re.search(r"\bleetcode 1629\b|\bslowest key\b", low)
            ),
            (
                (([9, 29, 49, 50], "cbcd"), "c"),
                (([12, 23, 36, 46, 62], "spuda"), "a"),
            ),
        ),
        T(
            "replace_elements_right",
            "def replace_elements_right(arr):\n"
            '    """Replace each element with the max to its right (LeetCode 1299)."""\n'
            "    out = [-1] * len(arr)\n"
            "    best = -1\n"
            "    for i in range(len(arr) - 1, -1, -1):\n"
            "        out[i] = best\n"
            "        if arr[i] > best:\n"
            "            best = arr[i]\n"
            "    return out\n"
            "\n"
            "def replaceElements(arr):\n"
            "    return replace_elements_right(arr)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1299\b|\bgreatest element on right\b",
                    low,
                )
            ),
            (
                (([17, 18, 5, 4, 6, 1],), [18, 6, 6, 6, 1, -1]),
                (([400],), [-1]),
            ),
        ),
    ]
