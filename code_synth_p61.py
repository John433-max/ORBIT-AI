"""Cycle 323: furthest from origin / k-element max sum / circular losers /
min string after AB-CD removals / lex-smallest palindrome / fascinating number."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "furthest_distance_from_origin",
            "def furthest_distance_from_origin(moves):\n"
            '    """Max |pos| after L/R/_ moves; _ chosen freely (LeetCode 2833)."""\n'
            "    left = moves.count('L')\n"
            "    right = moves.count('R')\n"
            "    wild = moves.count('_')\n"
            "    return abs(left - right) + wild\n",
            lambda low: bool(
                re.search(
                    r"\bfurthest_distance_from_origin\b|"
                    r"\bfurthest[_ ]point[_ ]from[_ ]origin\b|"
                    r"\bleetcode[_ ]2833\b",
                    low,
                )
            ),
            (
                (("L_RL__R",), 3),
                (("_",), 1),
            ),
        ),
        T(
            "maximize_sum",
            "def maximize_sum(nums, k):\n"
            '    """k times take max then increment it; return score (LeetCode 2656)."""\n'
            "    m = max(nums)\n"
            "    return k * m + k * (k - 1) // 2\n",
            lambda low: bool(
                re.search(
                    r"\bmaximize_sum\b|"
                    r"\bmaximum[_ ]sum[_ ]with[_ ]exactly[_ ]k[_ ]elements\b|"
                    r"\bleetcode[_ ]2656\b",
                    low,
                )
            )
            and "subarray" not in low,
            (
                (([1, 2, 3, 4, 5], 3), 18),
                (([5, 5, 5], 2), 11),
            ),
        ),
        T(
            "circular_game_losers",
            "def circular_game_losers(n, k):\n"
            '    """1-indexed players who never received the ball (LeetCode 2682)."""\n'
            "    seen = set()\n"
            "    i, step = 0, 1\n"
            "    while i not in seen:\n"
            "        seen.add(i)\n"
            "        i = (i + step * k) % n\n"
            "        step += 1\n"
            "    return [j + 1 for j in range(n) if j not in seen]\n",
            lambda low: bool(
                re.search(
                    r"\bcircular_game_losers\b|"
                    r"\bfind[_ ]the[_ ]losers[_ ]of[_ ]the[_ ]circular[_ ]game\b|"
                    r"\bcircular[_ ]game[_ ]losers\b|"
                    r"\bleetcode[_ ]2682\b",
                    low,
                )
            ),
            (
                ((5, 2), [4, 5]),
                ((4, 4), [2, 3, 4]),
            ),
        ),
        T(
            "min_length",
            "def min_length(s):\n"
            '    """Repeatedly delete AB or CD; leftover length (LeetCode 2696)."""\n'
            "    st = []\n"
            "    for ch in s:\n"
            "        if st and ((st[-1] == 'A' and ch == 'B') or (st[-1] == 'C' and ch == 'D')):\n"
            "            st.pop()\n"
            "        else:\n"
            "            st.append(ch)\n"
            "    return len(st)\n",
            lambda low: bool(
                re.search(
                    r"\bmin_length\b|"
                    r"\bminimum[_ ]string[_ ]length[_ ]after[_ ]removing[_ ]substrings\b|"
                    r"\bleetcode[_ ]2696\b",
                    low,
                )
            )
            and "min_length_after" not in low
            and "window" not in low,
            (
                (("ABFCACDB",), 2),
                (("ACBBD",), 5),
            ),
        ),
        T(
            "make_smallest_palindrome",
            "def make_smallest_palindrome(s):\n"
            '    """Lex-smallest palindrome by replacing pairs with min char (LeetCode 2697)."""\n'
            "    a = list(s)\n"
            "    i, j = 0, len(a) - 1\n"
            "    while i < j:\n"
            "        if a[i] != a[j]:\n"
            "            c = min(a[i], a[j])\n"
            "            a[i] = a[j] = c\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return ''.join(a)\n",
            lambda low: bool(
                re.search(
                    r"\bmake_smallest_palindrome\b|"
                    r"\blexicographically[_ ]smallest[_ ]palindrome\b|"
                    r"\bleetcode[_ ]2697\b",
                    low,
                )
            )
            and "longest" not in low
            and "valid_palindrome" not in low,
            (
                (("egcfe",), "efcfe"),
                (("abcd",), "abba"),
            ),
        ),
        T(
            "is_fascinating",
            "def is_fascinating(n):\n"
            '    """n, 2n, 3n concat uses 1-9 each once (LeetCode 2729)."""\n'
            "    s = str(n) + str(2 * n) + str(3 * n)\n"
            "    return len(s) == 9 and set(s) == set('123456789')\n",
            lambda low: bool(
                re.search(
                    r"\bis_fascinating\b|"
                    r"\bfascinating[_ ]number\b|"
                    r"\bcheck[_ ]if[_ ]the[_ ]number[_ ]is[_ ]fascinating\b|"
                    r"\bleetcode[_ ]2729\b",
                    low,
                )
            ),
            (
                ((192,), True),
                ((100,), False),
            ),
        ),
    ]
