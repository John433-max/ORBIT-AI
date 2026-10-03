"""Cycle 380: Easy coding prompts that fell through to NotImplemented.

2515 / 1750 / 2658 / 1700 / 921 / 495 were unmatched. Examples follow published
LeetCode samples. 821 is covered by extending shortest_to_char (not duplicated).
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "circular_target_distance",
            "def circular_target_distance(words, target, start_index):\n"
            '    """Shortest circular distance to target string (LeetCode 2515)."""\n'
            "    n = len(words)\n"
            "    best = n\n"
            "    for i, word in enumerate(words):\n"
            "        if word == target:\n"
            "            dist = abs(i - start_index)\n"
            "            best = min(best, dist, n - dist)\n"
            "    return -1 if best == n else best\n"
            "\n"
            "def closetTarget(words, target, startIndex):\n"
            "    return circular_target_distance(words, target, startIndex)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 2515\b|\bshortest distance to target string\b",
                    low,
                )
            ),
            (
                ((["hello", "i", "am", "leetcode", "hello"], "hello", 1), 1),
                ((["a", "b", "leetcode"], "leetcode", 0), 1),
                ((["i", "eat", "leetcode"], "ate", 0), -1),
            ),
        ),
        T(
            "min_length_similar_ends",
            "def min_length_similar_ends(s):\n"
            '    """Min length after deleting similar ends (LeetCode 1750)."""\n'
            "    left, right = 0, len(s) - 1\n"
            "    while left < right and s[left] == s[right]:\n"
            "        ch = s[left]\n"
            "        while left <= right and s[left] == ch:\n"
            "            left += 1\n"
            "        while left <= right and s[right] == ch:\n"
            "            right -= 1\n"
            "    return right - left + 1\n"
            "\n"
            "def minimumLength(s):\n"
            "    return min_length_similar_ends(s)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1750\b|\bdeleting similar ends\b",
                    low,
                )
            ),
            (
                (("ca",), 2),
                (("cabaabac",), 0),
                (("aabccabba",), 3),
            ),
        ),
        T(
            "find_max_fish",
            "def find_max_fish(grid):\n"
            '    """Largest connected water component sum (LeetCode 2658)."""\n'
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    seen = [[False] * cols for _ in range(rows)]\n"
            "\n"
            "    def flood(r, c):\n"
            "        stack = [(r, c)]\n"
            "        seen[r][c] = True\n"
            "        total = 0\n"
            "        while stack:\n"
            "            x, y = stack.pop()\n"
            "            total += grid[x][y]\n"
            "            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nx, ny = x + dx, y + dy\n"
            "                if (\n"
            "                    0 <= nx < rows\n"
            "                    and 0 <= ny < cols\n"
            "                    and not seen[nx][ny]\n"
            "                    and grid[nx][ny]\n"
            "                ):\n"
            "                    seen[nx][ny] = True\n"
            "                    stack.append((nx, ny))\n"
            "        return total\n"
            "\n"
            "    best = 0\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] and not seen[r][c]:\n"
            "                best = max(best, flood(r, c))\n"
            "    return best\n"
            "\n"
            "def findMaxFish(grid):\n"
            "    return find_max_fish(grid)\n",
            lambda low: bool(
                re.search(r"\bleetcode 2658\b|\bmaximum number of fish\b", low)
            ),
            (
                (([[0, 2, 1, 0], [4, 0, 0, 3], [1, 0, 0, 4], [0, 3, 2, 0]],), 7),
                (([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]],), 1),
            ),
        ),
        T(
            "count_students_lunch",
            "def count_students_lunch(students, sandwiches):\n"
            '    """Students left when the sandwich queue stalls (LeetCode 1700)."""\n'
            "    counts = [0, 0]\n"
            "    for student in students:\n"
            "        counts[student] += 1\n"
            "    for sandwich in sandwiches:\n"
            "        if counts[sandwich] == 0:\n"
            "            return counts[0] + counts[1]\n"
            "        counts[sandwich] -= 1\n"
            "    return 0\n"
            "\n"
            "def countStudents(students, sandwiches):\n"
            "    return count_students_lunch(students, sandwiches)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 1700\b|\bstudents unable to eat lunch\b",
                    low,
                )
            ),
            (
                (([1, 1, 0, 0], [0, 1, 0, 1]), 0),
                (([1, 1, 1, 0, 0, 1], [1, 0, 0, 0, 1, 1]), 3),
            ),
        ),
        T(
            "min_add_parentheses",
            "def min_add_parentheses(s):\n"
            '    """Min insertions to make parentheses valid (LeetCode 921)."""\n'
            "    balance = added = 0\n"
            "    for ch in s:\n"
            "        if ch == '(':\n"
            "            balance += 1\n"
            "        elif balance:\n"
            "            balance -= 1\n"
            "        else:\n"
            "            added += 1\n"
            "    return balance + added\n"
            "\n"
            "def minAddToMakeValid(s):\n"
            "    return min_add_parentheses(s)\n",
            lambda low: bool(
                re.search(
                    r"\bleetcode 921\b|\bmake parentheses valid\b",
                    low,
                )
            ),
            (
                (("())",), 1),
                (("(((",), 3),
            ),
        ),
        T(
            "teemo_attacking",
            "def teemo_attacking(time_series, duration):\n"
            '    """Total poisoned seconds with non-stacking duration (LeetCode 495)."""\n'
            "    if not time_series:\n"
            "        return 0\n"
            "    total = 0\n"
            "    for i in range(len(time_series) - 1):\n"
            "        total += min(duration, time_series[i + 1] - time_series[i])\n"
            "    return total + duration\n"
            "\n"
            "def findPoisonedDuration(timeSeries, duration):\n"
            "    return teemo_attacking(timeSeries, duration)\n",
            lambda low: bool(
                re.search(r"\bleetcode 495\b|\bteemo attacking\b|\bpoisoned duration\b", low)
            ),
            (
                (([1, 4], 2), 4),
                (([1, 2], 2), 3),
            ),
        ),
    ]
