"""Cycle 326: unused Easy — triangle type / Harshad / clear digits /
final array after K multiplies / max string pairs / bowling winner."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "type_of_triangle",
            "def type_of_triangle(nums):\n"
            '    """Classify three side lengths (LeetCode 3024)."""\n'
            "    a, b, c = sorted(nums)\n"
            "    if a + b <= c:\n"
            "        return 'none'\n"
            "    if a == c:\n"
            "        return 'equilateral'\n"
            "    if a == b or b == c:\n"
            "        return 'isosceles'\n"
            "    return 'scalene'\n",
            lambda low: bool(
                re.search(
                    r"\btype_of_triangle\b|"
                    r"\btype[_ ]of[_ ]triangle\b|"
                    r"\bleetcode[_ ]3024\b",
                    low,
                )
            )
            and "pascal" not in low
            and "valid_triangle" not in low,
            (
                (([3, 3, 3],), "equilateral"),
                (([3, 4, 5],), "scalene"),
                (([1, 2, 3],), "none"),
                (([5, 5, 8],), "isosceles"),
            ),
        ),
        T(
            "sum_of_the_digits_of_harshad_number",
            "def sum_of_the_digits_of_harshad_number(x):\n"
            '    """Digit sum if x is Harshad, else -1 (LeetCode 3099)."""\n'
            "    s = 0\n"
            "    n = x\n"
            "    while n:\n"
            "        s += n % 10\n"
            "        n //= 10\n"
            "    return s if x % s == 0 else -1\n",
            lambda low: bool(
                re.search(
                    r"\bsum_of_the_digits_of_harshad_number\b|"
                    r"\bharshad[_ ]number\b|"
                    r"\bleetcode[_ ]3099\b",
                    low,
                )
            )
            and "happy" not in low,
            (
                ((18,), 9),
                ((23,), -1),
            ),
        ),
        T(
            "clear_digits",
            "def clear_digits(s):\n"
            '    """Delete each digit and the closest non-digit to its left (LeetCode 3174)."""\n'
            "    st = []\n"
            "    for ch in s:\n"
            "        if ch.isdigit():\n"
            "            if st:\n"
            "                st.pop()\n"
            "        else:\n"
            "            st.append(ch)\n"
            "    return ''.join(st)\n",
            lambda low: bool(
                re.search(
                    r"\bclear_digits\b|"
                    r"\bclear[_ ]digits\b|"
                    r"\bleetcode[_ ]3174\b",
                    low,
                )
            )
            and "add_digits" not in low
            and "count_digits" not in low,
            (
                (("abc",), "abc"),
                (("cb34",), ""),
            ),
        ),
        T(
            "get_final_state",
            "def get_final_state(nums, k, multiplier):\n"
            '    """k times replace the min value with min*multiplier (LeetCode 3264)."""\n'
            "    nums = list(nums)\n"
            "    for _ in range(k):\n"
            "        i = min(range(len(nums)), key=lambda j: (nums[j], j))\n"
            "        nums[i] *= multiplier\n"
            "    return nums\n",
            lambda low: bool(
                re.search(
                    r"\bget_final_state\b|"
                    r"\bfinal[_ ]array[_ ]state[_ ]after[_ ]k[_ ]multiplication\b|"
                    r"\bleetcode[_ ]3264\b",
                    low,
                )
            )
            and "final_string" not in low,
            (
                (([2, 1, 3, 5, 6], 5, 2), [8, 4, 6, 5, 6]),
                (([1, 2], 3, 4), [16, 8]),
            ),
        ),
        T(
            "maximum_number_of_string_pairs",
            "def maximum_number_of_string_pairs(words):\n"
            '    """Count pairs where one word is the reverse of the other (LeetCode 2744)."""\n'
            "    seen = set()\n"
            "    pairs = 0\n"
            "    for w in words:\n"
            "        rev = w[::-1]\n"
            "        if rev in seen:\n"
            "            pairs += 1\n"
            "            seen.remove(rev)\n"
            "        else:\n"
            "            seen.add(w)\n"
            "    return pairs\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum_number_of_string_pairs\b|"
                    r"\bmaximum[_ ]number[_ ]of[_ ]string[_ ]pairs\b|"
                    r"\bfind[_ ]maximum[_ ]number[_ ]of[_ ]string[_ ]pairs\b|"
                    r"\bleetcode[_ ]2744\b",
                    low,
                )
            )
            and "identical" not in low,
            (
                ((["cd", "ac", "dc", "ca", "zz"],), 2),
                ((["ab", "ba", "cc"],), 1),
                ((["aa", "ab"],), 0),
            ),
        ),
        T(
            "is_winner",
            "def is_winner(player1, player2):\n"
            '    """Bowling: double next two rolls after a 10 (LeetCode 2660)."""\n'
            "    def score(p):\n"
            "        n = len(p)\n"
            "        total = 0\n"
            "        for i, v in enumerate(p):\n"
            "            dbl = (i >= 1 and p[i - 1] == 10) or (i >= 2 and p[i - 2] == 10)\n"
            "            total += v * (2 if dbl else 1)\n"
            "        return total\n"
            "    a, b = score(player1), score(player2)\n"
            "    if a > b:\n"
            "        return 1\n"
            "    if a < b:\n"
            "        return 2\n"
            "    return 0\n",
            lambda low: bool(
                re.search(
                    r"\bis_winner\b|"
                    r"\bwinner[_ ]of[_ ]a[_ ]bowling[_ ]game\b|"
                    r"\bbowling[_ ]game\b|"
                    r"\bleetcode[_ ]2660\b",
                    low,
                )
            )
            and "tictactoe" not in low
            and "nim" not in low,
            (
                (([4, 10, 7, 9], [6, 5, 2, 3]), 1),
                (([3, 5, 7, 6], [8, 10, 10, 2]), 2),
                (([2, 3], [4, 1]), 0),
            ),
        ),
    ]
