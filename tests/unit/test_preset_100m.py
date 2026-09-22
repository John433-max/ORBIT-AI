"""TinyLM ~100M parameter preset (architecture only — no trained weights)."""

from tinylm.config import TinyLMConfig


def test_preset_100m_param_count():
    cfg = TinyLMConfig.preset("100m")
    n = cfg.estimate_parameters()
    assert 95_000_000 <= n <= 110_000_000, n
    assert cfg.n_embd == 768
    assert cfg.n_layer == 12
    assert cfg.vocab_size == 32000
    assert cfg.n_head == 12
    assert cfg.n_kv_head == 4
    assert cfg.block_size == 1024
    assert cfg.use_rope and cfg.use_swiglu and cfg.qk_norm


def test_preset_100m_aliases():
    a = TinyLMConfig.preset("100m").estimate_parameters()
    assert TinyLMConfig.preset("param_100m").estimate_parameters() == a
    assert TinyLMConfig.preset("one_hundred_million").estimate_parameters() == a


def test_preset_100m_construct_forward():
    """Build weights and run a tiny forward (memory ~400MB FP32)."""
    import numpy as np
    from tinylm.numpy_model import TinyLMNumPy

    cfg = TinyLMConfig.preset("100m")
    m = TinyLMNumPy(cfg)
    x = np.zeros((1, 4), dtype=np.int64)
    out = m.forward(x) if hasattr(m, "forward") else m(x)
    logits = out[0] if isinstance(out, tuple) else out
    arr = np.asarray(logits)
    assert arr.shape[-1] == cfg.vocab_size
    assert arr.shape[1] == 4
