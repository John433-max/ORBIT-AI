"""Cycle 474: hour/day/week conversions and simple geometry that fell through.

Loaded before p189 so minute/hour asks are not claimed by seconds converters.
Factors are exact SI (60 min/h, 24 h/day, 7 day/week). Trapezoid area is
(a+b)/2*h, distinct from triangle base/height.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "hours_to_minutes",
            "def hours_to_minutes(hours):\n"
            '    """Hours to minutes (1 h = 60 min)."""\n'
            "    return float(hours) * 60.0\n",
            lambda low: (
                "hour" in low
                and "minute" in low
                and "to minute" in low
                and "second" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 60.0),
                ((2.5,), 150.0),
            ),
        ),
        T(
            "minutes_to_hours",
            "def minutes_to_hours(minutes):\n"
            '    """Minutes to hours (60 min = 1 h)."""\n'
            "    return float(minutes) / 60.0\n",
            lambda low: (
                "minute" in low
                and "hour" in low
                and "to hour" in low
                and "second" not in low
            ),
            (
                ((0,), 0.0),
                ((60,), 1.0),
                ((90,), 1.5),
            ),
        ),
        T(
            "days_to_hours",
            "def days_to_hours(days):\n"
            '    """Days to hours (1 day = 24 h)."""\n'
            "    return float(days) * 24.0\n",
            lambda low: (
                "day" in low
                and "hour" in low
                and "to hour" in low
                and "week" not in low
                and "second" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 24.0),
                ((2,), 48.0),
            ),
        ),
        T(
            "weeks_to_days",
            "def weeks_to_days(weeks):\n"
            '    """Weeks to days (1 week = 7 days)."""\n'
            "    return float(weeks) * 7.0\n",
            lambda low: (
                "week" in low
                and "day" in low
                and "to day" in low
                and "hour" not in low
                and "second" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 7.0),
                ((3,), 21.0),
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
                and "area" not in low
            ),
            (
                ((0, 0), 0.0),
                ((3, 4), 14.0),
                ((1.5, 2.5), 8.0),
            ),
        ),
        T(
            "trapezoid_area",
            "def trapezoid_area(a, b, height):\n"
            '    """Area of a trapezoid ((a + b) / 2 * height)."""\n'
            "    return (float(a) + float(b)) / 2.0 * float(height)\n",
            lambda low: (
                "trapezoid" in low
                and "area" in low
                and "triangle" not in low
            ),
            (
                ((3, 5, 4), 16.0),
                ((2, 2, 3), 6.0),
                ((0, 4, 2), 4.0),
            ),
        ),
    ]
