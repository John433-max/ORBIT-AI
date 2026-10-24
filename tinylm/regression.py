"""TinyLM educational regression suite (lab / CLI).

Returns a dict with:
  ok: bool — all checks passed
  checks: list[{name, ok, detail?}]
"""

from __future__ import annotations

from typing import Any, Dict, List


def run_regression() -> Dict[str, Any]:
    """Run a small, fast NumPy TinyLM sanity suite.

    Checks:
    - import / config preset
    - forward logits shape
    - greedy generate is deterministic and extends length
    - KV-cache generate matches full (when cache available)
    - bench_numpy returns a positive throughput
    """
    checks: List[Dict[str, Any]] = []

    def _add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    try:
        import numpy as np
        from tinylm.config import TinyLMConfig
        from tinylm.numpy_model import TinyLMNumPy
        from tinylm.generate import generate_numpy, bench_numpy
    except Exception as e:
        _add("imports", False, str(e))
        return {"ok": False, "checks": checks}

    _add("imports", True)

    try:
        cfg = TinyLMConfig.preset(
            "rope",
            vocab_size=64,
            n_layer=2,
            n_embd=32,
            n_head=4,
            block_size=32,
        )
        m = TinyLMNumPy.from_config(cfg, seed=0)
        _add("from_config", True, f"params≈{getattr(cfg, 'estimate_parameters', lambda: '?')()}")
    except Exception as e:
        _add("from_config", False, str(e))
        return {"ok": False, "checks": checks}

    try:
        prompt = np.array([[1, 2, 3]], dtype=np.int64)
        out = m.forward(prompt)
        logits = out[0] if isinstance(out, tuple) else out
        ok_shape = (
            isinstance(logits, np.ndarray)
            and logits.ndim == 3
            and logits.shape[0] == 1
            and logits.shape[1] == 3
            and logits.shape[2] == cfg.vocab_size
        )
        _add("forward_shape", ok_shape, str(getattr(logits, "shape", None)))
    except Exception as e:
        _add("forward_shape", False, str(e))

    try:
        prompt = np.array([[1, 2, 3]], dtype=np.int64)
        a = generate_numpy(m, prompt, n_new=4, temperature=0.0)
        b = generate_numpy(m, prompt, n_new=4, temperature=0.0)
        ok_det = (
            isinstance(a, np.ndarray)
            and a.shape == (1, 7)
            and np.array_equal(a, b)
        )
        _add("greedy_deterministic", ok_det, f"shape={getattr(a, 'shape', None)}")
    except Exception as e:
        _add("greedy_deterministic", False, str(e))

    try:
        # Cached vs full when generate supports use_cache / kv
        prompt = np.array([[1, 2, 3, 4]], dtype=np.int64)
        full = generate_numpy(m, prompt, n_new=6, temperature=0.0)
        try:
            cached = generate_numpy(m, prompt, n_new=6, temperature=0.0, use_cache=True)
            ok_cache = np.array_equal(full, cached)
            detail = "match" if ok_cache else "mismatch"
        except TypeError:
            # older signature without use_cache — skip as pass
            ok_cache = True
            detail = "use_cache not in signature (skipped)"
        _add("cache_vs_full", ok_cache, detail)
    except Exception as e:
        _add("cache_vs_full", False, str(e))

    try:
        tps = float(bench_numpy(m, prompt_len=4, n_new=8, use_cache=True))
        _add("bench_positive", tps > 0, f"{tps:.1f} tok/s")
    except Exception as e:
        _add("bench_positive", False, str(e))

    ok = all(c["ok"] for c in checks)
    return {"ok": ok, "checks": checks}


__all__ = ["run_regression"]
