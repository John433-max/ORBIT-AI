"""Cycle 321: path-in-graph / split min sum / strong-pair XOR /
even-odd bits / concatenation value / acronym check."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "valid_path",
            "def valid_path(n, edges, source, destination):\n"
            '    """True if an undirected path exists (LeetCode 1971)."""\n'
            "    if source == destination:\n"
            "        return True\n"
            "    g = {i: [] for i in range(n)}\n"
            "    for a, b in edges:\n"
            "        g[a].append(b)\n"
            "        g[b].append(a)\n"
            "    seen = {source}\n"
            "    stack = [source]\n"
            "    while stack:\n"
            "        u = stack.pop()\n"
            "        for v in g[u]:\n"
            "            if v in seen:\n"
            "                continue\n"
            "            if v == destination:\n"
            "                return True\n"
            "            seen.add(v)\n"
            "            stack.append(v)\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bvalid_path\b|"
                    r"\bfind[_ ]if[_ ]path[_ ]exists[_ ]in[_ ]graph\b|"
                    r"\bpath[_ ]exists[_ ]in[_ ]graph\b|"
                    r"\bleetcode[_ ]1971\b",
                    low,
                )
            )
            and "shortest" not in low
            and "all_paths" not in low,
            (
                ((3, [[0, 1], [1, 2], [2, 0]], 0, 2), True),
                ((6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5), False),
            ),
        ),
        T(
            "split_num",
            "def split_num(num):\n"
            '    """Split digits into two numbers with minimum sum (LeetCode 2578)."""\n'
            "    digits = sorted(str(num))\n"
            "    a = b = ''\n"
            "    for i, ch in enumerate(digits):\n"
            "        if i % 2 == 0:\n"
            "            a += ch\n"
            "        else:\n"
            "            b += ch\n"
            "    return int(a or '0') + int(b or '0')\n",
            lambda low: bool(
                re.search(
                    r"\bsplit_num\b|"
                    r"\bsplit[_ ]with[_ ]minimum[_ ]sum\b|"
                    r"\bsplit[_ ]digits[_ ]with[_ ]minimum[_ ]sum\b|"
                    r"\bleetcode[_ ]2578\b",
                    low,
                )
            )
            and "split_array" not in low
            and "minimum_sum_of_mountain" not in low,
            (
                ((4325,), 59),
                ((687,), 75),
            ),
        ),
        T(
            "maximum_strong_pair_xor",
            "def maximum_strong_pair_xor(nums):\n"
            '    """Max XOR among strong pairs |x-y| <= min(x,y) (LeetCode 2932)."""\n'
            "    best = 0\n"
            "    n = len(nums)\n"
            "    for i in range(n):\n"
            "        for j in range(i, n):\n"
            "            x, y = nums[i], nums[j]\n"
            "            if abs(x - y) <= min(x, y):\n"
            "                best = max(best, x ^ y)\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmaximum_strong_pair_xor\b|"
                    r"\bmaximum[_ ]strong[_ ]pair[_ ]xor\b|"
                    r"\bstrong[_ ]pair[_ ]xor\b|"
                    r"\bleetcode[_ ]2932\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4, 5],), 7),
                (([10, 100],), 0),
            ),
        ),
        T(
            "even_odd_bit",
            "def even_odd_bit(n):\n"
            '    """Count even- and odd-indexed 1-bits (LeetCode 2595)."""\n'
            "    even = odd = 0\n"
            "    i = 0\n"
            "    while n:\n"
            "        if n & 1:\n"
            "            if i % 2 == 0:\n"
            "                even += 1\n"
            "            else:\n"
            "                odd += 1\n"
            "        n >>= 1\n"
            "        i += 1\n"
            "    return [even, odd]\n",
            lambda low: bool(
                re.search(
                    r"\beven_odd_bit\b|"
                    r"\bnumber[_ ]of[_ ]even[_ ]and[_ ]odd[_ ]bits\b|"
                    r"\beven[_ ]and[_ ]odd[_ ]bits\b|"
                    r"\bleetcode[_ ]2595\b",
                    low,
                )
            )
            and "hamming" not in low
            and "count_bits" not in low,
            (
                ((17,), [2, 0]),
                ((2,), [0, 1]),
            ),
        ),
        T(
            "find_the_array_conc_val",
            "def find_the_array_conc_val(nums):\n"
            '    """Sum concatenation of symmetric pairs (LeetCode 2562)."""\n'
            "    i, j = 0, len(nums) - 1\n"
            "    total = 0\n"
            "    while i < j:\n"
            "        total += int(str(nums[i]) + str(nums[j]))\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    if i == j:\n"
            "        total += nums[i]\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bfind_the_array_conc_val\b|"
                    r"\barray[_ ]concatenation[_ ]value\b|"
                    r"\bfind[_ ]the[_ ]array[_ ]concatenation[_ ]value\b|"
                    r"\bleetcode[_ ]2562\b",
                    low,
                )
            ),
            (
                (([7, 52, 2, 4],), 596),
                (([5, 14, 13, 8, 12],), 673),
            ),
        ),
        T(
            "is_acronym",
            "def is_acronym(words, s):\n"
            '    """True if s is the concatenation of first letters (LeetCode 2828)."""\n'
            "    return ''.join(w[0] for w in words) == s\n",
            lambda low: bool(
                re.search(
                    r"\bis_acronym\b|"
                    r"\bcheck[_ ]if[_ ]a[_ ]string[_ ]is[_ ]an[_ ]acronym\b|"
                    r"\bstring[_ ]is[_ ]an[_ ]acronym[_ ]of[_ ]words\b|"
                    r"\bleetcode[_ ]2828\b",
                    low,
                )
            )
            and "valid_word" not in low,
            (
                ((["alice", "bob", "charlie"], "abc"), True),
                ((["an", "apple"], "a"), False),
                ((["never", "gonna", "give", "up", "on", "you"], "ngguoy"), True),
            ),
        ),
    ]
