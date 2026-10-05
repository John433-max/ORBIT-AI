"""Cycle 456: unix timestamp to ISO-8601.

Loaded first so the phrase gate beats broader date/format hits.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "unix_to_iso8601",
            "def unix_to_iso8601(ts):\n"
            '    """UTC ISO-8601 from a unix timestamp (seconds)."""\n'
            "    from datetime import datetime, timezone\n"
            "    return datetime.fromtimestamp(float(ts), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')\n",
            lambda low: (
                ("unix" in low or "epoch" in low)
                and ("iso8601" in low or "iso-8601" in low or "iso 8601" in low)
            ),
            (
                ((0,), "1970-01-01T00:00:00Z"),
                ((1_700_000_000,), "2023-11-14T22:13:20Z"),
            ),
        ),
    ]
