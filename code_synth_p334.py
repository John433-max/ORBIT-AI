"""Cycle 627 (p334): Draft-confidence gate + token confidence for speculative decoding.

Educational pure-Python mirrors of TinyLM Cycle 164/165:
- draft_token_confidence: max-softmax of a logit row (greedy confidence).
- draft_confidence_gate: keep a draft prefix while max-softmax >= tau; stop early.

Also adds a simple rejection-sampling accept probability helper used by
Leviathan-style speculative decoding when temperature > 0.
"""
from __future__ import annotations

import math
import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "draft_token_confidence",
            '''def draft_token_confidence(logits):
    """Max-softmax confidence of a draft logit row (educational).

    Returns the probability of the greedy (argmax) token after softmax.
    Used as a draft-confidence signal: low values mean the draft model
    is uncertain and speculative decoding should stop proposing.
    Empty logits → 0.0.
    """
    import math
    if not logits:
        return 0.0
    m = max(float(v) for v in logits)
    exps = [math.exp(float(v) - m) for v in logits]
    total = sum(exps)
    if total <= 0.0:
        return 0.0
    return round(max(exps) / total, 10)
''',
            lambda low: bool(
                re.search(
                    r"\bdraft[ _-]?token[ _-]?confidence\b|"
                    r"\bdraft[ _-]?confidence\b|"
                    r"\bmax[-_ ]?softmax\b.{0,20}\b(draft|logit)|"
                    r"\b(confidence|max.?prob).{0,30}\b(draft|logit row)\b",
                    low,
                )
            )
            and "adaptive" not in low
            and "gate" not in low
            and "tau" not in low,
            (
                # clear winner
                (([0.0, 10.0, 0.0],), round(math.exp(10) / (2 + math.exp(10)), 10)),
                # uniform → ~1/3
                (([1.0, 1.0, 1.0],), round(1.0 / 3.0, 10)),
                # empty
                (([],), 0.0),
            ),
        ),
        T(
            "draft_confidence_gate",
            '''def draft_confidence_gate(draft_logits_rows, tau):
    """Keep draft prefix while max-softmax confidence >= tau (educational).

    draft_logits_rows: list of logit rows, one per proposed draft token.
    Returns the longest prefix length that passes the confidence gate
    (0 .. len(rows)). When tau <= 0 the gate is disabled (keep all).
    Mirrors TinyLM ORBIT_TINYLM_DRAFT_CONF / draft_conf early-stop.
    """
    import math
    tau = float(tau)
    if tau <= 0.0:
        return len(draft_logits_rows)
    kept = 0
    for row in draft_logits_rows:
        if not row:
            break
        m = max(float(v) for v in row)
        exps = [math.exp(float(v) - m) for v in row]
        total = sum(exps)
        conf = (max(exps) / total) if total > 0.0 else 0.0
        if conf < tau:
            break
        kept += 1
    return kept
''',
            lambda low: bool(
                re.search(
                    r"\bdraft[ _-]?confidence[ _-]?(gate|threshold|abort|cut)\b|"
                    r"\bconfidence[ _-]?gate\b|"
                    r"\bearly[-_ ]stop.{0,20}\bdraft\b|"
                    r"\bdraft[ _-]?conf(?:idence)?\b",
                    low,
                )
            )
            and "adaptive" not in low,
            (
                # two rows above tau=0.5, third low → keep 2
                (
                    (
                        [
                            [0.0, 5.0],
                            [1.0, 4.0],
                            [1.0, 1.0],
                        ],
                        0.6,
                    ),
                    2,
                ),
                # tau disabled
                (([[0.0, 0.0]], 0.0), 1),
                # empty
                (([], 0.3), 0),
            ),
        ),
        T(
            "speculative_accept_prob",
            '''def speculative_accept_prob(p_target, q_draft, token_id):
    """Leviathan rejection-sampling accept probability (educational).

    For temperature > 0 speculative decoding: accept draft token with
    probability min(1, p_target[token] / q_draft[token]).
    p_target / q_draft are probability vectors (or unnormalized masses).
    Returns a float in [0, 1]. Missing / zero draft mass → 0.
    """
    tid = int(token_id)
    if tid < 0 or tid >= len(p_target) or tid >= len(q_draft):
        return 0.0
    q = float(q_draft[tid])
    if q <= 0.0:
        return 0.0
    ratio = float(p_target[tid]) / q
    if ratio >= 1.0:
        return 1.0
    if ratio <= 0.0:
        return 0.0
    return round(ratio, 10)
''',
            lambda low: bool(
                re.search(
                    r"\bspeculative[ _-]?accept[ _-]?(prob|probability)\b|"
                    r"\bleviathan\b|"
                    r"\brejection[ _-]?sampling\b.{0,30}\b(speculat|draft)\b|"
                    r"\baccept probability\b.{0,20}\b(draft|speculat)",
                    low,
                )
            ),
            (
                # p >= q → 1
                (([0.1, 0.9], [0.2, 0.8], 1), 1.0),
                # p < q → ratio
                (([0.1, 0.3], [0.2, 0.8], 1), 0.375),
                # zero draft mass
                (([0.5, 0.5], [0.0, 1.0], 0), 0.0),
            ),
        ),

        T(
            "max_of_list",
            """def max_of_list(nums):
    \"\"\"Return the maximum value in a non-empty list of numbers.\"\"\"
    if not nums:
        raise ValueError("empty list")
    m = nums[0]
    for x in nums[1:]:
        if x > m:
            m = x
    return m
""",
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)?[ _-]?(?:of|in|value)[ _-]?(?:a |the )?list\b|"
                    r"\bfind (?:the )?max(?:imum)? (?:value )?(?:in|of) (?:a |the )?list\b|"
                    r"\bmax_of_list\b|"
                    r"\bmaximum value in a list\b",
                    low,
                )
            )
            and "two" not in low
            and "pair" not in low
            and "subarray" not in low
            and "window" not in low
            and "product" not in low
            and "index" not in low
            and "argmax" not in low
            and "running" not in low
            and "prefix" not in low,
            (
                (([1, 3, 2],), 3),
                (([-5, -1, -10],), -1),
                (([7],), 7),
            ),
        ),
    ]
