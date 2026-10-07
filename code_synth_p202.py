"""Cycle 486: prefix/suffix checks, strip prefix/suffix, repeat string, every nth.

Matchers stay phrase-specific so prefix-count, remove-nth-from-end, and
repeated-substring templates keep their asks.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "starts_with",
            "def starts_with(s, prefix):\n"
            '    """True if s begins with prefix. Empty prefix is always True."""\n'
            "    s, prefix = str(s), str(prefix)\n"
            "    return s.startswith(prefix)\n",
            lambda low: "start" in low
            and "prefix" in low
            and "string" in low
            and "remove" not in low
            and "common" not in low
            and "word" not in low,
            (
                (("orbit", "or"), True),
                (("orbit", "bit"), False),
                (("orbit", ""), True),
            ),
        ),
        T(
            "ends_with",
            "def ends_with(s, suffix):\n"
            '    """True if s ends with suffix. Empty suffix is always True."""\n'
            "    s, suffix = str(s), str(suffix)\n"
            "    return s.endswith(suffix)\n",
            lambda low: "end" in low
            and "suffix" in low
            and "string" in low
            and "remove" not in low,
            (
                (("orbit", "it"), True),
                (("orbit", "or"), False),
                (("orbit", ""), True),
            ),
        ),
        T(
            "remove_prefix",
            "def remove_prefix(s, prefix):\n"
            '    """Drop prefix once if s starts with it; otherwise return s."""\n'
            "    s, prefix = str(s), str(prefix)\n"
            "    if prefix and s.startswith(prefix):\n"
            "        return s[len(prefix):]\n"
            "    return s\n",
            lambda low: bool(re.search(r"remov(?:e|es|ing) a prefix", low))
            and "suffix" not in low,
            (
                (("prefix-orbit", "prefix-"), "orbit"),
                (("orbit", "xyz"), "orbit"),
                (("orbit", ""), "orbit"),
            ),
        ),
        T(
            "remove_suffix",
            "def remove_suffix(s, suffix):\n"
            '    """Drop suffix once if s ends with it; otherwise return s."""\n'
            "    s, suffix = str(s), str(suffix)\n"
            "    if suffix and s.endswith(suffix):\n"
            "        return s[: -len(suffix)]\n"
            "    return s\n",
            lambda low: bool(re.search(r"remov(?:e|es|ing) a suffix", low))
            and "prefix" not in low,
            (
                (("orbit.txt", ".txt"), "orbit"),
                (("orbit", ".txt"), "orbit"),
                (("orbit", ""), "orbit"),
            ),
        ),
        T(
            "repeat_string",
            "def repeat_string(s, n):\n"
            '    """Repeat s n times. Non-positive n returns an empty string."""\n'
            "    n = int(n)\n"
            "    if n <= 0:\n"
            "        return ''\n"
            "    return str(s) * n\n",
            lambda low: bool(re.search(r"repeats? a string", low))
            and "substring" not in low
            and "element" not in low
            and "pattern" not in low,
            (
                (("ab", 3), "ababab"),
                (("x", 0), ""),
                (("", 4), ""),
            ),
        ),
        T(
            "every_nth",
            "def every_nth(items, n):\n"
            '    """Items at indices 0, n, 2n, ... Non-positive n returns []."""\n'
            "    n = int(n)\n"
            "    if n <= 0:\n"
            "        return []\n"
            "    return list(items)[::n]\n",
            lambda low: bool(
                re.search(r"every n(?:th|-th| th) element", low)
            )
            and "remove" not in low,
            (
                (([0, 1, 2, 3, 4, 5], 2), [0, 2, 4]),
                (([1, 2, 3], 1), [1, 2, 3]),
                (([1, 2, 3], 0), []),
            ),
        ),
    ]
