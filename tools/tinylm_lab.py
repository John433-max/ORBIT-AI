"""TinyLM lab tool — bench / regression probes for LabAgent (Cycle 56)."""

from __future__ import annotations

from tools.base import BaseTool, ToolResult


class TinyLMLabTool(BaseTool):
    name = "tinylm.lab"
    description = (
        "Run a TinyLM educational probe: cached decode bench or regression suite. "
        "action=bench|regression. preset=rope|gqa|modern|swa|stable."
    )
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "bench (default) or regression",
            },
            "preset": {
                "type": "string",
                "description": "TinyLMConfig.preset name",
            },
        },
        "required": [],
    }
    timeout_s = 30.0

    def execute(self, action: str = "bench", preset: str = "rope", **_) -> ToolResult:
        action = (action or "bench").strip().lower()
        preset = (preset or "rope").strip().lower()
        try:
            from tinylm import TinyLMConfig
            from tinylm.numpy_model import TinyLMNumPy
            from tinylm.generate import bench_numpy
            from tinylm.regression import run_regression
        except Exception as e:
            return ToolResult(ok=False, content="", error=f"TinyLM lab unavailable: {e}")

        if action == "regression":
            try:
                reg = run_regression()
            except Exception as e:
                return ToolResult(ok=False, content="", error=str(e))
            ok = bool(reg.get("ok"))
            checks = ", ".join(
                f"{c['name']}={'pass' if c.get('ok') else 'fail'}"
                for c in reg.get("checks", [])
            )
            return ToolResult(
                ok=ok,
                content=f"TinyLM regression ok={ok}. Checks: {checks}",
                data=reg,
            )

        try:
            cfg = TinyLMConfig.preset(
                preset, vocab_size=64, n_layer=4, n_embd=64, n_head=4, block_size=64
            )
            m = TinyLMNumPy.from_config(cfg, seed=0)
            tps = bench_numpy(m, prompt_len=8, n_new=24, use_cache=True)
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))
        content = (
            f"TinyLM lab ({preset}): ~{cfg.estimate_parameters()} params, "
            f"RoPE={cfg.use_rope}, GQA={cfg.n_kv_head}/{cfg.n_head}, "
            f"SwiGLU={cfg.use_swiglu}, QK-Norm={cfg.qk_norm}. "
            f"Cached decode ≈ {tps:.0f} tok/s (CPU NumPy, toy size)."
        )
        return ToolResult(
            ok=True,
            content=content,
            data={"preset": preset, "tok_s": tps, "params": cfg.estimate_parameters()},
        )
