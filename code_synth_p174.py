"""Cycle 456: means, ISO timestamps, one-hot, quantile, variance, duration.

Loaded before broader date/mean packs so phrase gates win.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "harmonic_mean",
            "def harmonic_mean(values):\n"
            '    """Harmonic mean. Every value must be non-zero."""\n'
            "    xs = [float(x) for x in values]\n"
            "    if not xs or any(x == 0 for x in xs):\n"
            "        raise ValueError('need non-zero values')\n"
            "    return len(xs) / sum(1.0 / x for x in xs)\n",
            lambda low: "harmonic" in low and "mean" in low,
            (
                (([1, 2, 4],), 1.7142857142857142),
                (([1, 1, 1],), 1.0),
            ),
        ),
        T(
            "unix_to_iso",
            "def unix_to_iso(ts):\n"
            '    """UTC ISO-8601 from a unix timestamp (seconds)."""\n'
            "    from datetime import datetime, timezone\n"
            "    return datetime.fromtimestamp(float(ts), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')\n",
            lambda low: (
                ("unix" in low or "epoch" in low)
                and "iso" in low
                and "to unix" not in low
                and "to a unix" not in low
                and "to epoch" not in low
            ),
            (
                ((0,), "1970-01-01T00:00:00Z"),
                ((1_700_000_000,), "2023-11-14T22:13:20Z"),
            ),
        ),
        T(
            "iso_to_unix",
            "def iso_to_unix(text):\n"
            '    """Unix seconds from a UTC ISO-8601 timestamp."""\n'
            "    from datetime import datetime, timezone\n"
            "    raw = str(text).replace('Z', '+00:00')\n"
            "    dt = datetime.fromisoformat(raw)\n"
            "    if dt.tzinfo is None:\n"
            "        dt = dt.replace(tzinfo=timezone.utc)\n"
            "    return int(dt.timestamp())\n",
            lambda low: "iso" in low and ("to unix" in low or "to a unix" in low or "to epoch" in low),
            (
                (("1970-01-01T00:00:00Z",), 0),
                (("2023-11-14T22:13:20Z",), 1_700_000_000),
            ),
        ),
        T(
            "one_hot",
            "def one_hot(index, n):\n"
            '    """Length-n one-hot vector with a 1 at index."""\n'
            "    index = int(index)\n"
            "    n = int(n)\n"
            "    if n < 1 or index < 0 or index >= n:\n"
            "        raise ValueError('index out of range')\n"
            "    return [1 if i == index else 0 for i in range(n)]\n",
            lambda low: "one-hot" in low or "one hot" in low or "onehot" in low,
            (
                ((0, 3), [1, 0, 0]),
                ((2, 4), [0, 0, 1, 0]),
            ),
        ),
        T(
            "quantile",
            "def quantile(nums, q):\n"
            '    """Linear-interpolated quantile. q is 0..1."""\n'
            "    xs = sorted(float(x) for x in nums)\n"
            "    if not xs:\n"
            "        raise ValueError('empty')\n"
            "    q = float(q)\n"
            "    if q < 0 or q > 1:\n"
            "        raise ValueError('q must be 0..1')\n"
            "    if len(xs) == 1:\n"
            "        return xs[0]\n"
            "    pos = q * (len(xs) - 1)\n"
            "    lo = int(pos)\n"
            "    hi = min(lo + 1, len(xs) - 1)\n"
            "    frac = pos - lo\n"
            "    return xs[lo] * (1 - frac) + xs[hi] * frac\n",
            lambda low: "quantile" in low and "percentile" not in low,
            (
                (([1, 2, 3, 4], 0.0), 1.0),
                (([1, 2, 3, 4], 0.5), 2.5),
                (([1, 2, 3, 4], 1.0), 4.0),
            ),
        ),
        T(
            "population_variance",
            "def population_variance(nums):\n"
            '    """Population variance (divide by n)."""\n'
            "    xs = [float(x) for x in nums]\n"
            "    if not xs:\n"
            "        raise ValueError('empty')\n"
            "    mean = sum(xs) / len(xs)\n"
            "    return sum((x - mean) ** 2 for x in xs) / len(xs)\n",
            lambda low: "population" in low and "variance" in low,
            (
                (([1, 2, 3],), 2.0 / 3.0),
                (([4, 4, 4],), 0.0),
            ),
        ),
        T(
            "singularize",
            "def singularize(word):\n"
            '    """Tiny English singularizer for regular nouns."""\n'
            "    w = str(word)\n"
            "    low = w.lower()\n"
            "    if low.endswith('ies') and len(low) > 3:\n"
            "        return w[:-3] + ('Y' if w[-3].isupper() else 'y')\n"
            "    if low.endswith(('ches', 'shes', 'sses', 'xes', 'zes')):\n"
            "        return w[:-2]\n"
            "    if low.endswith('s') and not low.endswith('ss') and len(low) > 1:\n"
            "        return w[:-1]\n"
            "    return w\n",
            lambda low: "singular" in low and "plural" not in low,
            (
                (("cats",), "cat"),
                (("babies",), "baby"),
                (("boxes",), "box"),
            ),
        ),
        T(
            "parse_duration",
            "def parse_duration(text):\n"
            '    """Parse a duration like 1h30m into seconds."""\n'
            "    import re\n"
            "    units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}\n"
            "    found = re.findall(r'(\\d+)\\s*([dhms])', str(text).lower())\n"
            "    if not found:\n"
            "        raise ValueError('no duration parts')\n"
            "    return sum(int(n) * units[u] for n, u in found)\n",
            lambda low: (
                "duration" in low
                and ("parse" in low or "into seconds" in low or "1h30m" in low)
                and "human" not in low
            ),
            (
                (("1h30m",), 5400),
                (("90s",), 90),
                (("2d",), 172800),
            ),
        ),
        T(
            "unix_to_iso8601",
            "def unix_to_iso8601(ts):\n"
            '    """UTC ISO-8601 from a unix timestamp (seconds)."""\n'
            "    from datetime import datetime, timezone\n"
            "    return datetime.fromtimestamp(float(ts), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')\n",
            lambda low: (
                ("unix" in low or "epoch" in low)
                and ("iso8601" in low or "iso-8601" in low or "iso 8601" in low)
                and "to unix" not in low
                and "to a unix" not in low
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
            ((("helloWorld",), "hello_world"), (("A",), "a")),
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
            ((("hello_world",), "helloWorld"), (("a",), "a")),
        ),
    ]
