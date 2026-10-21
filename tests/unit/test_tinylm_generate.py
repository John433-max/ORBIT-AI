"""tinylm.generate must exist so chat.generate / TinyLMProvider can decode."""

import numpy as np


def test_generate_numpy_greedy_extends_prompt():
    from tinylm.config import TinyLMConfig
    from tinylm.generate import generate_numpy
    from tinylm.numpy_model import TinyLMNumPy

    cfg = TinyLMConfig.preset("rope", vocab_size=32, n_layer=2, n_embd=32, n_head=4, block_size=32)
    model = TinyLMNumPy.from_config(cfg, seed=0)
    idx = np.array([[1, 2, 3, 4]], dtype=np.int64)
    out = generate_numpy(model, idx, n_new=4, temperature=0.0, use_cache=True, seed=0)
    assert out.shape == (1, 8), out.shape
    assert np.array_equal(out[0, :4], idx[0])
    assert out.dtype == np.int64


def test_generate_numpy_stops_on_eos():
    from tinylm.config import TinyLMConfig
    from tinylm.generate import generate_numpy
    from tinylm.numpy_model import TinyLMNumPy

    cfg = TinyLMConfig.preset("rope", vocab_size=16, n_layer=1, n_embd=16, n_head=2, block_size=16)
    model = TinyLMNumPy.from_config(cfg, seed=1)
    idx = np.array([[1, 2]], dtype=np.int64)
    # Force a known next token by patching forward to always emit eos.
    def _fwd(ids, kv_caches=None, cache_pos=None):
        logits = np.full((ids.shape[0], ids.shape[1], cfg.vocab_size), -10.0, dtype=np.float32)
        logits[:, -1, 7] = 10.0
        return logits, kv_caches
    model.forward = _fwd
    out = generate_numpy(model, idx, n_new=6, eos_id=7, min_new_tokens=1)
    assert out.shape[1] == 3, out  # prompt + one eos
    assert int(out[0, -1]) == 7
