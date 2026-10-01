"""Cycle 328: unused Easy — digit game / snake matrix / chip moves /
encrypted string / purchase balance / left-right diffs."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "can_alice_win",
            "def can_alice_win(nums):\n"
            '    """Alice wins iff single-digit sum != double-digit sum (LeetCode 3232)."""\n'
            "    single = sum(x for x in nums if x < 10)\n"
            "    double = sum(x for x in nums if x >= 10)\n"
            "    return single != double\n",
            lambda low: bool(
                re.search(
                    r"\bcan_alice_win\b|"
                    r"\bdigit[_ ]game[_ ]can[_ ]be[_ ]won\b|"
                    r"\bfind[_ ]if[_ ]digit[_ ]game\b|"
                    r"\bleetcode[_ ]3232\b",
                    low,
                )
            )
            and "nim" not in low,
            (
                (([1, 2, 3, 4, 10],), False),
                (([1, 2, 3, 4, 5, 14],), True),
            ),
        ),
        T(
            "final_position_of_snake",
            "def final_position_of_snake(n, commands):\n"
            '    """Start at (0,0) on n x n; apply UP/DOWN/LEFT/RIGHT; return cell id (LeetCode 3248)."""\n'
            "    r = c = 0\n"
            "    for cmd in commands:\n"
            "        if cmd == 'UP':\n"
            "            r -= 1\n"
            "        elif cmd == 'DOWN':\n"
            "            r += 1\n"
            "        elif cmd == 'LEFT':\n"
            "            c -= 1\n"
            "        else:\n"
            "            c += 1\n"
            "    return r * n + c\n",
            lambda low: bool(
                re.search(
                    r"\bfinal_position_of_snake\b|"
                    r"\bsnake[_ ]in[_ ]matrix\b|"
                    r"\bfinal[_ ]position[_ ]of[_ ]snake\b|"
                    r"\bleetcode[_ ]3248\b",
                    low,
                )
            ),
            (
                ((2, ["RIGHT", "DOWN"]), 3),
                ((3, ["DOWN", "RIGHT", "UP"]), 1),
            ),
        ),
        T(
            "min_cost_to_move_chips",
            "def min_cost_to_move_chips(position):\n"
            '    """Move chips to one position; even hops cost 0, odd cost 1 (LeetCode 1217)."""\n'
            "    even = sum(1 for p in position if p % 2 == 0)\n"
            "    odd = len(position) - even\n"
            "    return min(even, odd)\n",
            lambda low: bool(
                re.search(
                    r"\bmin_cost_to_move_chips\b|"
                    r"\bminimum[_ ]cost[_ ]to[_ ]move[_ ]chips\b|"
                    r"\bmin[_ ]cost[_ ]to[_ ]move[_ ]chips\b|"
                    r"\bminimum[_ ]number[_ ]of[_ ]chips[_ ]to[_ ]move\b|"
                    r"\bleetcode[_ ]1217\b",
                    low,
                )
            )
            and "climb" not in low,
            (
                (([1, 2, 3],), 1),
                (([2, 2, 2, 3, 3],), 2),
            ),
        ),
        T(
            "get_encrypted_string",
            "def get_encrypted_string(s, k):\n"
            '    """Replace each char with the one k steps ahead, cyclic (LeetCode 3210)."""\n'
            "    n = len(s)\n"
            "    return ''.join(s[(i + k) % n] for i in range(n))\n",
            lambda low: bool(
                re.search(
                    r"\bget_encrypted_string\b|"
                    r"\bfind[_ ]the[_ ]encrypted[_ ]string\b|"
                    r"\bencrypted[_ ]string\b|"
                    r"\bleetcode[_ ]3210\b",
                    low,
                )
            )
            and "decode" not in low
            and "tinyurl" not in low,
            (
                (("dart", 3), "tdar"),
                (("aaa", 1), "aaa"),
            ),
        ),
        T(
            "account_balance_after_purchase",
            "def account_balance_after_purchase(purchase_amount):\n"
            '    """Start at 100; round purchase to nearest 10 (5 up) then subtract (LeetCode 2806)."""\n'
            "    rounded = ((purchase_amount + 5) // 10) * 10\n"
            "    return 100 - rounded\n",
            lambda low: bool(
                re.search(
                    r"\baccount_balance_after_purchase\b|"
                    r"\baccount[_ ]balance[_ ]after[_ ]purchase\b|"
                    r"\bbalance[_ ]after[_ ]purchase\b|"
                    r"\bleetcode[_ ]2806\b",
                    low,
                )
            )
            and "buy_choco" not in low,
            (
                ((9,), 90),
                ((15,), 80),
            ),
        ),
        T(
            "left_right_difference",
            "def left_right_difference(nums):\n"
            '    """|leftSum[i] - rightSum[i]| for each index (LeetCode 2574)."""\n'
            "    total = sum(nums)\n"
            "    left = 0\n"
            "    out = []\n"
            "    for x in nums:\n"
            "        right = total - left - x\n"
            "        out.append(abs(left - right))\n"
            "        left += x\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bleft_right_difference\b|"
                    r"\bleft[_ ]and[_ ]right[_ ]sum[_ ]differences\b|"
                    r"\bleft[_ ]right[_ ]difference\b|"
                    r"\bleetcode[_ ]2574\b",
                    low,
                )
            )
            and "two_sum" not in low
            and "distinct_difference" not in low,
            (
                (([10, 4, 8, 3],), [15, 1, 11, 22]),
                (([1],), [0]),
            ),
        ),
    ]
