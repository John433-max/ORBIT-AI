"""TinyLM ~1M parameter preset."""

from tinylm.config import TinyLMConfig


def test_preset_1m_param_count():
    cfg = TinyLMConfig.preset("1m")
    n = cfg.estimate_parameters()
    assert 1_000_000 <= n <= 1_300_000, n
    assert cfg.n_embd == 128
    assert cfg.n_layer == 6
    assert cfg.vocab_size == 512
    assert cfg.use_rope and cfg.use_swiglu and cfg.qk_norm
    assert cfg.n_kv_head == 2


def test_preset_1m_aliases():
    a = TinyLMConfig.preset("1m").estimate_parameters()
    assert TinyLMConfig.preset("param_1m").estimate_parameters() == a
    assert TinyLMConfig.preset("one_million").estimate_parameters() == a


def test_preset_1m_forward():
    import numpy as np
    from tinylm.numpy_model import TinyLMNumPy

    cfg = TinyLMConfig.preset("1m")
    m = TinyLMNumPy(cfg)
    x = np.zeros((1, 8), dtype=np.int64)
    out = m.forward(x) if hasattr(m, "forward") else m(x)
    logits = out[0] if isinstance(out, tuple) else out
    assert np.asarray(logits).shape[-1] == cfg.vocab_size
