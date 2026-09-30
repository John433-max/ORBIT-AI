"""Cycle 310: arithmetic progression / path crossing / final prices / prefix word / crawler logs / max nesting depth."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "can_make_arithmetic_progression",
            "def can_make_arithmetic_progression(arr):\n"
            '    """True if arr can be rearranged into an AP (LeetCode 1502)."""\n'
            "    a = sorted(arr)\n"
            "    if len(a) <= 2:\n"
            "        return True\n"
            "    d = a[1] - a[0]\n"
            "    return all(a[i] - a[i - 1] == d for i in range(2, len(a)))\n",
            lambda low: bool(
                re.search(
                    r"\bcan[_ ]make[_ ]arithmetic[_ ]progression\b|"
                    r"\barithmetic[_ ]progression[_ ]from[_ ]sequence\b|"
                    r"\bcan_make_arithmetic_progression\b",
                    low,
                )
            ),
            (
                (([3, 5, 1],), True),
                (([1, 2, 4],), False),
                (([1, 2, 3, 4],), True),
            ),
        ),
        T(
            "path_crossing",
            "def path_crossing(path):\n"
            '    """True if the NESW path visits a point twice (LeetCode 1496)."""\n'
            "    x = y = 0\n"
            "    seen = {(0, 0)}\n"
            "    move = {\"N\": (0, 1), \"S\": (0, -1), \"E\": (1, 0), \"W\": (-1, 0)}\n"
            "    for ch in path:\n"
            "        dx, dy = move[ch]\n"
            "        x += dx\n"
            "        y += dy\n"
            "        if (x, y) in seen:\n"
            "            return True\n"
            "        seen.add((x, y))\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bpath[_ ]crossing\b|"
                    r"\bpath[_ ]crosses[_ ]itself\b|"
                    r"\bpath_crossing\b",
                    low,
                )
            ),
            (
                (("NES",), False),
                (("NESWW",), True),
                (("N",), False),
            ),
        ),
        T(
            "final_prices",
            "def final_prices(prices):\n"
            '    """Apply next-smaller-or-equal discount (LeetCode 1475)."""\n'
            "    n = len(prices)\n"
            "    out = list(prices)\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            if prices[j] <= prices[i]:\n"
            "                out[i] = prices[i] - prices[j]\n"
            "                break\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bfinal[_ ]prices[_ ]with[_ ](a[_ ])?special[_ ]discount\b|"
                    r"\bfinal[_ ]prices\b|"
                    r"\bfinal_prices\b",
                    low,
                )
            ),
            (
                (([8, 4, 6, 2, 3],), [4, 2, 4, 2, 3]),
                (([1, 2, 3, 4, 5],), [1, 2, 3, 4, 5]),
                (([10, 1, 1, 6],), [9, 0, 1, 6]),
            ),
        ),
        T(
            "is_prefix_of_word",
            "def is_prefix_of_word(sentence, searchWord):\n"
            '    """1-based index of first word that starts with searchWord (LeetCode 1455)."""\n'
            "    for i, w in enumerate(sentence.split(), 1):\n"
            "        if w.startswith(searchWord):\n"
            "            return i\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bcheck[_ ]if[_ ]a[_ ]word[_ ]occurs[_ ]as[_ ](a[_ ])?prefix\b|"
                    r"\bis[_ ]prefix[_ ]of[_ ]word\b|"
                    r"\bprefix[_ ]of[_ ]word[_ ]in[_ ]sentence\b|"
                    r"\bis_prefix_of_word\b",
                    low,
                )
            ),
            (
                (("i love eating burger", "burg"), 4),
                (("this problem is an easy problem", "pro"), 2),
                (("i am tired", "you"), -1),
            ),
        ),
        T(
            "crawler_log_folder",
            "def crawler_log_folder(logs):\n"
            '    """Min operations to return to main folder (LeetCode 1598)."""\n'
            "    depth = 0\n"
            "    for log in logs:\n"
            "        if log == \"../\":\n"
            "            if depth:\n"
            "                depth -= 1\n"
            "        elif log != \"./\":\n"
            "            depth += 1\n"
            "    return depth\n",
            lambda low: bool(
                re.search(
                    r"\bcrawler[_ ]log[_ ]folder\b|"
                    r"\bcrawler[_ ]logs\b|"
                    r"\bcrawler_log_folder\b",
                    low,
                )
            ),
            (
                ((["d1/", "d2/", "../", "d21/", "./"],), 2),
                ((["d1/", "../", "../", "../"],), 0),
                ((["./", "../", "./"],), 0),
            ),
        ),
        T(
            "max_nesting_depth",
            "def max_nesting_depth(s):\n"
            '    """Maximum nesting depth of parentheses (LeetCode 1614)."""\n'
            "    cur = best = 0\n"
            "    for ch in s:\n"
            "        if ch == \"(\":\n"
            "            cur += 1\n"
            "            if cur > best:\n"
            "                best = cur\n"
            "        elif ch == \")\":\n"
            "            cur -= 1\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)?[_ ]nesting[_ ]depth\b|"
                    r"\bnesting[_ ]depth[_ ]of[_ ](the[_ ])?parentheses\b|"
                    r"\bmax_nesting_depth\b",
                    low,
                )
            ),
            (
                (("(1+(2*3)+((8)/4))+1",), 3),
                (("(1)+((2))+(((3)))",), 3),
                (("()(())((()()))",), 3),
            ),
        ),
    ]
