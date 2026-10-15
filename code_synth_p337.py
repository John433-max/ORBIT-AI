"""Cycle 630 (p337): educational pure-Python templates for weight tying + MMR.

Fills natural-language gaps that currently return None from the technique map:
  - weight tying / tied embeddings (GPT-2 style shared input/output matrix)
  - maximal marginal relevance (Carbonell & Goldstein 1998) for diverse RAG
  - mean pooling over token embeddings
  - simple embedding L2 normalize
  - shared-param count helper
  - residual add (for completeness with residual_init_scale neighbors)

Matchers are gated so existing neighbors (cosine_similarity, residual_init_scale,
swiglu, embedding_lookup) continue to win their primary phrases.
"""
from __future__ import annotations

import math
import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "weight_tying_params",
            '''def weight_tying_params(vocab_size, d_model, tied=True):
    """Count embedding + LM-head parameters with optional weight tying.

    Educational GPT-2 / TinyLM style: when tied=True the output projection
    reuses the input embedding matrix (no extra V*d parameters).
    Returns total parameter count for the embedding tables only.
    """
    v = int(vocab_size)
    d = int(d_model)
    if v <= 0 or d <= 0:
        return 0
    emb = v * d
    if tied:
        return emb
    return emb + emb
''',
            lambda low: bool(
                re.search(
                    r"\bweight[-_ ]?tying[-_ ]?params\b|"
                    r"\bparam(?:eter)?s?\b.{0,20}\b(?:tied|tying|shared)\b|"
                    r"\b(?:tied|tying)\b.{0,20}\bparam",
                    low,
                )
            )
            and "lora" not in low,
            (
                ((100, 64, True), 6400),
                ((100, 64, False), 12800),
                ((0, 64, True), 0),
            ),
        ),
        T(
            "tied_embedding_lookup",
            '''def tied_embedding_lookup(token_ids, embedding_matrix):
    """Lookup token embeddings from a shared (tied) matrix — educational.

    token_ids: list[int]
    embedding_matrix: list[list[float]] of shape (vocab, d)
    Out-of-range ids yield a zero vector of length d.
    Empty token_ids returns [].
    """
    if not token_ids:
        return []
    if not embedding_matrix:
        return []
    d = len(embedding_matrix[0])
    v = len(embedding_matrix)
    out = []
    for tid in token_ids:
        i = int(tid)
        if 0 <= i < v:
            out.append([float(x) for x in embedding_matrix[i]])
        else:
            out.append([0.0] * d)
    return out
''',
            lambda low: bool(
                re.search(
                    r"\btied[-_ ]?embedding[-_ ]?lookup\b|"
                    r"\bembedding[-_ ]?lookup\b.{0,30}\btied\b|"
                    r"\bshared[-_ ]?embedding[-_ ]?lookup\b",
                    low,
                )
            ),
            (
                (([0, 1], [[1.0, 2.0], [3.0, 4.0]]), [[1.0, 2.0], [3.0, 4.0]]),
                (([2], [[1.0, 0.0], [0.0, 1.0]]), [[0.0, 0.0]]),
                (([], [[1.0]]), []),
            ),
        ),
        T(
            "mmr_score",
            '''def mmr_score(query_sim, max_selected_sim, lambda_div=0.5):
    """Maximal Marginal Relevance score (Carbonell & Goldstein 1998).

    score = λ * sim(query, d) − (1−λ) * max_{s in S} sim(d, s)
    Higher is better. Educational pure-Python form for RAG diversity.
    """
    lam = float(lambda_div)
    return float(query_sim) * lam - (1.0 - lam) * float(max_selected_sim)
''',
            lambda low: bool(
                re.search(
                    r"\bmmr[-_ ]?score\b|"
                    r"\bmmr[-_ ]?score\b|"
                    r"\bmmr\b",
                    low,
                )
            )
            and "select" not in low
            and "rerank" not in low,
            (
                ((0.9, 0.1, 0.5), 0.4),
                ((1.0, 0.0, 1.0), 1.0),
                ((0.8, 0.8, 0.0), -0.8),
            ),
        ),
        T(
            "mmr_select",
            '''def mmr_select(candidates, k, lambda_div=0.5):
    """Greedy Maximal Marginal Relevance selection — educational.

    candidates: list of (doc_id, query_sim, list_of_sims_to_others)
      where list_of_sims_to_others[j] = sim(doc_i, doc_j) aligned with candidates.
    Returns list of selected doc_ids (length min(k, n)).
    Empty candidates or k<=0 returns [].
    """
    if not candidates or int(k) <= 0:
        return []
    n = len(candidates)
    selected = []
    selected_idx = []
    remaining = set(range(n))
    for _ in range(min(int(k), n)):
        best_i = None
        best_score = None
        for i in remaining:
            doc_id, qsim, sims = candidates[i]
            if not selected_idx:
                max_sel = 0.0
            else:
                max_sel = max(float(sims[j]) for j in selected_idx)
            score = float(qsim) * float(lambda_div) - (1.0 - float(lambda_div)) * max_sel
            if best_score is None or score > best_score:
                best_score = score
                best_i = i
        selected.append(candidates[best_i][0])
        selected_idx.append(best_i)
        remaining.remove(best_i)
    return selected
''',
            lambda low: bool(
                re.search(
                    r"\bmmr[-_ ]?select\b|"
                    r"\bmmr[-_ ]?rerank\b|"
                    r"\bselect(?:ion)?\b.{0,20}\bmmr\b|"
                    r"\bmaximal[-_ ]?marginal[-_ ]?relevance\b|"
                    r"\bmaximal[-_ ]?marginal[-_ ]?relevance\b.{0,30}\bselect",
                    low,
                )
            ),
            (
                # two docs, prefer the higher query_sim first
                (
                    (
                        [
                            ("a", 0.9, [1.0, 0.1]),
                            ("b", 0.8, [0.1, 1.0]),
                        ],
                        1,
                        0.5,
                    ),
                    ["a"],
                ),
                (
                    (
                        [
                            ("a", 0.9, [1.0, 0.9]),
                            ("b", 0.85, [0.9, 1.0]),
                        ],
                        2,
                        0.5,
                    ),
                    ["a", "b"],
                ),
                (([], 2, 0.5), []),
            ),
        ),
        T(
            "mean_pool",
            '''def mean_pool(token_embeddings):
    """Mean-pool a sequence of token embedding vectors — educational.

    token_embeddings: list[list[float]]
    Returns a single vector (list[float]) or [] if empty.
    """
    if not token_embeddings:
        return []
    d = len(token_embeddings[0])
    n = len(token_embeddings)
    acc = [0.0] * d
    for vec in token_embeddings:
        for j in range(d):
            acc[j] += float(vec[j])
    return [x / n for x in acc]
''',
            lambda low: bool(
                re.search(
                    r"\bmean[-_ ]?pool(?:ing)?\b|"
                    r"\baverage[-_ ]?pool(?:ing)?\b|"
                    r"\bmean[-_ ]?over[-_ ]?tokens?\b",
                    low,
                )
            )
            and "max" not in low,
            (
                (([[1.0, 2.0], [3.0, 4.0]],), [2.0, 3.0]),
                (([[5.0]],), [5.0]),
                (([],), []),
            ),
        ),
        T(
            "l2_normalize",
            '''def l2_normalize(vec, eps=1e-12):
    """L2-normalize a vector — educational embedding helper.

    Returns a unit vector (or zero vector if input is near-zero).
    """
    import math
    if not vec:
        return []
    s = math.sqrt(sum(float(x) * float(x) for x in vec))
    if s < float(eps):
        return [0.0] * len(vec)
    return [float(x) / s for x in vec]
''',
            lambda low: bool(
                re.search(
                    r"\bl2[-_ ]?normali[sz]es?\b|"
                    r"\bunit[-_ ]?normali[sz]es?\b|"
                    r"\bnormalize\b.{0,15}\bembed",
                    low,
                )
            )
            and "layer" not in low
            and "batch" not in low
            and "rms" not in low,
            (
                (([3.0, 4.0],), [0.6, 0.8]),
                (([0.0, 0.0],), [0.0, 0.0]),
                (([],), []),
            ),
        ),
    ]
