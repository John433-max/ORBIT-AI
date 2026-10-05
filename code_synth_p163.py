"""Cycle 445: Luhn, Atbash, pig Latin, ISBN-10, Soundex, seconds-to-HMS.

Everyday asks with no template. Matchers are phrase-gated so Caesar/rot13,
title-case, and generic digit-sum keep their names. Pack loads before p162.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "luhn_valid",
            "def luhn_valid(s):\n"
            '    """True if digits pass the Luhn mod-10 check (ISO/IEC 7812-1)."""\n'
            "    digits = [int(ch) for ch in str(s) if ch.isdigit()]\n"
            "    if len(digits) < 2:\n"
            "        return False\n"
            "    total = 0\n"
            "    for i, d in enumerate(reversed(digits)):\n"
            "        if i % 2 == 1:\n"
            "            d *= 2\n"
            "            if d > 9:\n"
            "                d -= 9\n"
            "        total += d\n"
            "    return total % 10 == 0\n",
            lambda low: "luhn" in low and "isbn" not in low,
            ((("79927398713",), True), (("79927398714",), False), (("1",), False)),
        ),
        T(
            "atbash",
            "def atbash(s):\n"
            '    """Reverse-alphabet cipher; case kept, non-letters unchanged."""\n'
            "    out = []\n"
            "    for ch in str(s):\n"
            "        if 'A' <= ch <= 'Z':\n"
            "            out.append(chr(ord('Z') - (ord(ch) - ord('A'))))\n"
            "        elif 'a' <= ch <= 'z':\n"
            "            out.append(chr(ord('z') - (ord(ch) - ord('a'))))\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n",
            lambda low: "atbash" in low and "caesar" not in low and "rot13" not in low,
            ((("Abc!",), "Zyx!"), (("wizard",), "draziw")),
        ),
        T(
            "pig_latin",
            "def pig_latin(s):\n"
            '    """Move leading consonants and add ay; vowel words get way."""\n'
            "    words = str(s).split()\n"
            "    vowels = set('aeiouAEIOU')\n"
            "    out = []\n"
            "    for word in words:\n"
            "        if not word:\n"
            "            continue\n"
            "        if word[0] in vowels:\n"
            "            out.append(word + 'way')\n"
            "            continue\n"
            "        i = 0\n"
            "        while i < len(word) and word[i] not in vowels:\n"
            "            i += 1\n"
            "        if i == 0 or i == len(word):\n"
            "            out.append(word + 'ay')\n"
            "        else:\n"
            "            out.append(word[i:] + word[:i] + 'ay')\n"
            "    return ' '.join(out)\n",
            lambda low: "pig" in low and "latin" in low,
            ((("apple",), "appleway"), (("string",), "ingstray"), (("hello world",), "ellohay orldway")),
        ),
        T(
            "isbn10_valid",
            "def isbn10_valid(s):\n"
            '    """True if 10 symbols pass the ISBN-10 mod-11 check (X = 10)."""\n'
            "    chars = [ch for ch in str(s).upper() if ch.isdigit() or ch == 'X']\n"
            "    if len(chars) != 10:\n"
            "        return False\n"
            "    if 'X' in chars[:-1]:\n"
            "        return False\n"
            "    total = 0\n"
            "    for i, ch in enumerate(chars):\n"
            "        val = 10 if ch == 'X' else int(ch)\n"
            "        total += (10 - i) * val\n"
            "    return total % 11 == 0\n",
            lambda low: "isbn" in low and "13" not in low and "luhn" not in low,
            ((("0-306-40615-2",), True), (("0-306-40615-3",), False), (("123",), False)),
        ),
        T(
            "soundex",
            "def soundex(name):\n"
            '    """American Soundex (NARA): letter plus three digits, zero-padded."""\n'
            "    s = ''.join(ch for ch in str(name).upper() if 'A' <= ch <= 'Z')\n"
            "    if not s:\n"
            "        return ''\n"
            "    codes = {\n"
            "        'B': '1', 'F': '1', 'P': '1', 'V': '1',\n"
            "        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',\n"
            "        'D': '3', 'T': '3',\n"
            "        'L': '4',\n"
            "        'M': '5', 'N': '5',\n"
            "        'R': '6',\n"
            "    }\n"
            "    out = [s[0]]\n"
            "    prev = codes.get(s[0], '')\n"
            "    for ch in s[1:]:\n"
            "        code = codes.get(ch, '')\n"
            "        if code and code != prev:\n"
            "            out.append(code)\n"
            "        if ch not in 'HW':\n"
            "            prev = code\n"
            "        if len(out) == 4:\n"
            "            break\n"
            "    return (''.join(out) + '000')[:4]\n",
            lambda low: "soundex" in low,
            ((("Robert",), "R163"), (("Ashcraft",), "A261"), (("",), "")),
        ),
        T(
            "seconds_to_hms",
            "def seconds_to_hms(n):\n"
            '    """Format a non-negative second count as H:MM:SS."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        n = 0\n"
            "    h, rem = divmod(n, 3600)\n"
            "    m, s = divmod(rem, 60)\n"
            "    return f'{h}:{m:02d}:{s:02d}'\n",
            lambda low: (
                ("hms" in low or ("seconds" in low and ("h:mm:ss" in low or "hh:mm:ss" in low or "hours minutes" in low)))
                and "to seconds" not in low
                and "into seconds" not in low
                and "parse" not in low
            ),
            (((3661,), "1:01:01"), ((0,), "0:00:00"), ((-5,), "0:00:00")),
        ),
    ]
