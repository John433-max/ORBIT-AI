"""Cycle 470: reverse length/mass conversions that still fell through.

Loaded first so meters→feet and ounces↔grams do not miss, and so the
linked-list binary integer ask is not required to live in this pack.
"""
from __future__ import annotations

from code_synth import Template

_FT_M = 0.3048
_OZ_G = 28.349523125


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "meters_to_feet",
            "def meters_to_feet(meters):\n"
            '    """Metres to international feet (1 ft = 0.3048 m)."""\n'
            "    return round(float(meters) / 0.3048, 10)\n",
            lambda low: (
                ("meter" in low or "metre" in low)
                and ("foot" in low or "feet" in low)
                and "kilo" not in low
                and ("to foot" in low or "to feet" in low)
            ),
            (
                ((0.3048,), 1.0),
                ((0,), 0.0),
                ((3.048,), 10.0),
            ),
        ),
        T(
            "ounces_to_grams",
            "def ounces_to_grams(ounces):\n"
            '    """Avoirdupois ounces to grams (1 oz = 28.349523125 g)."""\n'
            "    return round(float(ounces) * 28.349523125, 10)\n",
            lambda low: (
                ("ounce" in low or "oz" in low)
                and ("gram" in low or " g" in low)
                and ("to gram" in low or "to g" in low or "ounces to" in low)
                and "kilogram" not in low
            ),
            (
                ((1,), 28.349523125),
                ((0,), 0.0),
                ((2,), 56.69904625),
            ),
        ),
        T(
            "grams_to_ounces",
            "def grams_to_ounces(grams):\n"
            '    """Grams to avoirdupois ounces (1 oz = 28.349523125 g)."""\n'
            "    return round(float(grams) / 28.349523125, 10)\n",
            lambda low: (
                ("gram" in low)
                and ("ounce" in low or "oz" in low)
                and ("to ounce" in low or "to oz" in low or "grams to" in low)
                and "kilogram" not in low
            ),
            (
                ((28.349523125,), 1.0),
                ((0,), 0.0),
                ((56.69904625,), 2.0),
            ),
        ),
    ]
