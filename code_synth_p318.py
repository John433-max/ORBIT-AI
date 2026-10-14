"""Cycle 614 (p318): Educational pure-Python samplers matching TinyLM generate paths.

min_p (Nguyen / llama.cpp), nucleus top-p (Holtzman et al.), typical_p (Meister),
repetition penalty, temperature scale, and frequency penalty. Highest pack so
specific matchers win over broader neighbors (softmax, top_k).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "min_p_mask",
            "def min_p_mask(probs, min_p):\n"
            '    """Keep indices where p >= min_p * max(p). Educational TinyLM min_p.\n'
            "    Returns sorted list of kept indices. min_p<=0 keeps all.\n"
            '    """\n'
            "    if not probs or min_p <= 0:\n"
            "        return list(range(len(probs)))\n"
            "    pmax = max(probs)\n"
            "    thresh = min_p * pmax\n"
            "    return [i for i, p in enumerate(probs) if p >= thresh]\n",
            lambda low: bool(re.search(r"\bmin[-_ ]?p\b", low))
            and ("mask" in low or "keep" in low or "filter" in low),
            (
                (([0.5, 0.3, 0.2], 0.7), [0]),
                (([0.4, 0.4, 0.2], 0.9), [0, 1]),
                (([0.1, 0.1, 0.1], 0.0), [0, 1, 2]),
            ),
        ),
        T(
            "nucleus_top_p",
            "def nucleus_top_p(probs, top_p):\n"
            '    """Nucleus (top-p) cutoff indices, sorted by descending prob.\n'
            "    Educational Holtzman et al. Cumulative sum until >= top_p.\n"
            "    Returns list of kept indices in original order.\n"
            '    """\n'
            "    if not probs or top_p >= 1.0:\n"
            "        return list(range(len(probs)))\n"
            "    order = sorted(range(len(probs)), key=lambda i: -probs[i])\n"
            "    cum = 0.0\n"
            "    kept = []\n"
            "    for i in order:\n"
            "        kept.append(i)\n"
            "        cum += probs[i]\n"
            "        if cum >= top_p:\n"
            "            break\n"
            "    return sorted(kept)\n",
            lambda low: (
                bool(re.search(r"\b(nucleus[_ ]top[_ ]p|top[-_ ]?p)\b", low))
                or ("nucleus" in low and "top" in low and re.search(r"\bp\b", low))
            )
            and "top_k" not in low
            and "topk" not in low
            and not re.search(r"\bnucleus\s+sampling\b", low),
            (
                (([0.5, 0.3, 0.2], 0.4), [0]),
                (([0.4, 0.35, 0.25], 0.5), [0, 1]),
                (([0.1, 0.1, 0.1], 1.0), [0, 1, 2]),
            ),
        ),
        T(
            "typical_p_mask",
            "def typical_p_mask(probs, typical_p):\n"
            '    """Typical sampling mask (Meister et al. educational).\n'
            "    Keep tokens whose local entropy is within band of mean.\n"
            "    Returns indices. typical_p>=1 keeps all.\n"
            '    """\n'
            "    import math\n"
            "    if not probs or typical_p >= 1.0:\n"
            "        return list(range(len(probs)))\n"
            "    ents = []\n"
            "    for p in probs:\n"
            "        if p <= 1e-12:\n"
            "            ents.append(0.0)\n"
            "        else:\n"
            "            ents.append(-p * math.log(p))\n"
            "    mean_e = sum(ents) / len(ents)\n"
            "    band = typical_p * (mean_e + 1e-12)\n"
            "    return [i for i, e in enumerate(ents) if abs(e - mean_e) <= band]\n",
            lambda low: bool(re.search(r"\btypical[-_ ]?p\b", low)),
            (
                (([0.5, 0.3, 0.2], 0.9), [0, 1, 2]),
                (([0.9, 0.05, 0.05], 0.5), [0, 1, 2]),
                (([0.33, 0.33, 0.34], 1.0), [0, 1, 2]),
            ),
        ),
        T(
            "repetition_penalty_logits",
            "def repetition_penalty_logits(logits, recent, penalty):\n"
            '    """Apply HF-style repetition penalty to a logit list.\n'
            "    Positive logits divided by penalty; negative multiplied. Educational.\n"
            "    Returns new list of floats rounded to 4 decimals.\n"
            '    """\n'
            "    out = list(logits)\n"
            "    if penalty == 1.0 or not recent:\n"
            "        return [round(x, 4) for x in out]\n"
            "    for i in set(recent):\n"
            "        if 0 <= i < len(out):\n"
            "            if out[i] > 0:\n"
            "                out[i] /= penalty\n"
            "            else:\n"
            "                out[i] *= penalty\n"
            "    return [round(x, 4) for x in out]\n",
            lambda low: bool(re.search(r"\brepetition[-_ ]penalty\b", low))
            and "freq" not in low
            and "presence" not in low,
            (
                (([2.0, 1.0, -1.0], [0], 2.0), [1.0, 1.0, -1.0]),
                (([1.5, 0.5], [1], 1.5), [1.5, 0.3333]),
                (([1.0, 1.0], [], 2.0), [1.0, 1.0]),
            ),
        ),
        T(
            "temperature_scale",
            "def temperature_scale(logits, temperature):\n"
            '    """Divide logits by temperature (standard sampling warp).\n'
            "    Educational TinyLM path. temperature<=0 returns original.\n"
            "    Returns rounded list.\n"
            '    """\n'
            "    if temperature <= 0:\n"
            "        return [round(x, 4) for x in logits]\n"
            "    return [round(x / temperature, 4) for x in logits]\n",
            lambda low: bool(re.search(r"\btemperature[-_ ]scale\b", low))
            and "logit" not in low,
            (
                (([2.0, 1.0, 0.0], 2.0), [1.0, 0.5, 0.0]),
                (([1.0, -1.0], 0.5), [2.0, -2.0]),
                (([1.0], 1.0), [1.0]),
            ),
        ),
        T(
            "frequency_penalty_logits",
            "def frequency_penalty_logits(logits, counts, penalty):\n"
            '    """OpenAI-style frequency penalty: subtract penalty * count from logits.\n'
            "    Educational. Returns rounded list.\n"
            '    """\n'
            "    out = list(logits)\n"
            "    for i, c in enumerate(counts):\n"
            "        if i < len(out):\n"
            "            out[i] -= penalty * c\n"
            "    return [round(x, 4) for x in out]\n",
            lambda low: bool(re.search(r"\bfrequency[-_ ]penalty\b", low)),
            (
                (([1.0, 1.0, 1.0], [1, 0, 2], 0.5), [0.5, 1.0, 0.0]),
                (([2.0, 0.0], [0, 1], 1.0), [2.0, -1.0]),
                (([0.0], [0], 0.0), [0.0]),
            ),
        ),
    ]
