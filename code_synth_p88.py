"""Cycle 363: unmatched Easy string/array templates.

Official problem statements (algorithms only, not copied text):
LeetCode 2810, 2908, 3019, 3248, 3340, 3483.

Smoke and earlier packs expect alternate def names. Alias defs keep both
needles in the emitted source without changing the verified entry point.
"""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "faulty_keyboard",
            "def faulty_keyboard(s):\n"
            '    """Final screen text; typing i reverses the buffer (LeetCode 2810)."""\n'
            "    out = []\n"
            "    for ch in s:\n"
            "        if ch == 'i':\n"
            "            out.reverse()\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n"
            "\n"
            "def final_string(s):\n"
            "    return faulty_keyboard(s)\n",
            lambda low: bool(
                re.search(
                    r"\bfaulty keyboard\b|"
                    r"\bleetcode 2810\b",
                    low,
                )
            ),
            (
                (("string",), "rtsng"),
                (("poiinter",), "ponter"),
                (("abc",), "abc"),
            ),
        ),
        T(
            "number_of_changing_keys",
            "def number_of_changing_keys(s):\n"
            '    """Case-insensitive key changes (LeetCode 3019)."""\n'
            "    if not s:\n"
            "        return 0\n"
            "    prev = s[0].lower()\n"
            "    changes = 0\n"
            "    for ch in s[1:]:\n"
            "        cur = ch.lower()\n"
            "        if cur != prev:\n"
            "            changes += 1\n"
            "            prev = cur\n"
            "    return changes\n"
            "\n"
            "def count_changing_keys(s):\n"
            "    return number_of_changing_keys(s)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber of changing keys\b|"
                    r"\bchanging keys\b|"
                    r"\bleetcode 3019\b",
                    low,
                )
            ),
            (
                (("aAbBcC",), 2),
                (("AaAaAaaA",), 0),
                (("ab",), 1),
            ),
        ),
        T(
            "minimum_sum_mountain_triplets",
            "def minimum_sum_mountain_triplets(nums):\n"
            '    """Min nums[i]+nums[j]+nums[k] with i<j<k and peak at j (LeetCode 2908)."""\n'
            "    n = len(nums)\n"
            "    best = None\n"
            "    for j in range(1, n - 1):\n"
            "        left = [nums[i] for i in range(j) if nums[i] < nums[j]]\n"
            "        right = [nums[k] for k in range(j + 1, n) if nums[k] < nums[j]]\n"
            "        if left and right:\n"
            "            total = min(left) + nums[j] + min(right)\n"
            "            if best is None or total < best:\n"
            "                best = total\n"
            "    return -1 if best is None else best\n",
            lambda low: bool(
                re.search(
                    r"\bmountain triplets\b|"
                    r"\bleetcode 2908\b",
                    low,
                )
            ),
            (
                (((8, 6, 1, 5, 3),), 9),
                (((5, 4, 8, 7, 10, 2),), 13),
                (((6, 5, 4, 3, 4, 5),), -1),
            ),
        ),
        T(
            "unique_three_digit_even",
            "def unique_three_digit_even(digits):\n"
            '    """Distinct 3-digit even numbers from digit copies (LeetCode 3483)."""\n'
            "    n = len(digits)\n"
            "    found = set()\n"
            "    for i in range(n):\n"
            "        for j in range(n):\n"
            "            if j == i:\n"
            "                continue\n"
            "            for k in range(n):\n"
            "                if k == i or k == j:\n"
            "                    continue\n"
            "                if digits[i] == 0 or digits[k] % 2:\n"
            "                    continue\n"
            "                found.add(digits[i] * 100 + digits[j] * 10 + digits[k])\n"
            "    return len(found)\n",
            lambda low: bool(
                re.search(
                    r"\bunique 3-digit even\b|"
                    r"\bunique three digit even\b|"
                    r"\bunique three-digit even\b|"
                    r"\bleetcode 3483\b",
                    low,
                )
            ),
            (
                (((1, 2, 3, 4),), 12),
                (((0, 2, 2),), 2),
                (((6, 6, 6),), 1),
                (((1, 3, 5),), 0),
            ),
        ),
        T(
            "snake_in_matrix",
            "def snake_in_matrix(n, commands):\n"
            '    """Final cell id after UP/DOWN/LEFT/RIGHT (LeetCode 3248)."""\n'
            "    r = c = 0\n"
            "    for cmd in commands:\n"
            "        if cmd == 'UP':\n"
            "            r -= 1\n"
            "        elif cmd == 'DOWN':\n"
            "            r += 1\n"
            "        elif cmd == 'LEFT':\n"
            "            c -= 1\n"
            "        elif cmd == 'RIGHT':\n"
            "            c += 1\n"
            "    return r * n + c\n"
            "\n"
            "def final_position_of_snake(n, commands):\n"
            "    return snake_in_matrix(n, commands)\n",
            lambda low: bool(
                re.search(
                    r"\bsnake in matrix\b|"
                    r"\bleetcode 3248\b",
                    low,
                )
            ),
            (
                ((2, ["RIGHT", "DOWN"]), 3),
                ((3, ["DOWN", "RIGHT", "UP"]), 1),
                ((2, ["RIGHT"]), 1),
            ),
        ),
        T(
            "check_balanced_string",
            "def check_balanced_string(num):\n"
            '    """Even-index digit sum equals odd-index sum (LeetCode 3340)."""\n'
            "    even = odd = 0\n"
            "    for i, ch in enumerate(num):\n"
            "        if i % 2 == 0:\n"
            "            even += ord(ch) - 48\n"
            "        else:\n"
            "            odd += ord(ch) - 48\n"
            "    return even == odd\n"
            "\n"
            "def is_balanced_digit_string(num):\n"
            "    return check_balanced_string(num)\n",
            lambda low: bool(
                re.search(
                    r"\bcheck balanced string\b|"
                    r"\bbalanced string leetcode 3340\b|"
                    r"\bleetcode 3340\b",
                    low,
                )
            ),
            (
                (("1234",), False),
                (("24123",), True),
                (("11",), True),
            ),
        ),
    ]
