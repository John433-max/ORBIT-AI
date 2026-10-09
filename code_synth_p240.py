"""Cycle 543: JSON file/object key listing.

"write code that reads a json file and returns the keys" was a draft stub
(`write_code_that_reads_a_json_file_and_re`). Accept a JSON object string
or an existing file path. No network.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "json_keys",
            "def json_keys(source):\n"
            '    """Return keys of a JSON object given as text or a file path."""\n'
            "    import json\n"
            "    import os\n"
            "    text = source\n"
            "    if isinstance(source, str) and os.path.isfile(source):\n"
            "        with open(source, encoding=\"utf-8\") as handle:\n"
            "            text = handle.read()\n"
            "    data = json.loads(text)\n"
            "    if not isinstance(data, dict):\n"
            "        raise ValueError(\"JSON root must be an object\")\n"
            "    return list(data.keys())\n",
            lambda low: bool(
                re.search(r"\bjson\b", low)
                and re.search(r"\bkeys?\b", low)
                and re.search(r"\b(file|read|reads|load|loads|parse|parses)\b", low)
            )
            and "schema" not in low
            and "stringify" not in low
            and "dumps" not in low,
            (
                (('{"a": 1, "b": 2}',), ["a", "b"]),
                (('{"z": true}',), ["z"]),
            ),
        ),
    ]
