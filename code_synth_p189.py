"""Cycle 473: time, speed, area, and byte asks that fell through to NotImplemented.

Loaded first so mph is not stolen by miles_to_km and base/height area is not
stolen by point-triangle templates. Factors are exact SI / international.
"""
from __future__ import annotations

from code_synth import Template

_MPH_KPH = 1.609344  # international mile


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "hours_to_seconds",
            "def hours_to_seconds(hours):\n"
            '    """Hours to seconds (1 h = 3600 s)."""\n'
            "    return float(hours) * 3600.0\n",
            lambda low: (
                "hour" in low
                and "second" in low
                and "to second" in low
                and "minute" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 3600.0),
                ((2,), 7200.0),
            ),
        ),
        T(
            "minutes_to_seconds",
            "def minutes_to_seconds(minutes):\n"
            '    """Minutes to seconds (1 min = 60 s)."""\n'
            "    return float(minutes) * 60.0\n",
            lambda low: (
                "minute" in low
                and "second" in low
                and "to second" in low
                and "hour" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), 60.0),
                ((2.5,), 150.0),
            ),
        ),
        T(
            "seconds_to_minutes",
            "def seconds_to_minutes(seconds):\n"
            '    """Seconds to minutes (60 s = 1 min)."""\n'
            "    return float(seconds) / 60.0\n",
            lambda low: (
                "second" in low
                and "minute" in low
                and "to minute" in low
                and "hour" not in low
                and "hms" not in low
            ),
            (
                ((0,), 0.0),
                ((60,), 1.0),
                ((90,), 1.5),
            ),
        ),
        T(
            "seconds_to_hours",
            "def seconds_to_hours(seconds):\n"
            '    """Seconds to hours (3600 s = 1 h)."""\n'
            "    return float(seconds) / 3600.0\n",
            lambda low: (
                "second" in low
                and "hour" in low
                and "to hour" in low
                and "minute" not in low
            ),
            (
                ((0,), 0.0),
                ((3600,), 1.0),
                ((1800,), 0.5),
            ),
        ),
        T(
            "mph_to_kph",
            "def mph_to_kph(mph):\n"
            '    """Miles per hour to kilometres per hour (1 mph = 1.609344 km/h)."""\n'
            "    return round(float(mph) * 1.609344, 10)\n",
            lambda low: (
                ("mph" in low or "per hour" in low or "miles per hour" in low)
                and ("kph" in low or "km/h" in low or "kilometer" in low or "kilometre" in low)
                and "to mile" not in low
            ),
            (
                ((0,), 0.0),
                ((1,), round(_MPH_KPH, 10)),
                ((10,), round(10 * _MPH_KPH, 10)),
            ),
        ),
        T(
            "triangle_area_base_height",
            "def triangle_area_base_height(base, height):\n"
            '    """Area of a triangle from base and height (b*h/2)."""\n'
            "    return float(base) * float(height) / 2.0\n",
            lambda low: (
                "triangle" in low
                and "area" in low
                and ("base" in low or "height" in low)
                and "point" not in low
                and "heron" not in low
                and "largest" not in low
            ),
            (
                ((4, 3), 6.0),
                ((0, 5), 0.0),
                ((10, 2), 10.0),
            ),
        ),
        T(
            "bytes_to_kilobytes",
            "def bytes_to_kilobytes(n_bytes):\n"
            '    """Bytes to kibibytes (1 KiB = 1024 bytes)."""\n'
            "    return float(n_bytes) / 1024.0\n",
            lambda low: (
                "byte" in low
                and ("kilobyte" in low or "kibibyte" in low)
                and "to kilo" in low
                and "human" not in low
            ),
            (
                ((0,), 0.0),
                ((1024,), 1.0),
                ((512,), 0.5),
            ),
        ),
    ]
