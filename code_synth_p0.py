"""ORBIT code_synth basics pack (p0).

Covers the early unit tests (add/multiply/sort/gcd/…) that lettered and
numeric packs do not ship. Higher-numbered packs still win name collisions.
"""
from __future__ import annotations

import re

from code_synth import Template, _TWO


def templates():
    return [
        Template(
            "add",
            "def add(a, b):\n"
            '    """Return the sum of a and b."""\n'
            "    return a + b\n",
            lambda low: bool(
                re.search(r"\badd(?:s|ing)?\b.{0,24}\b" + _TWO, low)
                and "integer" not in low
                and "2235" not in low
            ),
            (((2, 3), 5), ((-1, 4), 3)),
        ),
        Template(
            "multiply",
            "def multiply(a, b):\n"
            '    """Return the product of a and b."""\n'
            "    return a * b\n",
            lambda low: bool(
                "dot" not in low
                and re.search(r"\bmultipl(?:y|ies|ied|ying)\b.{0,24}\b" + _TWO, low)
            ),
            (((2, 3), 6), ((-2, 4), -8)),
        ),
        Template(
            "subtract",
            "def subtract(a, b):\n"
            '    """Return a minus b."""\n'
            "    return a - b\n",
            lambda low: bool(re.search(r"\bsubtract(?:s|ing)?\b.{0,24}\b" + _TWO, low)),
            (((5, 3), 2), ((1, 4), -3)),
        ),
        Template(
            "divide",
            "def divide(a, b):\n"
            '    """Return a divided by b."""\n'
            "    return a / b\n",
            lambda low: bool(
                "division" not in low
                and re.search(r"\bdivid(?:e|es|ed|ing)\b.{0,24}\b" + _TWO, low)
            ),
            (((6, 2), 3.0), ((5, 2), 2.5)),
        ),
        Template(
            "average",
            "def average(a, b):\n"
            '    """Return the average of a and b."""\n'
            "    return (a + b) / 2\n",
            lambda low: bool(re.search(r"\baverage(?:s|d)?\b.{0,24}\b" + _TWO, low)),
            (((2, 4), 3.0), ((1, 2), 1.5)),
        ),
        Template(
            "absolute",
            "def absolute(n):\n"
            '    """Return the absolute value of n."""\n'
            "    return n if n >= 0 else -n\n",
            lambda low: bool(re.search(r"\babs(?:olute)?\b", low)),
            (((-3,), 3), ((4,), 4)),
        ),
        Template(
            "power",
            "def power(a, b):\n"
            '    """Return a raised to the power b."""\n'
            "    return a ** b\n",
            lambda low: bool(
                re.search(r"\b(power|raises?|exponent)\b", low)
                and "of two" not in low
                and "of four" not in low
            ),
            (((2, 3), 8), ((5, 0), 1)),
        ),
        Template(
            "maximum",
            "def maximum(a, b):\n"
            '    """Return the larger of a and b."""\n'
            "    return a if a >= b else b\n",
            lambda low: bool(
                "stack" not in low
                and re.search(r"\bmax(?:imum)?\b.{0,40}\b" + _TWO, low)
            ),
            (((2, 9), 9), ((-1, -8), -1)),
        ),
        Template(
            "reverse_string",
            "def reverse_string(s):\n"
            '    """Return a new string with characters reversed."""\n'
            "    return s[::-1]\n",
            lambda low: bool(
                re.search(r"\breverse(?:s|d|ing)?\b.{0,20}\bstring\b", low)
                and "vowel" not in low
            ),
            ((("ab",), "ba"), (("x",), "x")),
        ),
        Template(
            "factorial",
            "def factorial(n):\n"
            '    """Return n! for a non-negative integer n."""\n'
            "    out = 1\n"
            "    for i in range(2, int(n) + 1):\n"
            "        out *= i\n"
            "    return out\n",
            lambda low: bool(re.search(r"\bfactorial\b", low)),
            (((5,), 120), ((0,), 1)),
        ),
        Template(
            "sort_list",
            "def sort_list(items):\n"
            '    """Return a new sorted list."""\n'
            "    return sorted(items)\n",
            lambda low: bool(
                "dutch" not in low
                and "0-1-2" not in low
                and "colors" not in low
                and re.search(r"\bsort(?:s|ed|ing)?\b.{0,24}\b(list|array|items)\b", low)
            ),
            ((([3, 1, 2],), [1, 2, 3]),),
        ),
        Template(
            "is_palindrome",
            "def is_palindrome(s):\n"
            '    """Return True if s reads the same forwards and backwards."""\n'
            "    t = str(s)\n"
            "    return t == t[::-1]\n",
            lambda low: bool(
                "linked" not in low
                and re.search(r"\bpalindrome\b", low)
            ),
            ((("aba",), True), (("ab",), False)),
        ),
        Template(
            "is_even",
            "def is_even(n):\n"
            '    """Return True if n is even."""\n'
            "    return n % 2 == 0\n",
            lambda low: bool(re.search(r"\beven\b", low) and "odd" not in low),
            (((4,), True), ((3,), False)),
        ),
        Template(
            "gcd",
            "def gcd(a, b):\n"
            '    """Return the greatest common divisor of a and b."""\n'
            "    a, b = abs(int(a)), abs(int(b))\n"
            "    while b:\n"
            "        a, b = b, a % b\n"
            "    return a\n",
            lambda low: bool(re.search(r"\bgcd\b|\bgreatest common divisor\b", low)),
            (((12, 8), 4), ((7, 3), 1)),
        ),
        Template(
            "fibonacci",
            "def fibonacci(n):\n"
            '    """Return the nth Fibonacci number (0-indexed)."""\n'
            "    a, b = 0, 1\n"
            "    for _ in range(int(n)):\n"
            "        a, b = b, a + b\n"
            "    return a\n",
            lambda low: bool(re.search(r"\bfibonacci\b", low)),
            (((0,), 0), ((6,), 8)),
        ),
        Template(
            "count_vowels",
            "def count_vowels(s):\n"
            '    """Return the number of vowels in s."""\n'
            "    return sum(1 for c in str(s).lower() if c in 'aeiou')\n",
            lambda low: bool(re.search(r"\bvowel", low)),
            ((("hello",), 2), (("xyz",), 0)),
        ),
        Template(
            "unique",
            "def unique(items):\n"
            '    """Return unique items, preserving first-seen order."""\n'
            "    seen = set()\n"
            "    out = []\n"
            "    for x in items:\n"
            "        if x not in seen:\n"
            "            seen.add(x)\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bunique\b.{0,24}\b(items|list|array)\b", low)
                or re.search(r"\breturns? unique\b", low)
            ),
            ((([1, 1, 2],), [1, 2]),),
        ),
        Template(
            "is_odd",
            "def is_odd(n):\n"
            '    """Return True if n is odd."""\n'
            "    return n % 2 != 0\n",
            lambda low: bool(re.search(r"\bodd\b", low) and "even" not in low),
            (((3,), True), ((4,), False)),
        ),
        Template(
            "sum_list",
            "def sum_list(items):\n"
            '    """Return the sum of numbers in items."""\n'
            "    return sum(items)\n",
            lambda low: bool(re.search(r"\bsum(?:s|ming)?\b.{0,24}\b(list|numbers|items)\b", low)),
            ((([1, 2, 3],), 6),),
        ),
        Template(
            "lcm",
            "def lcm(a, b):\n"
            '    """Return the least common multiple of a and b."""\n'
            "    a, b = abs(int(a)), abs(int(b))\n"
            "    if a == 0 or b == 0:\n"
            "        return 0\n"
            "    return a // gcd(a, b) * b\n"
            "\n"
            "def gcd(a, b):\n"
            "    a, b = abs(int(a)), abs(int(b))\n"
            "    while b:\n"
            "        a, b = b, a % b\n"
            "    return a\n",
            lambda low: bool(re.search(r"\blcm\b|\bleast common multiple\b", low)),
            (((4, 6), 12), ((3, 5), 15)),
        ),
        Template(
            "flatten",
            "def flatten(items):\n"
            '    """Flatten one level of nesting."""\n'
            "    out = []\n"
            "    for x in items:\n"
            "        if isinstance(x, (list, tuple)):\n"
            "            out.extend(x)\n"
            "        else:\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: bool(re.search(r"\bflatten(?:s|ed|ing)?\b", low)),
            ((([[1, 2], [3]],), [1, 2, 3]),),
        ),
        Template(
            "count_words",
            "def count_words(s):\n"
            '    """Return the number of whitespace-separated words."""\n'
            "    return len(str(s).split())\n",
            lambda low: bool(re.search(r"\bcount(?:s|ing)?\b.{0,16}\bwords\b", low)),
            ((("a b c",), 3),),
        ),
        Template(
            "clamp",
            "def clamp(n, lo, hi):\n"
            '    """Clamp n to the inclusive range [lo, hi]."""\n'
            "    return lo if n < lo else hi if n > hi else n\n",
            lambda low: bool(re.search(r"\bclamp(?:s|ed|ing)?\b", low)),
            (((5, 0, 3), 3), ((1, 0, 3), 1)),
        ),
        Template(
            "is_prime",
            "def is_prime(n):\n"
            '    """Return True if n is a prime number."""\n'
            "    n = int(n)\n"
            "    if n < 2:\n"
            "        return False\n"
            "    if n % 2 == 0:\n"
            "        return n == 2\n"
            "    d = 3\n"
            "    while d * d <= n:\n"
            "        if n % d == 0:\n"
            "            return False\n"
            "        d += 2\n"
            "    return True\n",
            lambda low: bool(re.search(r"\bprime\b", low) and "count" not in low),
            (((2,), True), ((9,), False), ((1,), False)),
        ),
        Template(
            "median",
            "def median(items):\n"
            '    """Return the median of a list of numbers."""\n'
            "    xs = sorted(items)\n"
            "    n = len(xs)\n"
            "    if n == 0:\n"
            "        raise ValueError('empty')\n"
            "    mid = n // 2\n"
            "    if n % 2:\n"
            "        return xs[mid]\n"
            "    return (xs[mid - 1] + xs[mid]) / 2\n",
            lambda low: bool(re.search(r"\bmedian\b", low)),
            ((([1, 3, 2],), 2), (([1, 2, 3, 4],), 2.5)),
        ),
        Template(
            "title_case",
            "def title_case(s):\n"
            '    """Return s in title case."""\n'
            "    return str(s).title()\n",
            lambda low: bool(re.search(r"\btitle[- ]?case", low)),
            ((("hello world",), "Hello World"),),
        ),
        Template(
            "count_occurrences",
            "def count_occurrences(items, value):\n"
            '    """Return how many times value appears in items."""\n'
            "    return sum(1 for x in items if x == value)\n",
            lambda low: bool(re.search(r"\bcount(?:s|ing)?\b.{0,24}\boccurrences\b", low)),
            ((([1, 2, 1], 1), 2),),
        ),
        Template(
            "is_leap_year",
            "def is_leap_year(year):\n"
            '    """Return True if year is a leap year."""\n'
            "    y = int(year)\n"
            "    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)\n",
            lambda low: bool(re.search(r"\bleap[- ]?year\b", low)),
            (((2000,), True), ((1900,), False), ((2024,), True)),
        ),
        Template(
            "fizzbuzz",
            "def fizzbuzz(n):\n"
            '    """Return fizzbuzz labels for 1..n."""\n'
            "    out = []\n"
            "    for i in range(1, int(n) + 1):\n"
            "        if i % 15 == 0:\n"
            "            out.append('fizzbuzz')\n"
            "        elif i % 3 == 0:\n"
            "            out.append('fizz')\n"
            "        elif i % 5 == 0:\n"
            "            out.append('buzz')\n"
            "        else:\n"
            "            out.append(str(i))\n"
            "    return out\n",
            lambda low: bool(re.search(r"\bfizzbuzz\b", low)),
            (((5,), ["1", "2", "fizz", "4", "buzz"]),),
        ),
    ]
