"""Cycle 456: Levenshtein, sigmoid, log-softmax, urlencode, snake_case, Luhn.

Pack loads first so phrase gates beat broader string/math hits.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "levenshtein",
            "def levenshtein(a, b):\n"
            '    """Edit distance (insert, delete, substitute) between two strings."""\n'
            "    s, t = str(a), str(b)\n"
            "    if s == t:\n"
            "        return 0\n"
            "    if not s:\n"
            "        return len(t)\n"
            "    if not t:\n"
            "        return len(s)\n"
            "    prev = list(range(len(t) + 1))\n"
            "    for i, cs in enumerate(s, 1):\n"
            "        cur = [i]\n"
            "        for j, ct in enumerate(t, 1):\n"
            "            ins = cur[j - 1] + 1\n"
            "            delete = prev[j] + 1\n"
            "            sub = prev[j - 1] + (cs != ct)\n"
            "            cur.append(min(ins, delete, sub))\n"
            "        prev = cur\n"
            "    return prev[-1]\n",
            lambda low: "levenshtein" in low and "damerau" not in low,
            (
                (("kitten", "sitting"), 3),
                (("", "abc"), 3),
                (("same", "same"), 0),
            ),
        ),
        T(
            "sigmoid",
            "def sigmoid(x):\n"
            '    """Logistic sigmoid, rounded to 6 decimals."""\n'
            "    import math\n"
            "    z = max(-60.0, min(60.0, float(x)))\n"
            "    return round(1.0 / (1.0 + math.exp(-z)), 6)\n",
            lambda low: "sigmoid" in low and "log" not in low and "relu" not in low and "activation" not in low,
            (
                ((0,), 0.5),
                ((1,), 0.731059),
            ),
        ),
        T(
            "log_softmax",
            "def log_softmax(xs):\n"
            '    """Stable log-softmax, each value rounded to 6 decimals."""\n'
            "    import math\n"
            "    if not xs:\n"
            "        return []\n"
            "    m = max(xs)\n"
            "    exps = [math.exp(x - m) for x in xs]\n"
            "    total = sum(exps)\n"
            "    return [round(math.log(e / total), 6) for e in exps]\n",
            lambda low: "log_softmax" in low or "log softmax" in low or "log-softmax" in low,
            (
                (([0, 0],), [-0.693147, -0.693147]),
                (([1],), [0.0]),
                (([],), []),
            ),
        ),
        T(
            "urlencode",
            "def urlencode(pairs):\n"
            '    """Encode a dict or list of pairs as an application/x-www-form-urlencoded string."""\n'
            "    from urllib.parse import quote_plus\n"
            "    items = pairs.items() if hasattr(pairs, \"items\") else pairs\n"
            "    return \"&\".join(\n"
            "        quote_plus(str(k)) + \"=\" + quote_plus(str(v)) for k, v in items\n"
            "    )\n",
            lambda low: "urlencode" in low or "url-encode" in low or "url encode" in low,
            (
                (({"a": "b c"},), "a=b+c"),
                (([("q", "x&y")],), "q=x%26y"),
            ),
        ),
        T(
            "snake_case",
            "def snake_case(text):\n"
            '    """CamelCase or spaced text to lower_snake_case."""\n'
            "    import re\n"
            "    s = re.sub(r\"(.)([A-Z][a-z]+)\", r\"\\1_\\2\", str(text))\n"
            "    s = re.sub(r\"([a-z0-9])([A-Z])\", r\"\\1_\\2\", s)\n"
            "    s = re.sub(r\"[^A-Za-z0-9]+\", \"_\", s).strip(\"_\").lower()\n"
            "    return s\n",
            lambda low: (
                "to snake_case" in low
                or "to snake case" in low
                or "into snake" in low
                or "as snake_case" in low
                or "as snake case" in low
            )
            and "camel" not in low
            and "kebab" not in low
            and "snake_case converts" not in low,
            (
                (("HelloWorld",), "hello_world"),
                (("already_snake",), "already_snake"),
                (("XMLHttp",), "xml_http"),
            ),
        ),

        T(
            "camel_case",
            "def camel_case(text):\n"
            '    """Spaced or snake_case text to lowerCamelCase."""\n'
            "    import re\n"
            "    parts = [p for p in re.split(r\"[^A-Za-z0-9]+\", str(text)) if p]\n"
            "    if not parts:\n"
            "        return \"\"\n"
            "    head = parts[0].lower()\n"
            "    tail = \"\".join(p[:1].upper() + p[1:].lower() for p in parts[1:])\n"
            "    return head + tail\n",
            lambda low: ("camel_case" in low or "camel case" in low)
            and "snake" not in low
            and "kebab" not in low,
            (
                (("hello_world",), "helloWorld"),
                (("Hello world",), "helloWorld"),
            ),
        ),
    ]
