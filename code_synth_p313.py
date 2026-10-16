"""Cycle 610: Transformer educational templates (residual, temp scale, GQA, RPB, PPL, causal mask).

Pack 313 — matchers for test_p313_transformer_edu.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "residual_connection",
            "def residual_connection(x, y):\n"
            '    """Element-wise residual / skip connection: x + y.\n'
            "    Lengths must match. Educational building block of Transformers.\n"
            '    """\n'
            "    return [a + b for a, b in zip(x, y)]\n",
            lambda low: bool(
                re.search(r"\bresidual(?: connection| add| stream)?\b|\bskip connection\b", low)
            )
            and "block" not in low,
            (
                (([1.0, 2.0], [0.5, -1.0]), [1.5, 1.0]),
                (([0.0], [0.0]), [0.0]),
                (([1, 2, 3], [3, 2, 1]), [4, 4, 4]),
            ),
        ),
        T(
            "scale_logits_temperature",
            "def scale_logits_temperature(logits, temperature):\n"
            '    """Divide logits by temperature (T>0). Educational sampling scale.\n'
            "    Returns list rounded to 6 decimals. temperature<=0 returns logits unchanged.\n"
            '    """\n'
            "    if temperature is None or temperature <= 0:\n"
            "        return list(logits)\n"
            "    return [round(float(x) / float(temperature), 6) for x in logits]\n",
            lambda low: bool(
                re.search(
                    r"\b(scale(?:d)? logits|logits? by temperature|temperature scaling)\b",
                    low,
                )
            ),
            (
                (([2.0, 4.0], 2.0), [1.0, 2.0]),
                (([1.0], 1.0), [1.0]),
                (([3.0, 6.0], 0.0), [3.0, 6.0]),
            ),
        ),
        T(
            "gqa_kv_head",
            "def gqa_kv_head(query_head, n_kv_heads, n_query_heads):\n"
            '    """Map a query-head index to its shared KV head under GQA.\n'
            "    Educational grouped-query attention head routing.\n"
            "    Returns kv_head = query_head // (n_query_heads // n_kv_heads).\n"
            '    """\n'
            "    if n_kv_heads <= 0 or n_query_heads <= 0 or n_query_heads % n_kv_heads != 0:\n"
            "        return -1\n"
            "    group = n_query_heads // n_kv_heads\n"
            "    return int(query_head) // group\n",
            lambda low: bool(
                re.search(r"\b(gqa|grouped[- ]query(?: attention)?)\b", low)
            ),
            (
                ((0, 2, 8), 0),
                ((3, 2, 8), 0),
                ((4, 2, 8), 1),
                ((7, 2, 8), 1),
            ),
        ),
        T(
            "relative_position_bias",
            "def relative_position_bias(i, j, max_bias=128):\n"
            '    """Clipped relative position i-j for T5-style bias buckets (simplified).\n'
            "    Returns int bias index in [-max_bias, max_bias]. Educational RPB.\n"
            '    """\n'
            "    d = int(i) - int(j)\n"
            "    if d > max_bias:\n"
            "        d = max_bias\n"
            "    if d < -max_bias:\n"
            "        d = -max_bias\n"
            "    return d\n",
            lambda low: bool(
                re.search(r"\brelative(?: position)?(?: bias| encoding)?\b|\brpb\b", low)
            )
            and "rope" not in low
            and "rotary" not in low,
            (
                ((5, 3, 128), 2),
                ((0, 10, 5), -5),
                ((100, 0, 10), 10),
            ),
        ),
        T(
            "perplexity_from_nll",
            "def perplexity_from_nll(nll):\n"
            '    """Perplexity = exp(mean negative log-likelihood).\n'
            "    nll is a scalar average NLL in nats. Returns round(ppl, 6).\n"
            '    """\n'
            "    import math\n"
            "    return round(math.exp(float(nll)), 6)\n",
            lambda low: bool(
                re.search(r"\bperplexity\b|\bppl from nll\b", low)
            ),
            (
                ((0.0,), 1.0),
                ((0.693147,), 2.0),
                ((1.0,), 2.718282),
            ),
        ),
        T(
            "causal_mask",
            "def causal_mask(n):\n"
            '    """Lower-triangular causal attention mask of size n x n.\n'
            "    1 = allowed (attend), 0 = blocked. Educational GPT-style mask.\n"
            '    """\n'
            "    n = int(n)\n"
            "    return [[1 if j <= i else 0 for j in range(n)] for i in range(n)]\n",
            lambda low: bool(
                re.search(r"\bcausal(?: attention)? mask\b|\blook[- ]ahead mask\b", low)
            ),
            (
                ((1,), [[1]]),
                ((2,), [[1, 0], [1, 1]]),
                ((3,), [[1, 0, 0], [1, 1, 0], [1, 1, 1]]),
            ),
        ),
    ]
