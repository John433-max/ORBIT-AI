"""Cycle expand: additional verified Python templates (pack 4)."""

from __future__ import annotations

import re
from code_synth import Template as T


def templates():
    return [
        T(
            "last_n",
            "def last_n(items, n):\n"
            '    """Return the last n items (n clamped to length)."""\n'
            "    n = max(0, int(n))\n"
            "    return list(items)[-n:] if n else []\n",
            lambda low: bool(
                re.search(
                    r"\blast n\b|\blast[_ ]n[_ ](?:items|elements)\b|"
                    r"\btakes? the last n\b|\breturns? the last n\b|"
                    r"\blast[_ ]n\b",
                    low,
                )
            )
            and "drop" not in low
            and "remove" not in low,
            ((([1, 2, 3, 4, 5], 2), [4, 5]),),
        ),
        T(
            "clamp_list",
            "def clamp_list(items, lo, hi):\n"
            '    """Clamp each value into [lo, hi]."""\n'
            "    return [lo if x < lo else hi if x > hi else x for x in items]\n",
            lambda low: bool(re.search(r"\bclamp (list|array|values)\b", low)),
            ((([0, 5, 10], 1, 8), [1, 5, 8]),),
        ),
        T(
            "count_bits",
            "def count_bits(n):\n"
            '    """Number of set bits in non-negative integer n."""\n'
            "    n = int(n)\n"
            "    if n < 0:\n"
            "        raise ValueError('n must be >= 0')\n"
            "    return bin(n).count('1')\n",
            lambda low: bool(
                re.search(r"\b(count bits|counting bits|hamming weight|set bits|popcount)\b", low)
            ),
            (((7,), 3), ((0,), 0)),
        ),
        T(
            "reverse_vowels",
            "def reverse_vowels(s):\n"
            '    """Reverse only the vowels in s; keep other characters."""\n'
            "    vowels = set('aeiouAEIOU')\n"
            "    chars = list(s)\n"
            "    i, j = 0, len(chars) - 1\n"
            "    while i < j:\n"
            "        while i < j and chars[i] not in vowels:\n"
            "            i += 1\n"
            "        while i < j and chars[j] not in vowels:\n"
            "            j -= 1\n"
            "        chars[i], chars[j] = chars[j], chars[i]\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return ''.join(chars)\n",
            lambda low: bool(re.search(r"\breverse(?:s|d|ing)?\b.{0,24}\bvowels?\b|\bvowels?\b.{0,20}\breverse", low)),
            ((("hello",), "holle"), (("leetcode",), "leotcede")),
        ),
        T(
            "count_primes",
            "def count_primes(n):\n"
            '    """Count primes strictly less than n (sieve)."""\n'
            "    n = int(n)\n"
            "    if n <= 2:\n"
            "        return 0\n"
            "    sieve = [True] * n\n"
            "    sieve[0] = sieve[1] = False\n"
            "    p = 2\n"
            "    while p * p < n:\n"
            "        if sieve[p]:\n"
            "            step = p\n"
            "            start = p * p\n"
            "            sieve[start:n:step] = [False] * (((n - 1 - start) // step) + 1)\n"
            "        p += 1\n"
            "    return sum(sieve)\n",
            lambda low: bool(
                re.search(r"\bcount(?:s|ing)? primes?\b|\bnumber of primes\b|\bsieve of eratosthenes\b|\bcount_primes\b", low)
            ),
            (((10,), 4), ((0,), 0), ((2,), 0)),
        ),
        T(
            "detect_capital",
            "def detect_capital(word):\n"
            '    """True if capitalization is all-caps, all-lower, or Title."""\n'
            "    w = str(word)\n"
            "    return w.isupper() or w.islower() or w.istitle()\n",
            lambda low: bool(
                re.search(r"\bdetect[_ ]capital\b|\bdetect capital(?:ization)?\b|\bvalid capital(?:ization)?\b", low)
            ),
            ((("USA",), True), (("FlaG",), False), (("Google",), True)),
        ),
        T(
            "rotate_string",
            "def rotate_string(s, k):\n"
            '    """Rotate string left by k positions."""\n'
            "    s = str(s)\n"
            "    if not s:\n"
            "        return s\n"
            "    k = int(k) % len(s)\n"
            "    return s[k:] + s[:k]\n",
            lambda low: bool(
                re.search(
                    r"\brotate string\b|\bstring rotation\b|"
                    r"rotat(?:e|es|ing) (?:a |the )?string (?:left|right)",
                    low,
                )
            )
            and "matrix" not in low
            and "image" not in low
            and "list" not in low,
            ((("abcde", 2), "cdeab"),),
        ),
    ]
