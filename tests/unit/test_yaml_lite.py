"""yaml_lite covers shipped configs and OrbitConfig falls back when PyYAML is absent."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIGS = ROOT / "configs"


def _load_yaml_lite():
    path = ROOT / "model" / "yaml_lite.py"
    spec = importlib.util.spec_from_file_location("orbit_yaml_lite_standalone", path)
    if spec is None or spec.loader is None:
        raise unittest.SkipTest("yaml_lite.py missing")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_yl = _load_yaml_lite()
safe_load = _yl.safe_load
safe_dump = _yl.safe_dump


class YamlLiteTests(unittest.TestCase):
    def test_tiny_matches_expected_shape(self):
        data = safe_load((CONFIGS / "tiny.yaml").read_text(encoding="utf-8"))
        self.assertEqual(data["model"]["d_model"], 128)
        self.assertEqual(data["model"]["n_layers"], 4)
        self.assertTrue(data["model"]["tie_embeddings"])
        self.assertEqual(data["model"]["n_heads"], 8)
        self.assertEqual(data["training"]["lr_scheduler"], "cosine")
        self.assertEqual(data["runtime"]["device"], "cpu")

    def test_flow_list_betas(self):
        data = safe_load((CONFIGS / "1m.yaml").read_text(encoding="utf-8"))
        self.assertEqual(data["training"]["betas"], [0.9, 0.95])

    def test_all_shipped_configs_parse(self):
        for path in sorted(CONFIGS.glob("*.yaml")):
            data = safe_load(path.read_text(encoding="utf-8"))
            self.assertIn("model", data, path.name)
            self.assertIsInstance(data["model"]["d_model"], int)

    def test_roundtrip_subset(self):
        src = {"model": {"d_model": 64, "tie_embeddings": True, "threads": None}, "betas": [0.9, 0.95]}
        again = safe_load(safe_dump(src))
        self.assertEqual(again["model"]["d_model"], 64)
        self.assertTrue(again["model"]["tie_embeddings"])
        self.assertIsNone(again["model"]["threads"])
        self.assertEqual(again["betas"], [0.9, 0.95])

    def test_config_load_forces_yaml_lite(self):
        """OrbitConfig.load must parse shipped YAML when PyYAML is absent."""
        try:
            import model.config as mc
            from model.config import OrbitConfig
        except Exception as exc:
            self.skipTest(f"model.config unavailable: {exc}")
        saved = mc.yaml
        mc.yaml = None
        try:
            cfg = OrbitConfig.load(CONFIGS / "tiny.yaml")
            self.assertEqual(cfg.model.d_model, 128)
            self.assertEqual(cfg.model.n_layers, 4)
            self.assertEqual(cfg.training.lr_scheduler, "cosine")
        finally:
            mc.yaml = saved


if __name__ == "__main__":
    unittest.main()
