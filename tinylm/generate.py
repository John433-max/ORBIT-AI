"""Minimal NumPy/Torch decode for the educational TinyLM path.

chat.generate and TinyLMProvider import generate_numpy from here.
The full speculative/quant stack is optional; this module only needs a
correct greedy/sample loop so the provider fallback actually runs.
"""

from __future__ import annotations

import time
from typing import Optional

import numpy as np


def _sample_row(
    logits: np.ndarray,
    *,
    temperature: float,
    top_k: int,
    top_p: float,
    repetition_penalty: float,
    prev_ids: np.ndarray,
    rng: np.random.Generator,
) -> int:
    scores = np.array(logits, dtype=np.float64, copy=True)
    if repetition_penalty and repetition_penalty != 1.0 and prev_ids.size:
        for tid in np.unique(prev_ids):
            tid = int(tid)
            if 0 <= tid < scores.shape[0]:
                if scores[tid] > 0:
                    scores[tid] /= repetition_penalty
                else:
                    scores[tid] *= repetition_penalty
    if temperature and temperature > 0:
        scores = scores / float(temperature)
    else:
        return int(np.argmax(scores))

    if top_k and top_k > 0 and top_k < scores.shape[0]:
        cutoff = np.partition(scores, -top_k)[-top_k]
        scores[scores < cutoff] = -1e9
    # stable softmax
    scores = scores - np.max(scores)
    probs = np.exp(scores)
    probs_sum = float(probs.sum())
    if probs_sum <= 0 or not np.isfinite(probs_sum):
        return int(np.argmax(logits))
    probs /= probs_sum
    if top_p and 0 < top_p < 1.0:
        order = np.argsort(-probs)
        csum = np.cumsum(probs[order])
        keep = csum <= top_p
        keep[0] = True
        mask = np.zeros_like(probs, dtype=bool)
        mask[order[keep]] = True
        probs = np.where(mask, probs, 0.0)
        total = float(probs.sum())
        if total <= 0:
            return int(np.argmax(logits))
        probs /= total
    return int(rng.choice(scores.shape[0], p=probs))


def generate_numpy(
    model,
    idx: np.ndarray,
    n_new: int = 1,
    use_cache: bool = True,
    prealloc: bool = True,
    temperature: float = 0.0,
    top_k: int = 0,
    top_p: float = 1.0,
    repetition_penalty: float = 1.0,
    seed: int = 0,
    eos_id: Optional[int] = None,
    stop_ids=(),
    min_new_tokens: int = 0,
    **kwargs,
) -> np.ndarray:
    """Greedy or sampled decode. Returns (B, T+n) ids including the prompt.

    Extra sampler kwargs from chat.generate are accepted and ignored so a
    slim generate module stays compatible with the full call site.
    """
    del prealloc, kwargs
    if idx.ndim != 2:
        raise ValueError("idx must be (batch, seq)")
    out = np.array(idx, dtype=np.int64, copy=True)
    rng = np.random.default_rng(int(seed or 0))
    halt = set()
    if eos_id is not None:
        halt.add(int(eos_id))
    halt.update(int(s) for s in (stop_ids or ()))
    caches = None
    produced = 0
    for _ in range(int(n_new)):
        if use_cache and caches is not None:
            step = out[:, -1:]
            logits, caches = model.forward(step, kv_caches=caches)
        else:
            logits, caches = model.forward(out)
            if not use_cache:
                caches = None
        last = np.asarray(logits)[:, -1, :]
        next_id = _sample_row(
            last[0],
            temperature=float(temperature or 0.0),
            top_k=int(top_k or 0),
            top_p=float(top_p if top_p is not None else 1.0),
            repetition_penalty=float(repetition_penalty or 1.0),
            prev_ids=out[0],
            rng=rng,
        )
        out = np.concatenate([out, np.array([[next_id]], dtype=np.int64)], axis=1)
        produced += 1
        if produced >= int(min_new_tokens or 0) and next_id in halt:
            break
    return out


def sample_numpy(*args, **kwargs) -> np.ndarray:
    kwargs.setdefault("temperature", 0.8)
    return generate_numpy(*args, **kwargs)


def generate_torch(model, idx, n_new: int = 1, **kwargs):
    """Torch path: convert to NumPy, run generate_numpy, convert back if needed."""
    import torch

    if isinstance(idx, torch.Tensor):
        arr = idx.detach().cpu().numpy().astype(np.int64)
    else:
        arr = np.asarray(idx, dtype=np.int64)
    # Prefer a NumPy twin if the torch model can export one; else require forward on numpy-like.
    if hasattr(model, "forward") and not hasattr(model, "config") and hasattr(model, "cfg"):
        pass
    out = generate_numpy(model, arr, n_new=n_new, **kwargs)
    if isinstance(idx, torch.Tensor):
        return torch.tensor(out, dtype=idx.dtype, device=idx.device)
    return out


def sample_torch(*args, **kwargs):
    kwargs.setdefault("temperature", 0.8)
    return generate_torch(*args, **kwargs)


def bench_numpy(model, prompt_len: int = 8, n_new: int = 24, use_cache: bool = True) -> float:
    vocab = int(getattr(getattr(model, "config", None), "vocab_size", 64) or 64)
    idx = np.arange(prompt_len, dtype=np.int64)[None, :] % max(1, vocab)
    t0 = time.perf_counter()
    out = generate_numpy(model, idx, n_new=n_new, use_cache=use_cache, temperature=0.0)
    elapsed = max(time.perf_counter() - t0, 1e-9)
    produced = max(0, int(out.shape[1] - idx.shape[1]))
    return produced / elapsed


def bench_torch(model, prompt_len: int = 8, n_new: int = 24, use_cache: bool = True) -> float:
    try:
        import torch
    except Exception:
        return 0.0
    vocab = int(getattr(getattr(model, "config", None), "vocab_size", 64) or 64)
    idx = torch.arange(prompt_len).unsqueeze(0) % max(1, vocab)
    t0 = time.perf_counter()
    out = generate_torch(model, idx, n_new=n_new, use_cache=use_cache, temperature=0.0)
    elapsed = max(time.perf_counter() - t0, 1e-9)
    produced = max(0, int(out.shape[1] - idx.shape[1]))
    return produced / elapsed
