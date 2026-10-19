"""Cycle 407: pure functions that fell through to NotImplemented drafts.

Covers run-length encode, argmax, slugify, IPv4 check, Collatz steps, and rot13.
Matchers stay specific so they do not steal existing templates.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "run_length_encode",
            "def run_length_encode(s):\n"
            '    """Run-length encode consecutive characters as char+count."""\n'
            "    s = str(s)\n"
            "    if not s:\n"
            "        return ''\n"
            "    out = []\n"
            "    prev, n = s[0], 1\n"
            "    for ch in s[1:]:\n"
            "        if ch == prev:\n"
            "            n += 1\n"
            "        else:\n"
            "            out.append(prev + str(n))\n"
            "            prev, n = ch, 1\n"
            "    out.append(prev + str(n))\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(r"\brun[-_ ]length[-_ ]encode(?:s|d)?\b|\brle\b", low)
            )
            and "decompress" not in low
            and "decode" not in low,
            [(("aaabb",), "a3b2"), (("abc",), "a1b1c1"), (("",), "")],
        ),
        T(
            "decompress_rl_elist",
            "def decompress_rl_elist(nums):\n"
            '    """Decompress a run-length encoded list [freq, val, ...] (LeetCode 1313)."""\n'
            "    out = []\n"
            "    nums = list(nums)\n"
            "    for i in range(0, len(nums), 2):\n"
            "        freq, val = int(nums[i]), nums[i + 1]\n"
            "        out.extend([val] * freq)\n"
            "    return out\n",
            lambda low: (
                "decompress" in low
                and ("run-length" in low or "run length" in low or "rle" in low)
            )
            or bool(re.search(r"\bdecompress_rl_elist\b", low)),
            [(([1, 2, 3, 4],), [2, 4, 4, 4]), (([1, 1, 2, 3],), [1, 3, 3]), (([],), [])],
        ),
        T(
            "argmax_list",
            "def argmax_list(nums):\n"
            '    """Index of the maximum value; -1 if empty."""\n'
            "    nums = list(nums)\n"
            "    if not nums:\n"
            "        return -1\n"
            "    best_i, best = 0, nums[0]\n"
            "    for i, x in enumerate(nums):\n"
            "        if x > best:\n"
            "            best, best_i = x, i\n"
            "    return best_i\n",
            lambda low: bool(re.search(r"\bargmax\b", low)),
            [(([1, 3, 2],), 1), (([],), -1), (([5],), 0)],
        ),
        T(
            "slugify",
            "def slugify(s):\n"
            '    """Lowercase slug: alnum kept, other runs become single dashes."""\n'
            "    out = []\n"
            "    prev_dash = False\n"
            "    for ch in str(s).lower():\n"
            "        if ch.isalnum():\n"
            "            out.append(ch)\n"
            "            prev_dash = False\n"
            "        elif not prev_dash and out:\n"
            "            out.append('-')\n"
            "            prev_dash = True\n"
            "    if out and out[-1] == '-':\n"
            "        out.pop()\n"
            "    return ''.join(out)\n",
            lambda low: bool(re.search(r"\bslugif(?:y|ies)\b|\bslug\b", low)),
            [(("Hello World",), "hello-world"), (("  A--B  ",), "a-b"), (("",), "")],
        ),
        T(
            "is_ipv4",
            "def is_ipv4(s):\n"
            '    """True if s is a dotted IPv4 address with four 0-255 octets."""\n'
            "    parts = str(s).split('.')\n"
            "    if len(parts) != 4:\n"
            "        return False\n"
            "    for p in parts:\n"
            "        if not p.isdigit() or (len(p) > 1 and p[0] == '0'):\n"
            "            return False\n"
            "        n = int(p)\n"
            "        if n < 0 or n > 255:\n"
            "            return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(r"\bipv4\b|\bvalid ip(?:v4)? address\b", low)
            ),
            [(("192.168.1.1",), True), (("256.1.1.1",), False), (("1.2.3",), False)],
        ),
        T(
            "collatz_steps",
            "def collatz_steps(n):\n"
            '    """Steps to reach 1 under the Collatz map (3n+1 / n/2)."""\n'
            "    n = int(n)\n"
            "    steps = 0\n"
            "    while n != 1:\n"
            "        n = n // 2 if n % 2 == 0 else 3 * n + 1\n"
            "        steps += 1\n"
            "    return steps\n",
            lambda low: bool(re.search(r"\bcollatz\b", low)),
            [((1,), 0), ((2,), 1), ((3,), 7)],
        ),
        T(
            "rot13",
            "def rot13(s):\n"
            '    """ROT13 cipher (letters only; other chars unchanged)."""\n'
            "    out = []\n"
            "    for ch in str(s):\n"
            "        if 'a' <= ch <= 'z':\n"
            "            out.append(chr((ord(ch) - 97 + 13) % 26 + 97))\n"
            "        elif 'A' <= ch <= 'Z':\n"
            "            out.append(chr((ord(ch) - 65 + 13) % 26 + 65))\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n",
            lambda low: bool(re.search(r"\brot13\b|\brot-?13\b", low)),
            [(("Hello",), "Uryyb"), (("ABC",), "NOP"), (("xyz",), "klm")],
        ),
    ]
