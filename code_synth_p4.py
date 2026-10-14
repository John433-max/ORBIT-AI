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
            "integer_to_roman",
            "def integer_to_roman(num):\n"
            '    """Convert a positive integer to a Roman numeral."""\n'
            "    num = int(num)\n"
            "    vals = [\n"
            "        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),\n"
            "        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),\n"
            "        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'),\n"
            "    ]\n"
            "    out = []\n"
            "    for v, s in vals:\n"
            "        if num >= v:\n"
            "            k, num = divmod(num, v)\n"
            "            out.append(s * k)\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\binteger[_ ]to[_ ]roman\b|"
                    r"\bint(?:eger)?[_ ]to[_ ]roman\b|"
                    r"\bconvert(?:s|ing)? (?:an? )?integer to (?:a )?roman\b",
                    low,
                )
            )
            and "roman_to" not in low
            and "from roman" not in low,
            (((3,), "III"), ((58,), "LVIII"), ((1994,), "MCMXCIV")),
        ),
        T(
            "valid_palindrome_ii",
            "def valid_palindrome_ii(s):\n"
            '    """True if s is a palindrome after deleting at most one char."""\n'
            "    def ok(i, j):\n"
            "        while i < j:\n"
            "            if s[i] != s[j]:\n"
            "                return False\n"
            "            i += 1\n"
            "            j -= 1\n"
            "        return True\n"
            "    i, j = 0, len(s) - 1\n"
            "    while i < j:\n"
            "        if s[i] != s[j]:\n"
            "            return ok(i + 1, j) or ok(i, j - 1)\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bvalid[_ ]palindrome[_ ]ii\b|"
                    r"\bvalid palindrome ii\b|"
                    r"\bpalindrome.{0,20}delete one\b|"
                    r"\bdelete one character.{0,20}palindrome\b",
                    low,
                )
            ),
            ((("aba",), True), (("abca",), True), (("abc",), False)),
        ),
        T(
            "my_sqrt",
            "def my_sqrt(x):\n"
            '    """Integer square root of a non-negative integer (floor)."""\n'
            "    x = int(x)\n"
            "    if x < 2:\n"
            "        return x\n"
            "    lo, hi = 1, x // 2\n"
            "    ans = 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if mid * mid <= x:\n"
            "            ans = mid\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bmy_sqrt\b|"
                    r"\binteger[_ ]square[_ ]root\b|"
                    r"\bsqrt\b.{0,20}\binteger\b|"
                    r"\bfloor(?:ed)?[_ ]sqrt\b",
                    low,
                )
            )
            and "perfect" not in low,
            (((4,), 2), ((8,), 2), ((0,), 0)),
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
