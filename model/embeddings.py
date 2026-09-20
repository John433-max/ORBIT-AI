"""Token embeddings and output projection helpers."""

from __future__ import annotations

from typing import Optional

import numpy as np

from autograd import Tensor


def init_token_embeddings(
    vocab_size: int,
    d_model: int,
    std: float = 0.02,
    seed: int = 0,
) -> Tensor:
    """Initialize token embedding matrix of shape (vocab_size, d_model)."""
    rng = np.random.default_rng(seed)
    return Tensor(rng.normal(scale=std, size=(vocab_size, d_model)))


def tied_lm_head(h: Tensor, tok_emb: Tensor) -> Tensor:
    """
    Project hidden states to vocabulary logits using the *tied* embedding matrix.
    h: (B*T, D) or (..., D)
    tok_emb: (V, D)
    returns logits (..., V)
    """
    return h @ tok_emb.transpose(1, 0)
