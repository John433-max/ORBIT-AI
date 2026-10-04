"""Cycle 432: elimination game, min parentheses add, width ramp, bag of tokens, rescue boats, car fleet.

Unmatched medium problems. Matchers are phrase- or id-gated so valid-parentheses,
car pooling, and sort-array-by-parity stay on their existing templates.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "elimination_game",
            "def elimination_game(n):\n"
            '    """Last remaining number after alternate elimination (LeetCode 390)."""\n'
            "    n = int(n)\n"
            "    left = True\n"
            "    remaining = n\n"
            "    step = 1\n"
            "    head = 1\n"
            "    while remaining > 1:\n"
            "        if left or remaining % 2 == 1:\n"
            "            head += step\n"
            "        remaining //= 2\n"
            "        step *= 2\n"
            "        left = not left\n"
            "    return head\n",
            lambda low: bool(
                re.search(r"\bleetcode 390\b", low)
                or "elimination game" in low
                or "last remaining number" in low
            ),
            (
                ((9,), 6),
                ((1,), 1),
                ((6,), 4),
            ),
        ),
        T(
            "min_add_to_make_valid",
            "def min_add_to_make_valid(s):\n"
            '    """Minimum parentheses to add so the string is valid (LeetCode 921)."""\n'
            "    bal = add = 0\n"
            "    for c in str(s):\n"
            "        if c == '(':\n"
            "            bal += 1\n"
            "        elif c == ')':\n"
            "            if bal:\n"
            "                bal -= 1\n"
            "            else:\n"
            "                add += 1\n"
            "    return add + bal\n"
            "\n"
            "def min_add_parentheses(s):\n"
            "    return min_add_to_make_valid(s)\n",
            lambda low: bool(
                re.search(r"\bleetcode 921\b", low)
                or "minimum add to make parentheses valid" in low
                or "min add to make valid" in low
                or "minimum parentheses to add" in low
            ),
            (
                (("())",), 1),
                (("(((",), 3),
                (("()",), 0),
            ),
        ),
        T(
            "maximum_width_ramp",
            "def maximum_width_ramp(nums):\n"
            '    """Max j-i with i < j and nums[i] <= nums[j] (LeetCode 962)."""\n'
            "    nums = [int(x) for x in nums]\n"
            "    stack = []\n"
            "    for i, x in enumerate(nums):\n"
            "        if not stack or x < nums[stack[-1]]:\n"
            "            stack.append(i)\n"
            "    ans = 0\n"
            "    for j in range(len(nums) - 1, -1, -1):\n"
            "        while stack and nums[stack[-1]] <= nums[j]:\n"
            "            ans = max(ans, j - stack.pop())\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode 962\b", low)
                or "maximum width ramp" in low
                or "max width ramp" in low
            ),
            (
                (([6, 0, 8, 2, 1, 5],), 4),
                (([9, 8, 1, 0, 1, 9, 4, 0, 4, 1],), 7),
            ),
        ),
        T(
            "bag_of_tokens",
            "def bag_of_tokens_score(tokens, power):\n"
            '    """Max score from face-up/face-down token plays (LeetCode 948)."""\n'
            "    tokens = sorted(int(t) for t in tokens)\n"
            "    power = int(power)\n"
            "    lo, hi = 0, len(tokens) - 1\n"
            "    score = ans = 0\n"
            "    while lo <= hi:\n"
            "        if power >= tokens[lo]:\n"
            "            power -= tokens[lo]\n"
            "            lo += 1\n"
            "            score += 1\n"
            "            ans = max(ans, score)\n"
            "        elif score and lo < hi:\n"
            "            power += tokens[hi]\n"
            "            hi -= 1\n"
            "            score -= 1\n"
            "        else:\n"
            "            break\n"
            "    return ans\n"
            "\n"
            "def bag_of_tokens(tokens, power):\n"
            "    return bag_of_tokens_score(tokens, power)\n",
            lambda low: bool(
                re.search(r"\bleetcode 948\b", low)
                or "bag of tokens" in low
            ),
            (
                (([100], 50), 0),
                (([200, 100], 150), 1),
                (([100, 200, 300, 400], 200), 2),
            ),
        ),
        T(
            "boats_to_save",
            "def num_rescue_boats(people, limit):\n"
            '    """Minimum boats so each pair weighs at most limit (LeetCode 881)."""\n'
            "    people = sorted(int(p) for p in people)\n"
            "    limit = int(limit)\n"
            "    i, j = 0, len(people) - 1\n"
            "    boats = 0\n"
            "    while i <= j:\n"
            "        if people[i] + people[j] <= limit:\n"
            "            i += 1\n"
            "        j -= 1\n"
            "        boats += 1\n"
            "    return boats\n"
            "\n"
            "def boats_to_save_people(people, limit):\n"
            "    return num_rescue_boats(people, limit)\n",
            lambda low: bool(
                re.search(r"\bleetcode 881\b", low)
                or "boats to save" in low
                or "rescue boats" in low
            ),
            (
                (([1, 2], 3), 1),
                (([3, 2, 2, 1], 3), 3),
                (([3, 5, 3, 4], 5), 4),
            ),
        ),
        T(
            "car_fleet",
            "def car_fleet(target, position, speed):\n"
            '    """Number of car fleets that reach target (LeetCode 853)."""\n'
            "    target = int(target)\n"
            "    cars = sorted(zip(position, speed), key=lambda x: -int(x[0]))\n"
            "    fleets = 0\n"
            "    prev = -1.0\n"
            "    for p, s in cars:\n"
            "        t = (target - int(p)) / float(s)\n"
            "        if t > prev:\n"
            "            fleets += 1\n"
            "            prev = t\n"
            "    return fleets\n",
            lambda low: bool(
                re.search(r"\bleetcode 853\b", low)
                or "car fleet" in low
            )
            and "pooling" not in low
            and "car pooling" not in low,
            (
                ((12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), 3),
                ((10, [3], [3]), 1),
                ((100, [0, 2, 4], [4, 2, 1]), 1),
            ),
        ),
    ]
