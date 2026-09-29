"""Cycle 299: permutation build / concat array / ops value / product sign / truncate sentence / tournament matches."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "build_array_from_permutation",
            "def build_array_from_permutation(nums):\n"
            '    """Build array ans[i] = nums[nums[i]] (LeetCode 1920)."""\n'
            "    return [nums[nums[i]] for i in range(len(nums))]\n",
            lambda low: bool(
                re.search(
                    r"\bbuild[_ ]array[_ ]from[_ ]permutation\b|"
                    r"\bbuild (?:an? )?array from (?:a )?permutation\b|"
                    r"\bans\[i\] ?= ?nums\[nums\[i\]\]\b",
                    low,
                )
            ),
            (
                (([0, 2, 1, 5, 3, 4],), [0, 1, 2, 4, 5, 3]),
                (([5, 0, 1, 2, 3, 4],), [4, 5, 0, 1, 2, 3]),
                (([0, 1],), [0, 1]),
            ),
        ),
        T(
            "concatenation_of_array",
            "def concatenation_of_array(nums):\n"
            '    """Return nums concatenated with itself (LeetCode 1929)."""\n'
            "    return nums + nums\n",
            lambda low: bool(
                re.search(
                    r"\bconcatenation[_ ]of[_ ]array\b|"
                    r"\bconcatenation of (?:an? )?array\b|"
                    r"\bconcatenate (?:an? )?array with itself\b",
                    low,
                )
            ),
            (
                (([1, 2, 1],), [1, 2, 1, 1, 2, 1]),
                (([1, 3, 2, 1],), [1, 3, 2, 1, 1, 3, 2, 1]),
                (([1],), [1, 1]),
            ),
        ),
        T(
            "final_value_after_operations",
            "def final_value_after_operations(operations):\n"
            '    """Final value of x after ++/-- operations (LeetCode 2011)."""\n'
            "    x = 0\n"
            "    for op in operations:\n"
            "        if '+' in op:\n"
            "            x += 1\n"
            "        else:\n"
            "            x -= 1\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bfinal[_ ]value[_ ]after[_ ]operations\b|"
                    r"\bfinal value of (?:a )?variable after (?:performing )?operations\b|"
                    r"\bfinal value after performing operations\b",
                    low,
                )
            ),
            (
                ((["--X", "X++", "X++"],), 1),
                ((["++X", "++X", "X++"],), 3),
                ((["X++", "++X", "--X", "X--"],), 0),
            ),
        ),
        T(
            "sign_of_product",
            "def sign_of_product(nums):\n"
            '    """Sign of the product of an array (LeetCode 1822)."""\n'
            "    sign = 1\n"
            "    for n in nums:\n"
            "        if n == 0:\n"
            "            return 0\n"
            "        if n < 0:\n"
            "            sign = -sign\n"
            "    return sign\n",
            lambda low: bool(
                re.search(
                    r"\bsign[_ ]of[_ ]product\b|"
                    r"\bsign of the product of an array\b|"
                    r"\bsign func(?:tion)? of (?:an? )?array product\b",
                    low,
                )
            ),
            (
                (([-1, -2, -3, -4, 3, 2, 1],), 1),
                (([1, 5, 0, 2, -3],), 0),
                (([-1, 1, -1, 1, -1],), -1),
            ),
        ),
        T(
            "truncate_sentence",
            "def truncate_sentence(s, k):\n"
            '    """Keep the first k words of the sentence (LeetCode 1816)."""\n'
            "    return ' '.join(s.split()[:k])\n",
            lambda low: bool(
                re.search(
                    r"\btruncate[_ ]sentence\b|"
                    r"\btruncate (?:a |the )?sentence\b|"
                    r"\bkeep the first k words\b",
                    low,
                )
            ),
            (
                (("Hello how are you Contestant", 4), "Hello how are you"),
                (("What is the solution to this problem", 4), "What is the solution"),
                (("chopper is not a chopper", 5), "chopper is not a chopper"),
            ),
        ),
        T(
            "count_matches",
            "def count_matches(n):\n"
            '    """Matches played in a single-elim tournament (LeetCode 1688)."""\n'
            "    return n - 1\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]matches\b|"
                    r"\bcount of matches in (?:a )?tournament\b|"
                    r"\bmatches in (?:a )?tournament\b",
                    low,
                )
            ),
            (
                ((7,), 6),
                ((14,), 13),
                ((1,), 0),
            ),
        ),
    ]
