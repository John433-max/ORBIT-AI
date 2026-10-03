"""Cycle 394: unmatched LeetCode easies 1332 / 1370 / 1441 / 1576 / 1668 / 2396.

These titles previously fell through to the unverified draft stub.

Official examples:
- 1332 Remove Palindromic Subsequences: empty 0, palindrome 1, else 2.
  "ababa" -> 1, "abb" -> 2, "baabb" -> 2.
- 1370 Increasing Decreasing String: take remaining chars ascending, then
  descending, repeat. "aaaabbbbcccc" -> "abccbaabccba"; "rat" -> "art".
- 1441 Build an Array With Stack Operations: push every integer, pop misses.
  target [1,3] n=3 -> Push, Push, Pop, Push. [1,2,3] n=3 -> three Push.
- 1576 Replace All ?'s: first of a/b/c that differs from both neighbors.
  "?zs" -> "azs"; "ubv?w" -> "ubvaw"; "j?qg??b" -> "jaqgacb".
- 1668 Maximum Repeating Substring: largest k with word*k inside sequence.
  ("ababc","ab") -> 2; ("ababc","ba") -> 1; ("ababc","ac") -> 0.
- 2396 Strictly Palindromic Number: palindrome in every base 2..n-2.
  Official 9 and 4 are both false (base n-2 is "12").
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "remove_palindrome_sub",
            "def remove_palindrome_sub(s):\n"
            '    """Steps to remove palindromic subsequences (LeetCode 1332)."""\n'
            "    if not s:\n"
            "        return 0\n"
            "    return 1 if s == s[::-1] else 2\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1332\b", low)
                or "palindromic subsequences" in low
            ),
            examples=(
                (("ababa",), 1),
                (("abb",), 2),
                (("baabb",), 2),
                (("",), 0),
            ),
        ),
        T(
            "increasing_decreasing_string",
            "def increasing_decreasing_string(s):\n"
            '    """Rebuild s by ascending then descending passes (LeetCode 1370)."""\n'
            "    counts = [0] * 26\n"
            "    for ch in s:\n"
            "        counts[ord(ch) - 97] += 1\n"
            "    out = []\n"
            "    while len(out) < len(s):\n"
            "        for i in range(26):\n"
            "            if counts[i]:\n"
            "                out.append(chr(97 + i))\n"
            "                counts[i] -= 1\n"
            "        for i in range(25, -1, -1):\n"
            "            if counts[i]:\n"
            "                out.append(chr(97 + i))\n"
            "                counts[i] -= 1\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1370\b", low)
                or "increasing decreasing string" in low
            ),
            examples=(
                (("aaaabbbbcccc",), "abccbaabccba"),
                (("rat",), "art"),
            ),
        ),
        T(
            "build_array_stack",
            "def build_array_stack(target, n):\n"
            '    """Stack ops to build target from 1..n (LeetCode 1441)."""\n'
            "    ops = []\n"
            "    cur = 1\n"
            "    for x in target:\n"
            "        while cur < x:\n"
            "            ops.append('Push')\n"
            "            ops.append('Pop')\n"
            "            cur += 1\n"
            "        ops.append('Push')\n"
            "        cur += 1\n"
            "    return ops\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1441\b", low)
                or "array with stack operations" in low
                or "build an array with stack" in low
            ),
            examples=(
                (([1, 3], 3), ["Push", "Push", "Pop", "Push"]),
                (([1, 2, 3], 3), ["Push", "Push", "Push"]),
                (([1, 2], 4), ["Push", "Push"]),
            ),
        ),
        T(
            "modify_string",
            "def modify_string(s):\n"
            '    """Replace ? so no two adjacent letters match (LeetCode 1576)."""\n'
            "    chars = list(s)\n"
            "    n = len(chars)\n"
            "    for i in range(n):\n"
            "        if chars[i] != '?':\n"
            "            continue\n"
            "        for cand in 'abc':\n"
            "            left = chars[i - 1] if i else ''\n"
            "            right = chars[i + 1] if i + 1 < n else ''\n"
            "            if cand != left and cand != right:\n"
            "                chars[i] = cand\n"
            "                break\n"
            "    return ''.join(chars)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1576\b", low)
                or "avoid consecutive repeating" in low
                or re.search(r"replace all \\?+", low)
                or "replace all question marks" in low
            ),
            examples=(
                (("?zs",), "azs"),
                (("ubv?w",), "ubvaw"),
                (("j?qg??b",), "jaqgacb"),
            ),
        ),
        T(
            "max_repeating",
            "def max_repeating(sequence, word):\n"
            '    """Largest k with word*k as a substring (LeetCode 1668)."""\n'
            "    k = 0\n"
            "    block = word\n"
            "    while block and block in sequence:\n"
            "        k += 1\n"
            "        block += word\n"
            "    return k\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1668\b", low)
                or "maximum repeating substring" in low
            ),
            examples=(
                (("ababc", "ab"), 2),
                (("ababc", "ba"), 1),
                (("ababc", "ac"), 0),
            ),
        ),
        T(
            "is_strictly_palindromic",
            "def is_strictly_palindromic(n):\n"
            '    """True if n is palindromic in every base 2..n-2 (LeetCode 2396)."""\n'
            "    def pal(x, base):\n"
            "        digits = []\n"
            "        while x:\n"
            "            digits.append(x % base)\n"
            "            x //= base\n"
            "        return digits == digits[::-1]\n"
            "    return all(pal(n, base) for base in range(2, n - 1))\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2396\b", low)
                or "strictly palindromic" in low
            ),
            examples=(
                ((9,), False),
                ((4,), False),
            ),
        ),
    ]
