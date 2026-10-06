"""Cycle 474: acre, day/hour, and rectangle asks that fell through to NotImplemented.

Loaded first so day/hour phrases are not stolen by hours↔seconds templates.
International acre is 43560 ft² with 1 ft = 0.3048 m exactly (NIST SP 811).
"""
from __future__ import annotations

from code_synth import Template

# 1 international acre = 43560 * 0.3048**2 m²
_ACRE_M2 = 4046.8564224


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "acres_to_square_meters",
            "def acres_to_square_meters(acres):\n"
            '    """International acres to square meters (1 acre = 4046.8564224 m²)."""\n'
            "    return float(acres) * 4046.8564224\n",
            lambda low: (
                "acre" in low
                and "to square meter" in low
            ),
            (
                ((0,), 0.0),
                ((1,), 4046.8564224),
                ((2,), 8093.7128448),
            ),
        ),
        T(
            "square_meters_to_acres",
            "def square_meters_to_acres(square_meters):\n"
            '    """Square meters to international acres (1 acre = 4046.8564224 m²)."""\n'
            "    return float(square_meters) / 4046.8564224\n",
            lambda low: (
                "acre" in low
                and "square meter" in low
                and "to acre" in low
            ),
            (
                ((0,), 0.0),
                ((4046.8564224,), 1.0),
                ((8093.7128448,), 2.0),
            ),
        ),
        T(
            "days_to_hours",
            "def days_to_hours(days):\n"
            '    """Days to hours (1 day = 24 h)."""\n'
            "    return float(days) * 24.0\n",
            lambda low: (
                "day" in low
                and "to hour" in low
                and "week" not in low
                and "second" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 24.0),
                ((1.5,), 36.0),
            ),
        ),
        T(
            "hours_to_days",
            "def hours_to_days(hours):\n"
            '    """Hours to days (24 h = 1 day)."""\n'
            "    return float(hours) / 24.0\n",
            lambda low: (
                "hour" in low
                and "to day" in low
                and "second" not in low
                and "minute" not in low
                and "week" not in low
            ),
            (
                ((0,), 0.0),
                ((24,), 1.0),
                ((36,), 1.5),
            ),
        ),
        T(
            "weeks_to_days",
            "def weeks_to_days(weeks):\n"
            '    """Weeks to days (1 week = 7 days)."""\n'
            "    return float(weeks) * 7.0\n",
            lambda low: (
                "week" in low
                and "to day" in low
                and "hour" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 7.0),
                ((2,), 14.0),
            ),
        ),
        T(
            "rectangle_area",
            "def rectangle_area(width, height):\n"
            '    """Area of a rectangle (width * height)."""\n'
            "    return float(width) * float(height)\n",
            lambda low: (
                "rectangle" in low
                and "area" in low
                and "perimeter" not in low
                and "triangle" not in low
            ),
            (
                ((0, 5), 0.0),
                ((3, 4), 12.0),
                ((2.5, 2), 5.0),
            ),
        ),
        T(
            "rectangle_perimeter",
            "def rectangle_perimeter(width, height):\n"
            '    """Perimeter of a rectangle (2 * (width + height))."""\n'
            "    return 2.0 * (float(width) + float(height))\n",
            lambda low: (
                "rectangle" in low
                and "perimeter" in low
                and "triangle" not in low
            ),
            (
                ((0, 0), 0.0),
                ((3, 4), 14.0),
                ((2.5, 1.5), 8.0),
            ),
        ),
    ]
