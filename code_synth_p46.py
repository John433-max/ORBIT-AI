"""Cycle 308: senior citizens / sum of multiples / convert temperature / equal pairs / letter percent / employees target."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "count_seniors",
            "def count_seniors(details):\n"
            '    """Count passengers older than 60 from 15-char tickets (LeetCode 2678)."""\n'
            "    return sum(int(s[11:13]) > 60 for s in details)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]of[_ ]senior[_ ]citizens\b|"
                    r"\bcount[_ ]senior[_ ]citizens\b|"
                    r"\bcount_seniors\b",
                    low,
                )
            ),
            (
                ((["7868190130M7522", "5303914400F9211", "9273338290F4010"],), 2),
                ((["1313579440F2036", "2921522980M5644"],), 0),
                ((["5612624052M0130"],), 0),
            ),
        ),
        T(
            "sum_of_multiples",
            "def sum_of_multiples(n):\n"
            '    """Sum of positives <= n divisible by 3, 5, or 7 (LeetCode 2652)."""\n'
            "    n = int(n)\n"
            "    return sum(i for i in range(1, n + 1) if i % 3 == 0 or i % 5 == 0 or i % 7 == 0)\n",
            lambda low: bool(
                re.search(
                    r"\bsum[_ ](of[_ ])?multiples\b|"
                    r"\bsum_of_multiples\b",
                    low,
                )
            ),
            (
                ((7,), 21),
                ((10,), 40),
                ((9,), 30),
            ),
        ),
        T(
            "convert_temperature",
            "def convert_temperature(celsius):\n"
            '    """Return [kelvin, fahrenheit] from celsius (LeetCode 2469)."""\n'
            "    c = float(celsius)\n"
            "    return [c + 273.15, c * 1.80 + 32.00]\n",
            lambda low: bool(
                re.search(
                    r"\bconvert[_ ]the[_ ]temperature\b|"
                    r"\bconvert[_ ]temperature\b|"
                    r"\bcelsius to kelvin and fahrenheit\b|"
                    r"\bconvert_temperature\b",
                    low,
                )
            ),
            (
                ((36.50,), [309.65, 97.7]),
                ((122.11,), [395.26, 251.798]),
                ((0.0,), [273.15, 32.0]),
            ),
        ),
        T(
            "divide_array_equal_pairs",
            "def divide_array_equal_pairs(nums):\n"
            '    """True if nums can be split into equal pairs (LeetCode 2206)."""\n'
            "    from collections import Counter\n"
            "    return all(v % 2 == 0 for v in Counter(nums).values())\n",
            lambda low: bool(
                re.search(
                    r"\bdivide[_ ]array[_ ]into[_ ]equal[_ ]pairs\b|"
                    r"\bdivide_array_equal_pairs\b",
                    low,
                )
            ),
            (
                (([3, 2, 3, 2, 2, 2],), True),
                (([1, 2, 3, 4],), False),
                (([1, 1],), True),
            ),
        ),
        T(
            "percentage_of_letter",
            "def percentage_of_letter(s, letter):\n"
            '    """Floor percent of characters equal to letter (LeetCode 2278)."""\n'
            "    if not s:\n"
            "        return 0\n"
            "    return (sum(ch == letter for ch in s) * 100) // len(s)\n",
            lambda low: bool(
                re.search(
                    r"\bpercentage[_ ]of[_ ]letter[_ ]in[_ ]string\b|"
                    r"\bpercentage[_ ]of[_ ]letter\b|"
                    r"\bpercentage_of_letter\b",
                    low,
                )
            ),
            (
                (("foobar", "o"), 33),
                (("jjjj", "k"), 0),
                (("sgowz", "s"), 20),
            ),
        ),
        T(
            "number_of_employees_who_met_target",
            "def number_of_employees_who_met_target(hours, target):\n"
            '    """Employees with hours >= target (LeetCode 2798)."""\n'
            "    t = int(target)\n"
            "    return sum(h >= t for h in hours)\n",
            lambda low: bool(
                re.search(
                    r"\bnumber[_ ]of[_ ]employees[_ ]who[_ ]met[_ ]the[_ ]target\b|"
                    r"\bemployees[_ ]who[_ ]met[_ ](the[_ ])?target\b|"
                    r"\bnumber_of_employees_who_met_target\b",
                    low,
                )
            ),
            (
                (([0, 1, 2, 3, 4], 2), 3),
                (([5, 1, 4, 2, 2], 6), 0),
                (([10], 10), 1),
            ),
        ),
    ]
