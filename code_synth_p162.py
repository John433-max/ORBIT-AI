"""Cycle 444: collatz steps, run-length encode, argmax, rot13, slugify, ipv4.

Everyday asks with no template. Matchers are phrase-gated so Caesar shift,
defang-ip, and title-case keep their names. Pack loads before p161.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "collatz_steps",
            "def collatz_steps(n):\n"
            '    """Count Collatz steps until n reaches 1 (sign ignored)."""\n'
            "    n = abs(int(n))\n"
            "    steps = 0\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    while n != 1 and steps < 100000:\n"
            "        n = n // 2 if n % 2 == 0 else 3 * n + 1\n"
            "        steps += 1\n"
            "    return steps\n",
            lambda low: "collatz" in low,
            (((1,), 0), ((6,), 8)),
        ),
        T(
            "run_length_encode",
            "def run_length_encode(s):\n"
            '    """Encode consecutive runs as (char, count) pairs."""\n'
            "    s = str(s)\n"
            "    if not s:\n"
            "        return []\n"
            "    out = []\n"
            "    prev = s[0]\n"
            "    count = 1\n"
            "    for ch in s[1:]:\n"
            "        if ch == prev:\n"
            "            count += 1\n"
            "        else:\n"
            "            out.append((prev, count))\n"
            "            prev = ch\n"
            "            count = 1\n"
            "    out.append((prev, count))\n"
            "    return out\n",
            lambda low: "run" in low
            and "length" in low
            and "encod" in low
            and "decod" not in low
            and "decompress" not in low,
            ((("aaabb",), [("a", 3), ("b", 2)]), (("",), [])),
        ),
        T(
            "argmax_list",
            "def argmax_list(nums):\n"
            '    """Index of the first maximum; empty input returns -1."""\n'
            "    if not nums:\n"
            "        return -1\n"
            "    best_i = 0\n"
            "    best = nums[0]\n"
            "    for i, x in enumerate(nums):\n"
            "        if x > best:\n"
            "            best = x\n"
            "            best_i = i\n"
            "    return best_i\n",
            lambda low: "argmax" in low
            and "matrix" not in low
            and "axis" not in low,
            ((([1, 5, 3, 5],), 1), (([],), -1)),
        ),
        T(
            "rot13",
            "def rot13(s):\n"
            '    """Rotate A-Z/a-z by 13; leave other characters unchanged."""\n'
            "    out = []\n"
            "    for ch in str(s):\n"
            "        o = ord(ch)\n"
            "        if 65 <= o <= 90:\n"
            "            out.append(chr((o - 65 + 13) % 26 + 65))\n"
            "        elif 97 <= o <= 122:\n"
            "            out.append(chr((o - 97 + 13) % 26 + 97))\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return \"\".join(out)\n",
            lambda low: bool(re.search(r"\brot-?13\b", low)) and "caesar" not in low,
            ((("hello",), "uryyb"), (("uryyb",), "hello")),
        ),
        T(
            "slugify",
            "def slugify(s):\n"
            '    """Lowercase alnum tokens joined by single hyphens."""\n'
            "    out = []\n"
            "    prev_dash = False\n"
            "    for ch in str(s).lower():\n"
            "        if ch.isalnum():\n"
            "            out.append(ch)\n"
            "            prev_dash = False\n"
            "        elif out and not prev_dash:\n"
            "            out.append(\"-\")\n"
            "            prev_dash = True\n"
            "    if out and out[-1] == \"-\":\n"
            "        out.pop()\n"
            "    return \"\".join(out)\n",
            lambda low: "slug" in low and "title case" not in low and "camel" not in low,
            ((("Hello, World!",), "hello-world"), (("a--b",), "a-b")),
        ),
        T(
            "is_ipv4",
            "def is_ipv4(s):\n"
            '    """True for four dotted octets in 0..255 with no leading zeros."""\n'
            "    parts = str(s).split(\".\")\n"
            "    if len(parts) != 4:\n"
            "        return False\n"
            "    for part in parts:\n"
            "        if not part.isdigit():\n"
            "            return False\n"
            "        if len(part) > 1 and part[0] == \"0\":\n"
            "            return False\n"
            "        n = int(part)\n"
            "        if n > 255:\n"
            "            return False\n"
            "    return True\n",
            lambda low: "ipv4" in low and "defang" not in low and "ipv6" not in low,
            ((("127.0.0.1",), True), (("256.1.1.1",), False), (("01.2.3.4",), False)),
        ),
    ]
