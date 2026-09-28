"""ORBIT code_synth extra pack p1b (median..dot_product gap for GitHub p1)."""
from __future__ import annotations
import re
from code_synth import Template, _TWO


def templates():
    return [
        Template(
            "minimum",
            "def minimum(a, b):\n"
            '    """Return the smaller of a and b."""\n'
            "    return a if a <= b else b\n",
            lambda low: bool(
                "stack" not in low
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
            ),
            ((([2, 7, 11, 15], 9), (0, 1)), (([3, 2, 4], 6), (1, 2)), (([1, 2], 9), (-1, -1))),
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
    ]
