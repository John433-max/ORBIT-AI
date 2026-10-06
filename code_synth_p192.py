"""Cycle 475: leftover SI time spans and solid geometry that fell through.

Loaded before p189/p191 so week→hours is not claimed by weeks→days and
day→seconds is not claimed by hours→seconds. Factors are exact:
1 week = 168 h, 1 day = 86400 s. Volumes use pi rounded to 6 decimals,
matching sphere_volume.
"""
from __future__ import annotations

from code_synth import Template

_PI = 3.141592653589793


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "weeks_to_hours",
            "def weeks_to_hours(weeks):\n"
            '    """Weeks to hours (1 week = 7*24 = 168 h)."""\n'
            "    return float(weeks) * 168.0\n",
            lambda low: (
                "week" in low
                and "hour" in low
                and "to hour" in low
                and "day" not in low
                and "minute" not in low
                and "second" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 168.0),
                ((2,), 336.0),
            ),
        ),
        T(
            "days_to_seconds",
            "def days_to_seconds(days):\n"
            '    """Days to seconds (1 day = 86400 s)."""\n'
            "    return float(days) * 86400.0\n",
            lambda low: (
                "day" in low
                and "second" in low
                and "to second" in low
                and "hour" not in low
                and "minute" not in low
                and "week" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 86400.0),
                ((2,), 172800.0),
            ),
        ),
        T(
            "cylinder_volume",
            "def cylinder_volume(r, h):\n"
            '    """Right circular cylinder volume pi*r^2*h, rounded to 6 decimals."""\n'
            f"    return round({_PI} * float(r) ** 2 * float(h), 6)\n",
            lambda low: (
                "cylinder" in low
                and "volume" in low
                and "surface" not in low
                and "cone" not in low
            ),
            (
                ((1, 1), 3.141593),
                ((0, 5), 0.0),
                ((2, 3), 37.699112),
            ),
        ),
        T(
            "cone_volume",
            "def cone_volume(r, h):\n"
            '    """Right circular cone volume (1/3)*pi*r^2*h, rounded to 6 decimals."""\n'
            f"    return round((1.0 / 3.0) * {_PI} * float(r) ** 2 * float(h), 6)\n",
            lambda low: (
                "cone" in low
                and "volume" in low
                and "surface" not in low
                and "cylinder" not in low
            ),
            (
                ((3, 4), 37.699112),
                ((0, 5), 0.0),
                ((1, 3), 3.141593),
            ),
        ),
        T(
            "cube_surface_area",
            "def cube_surface_area(a):\n"
            '    """Cube surface area 6*a^2."""\n'
            "    return 6.0 * float(a) ** 2\n",
            lambda low: (
                "cube" in low
                and "surface" in low
                and "volume" not in low
                and "stacked" not in low
                and "grid" not in low
            ),
            (
                ((1,), 6.0),
                ((0,), 0.0),
                ((3,), 54.0),
            ),
        ),
        T(
            "sphere_surface_area",
            "def sphere_surface_area(r):\n"
            '    """Sphere surface area 4*pi*r^2, rounded to 6 decimals."""\n'
            f"    return round(4.0 * {_PI} * float(r) ** 2, 6)\n",
            lambda low: (
                "sphere" in low
                and "surface" in low
                and "volume" not in low
            ),
            (
                ((1,), 12.566371),
                ((0,), 0.0),
                ((2,), 50.265482),
            ),
        ),
    ]
