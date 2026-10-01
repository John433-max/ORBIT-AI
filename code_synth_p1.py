"""ORBIT code_synth template pack (Cycle 244 split)."""
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
                and "found values" not in low
                and "keep multiplying" not in low
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
            lambda low: bool(
                "product difference" not in low
                and "pairs" not in low
                and "leetcode" not in low
                and "odd binary" not in low
                and "bit flip" not in low
                and re.search(r"\b(max(?:imum)?|larger|greater)\b.{0,40}\b" + _TWO, low)
            ),
            (((2, 9), 9), ((-1, -8), -1)),
        ),
        Template(
            "minimum",
            "def minimum(a, b):\n"
            '    """Return the smaller of a and b."""\n'
            "    return a if a <= b else b\n",
            lambda low: bool(
                "stack" not in low
                and "leetcode" not in low
                and "common value" not in low
                and "bit flip" not in low
                and re.search(r"\b(min(?:imum)?|smaller|lesser)\b.{0,40}\b" + _TWO, low)
            ),
            (((2, 9), 2), ((-1, -8), -8)),
        ),
        Template(
            "reverse_list",
            "def reverse_list(items):\n"
            '    """Return a new list with items reversed."""\n'
            "    return list(items)[::-1]\n",
            lambda low: bool(
                "linked" not in low
                and re.search(
                    r"\breverse(?:s|d|ing)?\b.{0,32}\b(list|array|items)\b|"
                    r"\b(list|array|items)\b.{0,20}\breverse",
                    low,
                )
            ),
            ((([1, 2, 3],), [3, 2, 1]), (([],), [])),
        ),
        Template(
            "reverse_string",
            "def reverse_string(s):\n"
            '    """Return s reversed."""\n'
            "    return s[::-1]\n",
            lambda low: bool(
                re.search(r"\breverse\b.{0,40}\b(string|str|text)\b|\b(string|str|text)\b.{0,20}\breverse", low)
                and "word" not in low
                and "integer" not in low
                and "int " not in low
                and "vowel" not in low
                and "degree" not in low
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
            lambda low: bool(re.search(r"\b(divid(?:e|es|ing)|quotient of)\b.{0,40}\b" + _TWO + r"\b", low))
            and "digits that divide" not in low
            and "2520" not in low
            and "count_digits" not in low,
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
                and "power of three" not in low
                and "power of 3" not in low
                and "power of four" not in low
                and "power of 4" not in low
                and "power-of-four" not in low
                and "pow(x" not in low
                and "pow x n" not in low
                and "my_pow" not in low
                and "negative exponent" not in low
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
                and bool(
                    re.search(
                        r"\b(sort(?:s|ing)?|sort a|sort the)\b.{0,40}\b(list|array|numbers|items)\b",
                        low,
                    )
                )
                and "color" not in low
                and "dutch" not in low
                and "parity" not in low
                and "relative" not in low
                and not re.search(r"\b0s?\b.{0,12}\b1s?\b", low)
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
                and "smallest" not in low
                and "lexicographically" not in low
                and "built" not in low
                and "linked" not in low
                and "list" not in low
                and "partition" not in low
                and "delete" not in low
                and "remove one" not in low
                and "at most one" not in low
                and not re.search(r"\bpalindrome[_ ]ii\b", low)
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
                and "digit" not in low
                and "parity" not in low
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
            lambda low: bool(re.search(r"\b(gcd|greatest common divisor|hcf)\b", low))
            and "string" not in low
            and "strings" not in low,
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
            lambda low: bool(re.search(r"\bcount(?:s|ing)?\b.{0,32}\bvowels?\b|\bvowels?\b.{0,24}\bcount|\bnumber of vowels\b", low)),
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
            lambda low: bool(
                "remove duplicate" not in low
                and "removes duplicate" not in low
                and "removing duplicate" not in low
                and "deduplicat" not in low
                and re.search(r"\b(unique|dedup)\b.{0,24}\b(list|array|items)\b", low)
            ),
            ((([1, 2, 1, 3],), [1, 2, 3]),),
        ),
        Template(
            "is_odd",
            "def is_odd(n):\n"
            '    """Return True if n is odd."""\n'
            "    return n % 2 != 0\n",
            lambda low: (
                "interval" not in low
                and "count odd" not in low
                and "count_odds" not in low
                and "largest odd" not in low
                and "odd number in string" not in low
                and bool(
                    re.search(r"\b(is_odd|number is odd|checks? if .{0,20}is odd)\b", low)
                    or (
                        re.search(r"\bis odd\b|\bodd number\b", low)
                        and "even" not in low
                        and "linked" not in low
                        and "length" not in low
                        and "subarray" not in low
                        and "list" not in low
                        and "consecutive" not in low
                        and "triplet" not in low
                        and "numbers" not in low
                    )
                )
                and "even" not in low
                and "linked" not in low
                and "consecutive" not in low
            ),
            (((3,), True), ((8,), False)),
        ),
        Template(
            "two_sum",
            "def two_sum(items, target):\n"
            '    """Return indices of two items that add to target, or (-1, -1)."""\n'
            "    seen = {}\n"
            "    for i, x in enumerate(items):\n"
            "        need = target - x\n"
            "        if need in seen:\n"
            "            return (seen[need], i)\n"
            "        seen[x] = i\n"
            "    return (-1, -1)\n",
            lambda low: bool(
                re.search(
                    r"\btwo[- ]?sum\b|\bindices of two numbers\b|"
                    r"\btwo (?:numbers|items|values) that (?:add|sum)\b",
                    low,
                )
                and " ii" not in low
                and " iv" not in low
                and "two_sum_ii" not in low
                and "two_sum_iv" not in low
                and " bst" not in low
                and "binary search tree" not in low
                and "sorted array" not in low
                and "1-indexed" not in low
                and "1 indexed" not in low
            ),
            ((([2, 7, 11, 15], 9), (0, 1)), (([3, 2, 4], 6), (1, 2)), (([1, 2], 9), (-1, -1))),
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
                and "prefix" not in low
                and "cumulative" not in low
                and "three" not in low
                and "triplet" not in low
                and "combination" not in low
                and "two sum" not in low
                and "two-sum" not in low
                and "two_sum" not in low
                and "root to leaf" not in low
                and "root-to-leaf" not in low
                and "deepest" not in low
                and "left leaves" not in low
                and "pair" not in low
                and "partition" not in low
                and "good numbers" not in low
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
                and "multilevel" not in low
                and "multi-level" not in low
                and "doubly" not in low
                and "child" not in low
                and "linked" not in low
                and "binary tree" not in low
                and "btree" not in low
            ),
            ((([1, [2, 3], 4],), [1, 2, 3, 4]), (([],), [])),
        ),
        Template(
            "count_words",
            "def count_words(s):\n"
            '    """Return the number of whitespace-separated words in s."""\n'
            "    return len(str(s).split())\n",
            lambda low: bool(
                re.search(r"\bcount(?:s|ing)?\b.{0,32}\bwords?\b|\bnumber of words\b|\bword count\b", low)
            )
            and not re.search(r"\bprefix\b|\bgiven prefix\b", low),
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
            lambda low: bool(
                re.search(r"\b(is_prime|prime number|check(?:s|ing)? if .{0,16}prime)\b|\bis prime\b", low)
                and "count" not in low
                and "sieve" not in low
                and "set bit" not in low
                and "set_bits" not in low
            ),
            (((2,), True), ((1,), False), ((9,), False), ((13,), True)),
        ),
        Template(
            "median",
            "def median(items):\n"
            '    """Return the median of a non-empty numeric list."""\n'
            "    xs = sorted(items)\n"
            "    n = len(xs)\n"
            "    if n == 0:\n"
            "        raise ValueError('empty')\n"
            "    mid = n // 2\n"
            "    if n % 2:\n"
            "        return xs[mid]\n"
            "    return (xs[mid - 1] + xs[mid]) / 2\n",
            lambda low: bool(
                re.search(r"\bmedian\b", low)
                and "stream" not in low
                and "finder" not in low
                and "running" not in low
                and "sorted arrays" not in low
                and "two sorted" not in low
            ),
            ((([1, 3, 2],), 2), (([1, 2, 3, 4],), 2.5)),
        ),
        Template(
            "title_case",
            "def title_case(s):\n"
            '    """Return s with each whitespace-separated word capitalized."""\n'
            "    return ' '.join(w[:1].upper() + w[1:].lower() if w else w for w in str(s).split(' '))\n",
            lambda low: bool(re.search(r"\b(title[- ]?cas(?:e|es|ing)|titlecase|capitalize(?:s|d)? words)\b", low)),
            ((("hello world",), "Hello World"), (("ORBIT ai",), "Orbit Ai")),
        ),
        Template(
            "count_occurrences",
            "def count_occurrences(items, value):\n"
            '    """Return how many times value appears in items."""\n'
            "    n = 0\n"
            "    for x in items:\n"
            "        if x == value:\n"
            "            n += 1\n"
            "    return n\n",
            lambda low: bool(
                re.search(
                    r"\bcount(?:s|ing)?\b.{0,32}\b(occurrence|occurrences|how many times)\b|"
                    r"\bhow many times\b",
                    low,
                )
                and "index" not in low
                and "first occurrence" not in low
            ),
            ((([1, 2, 1, 1], 1), 3), (([], 0), 0)),
        ),
        Template(
            "is_leap_year",
            "def is_leap_year(year):\n"
            '    """Return True if year is a Gregorian leap year."""\n'
            "    y = int(year)\n"
            "    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)\n",
            lambda low: bool(re.search(r"\b(leap year|is_leap_year|leapyear)\b", low)),
            (((2024,), True), ((1900,), False), ((2000,), True)),
        ),
        Template(
            "fizzbuzz",
            "def fizzbuzz(n):\n"
            '    """Return Fizz/Buzz/FizzBuzz/n for 1-based n."""\n'
            "    n = int(n)\n"
            "    if n % 15 == 0:\n"
            "        return 'FizzBuzz'\n"
            "    if n % 3 == 0:\n"
            "        return 'Fizz'\n"
            "    if n % 5 == 0:\n"
            "        return 'Buzz'\n"
            "    return str(n)\n",
            lambda low: "fizzbuzz" in low or "fizz buzz" in low,
            (((3,), "Fizz"), ((5,), "Buzz"), ((15,), "FizzBuzz"), ((7,), "7")),
        ),
        Template(
            "binary_search",
            "def binary_search(items, value):\n"
            '    """Return the index of value in a sorted list, or -1."""\n'
            "    lo, hi = 0, len(items) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        cur = items[mid]\n"
            "        if cur == value:\n"
            "            return mid\n"
            "        if cur < value:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"\bbinary[- ]?search(?:es|ed|ing)?\b|\bbinsearch\b|\bbinary_search\b", low)
                and not re.search(r"\b(trees?|bst)\b", low)
            ),
            ((([1, 3, 5, 7], 5), 2), (([1, 3, 5], 2), -1)),
        ),
        Template(
            "transpose",
            "def transpose(matrix):\n"
            '    """Return the transpose of a rectangular matrix (list of lists)."""\n'
            "    if not matrix:\n"
            "        return []\n"
            "    rows = len(matrix)\n"
            "    cols = len(matrix[0])\n"
            "    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]\n",
            lambda low: bool(
                re.search(
                    r"\btranspos(?:e|es|ed|ing)\b.{0,40}\b(matrix|grid|2d)\b|"
                    r"\b(matrix|grid|2d)\b.{0,24}\btranspos(?:e|es|ed|ing)\b",
                    low,
                )
            ),
            (((([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]]),)),
        ),
        Template(
            "is_anagram",
            "def is_anagram(a, b):\n"
            '    """Return True if a and b use the same letters (ignore case/space)."""\n'
            "    def norm(s):\n"
            "        return sorted(ch.lower() for ch in str(s) if ch.isalnum())\n"
            "    return norm(a) == norm(b)\n",
            lambda low: bool(
                "group" not in low
                and "all anagrams" not in low
                and "anagrams in" not in low
                and re.search(r"\banagrams?\b|\bis_anagram\b", low)
            ),
            ((("Listen", "Silent"), True), (("orbit", "tribe"), False)),
        ),
        Template(
            "dot_product",
            "def dot_product(a, b):\n"
            '    """Return the dot product of two equal-length sequences."""\n'
            "    if len(a) != len(b):\n"
            "        raise ValueError('length mismatch')\n"
            "    total = 0\n"
            "    for x, y in zip(a, b):\n"
            "        total += x * y\n"
            "    return total\n",
            lambda low: bool(re.search(r"\bdot[- ]?product\b|\binner product\b", low)),
            ((([1, 2, 3], [4, 5, 6]), 32), (([], []), 0)),
        ),
        Template(
            "merge_sorted",
            "def merge_sorted(a, b):\n"
            '    """Merge two already-sorted lists into one sorted list."""\n'
            "    i = j = 0\n"
            "    out = []\n"
            "    while i < len(a) and j < len(b):\n"
            "        if a[i] <= b[j]:\n"
            "            out.append(a[i])\n"
            "            i += 1\n"
            "        else:\n"
            "            out.append(b[j])\n"
            "            j += 1\n"
            "    out.extend(a[i:])\n"
            "    out.extend(b[j:])\n"
            "    return out\n",
            lambda low: bool(
                "linked" not in low
                and not re.search(r"\bk\b|\bmerge_k\b|\bmultiple\b", low)
                and re.search(
                    r"\bmerge(?:s|d|ing)?\b.{0,40}\b(two |2 )?sorted (list|array)s?\b|"
                    r"\bmerge[- ]sorted\b|\bmerge_sorted\b",
                    low,
                )
            ),
            ((([1, 3, 5], [2, 4]), [1, 2, 3, 4, 5]), (([], [1]), [1])),
        ),
        Template(
            "intersection",
            "def intersection(a, b):\n"
            '    """Return items that appear in both sequences, first-seen in a."""\n'
            "    seen = set(b)\n"
            "    out = []\n"
            "    used = set()\n"
            "    for x in a:\n"
            "        if x in seen and x not in used:\n"
            "            used.add(x)\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bintersect(?:ion|s|ing)?\b.{0,32}\b(list|array|set|items)\b|"
                    r"\bcommon (?:items|elements)\b|\bintersection of two\b",
                    low,
                )
                and "linked" not in low
                and "node" not in low
                and " ii" not in low
                and "multiset" not in low
                and "2956" not in low
                and "intersection values" not in low
                and "between two arrays" not in low
            ),
            ((([1, 2, 3, 2], [2, 4, 1]), [1, 2]), (([1], [2]), [])),
        ),
        Template(
            "rotate_list",
            "def rotate_list(items, k):\n"
            '    """Rotate items left by k (negative k rotates right)."""\n'
            "    xs = list(items)\n"
            "    n = len(xs)\n"
            "    if n == 0:\n"
            "        return xs\n"
            "    k = int(k) % n\n"
            "    return xs[k:] + xs[:k]\n",
            lambda low: bool(
                re.search(
                    r"\brotat(?:e|es|ed|ing)\b.{0,32}\b(list|items)\b|"
                    r"\b(list)\b.{0,20}\brotat",
                    low,
                )
                and "search" not in low
                and "sorted" not in low
                and "linked" not in low
                and "rotate array" not in low
                and "rotate the array" not in low
            ),
            ((([1, 2, 3, 4], 1), [2, 3, 4, 1]), (([1, 2, 3], -1), [3, 1, 2]), (([], 3), [])),
        ),
        Template(
            "hamming_distance",
            "def hamming_distance(a, b):\n"
            '    """Return Hamming distance of two equal-length strings."""\n'
            "    if len(a) != len(b):\n"
            "        raise ValueError('length mismatch')\n"
            "    return sum(1 for x, y in zip(a, b) if x != y)\n",
            lambda low: bool(
                re.search(r"\bhamming[- ]?distance\b", low)
                or (
                    re.search(r"\bhamming\b", low)
                    and not re.search(r"\bweight\b|\bones\b|\bbits\b", low)
                )
            ),
            ((("karolin", "kathrin"), 3), (("101", "101"), 0)),
        ),
        Template(
            "caesar_shift",
            "def caesar_shift(s, k):\n"
            '    """Shift A-Z/a-z letters by k (mod 26); leave other chars."""\n'
            "    k = int(k) % 26\n"
            "    out = []\n"
            "    for ch in str(s):\n"
            "        if 'A' <= ch <= 'Z':\n"
            "            out.append(chr((ord(ch) - 65 + k) % 26 + 65))\n"
            "        elif 'a' <= ch <= 'z':\n"
            "            out.append(chr((ord(ch) - 97 + k) % 26 + 97))\n"
            "        else:\n"
            "            out.append(ch)\n"
            "    return ''.join(out)\n",
            lambda low: bool(re.search(r"\bcaesar\b|\brots?\s?13\b|\bshift cipher\b", low)),
            ((("Ab c!", 1), "Bc d!"), (("xyz", 3), "abc")),
        ),
        Template(
            "majority_element",
            "def majority_element(items):\n"
            '    """Return the Boyer-Moore majority element, or None."""\n'
            "    cand = None\n"
            "    votes = 0\n"
            "    for x in items:\n"
            "        if votes == 0:\n"
            "            cand = x\n"
            "        votes += 1 if x == cand else -1\n"
            "    if cand is None:\n"
            "        return None\n"
            "    if sum(1 for x in items if x == cand) > len(list(items)) // 2:\n"
            "        return cand\n"
            "    return None\n",
            lambda low: bool(
                re.search(
                    r"\bmajority(?: element)?\b|\bboyer[- ]?moore\b|"
                    r"\belement that appears more than n/?2\b",
                    low,
                )
                and not re.search(r"\bmajority element\s*(ii|2)\b|\bn/?3\b|\bmore than n/?3\b", low)
            ),
            ((([3, 2, 3],), 3), (([1, 2, 1, 1, 3],), 1), (([1, 2],), None)),
        ),
        Template(
            "valid_parentheses",
            "def valid_parentheses(s):\n"
            '    """Return True if (), [], {} in s are balanced."""\n'
            "    pairs = {')': '(', ']': '[', '}': '{'}\n"
            "    stack = []\n"
            "    for ch in str(s):\n"
            "        if ch in '([{':\n"
            "            stack.append(ch)\n"
            "        elif ch in pairs:\n"
            "            if not stack or stack[-1] != pairs[ch]:\n"
            "                return False\n"
            "            stack.pop()\n"
            "    return not stack\n",
            lambda low: bool(
                "generate" not in low
                and "longest" not in low
                and "outermost" not in low
                and "outer" not in low
                and re.search(
                    r"\bvalid(?:ate)?[- ]?parentheses\b|"
                    r"\bbalanced (?:brackets|parentheses|parens)\b|"
                    r"\bcheck .{0,24}\b(parentheses|brackets|parens)\b",
                    low,
                )
            ),
            ((("()[]{}",), True), (("(]",), False), (("([)]",), False), (("",), True)),
        ),
        Template(
            "longest_common_prefix",
            "def longest_common_prefix(strs):\n"
            '    """Return the longest common prefix of the given strings."""\n'
            "    if not strs:\n"
            "        return ''\n"
            "    prefix = str(strs[0])\n"
            "    for s in strs[1:]:\n"
            "        s = str(s)\n"
            "        while not s.startswith(prefix):\n"
            "            prefix = prefix[:-1]\n"
            "            if not prefix:\n"
            "                return ''\n"
            "    return prefix\n",
            lambda low: bool(
                re.search(
                    r"\blongest common prefix\b|\blcp\b|"
                    r"\bcommon prefix of\b",
                    low,
                )
            ),
            (((["flower", "flow", "flight"],), "fl"), ((["dog", "racecar"],), "")),
        ),
        Template(
            "is_sorted",
            "def is_sorted(items):\n"
            '    """Return True if items are non-decreasing."""\n'
            "    xs = list(items)\n"
            "    return all(xs[i] <= xs[i + 1] for i in range(len(xs) - 1))\n",
            lambda low: bool(
                re.search(
                    r"\b(is|check(?:s|ing)? if|already)\b.{0,20}\bsorted\b|"
                    r"\bsorted\b.{0,16}\b(list|array)\b.{0,16}\b(check|predicate|bool)",
                    low,
                )
            )
            and "square" not in low
            and "monotonic" not in low,
            ((([1, 2, 2, 5],), True), (([3, 1],), False), (([],), True)),
        ),
        Template(
            "chunk_list",
            "def chunk_list(items, size):\n"
            '    """Split items into consecutive chunks of length size."""\n'
            "    xs = list(items)\n"
            "    n = int(size)\n"
            "    if n <= 0:\n"
            "        raise ValueError('size must be > 0')\n"
            "    return [xs[i:i + n] for i in range(0, len(xs), n)]\n",
            lambda low: bool(
                re.search(
                    r"\bchunk(?:s|ed|ing)?\b.{0,24}\b(list|array|items)\b|"
                    r"\bsplit .{0,20}\b(list|array)\b.{0,20}\b(chunks|batches|groups)\b",
                    low,
                )
            ),
            ((([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]), (([], 3), [])),
        ),
        Template(
            "list_union",
            "def list_union(a, b):\n"
            '    """Return unique items from a then unseen items from b."""\n'
            "    seen = set()\n"
            "    out = []\n"
            "    for x in list(a) + list(b):\n"
            "        if x not in seen:\n"
            "            seen.add(x)\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bunion\b.{0,24}\b(two |2 )?(list|array|set)s?\b|"
                    r"\b(list|array) union\b",
                    low,
                )
                and "intersection" not in low
            ),
            ((([1, 2, 2], [2, 3]), [1, 2, 3]), (([], [4]), [4])),
        ),
        Template(
            "list_difference",
            "def list_difference(a, b):\n"
            '    """Return items in a that are not in b, preserving order."""\n'
            "    drop = set(b)\n"
            "    return [x for x in a if x not in drop]\n",
            lambda low: bool(
                re.search(
                    r"\b(list|set|array) difference\b|"
                    r"\bdifference of two (list|array|set)s\b|"
                    r"\bitems in .{0,12}\bnot in\b|"
                    r"\brelative complement\b",
                    low,
                )
                and "subtract" not in low
                and "leetcode" not in low
            ),
            ((([1, 2, 3, 2], [2, 4]), [1, 3]), (([1], []), [1])),
        ),
        Template(
            "running_sum",
            "def running_sum(items):\n"
            '    """Return prefix sums of items."""\n'
            "    out = []\n"
            "    acc = 0\n"
            "    for x in items:\n"
            "        acc += x\n"
            "        out.append(acc)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\brunning[- ]?sum\b|\bprefix sums?\b|\bcumulative sums?\b",
                    low,
                )
            ),
            ((([1, 2, 3],), [1, 3, 6]), (([],), []), (([-1, 1],), [-1, 0])),
        ),
        Template(
            "contains_duplicate",
            "def contains_duplicate(items):\n"
            '    """Return True if any value appears more than once."""\n'
            "    seen = set()\n"
            "    for x in items:\n"
            "        if x in seen:\n"
            "            return True\n"
            "        seen.add(x)\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bcontains[- ]?duplicates?\b|"
                    r"\bhas duplicates?\b|"
                    r"\bcheck(?:s|ing)? if .{0,24}\b(list|array|items).{0,16}\bduplicates?\b",
                    low,
                )
                and " ii" not in low
                and "nearby" not in low
                and "within k" not in low
            ),
            ((([1, 2, 3, 1],), True), (([1, 2, 3],), False), (([],), False)),
        ),
        Template(
            "missing_number",
            "def missing_number(items):\n"
            '    """Return the missing value from 0..n in a permutation of n of those."""\n'
            "    xs = list(items)\n"
            "    n = len(xs)\n"
            "    return n * (n + 1) // 2 - sum(xs)\n",
            lambda low: bool(
                re.search(
                    r"\bmissing[- ]?number\b|"
                    r"\bfind(?:s|ing)? the missing\b|"
                    r"\bmissing (?:value|integer) (?:in|from)\b",
                    low,
                )
                and "positive" not in low
            ),
            ((([3, 0, 1],), 2), (([0, 1],), 2), (([9, 6, 4, 2, 3, 5, 7, 0, 1],), 8)),
        ),
        Template(
            "is_power_of_two",
            "def is_power_of_two(n):\n"
            '    """Return True if n is a positive power of two."""\n'
            "    n = int(n)\n"
            "    return n > 0 and (n & (n - 1)) == 0\n",
            lambda low: bool(
                re.search(
                    r"\bpower of two\b|\bpower of 2\b|\bpower-of-two\b|"
                    r"\bis_power_of_two\b",
                    low,
                )
                and "reorder" not in low
                and "rearranged" not in low
            ),
            (((1,), True), ((2,), True), ((3,), False), ((0,), False), ((8,), True)),
        ),
        Template(
            "length_of_last_word",
            "def length_of_last_word(s):\n"
            '    """Return the length of the last whitespace-separated word."""\n'
            "    parts = str(s).split()\n"
            "    return len(parts[-1]) if parts else 0\n",
            lambda low: bool(
                re.search(
                    r"\blength of (?:the )?last word\b|"
                    r"\blast[- ]word[- ]length\b|"
                    r"\blength_of_last_word\b",
                    low,
                )
            ),
            ((("Hello World",), 5), (("   fly me   to   the moon  ",), 4), (("",), 0)),
        ),
        Template(
            "plus_one",
            "def plus_one(digits):\n"
            '    """Add one to a non-negative integer given as a digit list."""\n'
            "    xs = list(digits)\n"
            "    for i in range(len(xs) - 1, -1, -1):\n"
            "        if xs[i] < 9:\n"
            "            xs[i] += 1\n"
            "            return xs\n"
            "        xs[i] = 0\n"
            "    return [1] + xs\n",
            lambda low: bool(
                re.search(
                    r"\bplus[- ]?one\b|"
                    r"\badd one to (?:a )?(?:digit|digits)\b|"
                    r"\bincrement (?:a )?(?:digit array|digit list)\b",
                    low,
                )
                and "linked" not in low
            ),
            ((([1, 2, 3],), [1, 2, 4]), (([9],), [1, 0]), (([9, 9],), [1, 0, 0])),
        ),
        Template(
            "max_subarray",
            "def max_subarray(nums):\n"
            '    """Kadane: maximum contiguous subarray sum."""\n'
            "    xs = list(nums)\n"
            "    if not xs:\n"
            "        return 0\n"
            "    best = cur = xs[0]\n"
            "    for x in xs[1:]:\n"
            "        cur = x if cur + x < x else cur + x\n"
            "        if cur > best:\n"
            "            best = cur\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)?[- ]?subarray\b|"
                    r"\bkadane\b|"
                    r"\blargest (?:contiguous )?subarray sum\b|"
                    r"\bmaximum contiguous (?:subarray )?sum\b",
                    low,
                )
            ),
            ((([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6), (([1],), 1), (([5, 4, -1, 7, 8],), 23)),
        ),
        Template(
            "climb_stairs",
            "def climb_stairs(n):\n"
            '    """Number of ways to climb n stairs taking 1 or 2 steps."""\n'
            "    n = int(n)\n"
            "    if n <= 1:\n"
            "        return 1 if n >= 0 else 0\n"
            "    a, b = 1, 1\n"
            "    for _ in range(2, n + 1):\n"
            "        a, b = b, a + b\n"
            "    return b\n",
            lambda low: bool(
                re.search(
                    r"\bclimb(?:s|ing)?[- ]?stairs?\b|"
                    r"\bstair[- ]?climbing\b|"
                    r"\bways to climb\b",
                    low,
                )
                and "cost" not in low
                and "min cost" not in low
            ),
            (((2,), 2), ((3,), 3), ((1,), 1), ((5,), 8)),
        ),
        Template(
            "single_number",
            "def single_number(nums):\n"
            '    """Return the element that appears once (others twice) via XOR."""\n'
            "    acc = 0\n"
            "    for x in nums:\n"
            "        acc ^= int(x)\n"
            "    return acc\n",
            lambda low: bool(
                re.search(
                    r"\bsingle[- ]?number\b|"
                    r"\belement that appears once\b|"
                    r"\bfind the unique (?:number|element)\b",
                    low,
                )
                and "list of unique" not in low
                and not re.search(r"\b(ii|iii|2|3)\b|\bthree times\b|\btwice except\b", low)
            ),
            ((([2, 2, 1],), 1), (([4, 1, 2, 1, 2],), 4), (([1],), 1)),
        ),
        Template(
            "move_zeroes",
            "def move_zeroes(nums):\n"
            '    """Stable-partition zeros to the end; return the list."""\n'
            "    xs = list(nums)\n"
            "    write = 0\n"
            "    for x in xs:\n"
            "        if x != 0:\n"
            "            xs[write] = x\n"
            "            write += 1\n"
            "    for i in range(write, len(xs)):\n"
            "        xs[i] = 0\n"
            "    return xs\n",
            lambda low: bool(
                re.search(
                    r"\bmoves?[- ]?zeroe?s\b|"
                    r"\bzeroe?s to the end\b|"
                    r"\bmoves? all zeroe?s\b",
                    low,
                )
            ),
            ((([0, 1, 0, 3, 12],), [1, 3, 12, 0, 0]), (([0],), [0]), (([1, 2],), [1, 2])),
        ),
        Template(
            "roman_to_int",
            "def roman_to_int(s):\n"
            '    """Convert a Roman numeral string to an integer."""\n'
            "    val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n"
            "    total = 0\n"
            "    prev = 0\n"
            "    for ch in reversed(str(s).upper()):\n"
            "        n = val.get(ch, 0)\n"
            "        if n < prev:\n"
            "            total -= n\n"
            "        else:\n"
            "            total += n\n"
            "            prev = n\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\broman[- ]?to[- ]?int\b|"
                    r"\broman numeral\b|"
                    r"\bconvert(?:s|ing)? (?:a )?roman\b",
                    low,
                )
                and "to roman" not in low
                and "into roman" not in low
                and "integer to roman" not in low
                and "int to roman" not in low
            ),
            ((("III",), 3), (("LVIII",), 58), (("MCMXCIV",), 1994)),
        ),
        Template(
            "first_unique_char",
            "def first_unique_char(s):\n"
            '    """Return the index of the first non-repeating character, else -1."""\n'
            "    s = str(s)\n"
            "    counts = {}\n"
            "    for ch in s:\n"
            "        counts[ch] = counts.get(ch, 0) + 1\n"
            "    for i, ch in enumerate(s):\n"
            "        if counts[ch] == 1:\n"
            "            return i\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bfirst[- ]?unique[- ]?char\b|"
                    r"\bfirst non[- ]?repeating\b|"
                    r"\bfirst unique character\b",
                    low,
                )
            ),
            ((("leetcode",), 0), (("loveleetcode",), 2), (("aabb",), -1)),
        ),
        Template(
            "max_profit",
            "def max_profit(prices):\n"
            '    """Best time to buy and sell stock (one transaction)."""\n'
            "    prices = list(prices)\n"
            "    if not prices:\n"
            "        return 0\n"
            "    lo = prices[0]\n"
            "    best = 0\n"
            "    for p in prices[1:]:\n"
            "        if p - lo > best:\n"
            "            best = p - lo\n"
            "        if p < lo:\n"
            "            lo = p\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bbuy and sell stock\b|"
                    r"\bbest time to buy\b|"
                    r"\bmax(?:imum)? profit\b|"
                    r"\bstock profit\b",
                    low,
                )
            )
            and "cooldown" not in low
            and "cool down" not in low,
            ((([7, 1, 5, 3, 6, 4],), 5), (([7, 6, 4, 3, 1],), 0), (([1, 2],), 1)),
        ),
        Template(
            "house_robber",
            "def house_robber(nums):\n"
            '    """Max sum of non-adjacent house values."""\n'
            "    nums = list(nums)\n"
            "    prev = cur = 0\n"
            "    for n in nums:\n"
            "        prev, cur = cur, max(cur, prev + n)\n"
            "    return cur\n",
            lambda low: bool(
                re.search(
                    r"\bhouse[- ]?robber\b|"
                    r"\brob houses\b|"
                    r"\brobber\b",
                    low,
                )
                and not re.search(r"\b(ii+|2|3|circular|circle|tree)\b", low)
            ),
            ((([1, 2, 3, 1],), 4), (([2, 7, 9, 3, 1],), 12), (([2, 1, 1, 2],), 4)),
        ),
        Template(
            "can_jump",
            "def can_jump(nums):\n"
            '    """True if last index is reachable (jump game)."""\n'
            "    nums = list(nums)\n"
            "    reach = 0\n"
            "    for i, step in enumerate(nums):\n"
            "        if i > reach:\n"
            "            return False\n"
            "        reach = max(reach, i + int(step))\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bcan[- ]?jump\b|"
                    r"\bjump game\b|"
                    r"\breach(?:es)? the last index\b",
                    low,
                )
                and not re.search(r"\bjump game\s*(ii|2|ii+)\b|\bmin(?:imum)? jumps\b|\bjump_game_ii\b", low)
            ),
            ((([2, 3, 1, 1, 4],), True), (([3, 2, 1, 0, 4],), False), (([0],), True)),
        ),
        Template(
            "remove_duplicates",
            "def remove_duplicates(nums):\n"
            '    """Return unique values from a sorted list, preserving order."""\n'
            "    nums = list(nums)\n"
            "    out = []\n"
            "    for n in nums:\n"
            "        if not out or out[-1] != n:\n"
            "            out.append(n)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bremov(?:e|es|ing) duplicates\b|"
                    r"\bdeduplicat(?:e|es|ing)\b|"
                    r"\bunique values from a sorted\b",
                    low,
                )
                and "character" not in low
                and "linked" not in low
                and not re.search(
                    r"\bat most two\b|\bkeep(?:s|ing)? at most 2\b|"
                    r"\bremove_duplicates_ii\b|"
                    r"\bsorted array(?: ii| 2)\b|"
                    r"\bduplicates from sorted array ii\b",
                    low,
                )
            ),
            ((([1, 1, 2],), [1, 2]), (([0, 0, 1, 1, 1, 2, 2, 3],), [0, 1, 2, 3]), (([],), [])),
        ),
        Template(
            "product_except_self",
            "def product_except_self(nums):\n"
            '    """Prefix/suffix products; output[i] is product of all but nums[i]."""\n'
            "    nums = list(nums)\n"
            "    n = len(nums)\n"
            "    out = [1] * n\n"
            "    left = 1\n"
            "    for i in range(n):\n"
            "        out[i] = left\n"
            "        left *= nums[i]\n"
            "    right = 1\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        out[i] *= right\n"
            "        right *= nums[i]\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bproduct except self\b|"
                    r"\bproduct of array except\b|"
                    r"\bexcept itself\b",
                    low,
                )
            ),
            ((([1, 2, 3, 4],), [24, 12, 8, 6]), (([-1, 1, 0, -3, 3],), [0, 0, 9, 0, 0])),
        ),
        Template(
            "find_peak",
            "def find_peak(nums):\n"
            '    """Return an index of a peak element (greater than neighbors)."""\n'
            "    nums = list(nums)\n"
            "    n = len(nums)\n"
            "    if n == 0:\n"
            "        return -1\n"
            "    lo, hi = 0, n - 1\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] < nums[mid + 1]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return lo\n",
            lambda low: bool(
                re.search(
                    r"\bfind(?:s)?(?: a)? peak\b|"
                    r"\bpeak element\b|"
                    r"\bfind peak\b",
                    low,
                )
            ),
            ((([1, 2, 3, 1],), 2), (([1, 2, 1, 3, 5, 6, 4],), 5), (([1],), 0)),
        ),
        Template(
            "coin_change",
            "def coin_change(coins, amount):\n"
            '    """Fewest coins that sum to amount, or -1 if impossible."""\n'
            "    amount = int(amount)\n"
            "    inf = amount + 1\n"
            "    dp = [0] + [inf] * amount\n"
            "    for coin in coins:\n"
            "        c = int(coin)\n"
            "        if c <= 0:\n"
            "            continue\n"
            "        for x in range(c, amount + 1):\n"
            "            cand = dp[x - c] + 1\n"
            "            if cand < dp[x]:\n"
            "                dp[x] = cand\n"
            "    return dp[amount] if dp[amount] <= amount else -1\n",
            lambda low: bool(
                re.search(
                    r"\bcoin[- ]?change\b|"
                    r"\bfewest coins\b|"
                    r"\bminimum coins\b",
                    low,
                )
                and not re.search(r"\b(ii|2|combination|number of ways|combinations)\b", low)
            ),
            ((([1, 2, 5], 11), 3), (([2], 3), -1), (([1], 0), 0)),
        ),
        Template(
            "lis",
            "def lis(nums):\n"
            '    """Length of the longest strictly increasing subsequence."""\n'
            "    nums = list(nums)\n"
            "    n = len(nums)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    dp = [1] * n\n"
            "    best = 1\n"
            "    for i in range(n):\n"
            "        for j in range(i):\n"
            "            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:\n"
            "                dp[i] = dp[j] + 1\n"
            "        if dp[i] > best:\n"
            "            best = dp[i]\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blongest increasing subsequence\b|"
                    r"\blength of (?:the )?lis\b|"
                    r"\blis length\b",
                    low,
                )
            ),
            ((([10, 9, 2, 5, 3, 7, 101, 18],), 4), (([0, 1, 0, 3, 2, 3],), 4), (([7, 7, 7],), 1)),
        ),
    ]
