"""Cycle 279: additional verified Python templates (pack 21)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "goat_latin",
            "def to_goat_latin(sentence):\n"
            '    """Goat Latin transform of each word in sentence."""\n'
            "    vowels = set('aeiouAEIOU')\n"
            "    out = []\n"
            "    for i, w in enumerate(str(sentence).split(), 1):\n"
            "        if w and w[0] in vowels:\n"
            "            nw = w + 'ma'\n"
            "        else:\n"
            "            nw = (w[1:] + w[0] if w else w) + 'ma'\n"
            "        nw += 'a' * i\n"
            "        out.append(nw)\n"
            "    return ' '.join(out)\n",
            lambda low: bool(
                re.search(r"\bgoat latin\b|\bto_goat_latin\b|\bgoat_latin\b", low)
            ),
            (
                (("I speak Goat Latin",), "Imaa peaksmaaa oatGmaaaa atinLmaaaaa"),
                (("The quick brown fox",), "heTmaa uickqmaaa rownbmaaaa oxfmaaaaa"),
            ),
        ),
        T(
            "reordered_power_of_2",
            "def reordered_power_of_2(n):\n"
            '    """True if digits of n can be rearranged into a power of two."""\n'
            "    def sig(x):\n"
            "        return ''.join(sorted(str(x)))\n"
            "    target = sig(int(n))\n"
            "    return any(sig(1 << i) == target for i in range(31))\n",
            lambda low: bool(
                re.search(
                    r"\breordered power of 2\b|"
                    r"\breordered_power_of_2\b|"
                    r"\breorder.*power of two\b",
                    low,
                )
            )
            and "is power of two" not in low
            and "is_power_of_two" not in low,
            (((1,), True), ((10,), False), ((16,), True), ((24,), False), ((46,), True)),
        ),
        T(
            "prime_number_of_set_bits",
            "def prime_number_of_set_bits(left, right):\n"
            '    """Count integers in [left,right] whose popcount is prime."""\n'
            "    primes = {2, 3, 5, 7, 11, 13, 17, 19}\n"
            "    return sum(bin(i).count('1') in primes for i in range(int(left), int(right) + 1))\n",
            lambda low: bool(
                re.search(
                    r"\bprime number of set bits\b|"
                    r"\bprime_number_of_set_bits\b|"
                    r"\bprime number of set bit\b",
                    low,
                )
            )
            and "hamming" not in low
            and "count bits" not in low
            and "count_bits" not in low,
            (((6, 10), 4), ((10, 15), 5)),
        ),
        T(
            "valid_square",
            "def valid_square(p1, p2, p3, p4):\n"
            '    """True if four points form a square (nonzero side)."""\n'
            "    pts = [tuple(p1), tuple(p2), tuple(p3), tuple(p4)]\n"
            "    if len(set(pts)) != 4:\n"
            "        return False\n"
            "    dists = []\n"
            "    for i in range(4):\n"
            "        for j in range(i + 1, 4):\n"
            "            dx = pts[i][0] - pts[j][0]\n"
            "            dy = pts[i][1] - pts[j][1]\n"
            "            dists.append(dx * dx + dy * dy)\n"
            "    dists.sort()\n"
            "    return dists[0] > 0 and dists[0] == dists[1] == dists[2] == dists[3] and dists[4] == dists[5] and dists[4] == 2 * dists[0]\n",
            lambda low: bool(
                re.search(r"\bvalid square\b|\bvalid_square\b", low)
            )
            and "perfect square" not in low
            and "sudoku" not in low
            and "magic" not in low,
            (
                (([0, 0], [1, 1], [1, 0], [0, 1]), True),
                (([0, 0], [1, 1], [1, 0], [0, 12]), False),
                (([1, 0], [-1, 0], [0, 1], [0, -1]), True),
            ),
        ),
        T(
            "complex_number_multiply",
            "def complex_number_multiply(num1, num2):\n"
            '    """Multiply two complex numbers given as a+bi strings."""\n'
            "    def parse(s):\n"
            "        a, b = str(s).replace('i', '').split('+')\n"
            "        return int(a), int(b)\n"
            "    a, b = parse(num1)\n"
            "    c, d = parse(num2)\n"
            "    return f'{a*c - b*d}+{a*d + b*c}i'\n",
            lambda low: bool(
                re.search(
                    r"\bcomplex number multiply\b|"
                    r"\bcomplex_number_multiply\b|"
                    r"\bmultiply complex\b",
                    low,
                )
            )
            and "dot" not in low,
            ((("1+1i", "1+1i"), "0+2i"), (("1+-1i", "1+-1i"), "0+-2i")),
        ),
        T(
            "convert_to_base7",
            "def convert_to_base7(num):\n"
            '    """Convert integer num to base-7 string."""\n'
            "    n = int(num)\n"
            "    if n == 0:\n"
            "        return '0'\n"
            "    sign = '-' if n < 0 else ''\n"
            "    n = abs(n)\n"
            "    digits = []\n"
            "    while n:\n"
            "        digits.append(str(n % 7))\n"
            "        n //= 7\n"
            "    return sign + ''.join(reversed(digits))\n",
            lambda low: bool(
                re.search(
                    r"\bconvert to base 7\b|"
                    r"\bconvert_to_base7\b|"
                    r"\bbase 7\b|"
                    r"\bbase-7\b|"
                    r"\bbase7\b",
                    low,
                )
            )
            and "base 2" not in low
            and "hex" not in low,
            (((100,), "202"), ((-7,), "-10")),
        ),
    ]
