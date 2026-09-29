"""Cycle 266: additional verified Python templates (pack 9)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "lemonade_change",
            "def lemonade_change(bills):\n"
            '    """True if every customer paying with 5/10/20 can receive change."""\n'
            "    five = ten = 0\n"
            "    for bill in bills:\n"
            "        bill = int(bill)\n"
            "        if bill == 5:\n"
            "            five += 1\n"
            "        elif bill == 10:\n"
            "            if five == 0:\n"
            "                return False\n"
            "            five -= 1\n"
            "            ten += 1\n"
            "        else:\n"
            "            if ten and five:\n"
            "                ten -= 1\n"
            "                five -= 1\n"
            "            elif five >= 3:\n"
            "                five -= 3\n"
            "            else:\n"
            "                return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\blemonade change\b|"
                    r"\blemonade_change\b|"
                    r"\blemonade stand\b",
                    low,
                )
            ),
            (([[5, 5, 5, 10, 20]], True), ([[5, 5, 10, 10, 20]], False), ([[5, 5, 10]], True)),
        ),
        T(
            "judge_circle",
            "def judge_circle(moves):\n"
            '    """True if U/D/L/R moves return a robot to the origin."""\n'
            "    x = y = 0\n"
            "    for ch in str(moves).upper():\n"
            "        if ch == 'U':\n"
            "            y += 1\n"
            "        elif ch == 'D':\n"
            "            y -= 1\n"
            "        elif ch == 'L':\n"
            "            x -= 1\n"
            "        elif ch == 'R':\n"
            "            x += 1\n"
            "    return x == 0 and y == 0\n",
            lambda low: bool(
                re.search(
                    r"\bjudge circle\b|"
                    r"\bjudge_circle\b|"
                    r"\brobot return(?:s)? to (?:the )?origin\b|"
                    r"\brobot origin\b",
                    low,
                )
            ),
            ((("UD",), True), (("LL",), False), (("UDLR",), True)),
        ),
        T(
            "num_jewels_in_stones",
            "def num_jewels_in_stones(jewels, stones):\n"
            '    """Count how many stones are also jewels (case-sensitive)."""\n'
            "    bag = set(str(jewels))\n"
            "    return sum(1 for ch in str(stones) if ch in bag)\n",
            lambda low: bool(
                re.search(
                    r"\bjewels? (?:and|in) stones?\b|"
                    r"\bnum_jewels_in_stones\b|"
                    r"\bhow many jewels\b|"
                    r"\bjewel(?:s)? stones?\b",
                    low,
                )
            ),
            ((("aA", "aAAbbbb"), 3), (("z", "ZZ"), 0)),
        ),
        T(
            "unique_morse_representations",
            "def unique_morse_representations(words):\n"
            '    """Count distinct Morse encodings of the given words."""\n'
            "    table = [\n"
            "        '.-','-...','-.-.','-..','.','..-.','--.','....','..','.---',\n"
            "        '-.-','.-..','--','-.','---','.--.','--.-','.-.','...','-',\n"
            "        '..-','...-','.--','-..-','-.--','--..',\n"
            "    ]\n"
            "    seen = set()\n"
            "    for w in words:\n"
            "        code = ''.join(table[ord(ch.lower()) - 97] for ch in str(w) if ch.isalpha())\n"
            "        seen.add(code)\n"
            "    return len(seen)\n",
            lambda low: bool(
                re.search(
                    r"\bunique morse\b|"
                    r"\bmorse representations?\b|"
                    r"\bunique_morse_representations\b|"
                    r"\bmorse code words\b",
                    low,
                )
            ),
            (([["gin", "zen", "gig", "msg"]], 2),),
        ),
        T(
            "find_judge",
            "def find_judge(n, trust):\n"
            '    """Town judge: trusted by everyone else and trusts nobody."""\n'
            "    n = int(n)\n"
            "    score = [0] * (n + 1)\n"
            "    for a, b in trust:\n"
            "        score[int(a)] -= 1\n"
            "        score[int(b)] += 1\n"
            "    for i in range(1, n + 1):\n"
            "        if score[i] == n - 1:\n"
            "            return i\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bfind(?: the)? (?:town )?judge\b|"
                    r"\bfind_judge\b|"
                    r"\btown judge\b",
                    low,
                )
            ),
            (((2, [[1, 2]]), 2), ((3, [[1, 3], [2, 3]]), 3), ((3, [[1, 3], [2, 3], [3, 1]]), -1)),
        ),
        T(
            "peak_index_in_mountain_array",
            "def peak_index_in_mountain_array(arr):\n"
            '    """Index of the peak in a mountain array (strict up then down)."""\n'
            "    arr = list(arr)\n"
            "    lo, hi = 0, len(arr) - 1\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] < arr[mid + 1]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return lo\n",
            lambda low: bool(
                re.search(
                    r"\bpeak index in (?:a )?mountain\b|"
                    r"\bpeak_index_in_mountain_array\b|"
                    r"\bmountain array peak index\b",
                    low,
                )
            ),
            (([[0, 1, 0]], 1), ([[0, 2, 1, 0]], 1), ([[0, 10, 5, 2]], 1)),
        ),
    ]
