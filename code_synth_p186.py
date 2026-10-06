"""Cycle 469: radix sort, interest, and length/mass conversions that fell through.

Loaded first so radix sort does not become a stub, and inches/cm does not miss.
"""
from __future__ import annotations

from code_synth import Template

_INCH_CM = 2.54
_LB_KG = 0.45359237
_FT_M = 0.3048


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "radix_sort",
            "def radix_sort(nums):\n"
            '    """LSD radix sort (base 10) for non-negative integers. New list."""\n'
            "    xs = [int(x) for x in nums]\n"
            "    if not xs:\n"
            "        return []\n"
            "    if any(x < 0 for x in xs):\n"
            "        raise ValueError('radix sort expects non-negative ints')\n"
            "    out = xs\n"
            "    exp = 1\n"
            "    max_v = max(xs)\n"
            "    while max_v // exp:\n"
            "        buckets = [[] for _ in range(10)]\n"
            "        for x in out:\n"
            "            buckets[(x // exp) % 10].append(x)\n"
            "        out = [v for bucket in buckets for v in bucket]\n"
            "        exp *= 10\n"
            "    return out\n",
            lambda low: "radix sort" in low or "radixsort" in low or "lsd sort" in low,
            (
                (([170, 45, 75, 90, 802, 24, 2, 66],), [2, 24, 45, 66, 75, 90, 170, 802]),
                (([],), []),
                (([0, 10, 1],), [0, 1, 10]),
            ),
        ),
        T(
            "compound_interest",
            "def compound_interest(principal, rate, years):\n"
            '    """Future value A = P*(1+r)**t. Rate is a decimal (0.05 = 5%)."""\n'
            "    return round(float(principal) * (1.0 + float(rate)) ** float(years), 10)\n",
            lambda low: "compound interest" in low,
            (
                ((1000, 0.1, 2), 1210.0),
                ((100, 0.0, 5), 100.0),
                ((200, 0.05, 1), 210.0),
            ),
        ),
        T(
            "simple_interest",
            "def simple_interest(principal, rate, time):\n"
            '    """Interest I = P*r*t. Rate is a decimal (0.05 = 5%), not a percent."""\n'
            "    return round(float(principal) * float(rate) * float(time), 10)\n",
            lambda low: (
                "simple interest" in low
                or "interest on a principal" in low
                or "interest on principal" in low
            ),
            (
                ((1000, 0.05, 2), 100.0),
                ((500, 0.1, 1), 50.0),
                ((100, 0.0, 10), 0.0),
            ),
        ),
        T(
            "inches_to_cm",
            "def inches_to_cm(inches):\n"
            '    """International inch to centimetres (1 in = 2.54 cm)."""\n'
            "    return round(float(inches) * 2.54, 10)\n",
            lambda low: (
                ("inch" in low)
                and ("cm" in low or "centimet" in low)
                and ("to cm" in low or "to cent" in low or "in cm" in low or "into cm" in low)
            ),
            (
                ((1,), 2.54),
                ((0,), 0.0),
                ((10,), 25.4),
            ),
        ),
        T(
            "cm_to_inches",
            "def cm_to_inches(cm):\n"
            '    """Centimetres to international inches (1 in = 2.54 cm)."""\n'
            "    return round(float(cm) / 2.54, 10)\n",
            lambda low: (
                ("inch" in low)
                and ("cm" in low or "centimet" in low)
                and ("cm to" in low or "centimet" in low and "to inch" in low)
            ),
            (
                ((2.54,), 1.0),
                ((0,), 0.0),
                ((25.4,), 10.0),
            ),
        ),
        T(
            "pounds_to_kg",
            "def pounds_to_kg(pounds):\n"
            '    """Avoirdupois pound to kilograms (1 lb = 0.45359237 kg)."""\n'
            "    return round(float(pounds) * 0.45359237, 10)\n",
            lambda low: (
                ("pound" in low or "lbs" in low or " lb " in low)
                and ("kg" in low or "kilogram" in low)
                and ("to kg" in low or "to kilo" in low)
            ),
            (
                ((1,), 0.45359237),
                ((0,), 0.0),
                ((2,), 0.90718474),
            ),
        ),
        T(
            "kg_to_pounds",
            "def kg_to_pounds(kg):\n"
            '    """Kilograms to avoirdupois pounds (1 lb = 0.45359237 kg)."""\n'
            "    return round(float(kg) / 0.45359237, 10)\n",
            lambda low: (
                ("pound" in low or "lbs" in low)
                and ("kg" in low or "kilogram" in low)
                and ("kg to" in low or "kilogram" in low and "to pound" in low)
            ),
            (
                ((0.45359237,), 1.0),
                ((0,), 0.0),
                ((0.90718474,), 2.0),
            ),
        ),
        T(
            "feet_to_meters",
            "def feet_to_meters(feet):\n"
            '    """International foot to metres (1 ft = 0.3048 m)."""\n'
            "    return round(float(feet) * 0.3048, 10)\n",
            lambda low: (
                ("foot" in low or "feet" in low)
                and ("meter" in low or "metre" in low)
                and "kilo" not in low
                and ("to meter" in low or "to metre" in low)
            ),
            (
                ((1,), 0.3048),
                ((0,), 0.0),
                ((10,), 3.048),
            ),
        ),
    ]
