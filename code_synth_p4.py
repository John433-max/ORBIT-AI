"""Cycle expand: additional verified Python templates (pack 4)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "median_list",
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
                and re.search(r"\b(list|array|numbers|values)\b", low)
                and "stream" not in low
                and "two sorted" not in low
                and "finder" not in low
            ),
            ((([1, 3, 2],), 2), (([1, 2, 3, 4],), 2.5)),
        ),
        T(
            "mode_list",
            "def mode(items):\n"
            '    """Return the most frequent element (first on ties)."""\n'
            "    from collections import Counter\n"
            "    if not items:\n"
            "        raise ValueError('empty')\n"
            "    counts = Counter(items)\n"
            "    return max(items, key=lambda x: counts[x])\n",
            lambda low: bool(
                (re.search(r"\bmode\b", low) and "list" in low)
                or re.search(r"\bmost frequent\b", low)
            ),
            ((([1, 2, 2, 3],), 2), ((("a", "b", "a"),), "a")),
        ),
        T(
            "flatten_deep",
            "def flatten_deep(items):\n"
            '    """Recursively flatten nested lists."""\n'
            "    out = []\n"
            "    for x in items:\n"
            "        if isinstance(x, list):\n"
            "            out.extend(flatten_deep(x))\n"
            "        else:\n"
            "            out.append(x)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bflatten\b", low)
                and re.search(r"\b(deep|nested|recursive)\b", low)
            ),
            ((([1, [2, [3]]],), [1, 2, 3]),),
        ),
        T(
            "last_n",
            "def last_n(items, n):\n"
            '    """Return the last n elements of items."""\n'
            "    n = max(0, int(n))\n"
            "    return list(items)[-n:] if n else []\n",
            # "drop(s) the last n" means remove, not return — leave those to drop_last.
            lambda low: bool(
                re.search(r"\blast n\b|\btail of (list|array)\b", low)
                and not re.search(r"\bdrop(?:s|ping)?\b|\bwithout the last\b", low)
            ),
            ((([1, 2, 3, 4, 5], 2), [4, 5]),),
        ),
        T(
            "sliding_window_max",
            "def sliding_window_max(nums, k):\n"
            '    """Max of each contiguous window of size k."""\n'
            "    if k <= 0 or k > len(nums):\n"
            "        return []\n"
            "    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]\n",
            lambda low: bool(
                re.search(r"\bsliding window\b", low) and re.search(r"\bmax\b", low)
            ),
            ((([1, 3, 2, 5, 4], 3), [3, 5, 5]),),
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
                re.search(r"\b(count bits|hamming weight|set bits|popcount)\b", low)
            ),
            (((7,), 3), ((0,), 0)),
        ),
        T(
            "is_power_of_three",
            "def is_power_of_three(n):\n"
            '    """Return True if n is a power of three."""\n'
            "    if n < 1:\n"
            "        return False\n"
            "    while n % 3 == 0:\n"
            "        n //= 3\n"
            "    return n == 1\n",
            lambda low: bool(re.search(r"\bpower of three\b|\bpower of 3\b", low)),
            (((9,), True), ((10,), False)),
        ),
        T(
            "diagonal_sum",
            "def diagonal_sum(matrix):\n"
            '    """Sum of primary diagonal of a square matrix."""\n'
            "    return sum(matrix[i][i] for i in range(len(matrix)))\n",
            lambda low: bool(
                re.search(r"\bdiagonal sum\b", low)
                or (re.search(r"\bdiagonal\b", low) and "sum" in low and "matrix" in low)
            ),
            ((([[1, 2], [3, 4]],), 5),),
        ),
        T(
            "snake_to_camel",
            "def snake_to_camel(name):\n"
            '    """Convert snake_case to camelCase."""\n'
            "    parts = str(name).split('_')\n"
            "    if not parts:\n"
            "        return ''\n"
            "    return parts[0].lower() + ''.join(p.title() for p in parts[1:] if p)\n",
            lambda low: bool(re.search(
                r"\bsnake.?to.?camel\b|\bsnake[_ ]?case to camel\b",
                low,
            )) and "to snake" not in low,
            ((("hello_world",), "helloWorld"), (("a",), "a")),
        ),
        T(
            "camel_to_snake",
            "def camel_to_snake(name):\n"
            '    """Convert camelCase to snake_case."""\n'
            "    out = []\n"
            "    for i, ch in enumerate(str(name)):\n"
            "        if ch.isupper() and i:\n"
            "            out.append('_')\n"
            "            out.append(ch.lower())\n"
            "        else:\n"
            "            out.append(ch.lower())\n"
            "    return ''.join(out)\n",
            lambda low: bool(re.search(r"\bcamel.?to.?snake\b|\bcamelCase to snake\b|\bsnake[_ ]?case\b", low)) and "dict" not in low and "to camel" not in low,
            ((("helloWorld",), "hello_world"), (("A",), "a")),
        ),
        T(
            "unique_preserve_order",
            "def unique_preserve_order(items):\n"
            '    """Deduplicate while keeping first-seen order."""\n'
            "    seen = set()\n"
            "    out = []\n"
            "    for x in items:\n"
            "        if x in seen:\n"
            "            continue\n"
            "        seen.add(x)\n"
            "        out.append(x)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bunique\b", low)
                and re.search(r"\b(order|preserve|stable)\b", low)
            ),
            ((([1, 2, 1, 3, 2],), [1, 2, 3]),),
        ),
        T(
            "batch_list",
            "def batch(items, size):\n"
            '    """Split items into batches of at most size."""\n'
            "    size = max(1, int(size))\n"
            "    xs = list(items)\n"
            "    return [xs[i:i + size] for i in range(0, len(xs), size)]\n",
            lambda low: bool(re.search(r"\b(batch|chunk into)\b", low)),
            ((([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]),),
        ),
        T(
            "deep_merge_dicts",
            "def deep_merge(a, b):\n"
            '    """Shallow-recursive merge of dict b into a (copy)."""\n'
            "    out = dict(a)\n"
            "    for k, v in b.items():\n"
            "        if k in out and isinstance(out[k], dict) and isinstance(v, dict):\n"
            "            out[k] = deep_merge(out[k], v)\n"
            "        else:\n"
            "            out[k] = v\n"
            "    return out\n",
            lambda low: bool(re.search(r"\bdeep merge\b|\bmerge dicts?\b", low)),
            ((({"a": 1, "b": {"c": 2}}, {"b": {"d": 3}}), {"a": 1, "b": {"c": 2, "d": 3}}),),
        ),
        T(
            "parse_int_safe",
            "def parse_int(s, default=0):\n"
            '    """Parse int from string; return default on failure."""\n'
            "    try:\n"
            "        return int(str(s).strip())\n"
            "    except (TypeError, ValueError):\n"
            "        return default\n",
            lambda low: bool(
                re.search(r"\bparse int\b|\bsafe int\b", low) and "list" not in low
            ),
            ((("42",), 42), (("x",), 0)),
        ),
        T(
            "url_join",
            "def url_join(base, path):\n"
            '    """Join base URL and path with exactly one slash."""\n'
            "    base = str(base).rstrip(\"/\")\n"
            "    path = str(path).lstrip(\"/\")\n"
            "    return base + \"/\" + path if path else base\n",
            lambda low: bool(re.search(r"\burl join\b|\bjoin url\b", low)),
            ((("https://a.com/", "/b"), "https://a.com/b"),),
        ),
        T(
            "find_duplicates",
            "def find_duplicates(items):\n"
            '    """Return sorted list of values that appear more than once."""\n'
            "    from collections import Counter\n"
            "    counts = Counter(items)\n"
            "    return sorted([x for x, c in counts.items() if c > 1], key=lambda x: str(x))\n",
            lambda low: bool(re.search(r"\bfind duplicates\b|\blist duplicates\b", low)),
            ((([1, 2, 2, 3, 1],), [1, 2]),),
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
            lambda low: bool(re.search(r"\brotates? (?:a )?string\b|\bstring rotation\b", low)) and "list" not in low,
            ((("abcde", 2), "cdeab"),),
        ),
        T(
            "is_subarray",
            "def is_subarray(haystack, needle):\n"
            '    """Return True if needle appears contiguously in haystack."""\n'
            "    n, m = len(haystack), len(needle)\n"
            "    if m == 0:\n"
            "        return True\n"
            "    if m > n:\n"
            "        return False\n"
            "    for i in range(n - m + 1):\n"
            "        if list(haystack[i:i + m]) == list(needle):\n"
            "            return True\n"
            "    return False\n",
            lambda low: bool(re.search(r"\bis subarray\b|\bsubarray of\b", low)),
            ((([1, 2, 3, 4], [2, 3]), True),),
        ),
        T(
            "running_average",
            "def running_average(nums):\n"
            '    """Prefix averages for a numeric sequence."""\n'
            "    out, total = [], 0.0\n"
            "    for i, x in enumerate(nums, 1):\n"
            "        total += x\n"
            "        out.append(total / i)\n"
            "    return out\n",
            lambda low: bool(re.search(r"\brunning average\b|\bprefix average\b", low)),
            ((([2, 4, 6],), [2.0, 3.0, 4.0]),),
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
            "median_of_two_sorted",
            "def median_of_two_sorted(a, b):\n"
            '    """Median of two sorted arrays (merge then pick)."""\n'
            "    merged = []\n"
            "    i = j = 0\n"
            "    while i < len(a) and j < len(b):\n"
            "        if a[i] <= b[j]:\n"
            "            merged.append(a[i]); i += 1\n"
            "        else:\n"
            "            merged.append(b[j]); j += 1\n"
            "    merged.extend(a[i:]); merged.extend(b[j:])\n"
            "    n = len(merged)\n"
            "    if n == 0:\n"
            "        raise ValueError('empty')\n"
            "    mid = n // 2\n"
            "    if n % 2:\n"
            "        return float(merged[mid])\n"
            "    return (merged[mid - 1] + merged[mid]) / 2.0\n",
            lambda low: bool(
                re.search(r"\bmedian of two sorted\b", low)
                or (re.search(r"\bmedian\b", low) and "two sorted" in low)
            ),
            ((([1, 3], [2, 4]), 2.5), (([1, 2], [3]), 2.0)),
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
                    r"\bint(?:eger)? to roman\b|"
                    r"\bto roman numeral\b|"
                    r"\bconvert(?:s|ing)? (?:an? )?(?:int|integer|number) to roman\b",
                    low,
                )
            ),
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
                re.search(r"\bvalid[_ ]palindrome[_ ]ii\b", low)
                or (
                    "palindrome" in low
                    and (
                        "at most one" in low
                        or "delete one" in low
                        or "remove one" in low
                        or "deleting one" in low
                    )
                )
            ),
            ((("aba",), True), (("abca",), True), (("abc",), False)),
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
                    r"\binteger square root\b|"
                    r"\bsqrt\(x\)\b|"
                    r"\bmy_sqrt\b|"
                    r"\bfloor(?:ed)? square root\b",
                    low,
                )
            ),
            (((4,), 2), ((8,), 2), ((0,), 0)),
        ),
    ]
