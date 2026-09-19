"""
Sampling utilities shared by generate.py, agents.py, and api.py. Standard,
established techniques (nucleus/top-p sampling: Holtzman et al.'s "The
Curious Case of Neural Text Degeneration"; repetition penalty: common in
production decoding stacks) — not novel, just not previously wired in
(earlier generation code here used plain temperature sampling only).
"""
import numpy as np


def sample_next_token(logits_row: np.ndarray, recent_ids: list, temperature: float = 0.8,
                       top_p: float = 0.9, top_k: int = 0, repetition_penalty: float = 1.3,
                       rng: np.random.Generator = None) -> int:
    """
    temperature, top_p, top_k, and repetition_penalty are all applied — none
    are accepted-but-ignored. top_k=0 (the default) disables top-k filtering
    (i.e. no additional restriction beyond top_p); set it to a positive int
    to also cap the candidate set size before nucleus filtering, standard
    order (top-k first, then top-p on the reduced set) matches common
    decoding-stack implementations.
    """
    rng = rng or np.random.default_rng()
    logits = logits_row.astype(np.float64).copy()

    # repetition penalty: discourage tokens already used recently (divide
    # positive logits, multiply negative ones — the standard formulation)
    if repetition_penalty != 1.0 and recent_ids:
        for tid in set(recent_ids):
            if 0 <= tid < len(logits):
                if logits[tid] > 0:
                    logits[tid] /= repetition_penalty
                else:
                    logits[tid] *= repetition_penalty

    logits = logits / max(temperature, 1e-4)

    # top-k: restrict candidates to the k highest-logit tokens first
    if top_k and 0 < top_k < len(logits):
        kth_val = np.partition(logits, -top_k)[-top_k]
        logits = np.where(logits >= kth_val, logits, -np.inf)

    probs = np.exp(logits - np.max(logits[np.isfinite(logits)]))
    probs = np.where(np.isfinite(logits), probs, 0.0)
    probs /= probs.sum()

    # nucleus (top-p) sampling: keep the smallest set of tokens whose
    # cumulative probability exceeds top_p, renormalize, sample from that set
    order = np.argsort(-probs)
    sorted_probs = probs[order]
    cumulative = np.cumsum(sorted_probs)
    cutoff = np.searchsorted(cumulative, top_p) + 1
    cutoff = max(1, min(cutoff, len(order)))
    keep_idx = order[:cutoff]
    keep_probs = probs[keep_idx]
    keep_probs /= keep_probs.sum()

    return int(rng.choice(keep_idx, p=keep_probs))


def find_stop_sequence(text: str, stop_sequences: list) -> int:
    """Return the earliest index in `text` at which any stop sequence
    starts, or -1 if none are present. Callers truncate generated text at
    this index so `stop` parameters actually take effect instead of being
    accepted and silently ignored."""
    if not stop_sequences:
        return -1
    positions = [text.find(s) for s in stop_sequences if s]
    positions = [p for p in positions if p != -1]
    return min(positions) if positions else -1
