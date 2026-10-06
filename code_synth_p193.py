"""Cycle 476: leftover solid/perimeter asks and hex→decimal.

Loaded before p192 so cylinder surface is not confused with cylinder volume
and cube volume is not claimed by cube surface. Total cylinder surface is
2*pi*r*(h+r). Hex uses int(s, 16); direction requires "to decimal".
"""
from __future__ import annotations

from code_synth import Template

_PI = 3.141592653589793


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "cube_volume",
            "def cube_volume(a):\n"
            '    """Cube volume a^3."""\n'
            "    return float(a) ** 3\n",
            lambda low: (
                "cube" in low
                and "volume" in low
                and "surface" not in low
                and "stacked" not in low
                and "grid" not in low
            ),
            (
                ((0,), 0.0),
                ((2,), 8.0),
                ((3,), 27.0),
            ),
        ),
        T(
            "triangle_perimeter",
            "def triangle_perimeter(a, b, c):\n"
            '    """Perimeter of a triangle (a + b + c)."""\n'
            "    return float(a) + float(b) + float(c)\n",
            lambda low: (
                "triangle" in low
                and "perimeter" in low
                and "area" not in low
                and "rectangle" not in low
            ),
            (
                ((3, 4, 5), 12.0),
                ((0, 0, 0), 0.0),
                ((2, 2, 2), 6.0),
            ),
        ),
        T(
            "parallelogram_area",
            "def parallelogram_area(base, height):\n"
            '    """Parallelogram area base*height."""\n'
            "    return float(base) * float(height)\n",
            lambda low: (
                "parallelogram" in low
                and "area" in low
                and "perimeter" not in low
                and "triangle" not in low
                and "trapezoid" not in low
            ),
            (
                ((4, 5), 20.0),
                ((0, 9), 0.0),
                ((1.5, 2), 3.0),
            ),
        ),
        T(
            "cylinder_surface_area",
            "def cylinder_surface_area(r, h):\n"
            '    """Total cylinder surface 2*pi*r*(h+r), rounded to 6 decimals."""\n'
            f"    return round(2.0 * {_PI} * float(r) * (float(h) + float(r)), 6)\n",
            lambda low: (
                "cylinder" in low
                and "surface" in low
                and "volume" not in low
                and "cone" not in low
            ),
            (
                ((1, 1), 12.566371),
                ((0, 5), 0.0),
                ((2, 3), 62.831853),
            ),
        ),
        T(
            "hex_to_decimal",
            "def hex_to_decimal(digits):\n"
            '    """Hex digit string to int. Leading minus is honored."""\n'
            "    s = str(digits).strip().lower()\n"
            "    if s.startswith('0x'):\n"
            "        s = s[2:]\n"
            "    if s.startswith('-'):\n"
            "        return -hex_to_decimal(s[1:])\n"
            "    return int(s, 16)\n",
            lambda low: (
                ("hex" in low or "hexadecimal" in low)
                and "decimal" in low
                and "to decimal" in low
                and "to hex" not in low
                and "rgb" not in low
            ),
            (
                (("ff",), 255),
                (("0",), 0),
                (("1a",), 26),
            ),
        ),
        T(
            "square_perimeter",
            "def square_perimeter(a):\n"
            '    """Square perimeter 4*a."""\n'
            "    return 4.0 * float(a)\n",
            lambda low: (
                "square" in low
                and "perimeter" in low
                and "rectangle" not in low
                and "cube" not in low
                and "area" not in low
            ),
            (
                ((1,), 4.0),
                ((0,), 0.0),
                ((3,), 12.0),
            ),
        ),
    ]
