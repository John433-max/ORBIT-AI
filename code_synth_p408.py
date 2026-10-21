"""Cycle 408: delete/remove/pop a key from a dict (not dict_keys).

dict_keys previously matched any "key"+"dict" phrase, so
"write a function that deletes a key from a dict" returned list(d.keys()).
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "delete_key",
            "def delete_key(d, key):\n"
            '    """Return a new dict with key removed (original unchanged)."""\n'
            "    out = dict(d)\n"
            "    out.pop(key, None)\n"
            "    return out\n",
            lambda low: (
                ("delete" in low or "remove" in low or "pop" in low or "drop" in low)
                and "key" in low
                and ("dict" in low or "dictionary" in low)
                and "node" not in low
                and "bst" not in low
                and "tree" not in low
                and "hash" not in low
            ),
            (
                (({"a": 1, "b": 2}, "a"), {"b": 2}),
                (({"a": 1}, "z"), {"a": 1}),
                (({}, "a"), {}),
            ),
        ),
    ]
