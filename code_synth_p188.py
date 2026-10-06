"""Cycle 472: volume, length, and temperature conversions that fell through.

Loaded first so gallon/yard/kelvin asks are not stolen by broader matchers.
Constants follow NIST SP 811 exact international definitions.
"""
from __future__ import annotations

from code_synth import Template

# US liquid gallon (NIST): exactly 231 in^3 = 3.785411784 L
_GAL_L = 3.785411784
# International yard (NIST): exactly 0.9144 m
_YARD_M = 0.9144


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "liters_to_gallons",
            "def liters_to_gallons(liters):\n"
            '    """Litres to US liquid gallons (1 gal = 3.785411784 L)."""\n'
            "    return round(float(liters) / 3.785411784, 10)\n",
            lambda low: (
                ("liter" in low or "litre" in low)
                and "gallon" in low
                and ("to gallon" in low or "to us gallon" in low)
                and "to liter" not in low
                and "to litre" not in low
            ),
            (
                ((3.785411784,), 1.0),
                ((0,), 0.0),
                ((1,), round(1 / _GAL_L, 10)),
            ),
        ),
        T(
            "gallons_to_liters",
            "def gallons_to_liters(gallons):\n"
            '    """US liquid gallons to litres (1 gal = 3.785411784 L)."""\n'
            "    return round(float(gallons) * 3.785411784, 10)\n",
            lambda low: (
                "gallon" in low
                and ("liter" in low or "litre" in low)
                and ("to liter" in low or "to litre" in low)
            ),
            (
                ((1,), 3.785411784),
                ((0,), 0.0),
                ((2,), round(2 * _GAL_L, 10)),
            ),
        ),
        T(
            "yards_to_meters",
            "def yards_to_meters(yards):\n"
            '    """International yards to metres (1 yd = 0.9144 m)."""\n'
            "    return round(float(yards) * 0.9144, 10)\n",
            lambda low: (
                "yard" in low
                and ("meter" in low or "metre" in low)
                and "kilo" not in low
                and ("to meter" in low or "to metre" in low)
                and "to yard" not in low
            ),
            (
                ((1,), 0.9144),
                ((0,), 0.0),
                ((2,), round(2 * _YARD_M, 10)),
            ),
        ),
        T(
            "meters_to_yards",
            "def meters_to_yards(meters):\n"
            '    """Metres to international yards (1 yd = 0.9144 m)."""\n'
            "    return round(float(meters) / 0.9144, 10)\n",
            lambda low: (
                ("meter" in low or "metre" in low)
                and "yard" in low
                and "kilo" not in low
                and "foot" not in low
                and "feet" not in low
                and ("to yard" in low or "to yards" in low)
            ),
            (
                ((0.9144,), 1.0),
                ((0,), 0.0),
                ((1,), round(1 / _YARD_M, 10)),
            ),
        ),
        T(
            "kelvin_to_fahrenheit",
            "def kelvin_to_fahrenheit(kelvin):\n"
            '    """Kelvin to Fahrenheit. F = (K - 273.15) * 9/5 + 32."""\n'
            "    return round((float(kelvin) - 273.15) * 9 / 5 + 32, 10)\n",
            lambda low: (
                "kelvin" in low
                and "fahrenheit" in low
                and "to fahrenheit" in low
                and "to kelvin" not in low
            ),
            (
                ((273.15,), 32.0),
                ((0,), -459.67),
                ((373.15,), 212.0),
            ),
        ),
        T(
            "km_to_meters",
            "def km_to_meters(km):\n"
            '    """Kilometres to metres (1 km = 1000 m)."""\n'
            "    return round(float(km) * 1000, 10)\n",
            lambda low: (
                ("kilometer" in low or "kilometre" in low or " km" in low)
                and ("meter" in low or "metre" in low)
                and "mile" not in low
                and "foot" not in low
                and "feet" not in low
                and "yard" not in low
                and ("to meter" in low or "to metre" in low or "to meters" in low)
                and "to km" not in low
                and "to kilometer" not in low
            ),
            (
                ((1,), 1000.0),
                ((0,), 0.0),
                ((1.5,), 1500.0),
            ),
        ),
    ]
