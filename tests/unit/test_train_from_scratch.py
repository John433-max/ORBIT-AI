"""From-scratch train pipeline (1m smoke — keeps CI light).

CI checkouts may omit tinylm/train.py and do not install torch.
Skip collection instead of failing the whole unit-test job.
"""

from __future__ import annotations

import importlib.util

import pytest

pytest.importorskip("torch")
if importlib.util.find_spec("tinylm.train") is None:
    pytest.skip("tinylm.train not in this checkout", allow_module_level=True)

from tinylm.train import train_from_scratch


def test_train_from_scratch_1m_smoke():
    r = train_from_scratch(preset="1m", steps=4, batch=2, seq=32, lr=3e-3, seed=1, ckpt_path=None)
    assert r.get("ok") is True
    assert r["params"] == 1_148_160
    assert len(r["losses"]) == 4
    assert r["loss_end"] < r["loss_start"]  # should learn something on toy text
