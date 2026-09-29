"""Cycle 267: additional verified Python templates (pack 10)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "unique_email_addresses",
            "def unique_email_addresses(emails):\n"
            '    """Count unique addresses after +local ignore and . collapse."""\n'
            "    seen = set()\n"
            "    for raw in emails:\n"
            "        addr = str(raw).strip()\n"
            "        if '@' not in addr:\n"
            "            continue\n"
            "        local, domain = addr.split('@', 1)\n"
            "        local = local.split('+', 1)[0].replace('.', '')\n"
            "        seen.add(local.lower() + '@' + domain.lower())\n"
            "    return len(seen)\n",
            lambda low: bool(
                re.search(
                    r"\bunique email(?: address(?:es)?)?\b|"
                    r"\bunique_email_addresses\b|"
                    r"\bnum unique emails\b|"
                    r"\bcount unique emails?\b",
                    low,
                )
            )
            and "morse" not in low,
            (
                ([["test.email+alex@leetcode.com", "test.e.mail+bob.cathy@leetcode.com", "testemail+david@lee.tcode.com"]], 2),
                ([["a@leetcode.com", "b@leetcode.com", "c@leetcode.com"]], 3),
            ),
        ),
        T(
            "to_lower_case",
            "def to_lower_case(s):\n"
            '    """Return s with ASCII letters converted to lowercase."""\n'
            "    out = []\n"
            "    for ch in str(s):\n"
            "        o = ord(ch)\n"
            "        if 65 <= o <= 90:\n"
            "            out.append(chr(o + 32))\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\bto lower case\b|"
                    r"\bto_lower_case\b|"
                    r"\bconvert(?: a string)? to lowercase\b|"
                    r"\bimplement toLowerCase\b",
                    low,
                )
            )
            and "title" not in low
            and "vowel" not in low,
            ((("Hello",), "hello"), (("here",), "here"), (("LOVELY",), "lovely")),
        ),
        T(
            "sort_array_by_parity",
            "def sort_array_by_parity(nums):\n"
            '    """Even integers first, then odds; relative order otherwise free."""\n'
            "    evens = [int(x) for x in nums if int(x) % 2 == 0]\n"
            "    odds = [int(x) for x in nums if int(x) % 2 != 0]\n"
            "    return evens + odds\n",
            lambda low: bool(
                re.search(
                    r"\bsort array by parity\b|"
                    r"\bsort_array_by_parity\b|"
                    r"\bevens? (?:first|before odds)\b|"
                    r"\bparity sort\b",
                    low,
                )
            )
            and "color" not in low
            and " ii" not in low
            and "_ii" not in low
            and "even indices" not in low
            and "even indexes" not in low,
            (([[3, 1, 2, 4]], [2, 4, 3, 1]), ([[0]], [0])),
        ),
        T(
            "height_checker",
            "def height_checker(heights):\n"
            '    """Count students not standing at the expected sorted height."""\n'
            "    expected = sorted(int(h) for h in heights)\n"
            "    return sum(1 for a, b in zip(heights, expected) if int(a) != b)\n",
            lambda low: bool(
                re.search(
                    r"\bheight checker\b|"
                    r"\bheight_checker\b|"
                    r"\bstudents? (?:in )?(?:wrong|expected) (?:height|order)\b",
                    low,
                )
            ),
            (([[1, 1, 4, 2, 1, 3]], 3), ([[5, 1, 2, 3, 4]], 5), ([[1, 2, 3, 4, 5]], 0)),
        ),
        T(
            "shortest_to_char",
            "def shortest_to_char(s, c):\n"
            '    """Distance from each index in s to the nearest occurrence of c."""\n'
            "    s = str(s)\n"
            "    c = str(c)[0] if c else ''\n"
            "    n = len(s)\n"
            "    ans = [n] * n\n"
            "    prev = -n\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch == c:\n"
            "            prev = i\n"
            "        ans[i] = i - prev\n"
            "    prev = 2 * n\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        if s[i] == c:\n"
            "            prev = i\n"
            "        ans[i] = min(ans[i], prev - i)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bshortest (?:distance )?to (?:a )?char\b|"
                    r"\bshortest_to_char\b|"
                    r"\bshortest distance to character\b|"
                    r"\bnearest occurrence of (?:a )?character\b",
                    low,
                )
            ),
            ((("loveleetcode", "e"), [3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0]), (("aaab", "b"), [3, 2, 1, 0])),
        ),
        T(
            "flip_and_invert_image",
            "def flip_and_invert_image(image):\n"
            '    """Horizontally flip each row then invert 0/1 bits."""\n'
            "    out = []\n"
            "    for row in image:\n"
            "        flipped = list(row)[::-1]\n"
            "        out.append([1 - int(v) for v in flipped])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bflip and invert(?: image)?\b|"
                    r"\bflip_and_invert_image\b|"
                    r"\binvert(?: a)? flipped image\b|"
                    r"\bflipping an image\b",
                    low,
                )
            )
            and "rotate" not in low,
            (
                ([[[1, 1, 0], [1, 0, 1], [0, 0, 0]]], [[1, 0, 0], [0, 1, 0], [1, 1, 1]]),
                ([[[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]]], [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [1, 0, 1, 0]]),
            ),
        ),
    ]
