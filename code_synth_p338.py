"""Cycle 631 (p338): educational pure-Python templates for post-training quant + GQA/tying gaps.

Fills natural-language gaps that currently return None or wrong name:
  - gqa_attention_scores (smoke expects this name for "group query attention")
  - tied_embedding_logits (smoke expects this name for "weight tying")
  - gptq_quantize (Frantar et al. 2022 RTN core)
  - awq_scale (Lin et al. 2023 activation scales)
  - smoothquant_smooth (Xiao et al. 2022 migrate scales)

Matchers gated so neighbors hold: gqa_kv_head, int4_group_dequant, weight_tying_params.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "gqa_attention_scores",
            '''def gqa_attention_scores(q, k, n_kv_heads):
    """Grouped-query attention scores (Ainslie et al. 2023, educational).

    q: list[list[float]] query heads (n_q, d)
    k: list[list[float]] kv heads (n_kv, d)
    Repeats kv heads to match query groups, then returns scaled dot scores
    rounded to 6 decimals. Empty input returns [].
    """
    import math
    if not q or not k:
        return []
    n_q = len(q)
    n_kv = max(1, int(n_kv_heads))
    d = len(q[0]) or 1
    scale = 1.0 / math.sqrt(d)
    # map each query head onto a kv head
    group = max(1, n_q // n_kv)
    out = []
    for i, qi in enumerate(q):
        ki = k[min(i // group, len(k) - 1)]
        s = sum(float(a) * float(b) for a, b in zip(qi, ki)) * scale
        out.append(round(s, 6))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bgroup[-_ ]?query[-_ ]?attention\b|"
                    r"\bgqa[-_ ]?attention[-_ ]?scores\b|"
                    r"\bgqa[-_ ]?scores\b",
                    low,
                )
            )
            and "kv head" not in low
            and "kv_head" not in low,
            (
                (([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0]], 1), [0.707107, 0.0]),
                (([], [[1.0]], 1), []),
                (([[1.0]], [], 1), []),
            ),
        ),
        T(
            "tied_embedding_logits",
            '''def tied_embedding_logits(hidden, embedding_matrix):
    """Tied embedding logits: hidden @ E^T (Press & Wolf 2017, educational).

    hidden: list[float] (d,)
    embedding_matrix: list[list[float]] (vocab, d) shared with input embed.
    Returns vocab logits. Empty hidden or matrix returns [].
    """
    if not hidden or not embedding_matrix:
        return []
    h = [float(x) for x in hidden]
    out = []
    for row in embedding_matrix:
        s = sum(h[j] * float(row[j]) for j in range(min(len(h), len(row))))
        out.append(round(s, 6))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\btied[-_ ]?embedding[-_ ]?logits\b|"
                    r"\bweight[-_ ]?tying\b|"
                    r"\btied[-_ ]?embed(?:ding)?s?\b|"
                    r"\bshare(?:d)?[-_ ]?embed(?:ding)?s?\b",
                    low,
                )
            )
            and "lora" not in low
            and "lookup" not in low
            and "params" not in low,
            (
                (([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]), [1.0, 0.0, 1.0]),
                (([], [[1.0]]), []),
                (([1.0], []), []),
            ),
        ),
        T(
            "gptq_quantize",
            '''def gptq_quantize(w, bits=4, scale=None):
    """Uniform round-to-nearest quant (GPTQ quant step, educational).

    Frantar et al. GPTQ 2022 uses this RTN core after Hessian column
    updates. Full Hessian solve is out of scope; this is the quantizer.

    w: list[float]; bits >= 2; scale optional (default maxabs/(2^(b-1)-1)).
    Returns (q, scale). Empty input returns ([], 0.0).
    """
    if not w:
        return ([], 0.0)
    b = max(2, int(bits))
    qmax = (1 << (b - 1)) - 1
    xs = [float(x) for x in w]
    s = float(scale) if scale is not None else 0.0
    if s <= 0.0:
        m = max(abs(x) for x in xs) or 1.0
        s = m / qmax
    q = [int(round(max(-qmax, min(qmax, x / s)))) for x in xs]
    return (q, round(s, 10))
''',
            lambda low: bool(
                re.search(
                    r"\bgptq\b|"
                    r"\bgptq[-_ ]?quant",
                    low,
                )
            )
            and "awq" not in low
            and "smooth" not in low
            and "int4" not in low,
            (
                (([1.0, -1.0, 0.5], 4), ([7, -7, 4], round(1.0 / 7, 10))),
                (([], 4), ([], 0.0)),
                (([0.0, 0.0], 3), ([0, 0], round(1.0 / 3, 10))),
            ),
        ),
        T(
            "awq_scale",
            '''def awq_scale(act_mag, alpha=0.5):
    """AWQ per-channel activation scales (Lin et al. 2023, educational).

    scale_i = act_mag_i^alpha. Non-positive magnitudes map to 1.0.
    Empty input returns [].
    """
    if not act_mag:
        return []
    a = float(alpha)
    out = []
    for m in act_mag:
        m = float(m)
        out.append(1.0 if m <= 0.0 else round(m ** a, 10))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bawq\b|"
                    r"\bactivation[-_ ]?aware\b|"
                    r"\bawq[-_ ]?scale",
                    low,
                )
            )
            and "smooth" not in low,
            (
                (([4.0, 1.0, 0.0], 0.5), [2.0, 1.0, 1.0]),
                (([9.0], 1.0), [9.0]),
                (([], 0.5), []),
            ),
        ),
        T(
            "smoothquant_smooth",
            '''def smoothquant_smooth(act_max, weight_max, alpha=0.5):
    """SmoothQuant migrate scales (Xiao et al. 2022, educational).

    s_i = act_max_i^alpha / weight_max_i^(1-alpha).
    Non-positive entries map to 1.0. Empty input returns [].
    """
    if not act_max or not weight_max:
        return []
    a = float(alpha)
    out = []
    for am, wm in zip(act_max, weight_max):
        am, wm = float(am), float(wm)
        if am <= 0.0 or wm <= 0.0:
            out.append(1.0)
        else:
            out.append(round((am ** a) / (wm ** (1.0 - a)), 10))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bsmoothquant\b|"
                    r"\bsmooth[-_ ]?quant\b",
                    low,
                )
            )
            and "awq" not in low,
            (
                (([4.0, 1.0], [1.0, 4.0], 0.5), [2.0, 0.5]),
                (([0.0], [1.0], 0.5), [1.0]),
                (([], [1.0], 0.5), []),
            ),
        ),
    ]
