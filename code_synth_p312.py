"""Cycle 608: LLM inference educational templates (RoPE, sampling, KV, SwiGLU, BPE).

Loaded last (highest pack number) so phrase-specific matchers win.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "apply_rope",
            "def apply_rope(x, y, theta):\n"
            '    """Rotate a 2D pair (x, y) by angle theta (radians).\n'
            "    This is the elementary RoPE rotation used on Q/K pairs.\n"
            "    Returns (x', y') rounded to 6 decimals for stable checks.\n"
            '    """\n'
            "    import math\n"
            "    c = math.cos(theta)\n"
            "    s = math.sin(theta)\n"
            "    return (round(x * c - y * s, 6), round(x * s + y * c, 6))\n",
            lambda low: bool(
                re.search(
                    r"\b(rope|rotary(?: positional)?(?: embedding| encoding)?|apply rotary)\b",
                    low,
                )
            )
            and "absolute" not in low,
            (
                ((1.0, 0.0, 1.5707963267948966), (0.0, 1.0)),  # pi/2
                ((1.0, 0.0, 0.0), (1.0, 0.0)),
                ((2.0, 0.0, 3.141592653589793), (-2.0, 0.0)),  # pi
            ),
        ),
        T(
            "top_k_indices",
            "def top_k_indices(logits, k):\n"
            '    """Return indices of the k largest logits (stable sort).\n'
            "    Ties broken by smaller index. Educational top-k filter.\n"
            '    """\n'
            "    if k <= 0 or not logits:\n"
            "        return []\n"
            "    ranked = sorted(range(len(logits)), key=lambda i: (-logits[i], i))\n"
            "    return ranked[: min(k, len(logits))]\n",
            lambda low: bool(
                re.search(r"\btop[- ]?k(?: sampling| indices| filter)?\b", low)
            )
            and "top-p" not in low
            and "nucleus" not in low
            and "frequent" not in low,
            (
                (([1.0, 3.0, 2.0, 0.5], 2), [1, 2]),
                (([5.0, 5.0, 1.0], 2), [0, 1]),
                (([0.1], 3), [0]),
            ),
        ),
        T(
            "nucleus_indices",
            "def nucleus_indices(probs, p):\n"
            '    """Smallest set of indices whose probabilities sum to >= p.\n'
            "    Indices returned in descending-probability order (ties by index).\n"
            "    Educational nucleus / top-p mask. probs should sum to ~1.\n"
            '    """\n'
            "    if not probs or p <= 0:\n"
            "        return []\n"
            "    order = sorted(range(len(probs)), key=lambda i: (-probs[i], i))\n"
            "    kept = []\n"
            "    cum = 0.0\n"
            "    for i in order:\n"
            "        kept.append(i)\n"
            "        cum += probs[i]\n"
            "        if cum >= p:\n"
            "            break\n"
            "    return kept\n",
            lambda low: bool(
                re.search(
                    r"\b(nucleus(?: sampling)?|top[- ]?p(?: sampling| filter)?)\b",
                    low,
                )
            ),
            (
                (([0.5, 0.25, 0.15, 0.1], 0.8), [0, 1, 2]),
                (([0.9, 0.05, 0.05], 0.8), [0]),
                (([0.4, 0.4, 0.2], 0.5), [0, 1]),
            ),
        ),
        T(
            "kv_cache_append",
            "def kv_cache_append(cache, token_id):\n"
            '    """Append a token id to a simple list-based KV cache.\n'
            "    Returns the new cache and its length. Educational stand-in\n"
            "    for the append step of a decoder KV cache.\n"
            '    """\n'
            "    new_cache = list(cache) + [token_id]\n"
            "    return new_cache, len(new_cache)\n",
            lambda low: bool(
                re.search(r"\bkv[- ]?cache(?: append)?\b", low)
            ),
            (
                (([], 7), ([7], 1)),
                (([1, 2], 3), ([1, 2, 3], 3)),
                (([10], 20), ([10, 20], 2)),
            ),
        ),
        T(
            "swiglu",
            "def swiglu(gate, up):\n"
            '    """Element-wise SwiGLU: silu(gate) * up.\n'
            "    silu(x) = x * sigmoid(x). Lengths must match.\n"
            "    Educational gated activation used in modern LLMs.\n"
            '    """\n'
            "    import math\n"
            "    out = []\n"
            "    for g, u in zip(gate, up):\n"
            "        sig = 1.0 / (1.0 + math.exp(-g))\n"
            "        out.append(round(g * sig * u, 6))\n"
            "    return out\n",
            lambda low: bool(re.search(r"\bswiglu\b", low)),
            (
                (([0.0, 1.0], [2.0, 2.0]), [0.0, 1.462117]),
                (([2.0], [1.0]), [1.761594]),
                (([], []), []),
            ),
        ),
        T(
            "bpe_apply_merge",
            "def bpe_apply_merge(tokens, pair, new_id):\n"
            '    """Apply one BPE merge: replace non-overlapping occurrences of pair\n'
            "    with new_id. Educational single merge step.\n"
            '    """\n'
            "    if len(pair) != 2:\n"
            "        return list(tokens)\n"
            "    a, b = pair\n"
            "    out = []\n"
            "    i = 0\n"
            "    n = len(tokens)\n"
            "    while i < n:\n"
            "        if i + 1 < n and tokens[i] == a and tokens[i + 1] == b:\n"
            "            out.append(new_id)\n"
            "            i += 2\n"
            "        else:\n"
            "            out.append(tokens[i])\n"
            "            i += 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\b(bpe(?: merge| apply)?|byte[- ]pair(?: encoding| merge)?)\b", low)
            ),
            (
                (([1, 2, 3, 1, 2], (1, 2), 9), [9, 3, 9]),
                (([1, 1, 1], (1, 1), 5), [5, 1]),
                (([4, 5], (1, 2), 9), [4, 5]),
            ),
        ),
    ]
