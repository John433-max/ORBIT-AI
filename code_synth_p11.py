"""Cycle 268: additional verified Python templates (pack 11)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "sorted_squares",
            "def sorted_squares(nums):\n"
            '    """Return squares of nums in non-decreasing order."""\n'
            "    n = len(nums)\n"
            "    out = [0] * n\n"
            "    lo, hi = 0, n - 1\n"
            "    wr = n - 1\n"
            "    while lo <= hi:\n"
            "        a, b = int(nums[lo]), int(nums[hi])\n"
            "        if abs(a) > abs(b):\n"
            "            out[wr] = a * a\n"
            "            lo += 1\n"
            "        else:\n"
            "            out[wr] = b * b\n"
            "            hi -= 1\n"
            "        wr -= 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsquares of (?:a )?sorted array\b|"
                    r"\bsorted_squares\b|"
                    r"\bsorted squares\b|"
                    r"\bsquare(?:s)? (?:of )?(?:each )?(?:number|element).{0,20}sorted\b",
                    low,
                )
            )
            and "parity" not in low,
            (([[-4, -1, 0, 3, 10]], [0, 1, 9, 16, 100]), ([[-7, -3, 2, 3, 11]], [4, 9, 9, 49, 121])),
        ),
        T(
            "sort_array_by_parity_ii",
            "def sort_array_by_parity_ii(nums):\n"
            '    """Place evens at even indices and odds at odd indices."""\n'
            "    arr = [int(x) for x in nums]\n"
            "    even = [x for x in arr if x % 2 == 0]\n"
            "    odd = [x for x in arr if x % 2 != 0]\n"
            "    out = [0] * len(arr)\n"
            "    out[0::2] = even\n"
            "    out[1::2] = odd\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsort array by parity ii\b|"
                    r"\bsort_array_by_parity_ii\b|"
                    r"\bparity ii\b|"
                    r"\bevens? at even (?:indices|indexes)\b",
                    low,
                )
            ),
            (([[4, 2, 5, 7]], [4, 5, 2, 7]), ([[2, 3]], [2, 3])),
        ),
        T(
            "is_monotonic",
            "def is_monotonic(nums):\n"
            '    """True if nums is monotone increasing or decreasing."""\n'
            "    inc = dec = True\n"
            "    for i in range(1, len(nums)):\n"
            "        if int(nums[i]) < int(nums[i - 1]):\n"
            "            inc = False\n"
            "        if int(nums[i]) > int(nums[i - 1]):\n"
            "            dec = False\n"
            "    return inc or dec\n",
            lambda low: bool(
                re.search(
                    r"\bmonotonic array\b|"
                    r"\bis_monotonic\b|"
                    r"\bcheck(?:s|ing)? if (?:an? )?array is monotonic\b|"
                    r"\bis monotonic\b|"
                    r"\bmonotone (?:increasing or decreasing)\b",
                    low,
                )
            )
            and "mountain" not in low,
            (([[1, 2, 2, 3]], True), ([[6, 5, 4, 4]], True), ([[1, 3, 2]], False)),
        ),
        T(
            "backspace_compare",
            "def backspace_compare(s, t):\n"
            '    """True if s and t are equal after applying backspace \'#\'."""\n'
            "    def build(text):\n"
            "        stack = []\n"
            "        for ch in str(text):\n"
            "            if ch == '#':\n"
            "                if stack:\n"
            "                    stack.pop()\n"
            "            else:\n"
            "                stack.append(ch)\n"
            "        return ''.join(stack)\n"
            "    return build(s) == build(t)\n",
            lambda low: bool(
                re.search(
                    r"\bbackspace string compare\b|"
                    r"\bbackspace_compare\b|"
                    r"\bcompare strings? (?:with|after) backspace\b|"
                    r"\btyped strings? with backspace\b",
                    low,
                )
            ),
            ((("ab#c", "ad#c"), True), (("ab##", "c#d#"), True), (("a#c", "b"), False)),
        ),
        T(
            "to_goat_latin",
            "def to_goat_latin(sentence):\n"
            '    """Convert sentence to Goat Latin."""\n'
            "    vowels = set('aeiouAEIOU')\n"
            "    words = str(sentence).split()\n"
            "    out = []\n"
            "    for i, w in enumerate(words, 1):\n"
            "        if w and w[0] in vowels:\n"
            "            stem = w + 'ma'\n"
            "        else:\n"
            "            stem = (w[1:] + w[0] + 'ma') if w else 'ma'\n"
            "        out.append(stem + ('a' * i))\n"
            "    return ' '.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\bgoat latin\b|"
                    r"\bto_goat_latin\b|"
                    r"\bconvert (?:a )?sentence to goat latin\b",
                    low,
                )
            )
            and "morse" not in low
            and "roman" not in low,
            (
                (("I speak Goat Latin",), "Imaa peaksmaaa oatGmaaaa atinLmaaaaa"),
                (("The quick brown fox jumped over the lazy dog",),
                 "heTmaa uickqmaaa rownbmaaaa oxfmaaaaa umpedjmaaaaaa overmaaaaaaa hetmaaaaaaaa azylmaaaaaaaaa ogdmaaaaaaaaaa"),
            ),
        ),
        T(
            "fair_candy_swap",
            "def fair_candy_swap(alice_sizes, bob_sizes):\n"
            '    """Return [x, y] so Alice and Bob have equal candy after swap."""\n'
            "    a = [int(x) for x in alice_sizes]\n"
            "    b = [int(x) for x in bob_sizes]\n"
            "    sa, sb = sum(a), sum(b)\n"
            "    delta = (sa - sb) // 2\n"
            "    bob = set(b)\n"
            "    for x in a:\n"
            "        y = x - delta\n"
            "        if y in bob:\n"
            "            return [x, y]\n"
            "    return []\n",
            lambda low: bool(
                re.search(
                    r"\bfair candy swap\b|"
                    r"\bfair_candy_swap\b|"
                    r"\bswap candy to equalize\b|"
                    r"\bequal candy after (?:one )?swap\b",
                    low,
                )
            ),
            (([[1, 1], [2, 2]], [1, 2]), ([[1, 2], [2, 3]], [1, 2]), ([[2], [1, 3]], [2, 3])),
        ),
    ]
