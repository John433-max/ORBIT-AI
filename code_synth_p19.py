"""Cycle 277: additional verified Python templates (pack 19)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "num_rook_captures",
            "def num_rook_captures(board):\n"
            '    """Pawns a rook can capture on an empty chessboard (no blockers)."""\n'
            "    n = 8\n"
            "    ri = rj = -1\n"
            "    for i, row in enumerate(board):\n"
            "        for j, ch in enumerate(row):\n"
            "            if ch == 'R':\n"
            "                ri, rj = i, j\n"
            "    cap = 0\n"
            "    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "        i, j = ri + di, rj + dj\n"
            "        while 0 <= i < n and 0 <= j < n:\n"
            "            cell = board[i][j]\n"
            "            if cell == 'B':\n"
            "                break\n"
            "            if cell == 'p':\n"
            "                cap += 1\n"
            "                break\n"
            "            i += di\n"
            "            j += dj\n"
            "    return cap\n",
            lambda low: bool(
                re.search(
                    r"\bavailable captures for rook\b|"
                    r"\bnum_rook_captures\b|"
                    r"\brook captures\b|"
                    r"\bpawns a rook can capture\b",
                    low,
                )
            ),
            (
                (
                    [
                        [
                            "p.......",
                            "........",
                            "........",
                            "........",
                            "R.......",
                            "........",
                            "........",
                            "........",
                        ]
                    ],
                    1,
                ),
            ),
        ),
        T(
            "score_of_parentheses",
            "def score_of_parentheses(s):\n"
            '    """Score of a balanced parentheses string: ()=1, AB=A+B, (A)=2*A."""\n'
            "    st = [0]\n"
            "    for ch in str(s):\n"
            "        if ch == '(':\n"
            "            st.append(0)\n"
            "        else:\n"
            "            v = st.pop()\n"
            "            st[-1] += 1 if v == 0 else 2 * v\n"
            "    return st[-1]\n",
            lambda low: bool(
                re.search(
                    r"\bscore of parentheses\b|"
                    r"\bscore_of_parentheses\b",
                    low,
                )
            )
            and "valid parentheses" not in low
            and "longest valid" not in low,
            ((("()",), 1), (("(())",), 2), (("()()",), 2)),
        ),
        T(
            "number_of_lines",
            "def number_of_lines(widths, s):\n"
            '    """Lines used and last-line width when writing s with per-letter widths (max 100)."""\n'
            "    lines, cur = 1, 0\n"
            "    for ch in str(s):\n"
            "        w = int(widths[ord(ch) - 97])\n"
            "        if cur + w > 100:\n"
            "            lines += 1\n"
            "            cur = w\n"
            "        else:\n"
            "            cur += w\n"
            "    return [lines, cur]\n",
            lambda low: bool(
                re.search(
                    r"\bnumber of lines to write\b|"
                    r"\bnumber_of_lines\b|"
                    r"\bwrite string with widths\b",
                    low,
                )
            ),
            (
                ([[10] * 26, "abcdefghijklmnopqrstuvwxyz"], [3, 60]),
                ([[10] * 26, "bbb"], [1, 30]),
            ),
        ),
        T(
            "shortest_completing_word",
            "def shortest_completing_word(license_plate, words):\n"
            '    """Shortest word whose letters cover the plate letters (ignore digits/spaces)."""\n'
            "    from collections import Counter\n"
            "    need = Counter(ch.lower() for ch in str(license_plate) if ch.isalpha())\n"
            "    best = None\n"
            "    for w in words:\n"
            "        have = Counter(w.lower())\n"
            "        if all(have[c] >= n for c, n in need.items()):\n"
            "            if best is None or len(w) < len(best):\n"
            "                best = w\n"
            "    return best or ''\n",
            lambda low: bool(
                re.search(
                    r"\bshortest completing word\b|"
                    r"\bshortest_completing_word\b",
                    low,
                )
            ),
            (
                (("1s3 PSt", ["step", "steps", "stripe", "stepple"]), "steps"),
                (("1s3 456", ["looks", "pest", "stew", "show"]), "pest"),
            ),
        ),
        T(
            "reverse_only_letters",
            "def reverse_only_letters(s):\n"
            '    """Reverse letters in s, leaving non-letters in place."""\n'
            "    chars = list(str(s))\n"
            "    i, j = 0, len(chars) - 1\n"
            "    while i < j:\n"
            "        if not chars[i].isalpha():\n"
            "            i += 1\n"
            "        elif not chars[j].isalpha():\n"
            "            j -= 1\n"
            "        else:\n"
            "            chars[i], chars[j] = chars[j], chars[i]\n"
            "            i += 1\n"
            "            j -= 1\n"
            "    return ''.join(chars)\n",
            lambda low: bool(
                re.search(
                    r"\breverse only letters\b|"
                    r"\breverse_only_letters\b",
                    low,
                )
            )
            and "reverse vowels" not in low
            and "reverse_string" not in low
            and "reverse a string" not in low,
            ((("ab-cd",), "dc-ba"), (("a-bC-dEf-ghIj",), "j-Ih-gfE-dCba"), (("Test1ng-Leet=code-Q!",), "Qedo1ct-eeLg=ntse-T!")),
        ),
        T(
            "keyboard_row",
            "def keyboard_row(words):\n"
            '    """Words that can be typed using letters of only one American keyboard row."""\n'
            "    rows = [set('qwertyuiop'), set('asdfghjkl'), set('zxcvbnm')]\n"
            "    out = []\n"
            "    for w in words:\n"
            "        letters = set(w.lower())\n"
            "        if any(letters <= row for row in rows):\n"
            "            out.append(w)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bkeyboard row\b|"
                    r"\bkeyboard_row\b|"
                    r"\bwords on one keyboard row\b",
                    low,
                )
            ),
            (([["Hello", "Alaska", "Dad", "Peace"]], ["Alaska", "Dad"]),),
        ),
    ]
