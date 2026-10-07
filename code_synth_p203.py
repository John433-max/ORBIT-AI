"""Cycle 487: newline normalize, consecutive groups, left pad, common suffix, sentence case, numeric string.

Matchers are phrase-specific so prefix/suffix strip, hex conversion, and
digit-count templates keep their asks.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "normalize_newlines",
            "def normalize_newlines(s):\n"
            '    """Convert CRLF and CR to LF."""\n'
            "    s = str(s)\n"
            "    return s.replace('\\r\\n', '\\n').replace('\\r', '\\n')\n",
            lambda low: "newline" in low and "string" in low and "normaliz" in low,
            (
                (("a\r\nb\rc",), "a\nb\nc"),
                (("plain",), "plain"),
                (("\r\n",), "\n"),
            ),
        ),
        T(
            "group_consecutive",
            "def group_consecutive(items):\n"
            '    """Split a list into runs of equal adjacent values."""\n'
            "    items = list(items)\n"
            "    if not items:\n"
            "        return []\n"
            "    groups = [[items[0]]]\n"
            "    for x in items[1:]:\n"
            "        if x == groups[-1][-1]:\n"
            "            groups[-1].append(x)\n"
            "        else:\n"
            "            groups.append([x])\n"
            "    return groups\n",
            lambda low: (
                "consecutive" in low
                and "group" in low
                and "drop" not in low
                and "diff" not in low
                and "character" not in low
            ),
            (
                (([1, 1, 2, 2, 2, 3],), [[1, 1], [2, 2, 2], [3]]),
                (([],), []),
                ((["a", "b", "b"],), [["a"], ["b", "b"]]),
            ),
        ),
        T(
            "pad_left",
            "def pad_left(s, width, fill=' '):\n"
            '    """Left-pad s to width with fill. Wider strings are unchanged."""\n'
            "    s, fill = str(s), str(fill or ' ')\n"
            "    width = int(width)\n"
            "    if len(s) >= width:\n"
            "        return s\n"
            "    return (fill * width + s)[-width:]\n",
            lambda low: bool(re.search(r"pad(?:s|ding)? a string on the left", low))
            and "right" not in low,
            (
                (("7", 3, "0"), "007"),
                (("abcd", 3, "0"), "abcd"),
                (("x", 4, "-"), "---x"),
            ),
        ),
        T(
            "common_suffix",
            "def common_suffix(words):\n"
            '    """Longest common suffix of strings. Empty input returns ''."""\n'
            "    words = [str(w) for w in words]\n"
            "    if not words:\n"
            "        return ''\n"
            "    rev = [w[::-1] for w in words]\n"
            "    pref = rev[0]\n"
            "    for w in rev[1:]:\n"
            "        i = 0\n"
            "        while i < len(pref) and i < len(w) and pref[i] == w[i]:\n"
            "            i += 1\n"
            "        pref = pref[:i]\n"
            "        if not pref:\n"
            "            break\n"
            "    return pref[::-1]\n",
            lambda low: "common suffix" in low and "prefix" not in low,
            (
                ((["running", "walking"],), "ing"),
                ((["abc", "xyz"],), ""),
                ((["tail"],), "tail"),
            ),
        ),
        T(
            "sentence_case",
            "def sentence_case(s):\n"
            '    """First character upper, the rest lower. Empty stays empty."""\n'
            "    s = str(s)\n"
            "    if not s:\n"
            "        return ''\n"
            "    return s[0].upper() + s[1:].lower()\n",
            lambda low: "sentence case" in low,
            (
                (("hello WORLD",), "Hello world"),
                (("",), ""),
                (("a",), "A"),
            ),
        ),
        T(
            "is_numeric",
            "def is_numeric(s):\n"
            '    """True if s is an int or float literal. Empty and nan are False."""\n'
            "    s = str(s).strip()\n"
            "    if not s or s.lower() in ('nan', 'inf', '-inf', '+inf'):\n"
            "        return False\n"
            "    try:\n"
            "        float(s)\n"
            "    except ValueError:\n"
            "        return False\n"
            "    return True\n",
            lambda low: "numeric" in low
            and "string" in low
            and "digit" not in low
            and "count" not in low
            and "convert" not in low,
            (
                (("42",), True),
                (("3.14",), True),
                (("abc",), False),
                (("",), False),
            ),
        ),
    ]
