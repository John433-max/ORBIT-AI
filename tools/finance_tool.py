"""Paper-trading SMA backtest as a ToolRegistry tool (Cycle 60)."""

from __future__ import annotations

import hashlib

import numpy as np

from tools.base import BaseTool, ToolResult


def _stable_seed(text: str) -> int:
    digest = hashlib.sha256(text.encode("utf-8", errors="replace")).digest()
    return int.from_bytes(digest[:8], "big") % (2**32)


class FinanceBacktestTool(BaseTool):
    name = "finance.backtest"
    description = (
        "Run a paper-trading SMA-crossover backtest on a SYNTHETIC price series. "
        "Not live market data and not financial advice."
    )
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "seed_text": {
                "type": "string",
                "description": "Text used to seed the synthetic price series",
            },
            "n_bars": {"type": "integer", "default": 200},
            "fast": {"type": "integer", "default": 5},
            "slow": {"type": "integer", "default": 20},
        },
        "required": ["seed_text"],
    }
    timeout_s = 10.0

    def execute(self, seed_text: str = "", n_bars: int = 200, fast: int = 5, slow: int = 20, **_):
        from paper_trading import backtest_sma_crossover

        text = seed_text or "orbit-paper"
        n_bars = max(int(n_bars), int(slow) + 2)
        rng = np.random.default_rng(_stable_seed(text))
        prices = 100 + np.cumsum(rng.normal(0.05, 1.0, n_bars))
        prices = np.clip(prices, 1, None)
        try:
            perf = backtest_sma_crossover(prices, fast=int(fast), slow=int(slow))
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))
        perf = dict(
            perf,
            simulation=True,
            data_source="synthetic",
            warning="This result uses simulated data and is not financial advice.",
        )
        content = (
            "Ran a paper-trading SMA-crossover backtest on a SYNTHETIC price series "
            "(no live market data in this prototype — see DESIGN.md Part 12). "
            f"pnl={perf['pnl_pct']:.2f}% vs buy-and-hold={perf['buy_and_hold_pnl_pct']:.2f}%, "
            f"max drawdown={perf['max_drawdown_pct']:.2f}%, trades={perf['n_trades']}. "
            "This is a demo of the backtesting plumbing, not a trading recommendation."
        )
        return ToolResult(ok=True, content=content, data=perf)
