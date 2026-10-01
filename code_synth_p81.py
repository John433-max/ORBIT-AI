"""Cycle 350: unused Easy — odd/even freq gap, original typed string,
variable-length subarray sum, all-set-bits number, ball child, square triples."""

from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "max_freq_odd_even_diff",
            "def max_freq_odd_even_diff(s):\n"
            '    """Max odd-frequency minus min even-frequency (LeetCode 3442)."""\n'
            "    counts = {}\n"
            "    for ch in s:\n"
            "        counts[ch] = counts.get(ch, 0) + 1\n"
            "    max_odd = 0\n"
            "    min_even = 10 ** 9\n"
            "    for freq in counts.values():\n"
            "        if freq % 2:\n"
            "            if freq > max_odd:\n"
            "                max_odd = freq\n"
            "        elif freq < min_even:\n"
            "            min_even = freq\n"
            "    return max_odd - min_even\n",
            lambda low: "even and odd frequency" in low or (
                "odd frequency" in low and "even frequency" in low
            ),
            (
                (("aaaaabbc",), 3),
                (("abcabcab",), 1),
                (("xyyzzz",), 1),
            ),
        ),
        T(
            "possible_string_count",
            "def possible_string_count(word):\n"
            '    """Original strings if at most one key was long-pressed (LeetCode 3330)."""\n'
            "    extra = 0\n"
            "    for i in range(1, len(word)):\n"
            "        if word[i] == word[i - 1]:\n"
            "            extra += 1\n"
            "    return extra + 1\n",
            lambda low: "original typed string" in low,
            (
                (("abbcccc",), 5),
                (("abcd",), 1),
                (("aaaa",), 4),
            ),
        ),
        T(
            "variable_length_subarray_sum",
            "def variable_length_subarray_sum(nums):\n"
            '    """Sum of nums[max(0, i-nums[i]) .. i] for each i (LeetCode 3427)."""\n'
            "    total = 0\n"
            "    prefix = [0]\n"
            "    for value in nums:\n"
            "        prefix.append(prefix[-1] + value)\n"
            "    for i, value in enumerate(nums):\n"
            "        start = i - value\n"
            "        if start < 0:\n"
            "            start = 0\n"
            "        total += prefix[i + 1] - prefix[start]\n"
            "    return total\n",
            lambda low: "variable length subarrays" in low or "variable-length subarrays" in low,
            (
                (([2, 3, 1],), 11),
                (([3, 1, 1, 2],), 13),
                (([1],), 1),
            ),
        ),
        T(
            "smallest_number_all_set_bits",
            "def smallest_number_all_set_bits(n):\n"
            '    """Smallest x >= n whose bits are all set (LeetCode 3370)."""\n'
            "    x = 1\n"
            "    while x - 1 < n:\n"
            "        x <<= 1\n"
            "    return x - 1\n",
            lambda low: "all set bits" in low,
            (
                ((5,), 7),
                ((10,), 15),
                ((3,), 3),
            ),
        ),
        T(
            "child_with_ball",
            "def child_with_ball(n, k):\n"
            '    """Child holding the ball after k seconds (LeetCode 3178)."""\n'
            "    trips, mod = divmod(k, n - 1)\n"
            "    if trips & 1:\n"
            "        return n - mod - 1\n"
            "    return mod\n",
            lambda low: "child who has the ball" in low or "child with the ball" in low,
            (
                ((3, 5), 1),
                ((5, 6), 2),
                ((4, 2), 2),
            ),
        ),
        T(
            "count_square_sum_triples",
            "def count_square_sum_triples(n):\n"
            '    """Count a^2 + b^2 = c^2 with 1 <= a,b,c <= n (LeetCode 1925)."""\n'
            "    ans = 0\n"
            "    for a in range(1, n):\n"
            "        for b in range(1, n):\n"
            "            x = a * a + b * b\n"
            "            c = int(x ** 0.5)\n"
            "            if c <= n and c * c == x:\n"
            "                ans += 1\n"
            "    return ans\n",
            lambda low: "square sum triples" in low or "square triples" in low,
            (
                ((5,), 2),
                ((10,), 4),
                ((1,), 0),
            ),
        ),
    ]
