"""Cycle 305: delayed arrival / max achievable / sort people / target indices / element-digit sum / first letter twice."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "delayed_arrival_time",
            "def delayed_arrival_time(arrival_time, delayed_time):\n"
            '    """Arrival clock after delay (LeetCode 2651)."""\n'
            "    return (arrival_time + delayed_time) % 24\n",
            lambda low: bool(
                re.search(
                    r"\bdelayed[_ ]arrival[_ ]time\b|"
                    r"\bcalculate delayed arrival time\b|"
                    r"\bdelayed arrival\b",
                    low,
                )
            ),
            (
                ((15, 5), 20),
                ((13, 11), 0),
                ((23, 5), 4),
            ),
        ),
        T(
            "max_achievable_number",
            "def max_achievable_number(num, t):\n"
            '    """Max x after t +1/-1 steps vs num (LeetCode 2769)."""\n'
            "    return num + 2 * t\n",
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)?[_ ]achievable[_ ]number\b|"
                    r"\bfind the maximum achievable number\b|"
                    r"\bmaximum achievable\b",
                    low,
                )
            ),
            (
                ((4, 1), 6),
                ((3, 2), 7),
            ),
        ),
        T(
            "sort_the_people",
            "def sort_the_people(names, heights):\n"
            '    """Sort names by height descending (LeetCode 2418)."""\n'
            "    paired = sorted(zip(heights, names), reverse=True)\n"
            "    return [name for _, name in paired]\n",
            lambda low: bool(
                re.search(
                    r"\bsort[_ ]the[_ ]people\b|"
                    r"\bsort people by height\b|"
                    r"\bsort the people\b",
                    low,
                )
            ),
            (
                ((["Mary", "John", "Emma"], [180, 165, 170]), ["Mary", "Emma", "John"]),
                ((["Alice", "Bob", "Bob"], [155, 185, 150]), ["Bob", "Alice", "Bob"]),
            ),
        ),
        T(
            "target_indices_after_sorting",
            "def target_indices_after_sorting(nums, target):\n"
            '    """Indices of target after non-decreasing sort (LeetCode 2089)."""\n'
            "    return [i for i, v in enumerate(sorted(nums)) if v == target]\n",
            lambda low: bool(
                re.search(
                    r"\btarget[_ ]indices[_ ]after[_ ]sorting\b|"
                    r"\bfind target indices after sorting\b|"
                    r"\btarget indices after sorting array\b",
                    low,
                )
            ),
            (
                (([1, 2, 5, 2, 3], 2), [1, 2]),
                (([1, 2, 5, 2, 3], 3), [3]),
                (([1, 2, 5, 2, 3], 5), [4]),
            ),
        ),
        T(
            "difference_element_digit_sum",
            "def difference_element_digit_sum(nums):\n"
            '    """|element sum − digit sum| (LeetCode 2535)."""\n'
            "    elem = sum(nums)\n"
            "    digits = 0\n"
            "    for x in nums:\n"
            "        while x:\n"
            "            digits += x % 10\n"
            "            x //= 10\n"
            "    return abs(elem - digits)\n",
            lambda low: bool(
                re.search(
                    r"\bdifference[_ ]element[_ ]digit[_ ]sum\b|"
                    r"\bdifference between element sum and digit sum\b|"
                    r"\belement sum and digit sum\b",
                    low,
                )
            ),
            (
                (([1, 15, 6, 3],), 9),
                (([1, 2, 3, 4],), 0),
            ),
        ),
        T(
            "first_letter_twice",
            "def first_letter_twice(s):\n"
            '    """First letter that appears twice (LeetCode 2351)."""\n'
            "    seen = set()\n"
            "    for ch in s:\n"
            "        if ch in seen:\n"
            "            return ch\n"
            "        seen.add(ch)\n"
            "    return ''\n",
            lambda low: bool(
                re.search(
                    r"\bfirst[_ ]letter[_ ]twice\b|"
                    r"\bfirst letter to appear twice\b|"
                    r"\bfirst letter that appears twice\b",
                    low,
                )
            ),
            (
                (("abccbaacz",), "c"),
                (("abcdd",), "d"),
            ),
        ),
    ]
