"""Cycle 337: unused Easy — student attendance / next greatest letter /
dominant index / occurrences after bigram / baseball game / set mismatch."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "check_record",
            "def check_record(s):\n"
            '    """Eligible if fewer than 2 absences and no 3 late in a row (LeetCode 551)."""\n'
            "    return s.count('A') < 2 and 'LLL' not in s\n",
            lambda low: bool(
                re.search(
                    r"\bstudent[_ ]attendance[_ ]record\b|"
                    r"\bcheck[_ ]record\b",
                    low,
                )
            ),
            (
                (("PPALLP",), True),
                (("PPALLL",), False),
                (("AAAA",), False),
            ),
        ),
        T(
            "next_greatest_letter",
            "def next_greatest_letter(letters, target):\n"
            '    """Smallest letter in letters strictly greater than target (LeetCode 744)."""\n'
            "    for ch in letters:\n"
            "        if ch > target:\n"
            "            return ch\n"
            "    return letters[0]\n",
            lambda low: bool(
                re.search(
                    r"\bnext[_ ]greatest[_ ]letter\b|"
                    r"\bfind[_ ]smallest[_ ]letter[_ ]greater\b|"
                    r"\bsmallest[_ ]letter[_ ]greater[_ ]than[_ ]target\b",
                    low,
                )
            ),
            (
                ((["c", "f", "j"], "a"), "c"),
                ((["c", "f", "j"], "c"), "f"),
                ((["x", "x", "y", "y"], "z"), "x"),
            ),
        ),
        T(
            "dominant_index",
            "def dominant_index(nums):\n"
            '    """Index of unique max if it is >= 2*every other, else -1 (LeetCode 747)."""\n'
            "    m = max(nums)\n"
            "    idx = nums.index(m)\n"
            "    return idx if all(m >= 2 * x for i, x in enumerate(nums) if i != idx) else -1\n",
            lambda low: bool(
                re.search(
                    r"\blargest[_ ]number[_ ]at[_ ]least[_ ]twice\b|"
                    r"\bdominant[_ ]index\b",
                    low,
                )
            ),
            (
                (([3, 6, 1, 0],), 1),
                (([1, 2, 3, 4],), -1),
                (([1],), 0),
            ),
        ),
        T(
            "find_ocurrences",
            "def find_ocurrences(text, first, second):\n"
            '    """Words that follow the bigram (first, second) (LeetCode 1078)."""\n'
            "    words = text.split()\n"
            "    return [words[i + 2] for i in range(len(words) - 2)\n"
            "            if words[i] == first and words[i + 1] == second]\n",
            lambda low: bool(
                re.search(
                    r"\boccurrences[_ ]after[_ ]bigram\b|"
                    r"\bfind[_ ]ocurrences\b",
                    low,
                )
            ),
            (
                (("alice is a good girl she is a good student", "a", "good"), ["girl", "student"]),
                (("we will we will rock you", "we", "will"), ["we", "rock"]),
            ),
        ),
        T(
            "cal_points",
            "def cal_points(operations):\n"
            '    """Baseball game score from ops (LeetCode 682)."""\n'
            "    st = []\n"
            "    for op in operations:\n"
            "        if op == '+':\n"
            "            st.append(st[-1] + st[-2])\n"
            "        elif op == 'D':\n"
            "            st.append(2 * st[-1])\n"
            "        elif op == 'C':\n"
            "            st.pop()\n"
            "        else:\n"
            "            st.append(int(op))\n"
            "    return sum(st)\n",
            lambda low: bool(
                re.search(
                    r"\bbaseball[_ ]game\b|"
                    r"\bcal[_ ]points\b",
                    low,
                )
            ),
            (
                ((["5", "2", "C", "D", "+"],), 30),
                ((["5", "-2", "4", "C", "D", "9", "+", "+"],), 27),
                ((["1", "C"],), 0),
            ),
        ),
        T(
            "find_error_nums",
            "def find_error_nums(nums):\n"
            '    """[duplicate, missing] in 1..n with one repeat (LeetCode 645)."""\n'
            "    n = len(nums)\n"
            "    seen = set()\n"
            "    dup = 0\n"
            "    for x in nums:\n"
            "        if x in seen:\n"
            "            dup = x\n"
            "        seen.add(x)\n"
            "    missing = next(i for i in range(1, n + 1) if i not in seen)\n"
            "    return [dup, missing]\n",
            lambda low: bool(
                re.search(
                    r"\bset[_ ]mismatch\b|"
                    r"\bfind[_ ]error[_ ]nums\b|"
                    r"\bduplicate[_ ]and[_ ]missing\b",
                    low,
                )
            ),
            (
                (([1, 2, 2, 4],), [2, 3]),
                (([1, 1],), [1, 2]),
                (([2, 2],), [2, 1]),
            ),
        ),
    ]
