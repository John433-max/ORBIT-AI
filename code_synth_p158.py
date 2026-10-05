"""Cycle 439: dictionary helpers that were falling through to the draft stub.

Matchers require dict/dictionary (and zip/merge/invert phrases) so they do not
steal merge-intervals, alien-dictionary, or linked-list zip templates.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "merge_dicts",
            "def merge_dicts(left, right):\n"
            '    """Return a new dict; keys in right override left."""\n'
            "    out = dict(left)\n"
            "    out.update(right)\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bmerg(?:e|es|ing)\b", low)
                and re.search(r"\bdict(?:ionary|ionaries)?\b", low)
            )
            and "interval" not in low
            and "sorted" not in low
            and "k list" not in low,
            (
                (({"a": 1}, {"b": 2}), {"a": 1, "b": 2}),
                (({"a": 1, "b": 2}, {"b": 9, "c": 3}), {"a": 1, "b": 9, "c": 3}),
            ),
        ),
        T(
            "keys_sorted_by_value",
            "def keys_sorted_by_value(mapping):\n"
            '    """Return keys ordered by value, then by key string."""\n'
            "    return [k for k, _v in sorted(mapping.items(), key=lambda kv: (kv[1], str(kv[0])))]\n",
            lambda low: "sorted by value" in low
            and bool(re.search(r"\b(dict|dictionary|keys)\b", low)),
            (
                (({"b": 2, "a": 1, "c": 2},), ["a", "b", "c"]),
                (({"z": 1, "a": 3},), ["z", "a"]),
            ),
        ),
        T(
            "invert_dict",
            "def invert_dict(mapping):\n"
            '    """Swap keys and values. Later duplicate values win."""\n'
            "    return {v: k for k, v in mapping.items()}\n",
            lambda low: (
                ("invert" in low and bool(re.search(r"\bdict", low)))
                or ("swap" in low and "key" in low and "value" in low)
            )
            and "alien" not in low,
            (
                (({"a": 1, "b": 2},), {1: "a", 2: "b"}),
                (({"x": "y"},), {"y": "x"}),
            ),
        ),
        T(
            "zip_to_dict",
            "def zip_to_dict(keys, values):\n"
            '    """Zip two sequences into a dict; extra keys without values are dropped."""\n'
            "    return dict(zip(keys, values))\n",
            lambda low: "zip" in low
            and bool(re.search(r"\bdict", low))
            and bool(re.search(r"\blists?\b", low))
            and "linked" not in low,
            (
                ((["a", "b"], [1, 2]), {"a": 1, "b": 2}),
                ((["a", "b", "c"], [1]), {"a": 1}),
            ),
        ),
    ]
