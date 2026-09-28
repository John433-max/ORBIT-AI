"""Cycle 265: additional verified Python templates (pack 8)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "license_key_formatting",
            "def license_key_formatting(s, k):\n"
            '    """Reformat a license key into groups of k uppercase chars."""\n'
            "    raw = ''.join(ch for ch in str(s) if ch != '-').upper()\n"
            "    k = int(k)\n"
            "    if k <= 0 or not raw:\n"
            "        return raw\n"
            "    first = len(raw) % k\n"
            "    parts = [raw[:first]] if first else []\n"
            "    for i in range(first, len(raw), k):\n"
            "        parts.append(raw[i:i + k])\n"
            "    return '-'.join(p for p in parts if p)\n",
            lambda low: bool(
                re.search(
                    r"\blicense key\b|"
                    r"\blicense_key_formatting\b|"
                    r"\breformat(?: a)? license\b",
                    low,
                )
            ),
            (
                (("5F3Z-2e-9-w", 4), "5F3Z-2E9W"),
                (("2-5g-3-J", 2), "2-5G-3J"),
                (("---", 3), ""),
            ),
        ),
        T(
            "find_complement",
            "def find_complement(num):\n"
            '    """Bitwise complement of num\'s binary representation without leading zeros."""\n'
            "    n = int(num)\n"
            "    if n == 0:\n"
            "        return 1\n"
            "    mask = (1 << n.bit_length()) - 1\n"
            "    return n ^ mask\n",
            lambda low: bool(
                re.search(
                    r"\bnumber complement\b|"
                    r"\bfind complement\b|"
                    r"\bfind_complement\b|"
                    r"\bcomplement of (?:an? )?(?:integer|number)\b",
                    low,
                )
            ),
            (((5,), 2), ((1,), 0), ((0,), 1)),
        ),
        T(
            "convert_to_title",
            "def convert_to_title(column_number):\n"
            '    """Excel column title for a 1-indexed column number (1 -> A)."""\n'
            "    n = int(column_number)\n"
            "    out = []\n"
            "    while n > 0:\n"
            "        n, rem = divmod(n - 1, 26)\n"
            "        out.append(chr(ord('A') + rem))\n"
            "    return ''.join(reversed(out))\n",
            lambda low: bool(
                re.search(
                    r"\bexcel column title\b|"
                    r"\bconvert_to_title\b|"
                    r"\bcolumn number to title\b|"
                    r"\bexcel title from (?:column )?number\b",
                    low,
                )
            ),
            (((1,), "A"), ((28,), "AB"), ((701,), "ZY")),
        ),
        T(
            "title_to_number",
            "def title_to_number(column_title):\n"
            '    """1-indexed Excel column number from an uppercase title (A -> 1)."""\n'
            "    n = 0\n"
            "    for ch in str(column_title).strip().upper():\n"
            "        n = n * 26 + (ord(ch) - ord('A') + 1)\n"
            "    return n\n",
            lambda low: bool(
                re.search(
                    r"\bexcel column number\b|"
                    r"\btitle_to_number\b|"
                    r"\bcolumn title to number\b|"
                    r"\bexcel number from (?:column )?title\b",
                    low,
                )
            ),
            ((("A",), 1), (("AB",), 28), (("ZY",), 701)),
        ),
        T(
            "arrange_coins",
            "def arrange_coins(n):\n"
            '    """Complete rows of a coin staircase that uses at most n coins."""\n'
            "    n = int(n)\n"
            "    lo, hi, ans = 0, n, 0\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        need = mid * (mid + 1) // 2\n"
            "        if need <= n:\n"
            "            ans = mid\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\barrange coins\b|"
                    r"\barrange_coins\b|"
                    r"\bcoin staircase\b|"
                    r"\bstaircase of coins\b",
                    low,
                )
            ),
            (((5,), 2), ((8,), 3), ((1,), 1), ((0,), 0)),
        ),
        T(
            "self_dividing",
            "def self_dividing_numbers(left, right):\n"
            '    """Self-dividing integers in the inclusive range [left, right]."""\n'
            "    def ok(x):\n"
            "        n = x\n"
            "        while n:\n"
            "            d = n % 10\n"
            "            if d == 0 or x % d:\n"
            "                return False\n"
            "            n //= 10\n"
            "        return True\n"
            "    return [i for i in range(int(left), int(right) + 1) if ok(i)]\n",
            lambda low: bool(
                re.search(
                    r"\bself[- ]dividing\b|"
                    r"\bself_dividing\b",
                    low,
                )
            ),
            (((1, 22), [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 22]),),
        ),
    ]
