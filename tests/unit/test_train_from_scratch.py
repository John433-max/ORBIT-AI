"""From-scratch train pipeline (1m smoke — keeps CI light)."""

from tinylm.train import train_from_scratch


def test_train_from_scratch_1m_smoke():
    r = train_from_scratch(preset="1m", steps=4, batch=2, seq=32, lr=3e-3, seed=1, ckpt_path=None)
    assert r.get("ok") is True
    assert r["params"] == 1_148_160
    assert len(r["losses"]) == 4
    assert r["loss_end"] < r["loss_start"]
