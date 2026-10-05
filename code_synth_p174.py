"""Cycle 456: unix timestamp to ISO-8601.

Loaded first so the phrase gate beats broader date/format hits.
Cycle 457: direction-specific camel/snake converters register first (name wins).
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
        T(
            "camel_to_snake",
            "def camel_to_snake(name):\n"
            '    """Convert camelCase to snake_case."""\n'
            "    out = []\n"
            "    for i, ch in enumerate(str(name)):\n"
            "        if ch.isupper() and i:\n"
            "            out.append('_')\n"
            "            out.append(ch.lower())\n"
            "        else:\n"
            "            out.append(ch.lower())\n"
            "    return ''.join(out)\n",
            lambda low: (
                ("camel" in low and "snake" in low and "to camel" not in low and "kebab" not in low)
                or ("snake_case" in low and "convert" in low and "camel" not in low and "dict" not in low)
            ),
            (
                (("helloWorld",), "hello_world"),
                (("A",), "a"),
            ),
        ),
        T(
            "snake_to_camel",
            "def snake_to_camel(name):\n"
            '    """Convert snake_case to camelCase."""\n'
            "    parts = str(name).split('_')\n"
            "    if not parts:\n"
            "        return ''\n"
            "    return parts[0].lower() + ''.join(p.title() for p in parts[1:] if p)\n",
            lambda low: (
                "snake" in low and "camel" in low and "to snake" not in low and "kebab" not in low
            ),
            (
                (("hello_world",), "helloWorld"),
                (("a",), "a"),
            ),
        ),
    ]
