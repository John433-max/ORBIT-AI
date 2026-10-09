"""Cycle 525: take-n, drop-last, factors, letters-only, trim, and pair-split asks.

These returned NotImplemented drafts or were stolen by first_element / last_n.
This pack loads before p209/p4 so the more specific phrases win.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "take_n",
            "def take_n(items, n):\n"
            '    """Return the first n items. n <= 0 yields an empty list."""\n'
            "    n = int(n)\n"
            "    if n <= 0:\n"
            "        return []\n"
            "    return list(items)[:n]\n",
            lambda low: bool(
                re.search(r"\bfirst n\b|\btake(?:s| the)? first n\b", low)
            )
            and "missing" not in low
            and "positive" not in low
            and "linked" not in low,
            (
                (([1, 2, 3, 4], 2), [1, 2]),
                (([1, 2], 5), [1, 2]),
                (([1, 2], 0), []),
            ),
        ),
        T(
            "drop_last",
            "def drop_last(items, n=1):\n"
            '    """Drop the last n items (default 1). n <= 0 returns a copy."""\n'
            "    items = list(items)\n"
            "    n = int(n)\n"
            "    if n <= 0:\n"
            "        return items\n"
            "    if n >= len(items):\n"
            "        return []\n"
            "    return items[:-n]\n",
            # "drops the last n elements" means remove, not keep (last_n).
            lambda low: (
                "linked" not in low
                and "first" not in low
                and bool(
                    re.search(
                        r"\bdrop(?:s|ping)?(?: the)? last(?:\s+n)?(?:\s+(?:element|item|elements|items))?\b"
                        r"|\bdrop last\b"
                        r"|\bwithout the last\b",
                        low,
                    )
                )
            ),
            (
                (([1, 2, 3, 4], 2), [1, 2]),
                (([1, 2], 5), []),
                (([1, 2], 0), [1, 2]),
            ),
        ),
        T(
            "factors",
            "def factors(n):\n"
            '    """Positive divisors of n, sorted. Zero has no positive divisors here."""\n'
            "    n = abs(int(n))\n"
            "    if n == 0:\n"
            "        return []\n"
            "    out = []\n"
            "    i = 1\n"
            "    while i * i <= n:\n"
            "        if n % i == 0:\n"
            "            out.append(i)\n"
            "            if i != n // i:\n"
            "                out.append(n // i)\n"
            "        i += 1\n"
            "    return sorted(out)\n",
            lambda low: bool(re.search(r"\bfactors\b|\bdivisors\b", low))
            and "prime" not in low
            and "scale" not in low
            and "load" not in low,
            (((12,), [1, 2, 3, 4, 6, 12]), ((7,), [1, 7])),
        ),
        T(
            "is_letters",
            "def is_letters(s):\n"
            '    """True if s is non-empty and every character is a letter."""\n'
            "    s = str(s)\n"
            "    return bool(s) and s.isalpha()\n",
            lambda low: bool(re.search(r"\bonly letters\b|\ball letters\b|\bis[_ ]letters\b", low)),
            ((("abc",), True), (("ab1",), False), (("",), False)),
        ),
        T(
            "trim_string",
            "def trim_string(s):\n"
            '    """Strip leading and trailing whitespace."""\n'
            "    return str(s).strip()\n",
            lambda low: bool(re.search(r"\btrim(?:s|ming)? (?:a )?string\b|\bstrip whitespace\b", low)),
            ((("  hi  ",), "hi"),),
        ),
        T(
            "split_pair_lists",
            "def split_pair_lists(pairs):\n"
            '    """Split a list of pairs into two parallel lists."""\n'
            "    a, b = [], []\n"
            "    for x, y in pairs:\n"
            "        a.append(x)\n"
            "        b.append(y)\n"
            "    return a, b\n",
            lambda low: bool(re.search(r"\bsplit pairs\b|\bunzip pairs\b|\bpair.?lists\b", low)),
            ((((1, 2), (3, 4)), ([1, 3], [2, 4])),),
        ),
    ]
