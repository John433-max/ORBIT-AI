"""Lightweight model card builder for TinyLM checkpoints."""

from __future__ import annotations

from typing import Any, Dict, Optional


def build_model_card(
    cfg: Any = None,
    *,
    name: str = "tinylm",
    preset: str = "rope",
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    card: Dict[str, Any] = {
        "name": name,
        "preset": preset,
        "family": "ORBIT educational TinyLM",
        "license": "project-local",
    }
    if cfg is not None:
        for key in (
            "vocab_size", "n_layer", "n_embd", "n_head", "n_kv_head",
            "block_size", "use_rope", "use_swiglu", "qk_norm", "sliding_window",
        ):
            if hasattr(cfg, key):
                card[key] = getattr(cfg, key)
        if hasattr(cfg, "estimate_parameters"):
            try:
                card["parameters"] = int(cfg.estimate_parameters())
            except Exception:
                pass
    if extra:
        card.update(extra)
    return card
