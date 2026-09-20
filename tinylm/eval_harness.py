"""Tiny eval harness: next-token CE / perplexity + attention logit stats."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
import torch.nn.functional as F


@dataclass
class EvalResult:
    nll: float
    ppl: float
    tokens: int
    max_attn_logit: float | None = None


def nll_numpy(model, tokens: np.ndarray) -> EvalResult:
    """tokens: (B, T) int64. Teacher-forced NLL on positions 0..T-2 → 1..T-1."""
    logits, _ = model.forward(tokens[:, :-1])
    target = tokens[:, 1:]
    # log-softmax
    m = logits.max(axis=-1, keepdims=True)
    logp = logits - m - np.log(np.exp(logits - m).sum(axis=-1, keepdims=True))
    b, t, _ = logp.shape
    nll = float(-np.mean(np.take_along_axis(logp, target[..., None], axis=-1)))
    return EvalResult(nll=nll, ppl=float(np.exp(nll)), tokens=b * t)


def nll_torch(model, tokens: torch.Tensor) -> EvalResult:
    model.eval()
    with torch.no_grad():
        logits, _ = model.forward(tokens[:, :-1])
        target = tokens[:, 1:]
        nll = F.cross_entropy(logits.reshape(-1, logits.size(-1)), target.reshape(-1))
        return EvalResult(nll=float(nll), ppl=float(torch.exp(nll)), tokens=int(target.numel()))


def synthetic_copy_batch(vocab: int, batch: int, seq: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.integers(0, vocab, size=(batch, seq), dtype=np.int64)


def max_qk_logit_numpy(model, tokens: np.ndarray) -> float:
    """Largest pre-softmax attention score on a full-context forward (no cache)."""
    c = model.config
    # instrument by recomputing first-layer scores
    x = model.tok_emb[tokens]
    if not c.use_rope and model.pos_emb is not None and model.pos_emb.shape[0] > 0:
        x = x + model.pos_emb[np.arange(tokens.shape[1])][None, :, :]
    layer = model.layers[0]
    from .numpy_model import _rms_norm

    n1 = _rms_norm(x, layer["ln1_w"], c.rms_eps)
    b, t, _ = n1.shape
    h, d = c.n_head, c.head_dim
    q = (n1 @ layer["wq"]).reshape(b, t, h, d).transpose(0, 2, 1, 3)
    k = (n1 @ layer["wk"]).reshape(b, t, h, d).transpose(0, 2, 1, 3)
    if c.qk_norm:
        q = _rms_norm(q, layer["q_norm"], c.rms_eps)
        k = _rms_norm(k, layer["k_norm"], c.rms_eps)
    scores = (q @ np.swapaxes(k, -1, -2)) / np.sqrt(d)
    return float(scores.max())


def max_qk_logit_torch(model, tokens: torch.Tensor) -> float:
    """Largest pre-softmax attention score from layer 0 (no cache)."""
    from .torch_model import rms_norm

    c = model.config
    model.eval()
    with torch.no_grad():
        pos = torch.arange(tokens.size(1), device=tokens.device)
        x = model.tok_emb(tokens)
        if not c.use_rope and model.pos_emb is not None:
            x = x + model.pos_emb(pos)[None, :, :]
        layer = model.layers[0]
        n1 = rms_norm(x, layer.ln1_w, c.rms_eps)
        b, t, _ = n1.shape
        h, d = c.n_head, c.head_dim
        q = layer.wq(n1).view(b, t, h, d).transpose(1, 2)
        k = layer.wk(n1).view(b, t, h, d).transpose(1, 2)
        if c.qk_norm:
            q = rms_norm(q, layer.q_norm, c.rms_eps)
            k = rms_norm(k, layer.k_norm, c.rms_eps)
        scores = (q @ k.transpose(-2, -1)) / (d ** 0.5)
        return float(scores.max())
