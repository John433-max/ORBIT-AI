"""Cycle 44: KV-cache footprint report (MHA vs GQA, FP16/FP32)."""

from __future__ import annotations

from .config import TinyLMConfig


def kv_cache_bytes_report(
    preset: str = "rope",
    seq: int = 128,
    batch: int = 1,
    embd: int = 64,
    layers: int = 4,
    heads: int = 4,
    dtype_bytes: int = 2,
) -> dict:
    """Bytes for K+V caches: 2 * batch * n_kv_head * seq * head_dim * dtype * n_layer."""
    cfg = TinyLMConfig.preset(
        preset,
        vocab_size=64,
        n_layer=layers,
        n_embd=embd,
        n_head=heads,
        block_size=max(seq, 16),
    )
    dh = cfg.head_dim
    kvh = cfg.n_kv_head
    win = int(cfg.sliding_window)
    kv_seq = min(seq, win) if win > 0 else seq
    per_layer = 2 * batch * kvh * kv_seq * dh * dtype_bytes
    total = per_layer * cfg.n_layer
    mha_per = 2 * batch * cfg.n_head * seq * dh * dtype_bytes
    mha_total = mha_per * cfg.n_layer
    return {
        "preset": preset,
        "batch": batch,
        "seq": seq,
        "n_layer": cfg.n_layer,
        "n_head": cfg.n_head,
        "n_kv_head": kvh,
        "head_dim": dh,
        "dtype_bytes": dtype_bytes,
        "kv_cache_bytes": total,
        "kv_cache_mib": total / (1024 * 1024),
        "mha_kv_cache_bytes": mha_total,
        "gqa_saving_ratio": mha_total / total if total else None,
        "sliding_window": win,
        "kv_seq": kv_seq,
        "params_estimate": cfg.estimate_parameters(),
    }
