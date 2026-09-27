"""ORBIT code_synth template pack p1 (CI / GitHub)."""
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
                "binary" not in low
                and "linked" not in low
                and "list" not in low
                and (
                    re.search(r"add(s|ing)?\b.{0,24}\b" + _TWO + r"\b.{0,24}\b(number|int|value)", low)
                    or "adds two" in low
                )
            ),
            (((1, 2), 3), ((-4, 10), 6)),
        ),
        Template(
            "multiply",
            "def multiply(a, b):\n"
            '    """Return the product of a and b."""\n'
            "    return a * b\n",
            lambda low: bool(
                "dot" not in low
                and "inner product" not in low
                and re.search(
                    r"\b(multipl(?:y|ies|ied|ying)|product of)\b.{0,40}\b" + _TWO + r"\b",
                    low,
                )
            ),
            (((3, 4), 12), ((-2, 5), -10)),
        ),
        Template(
            "subtract",
            "def subtract(a, b):\n"
            '    """Return a minus b."""\n'
            "    return a - b\n",
            lambda low: bool(
                re.search(
                    r"\b(subtract(?:s|ing)?|minus)\b.{0,40}\b" + _TWO
                    + r"|"
                    + r"\bdifference (of|between)\b.{0,24}\b" + _TWO
                    + r"\b.{0,16}\b(number|int|value|float)",
                    low,
                )
                and "list" not in low
                and "array" not in low
                and "set" not in low
            ),
            (((9, 4), 5), ((0, 3), -3)),
        ),
        Template(
            "maximum",
            "def maximum(a, b):\n"
            '    """Return the larger of a and b."""\n'
            "    return a if a >= b else b\n",
            lambda low: bool(re.search(r"\b(max(?:imum)?|larger|greater)\b.{0,40}\b" + _TWO, low)),
            (((2, 9), 9), ((-1, -8), -1)),
        ),
        Template(
            "reverse_string",
            "def reverse_string(s):\n"
            '    """Return s reversed."""\n'
            "    return s[::-1]\n",
            lambda low: bool(
                re.search(r"\breverse\b.{0,40}\b(string|str|text)\b|\b(string|str|text)\b.{0,20}\breverse", low)
                and "word" not in low
            ),
            ((("ab",), "ba"), (("Orbit",), "tibrO")),
        ),
        Template(
            "factorial",
            "def factorial(n):\n"
            '    """Return n! for n >= 0."""\n'
            "    if n < 0:\n"
            "        raise ValueError('n must be >= 0')\n"
            "    out = 1\n"
            "    for i in range(2, n + 1):\n"
            "        out *= i\n"
            "    return out\n",
            lambda low: "factorial" in low,
            (((0,), 1), ((5,), 120)),
        ),
        Template(
            "divide",
            "def divide(a, b):\n"
            '    """Return a / b. Raises ZeroDivisionError if b is 0."""\n'
            "    return a / b\n",
            lambda low: bool(re.search(r"\b(divid(?:e|es|ing)|quotient of)\b.{0,40}\b" + _TWO, low)),
            (((10, 4), 2.5), ((9, 3), 3.0)),
        ),
        Template(
            "average",
            "def average(a, b):\n"
            '    """Return the arithmetic mean of a and b."""\n'
            "    return (a + b) / 2\n",
            lambda low: bool(re.search(r"\b(averag(?:e|es|ing)|mean)\b.{0,40}\b(two|2|list|numbers)\b", low)),
            (((2, 4), 3.0), ((0, 5), 2.5)),
        ),
        Template(
            "absolute",
            "def absolute(n):\n"
            '    """Return the absolute value of n."""\n'
            "    return n if n >= 0 else -n\n",
            lambda low: bool(re.search(r"absolute value|\babs\b", low)),
            (((-3,), 3), ((4,), 4)),
        ),
        Template(
            "power",
            "def power(base, exp):\n"
            '    """Return base raised to exp."""\n'
            "    return base ** exp\n",
            lambda low: bool(
                "power of two" not in low
                and "power of 2" not in low
                and "power-of-two" not in low
                and re.search(r"\b(power|exponent|raise .+ to)\b", low)
            ),
            (((2, 10), 1024), ((3, 0), 1)),
        ),
        Template(
            "sort_list",
            "def sort_list(items):\n"
            '    """Return a new list with items in ascending order."""\n'
            "    return sorted(items)\n",
            lambda low: (
                "binary" not in low
                and "linked" not in low
                and bool(re.search(r"\b(sort(?:s|ing)?|sort a|sort the)\b.{0,40}\b(list|array|numbers|items)\b", low))
                and "color" not in low
                and "dutch" not in low
                and not re.search(r"\bsorted\b", low)
            ),
            ((([3, 1, 2],), [1, 2, 3]),),
        ),
        Template(
            "is_palindrome",
            "def is_palindrome(s):\n"
            '    """Return True if s reads the same forwards and backwards."""\n'
            "    t = ''.join(ch.lower() for ch in str(s) if ch.isalnum())\n"
            "    return t == t[::-1]\n",
            lambda low: bool(
                "palindrome" in low
                and "longest" not in low
                and "linked" not in low
                and "list" not in low
            ),
            ((("Racecar",), True), (("orbit",), False)),
        ),
        Template(
            "is_even",
            "def is_even(n):\n"
            '    """Return True if n is even."""\n'
            "    return n % 2 == 0\n",
            lambda low: bool(
                re.search(r"\b(even|is_even|even number)\b", low)
                and "odd" not in low
                and "linked" not in low
            ),
            (((4,), True), ((7,), False)),
        ),
        Template(
            "gcd",
            "def gcd(a, b):\n"
            '    """Return the greatest common divisor of a and b."""\n'
            "    a, b = abs(int(a)), abs(int(b))\n"
            "    while b:\n"
            "        a, b = b, a % b\n"
            "    return a\n",
            lambda low: bool(re.search(r"\b(gcd|greatest common divisor|hcf)\b", low)),
            (((48, 18), 6), ((7, 13), 1)),
        ),
        Template(
            "fibonacci",
            "def fibonacci(n):\n"
            '    """Return the n-th Fibonacci number (F(0)=0, F(1)=1)."""\n'
            "    if n < 0:\n"
            "        raise ValueError('n must be >= 0')\n"
            "    a, b = 0, 1\n"
            "    for _ in range(n):\n"
            "        a, b = b, a + b\n"
            "    return a\n",
            lambda low: bool(re.search(r"\bfibonacci\b|\bfib\b", low)),
            (((0,), 0), ((10,), 55)),
        ),
        Template(
            "count_vowels",
            "def count_vowels(s):\n"
            '    """Return the number of English vowels in s."""\n'
            "    return sum(1 for ch in str(s).lower() if ch in 'aeiou')\n",
            lambda low: bool(re.search(r"\bcount(?:s|ing)?\b.{0,32}\bvowels?\b|\bnumber of vowels\b", low)),
            ((("Orbit AI",), 4), (("xyz",), 0)),
        ),
        Template(
            "unique",
            "def unique(items):\n"
            '    """Return items with duplicates removed, first-seen order kept."""\n'
            "    seen = set()\n"
            "    out = []\n"
            "    for x in items:\n"
            "        if x not in seen:\n"
            "            seen.add(x)\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: bool(re.search(r"\b(unique|dedup)\b.{0,24}\b(list|array|items)\b", low)),
            ((([1, 2, 1, 3],), [1, 2, 3]),),
        ),
        Template(
            "is_odd",
            "def is_odd(n):\n"
            '    """Return True if n is odd."""\n'
            "    return n % 2 != 0\n",
            lambda low: bool(
                re.search(r"\b(odd|is_odd|odd number)\b", low)
                and "even" not in low
                and "linked" not in low
            ),
            (((3,), True), ((8,), False)),
        ),
        Template(
            "sum_list",
            "def sum_list(items):\n"
            '    """Return the sum of items."""\n'
            "    total = 0\n"
            "    for x in items:\n"
            "        total += x\n"
            "    return total\n",
            lambda low: bool(
                "running" not in low
                and re.search(
                    r"\b(sum(?:s|ming)?|total)\b.{0,32}\b(list|array|items|numbers)\b|"
                    r"\b(list|array|items|numbers)\b.{0,24}\bsum\b",
                    low,
                )
            ),
            ((([1, 2, 3],), 6), (([],), 0)),
        ),
        Template(
            "lcm",
            "def lcm(a, b):\n"
            '    """Return the least common multiple of a and b."""\n'
            "    a, b = abs(int(a)), abs(int(b))\n"
            "    if a == 0 or b == 0:\n"
            "        return 0\n"
            "    x, y = a, b\n"
            "    while y:\n"
            "        x, y = y, x % y\n"
            "    return a // x * b\n",
            lambda low: bool(re.search(r"\b(lcm|least common multiple)\b", low)),
            (((4, 6), 12), ((0, 5), 0)),
        ),
        Template(
            "flatten",
            "def flatten(items):\n"
            '    """Flatten one level of nested lists."""\n'
            "    out = []\n"
            "    for x in items:\n"
            "        if isinstance(x, (list, tuple)):\n"
            "            out.extend(x)\n"
            "        else:\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bflatten(?:s|ed|ing)?\b.{0,40}\b(list|array|nested)\b|\bnested\b.{0,24}\bflatten", low)
                and "linked" not in low
            ),
            ((([1, [2, 3], 4],), [1, 2, 3, 4]), (([],), [])),
        ),
        Template(
            "count_words",
            "def count_words(s):\n"
            '    """Return the number of whitespace-separated words in s."""\n'
            "    return len(str(s).split())\n",
            lambda low: bool(re.search(r"\bcount(?:s|ing)?\b.{0,32}\bwords?\b|\bnumber of words\b|\bword count\b", low)),
            ((("hello world",), 2), (("  ",), 0)),
        ),
        Template(
            "clamp",
            "def clamp(x, lo, hi):\n"
            '    """Return x clipped to [lo, hi]."""\n'
            "    if lo > hi:\n"
            "        lo, hi = hi, lo\n"
            "    if x < lo:\n"
            "        return lo\n"
            "    if x > hi:\n"
            "        return hi\n"
            "    return x\n",
            lambda low: bool(re.search(r"\bclamp(?:s|ed|ing)?\b|\bclip(?:s|ping)?\b.{0,24}\b(range|min|max|bound)", low)),
            (((5, 0, 10), 5), ((-1, 0, 3), 0), ((9, 1, 4), 4)),
        ),
        Template(
            "is_prime",
            "def is_prime(n):\n"
            '    """Return True if n is a prime integer."""\n'
            "    n = int(n)\n"
            "    if n < 2:\n"
            "        return False\n"
            "    if n < 4:\n"
            "        return True\n"
            "    if n % 2 == 0 or n % 3 == 0:\n"
            "        return False\n"
            "    i = 5\n"
            "    while i * i <= n:\n"
            "        if n % i == 0 or n % (i + 2) == 0:\n"
            "            return False\n"
            "        i += 6\n"
            "    return True\n",
            lambda low: bool(re.search(r"\b(is_prime|prime number|check(?:s|ing)? if .{0,16}prime)\b|\bis prime\b", low)),
            (((2,), True), ((1,), False), ((9,), False), ((13,), True)),
        ),
    ]
