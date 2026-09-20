"""
Paper-trading engine (spec Part 12). Simulated portfolio only — no broker
connection, no real order routing, no live-market data feed.
"""
import numpy as np


class PaperPortfolio:
    def __init__(self, starting_cash: float = 100_000.0, transaction_cost_bps: float = 5.0,
                 spread_bps: float = 0.0, slippage_bps: float = 0.0):
        self.cash = starting_cash
        self.starting_cash = starting_cash
        self.positions = {}
        self.transaction_cost_bps = transaction_cost_bps
        self.spread_bps = spread_bps
        self.slippage_bps = slippage_bps
        self.trade_log = []
        self._avg_cost = {}
        self._closed_trade_pnls = []

    def _cost(self, notional: float) -> float:
        return abs(notional) * (self.transaction_cost_bps / 10_000.0)

    def _execution_price(self, price: float, side: str) -> float:
        adj_bps = (self.spread_bps / 2.0) + self.slippage_bps
        if side == "buy":
            return price * (1 + adj_bps / 10_000.0)
        return price * (1 - adj_bps / 10_000.0)

    def buy(self, symbol: str, price: float, shares: float):
        fill_price = self._execution_price(price, "buy")
        notional = fill_price * shares
        fee = self._cost(notional)
        total = notional + fee
        if total > self.cash:
            return {"ok": False, "error": "insufficient paper cash"}
        self.cash -= total
        prev_shares = self.positions.get(symbol, 0.0)
        prev_cost = self._avg_cost.get(symbol, 0.0)
        new_shares = prev_shares + shares
        self._avg_cost[symbol] = ((prev_cost * prev_shares) + (fill_price * shares)) / new_shares if new_shares else 0.0
        self.positions[symbol] = new_shares
        self.trade_log.append({"side": "buy", "symbol": symbol, "price": fill_price,
                                "shares": shares, "fee": fee})
        return {"ok": True, "cash": self.cash, "position": self.positions[symbol]}

    def sell(self, symbol: str, price: float, shares: float):
        held = self.positions.get(symbol, 0.0)
        if shares > held:
            return {"ok": False, "error": "insufficient paper position"}
        fill_price = self._execution_price(price, "sell")
        notional = fill_price * shares
        fee = self._cost(notional)
        self.cash += notional - fee
        self.positions[symbol] = held - shares
        realized_pnl = (fill_price - self._avg_cost.get(symbol, fill_price)) * shares - fee
        self._closed_trade_pnls.append(realized_pnl)
        self.trade_log.append({"side": "sell", "symbol": symbol, "price": fill_price,
                                "shares": shares, "fee": fee, "realized_pnl": realized_pnl})
        return {"ok": True, "cash": self.cash, "position": self.positions[symbol]}

    def mark_to_market(self, prices: dict) -> float:
        equity = self.cash
        for sym, shares in self.positions.items():
            equity += shares * prices.get(sym, 0.0)
        return equity

    def performance(self, prices: dict) -> dict:
        equity = self.mark_to_market(prices)
        pnl = equity - self.starting_cash
        wins = [t for t in self._closed_trade_pnls]
        n_wins = sum(1 for p in wins if p > 0)
        n_losses = sum(1 for p in wins if p <= 0)
        win_rate = n_wins / len(wins) if wins else None
        gross_profit = sum(p for p in wins if p > 0)
        gross_loss = -sum(p for p in wins if p < 0)
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (float("inf") if gross_profit > 0 else None)
        return {"equity": equity, "cash": self.cash, "pnl": pnl,
                "pnl_pct": 100.0 * pnl / self.starting_cash, "positions": dict(self.positions),
                "n_trades": len(self.trade_log), "win_rate": win_rate,
                "n_wins": n_wins, "n_losses": n_losses, "profit_factor": profit_factor}


def backtest_sma_crossover(prices: np.ndarray, fast: int = 5, slow: int = 20,
                            starting_cash: float = 100_000.0, symbol: str = "TOY",
                            spread_bps: float = 0.0, slippage_bps: float = 0.0,
                            stop_loss_pct: float = None, take_profit_pct: float = None):
    if len(prices) <= slow:
        raise ValueError("price series shorter than slow window")
    portfolio = PaperPortfolio(starting_cash, spread_bps=spread_bps, slippage_bps=slippage_bps)
    equity_curve = []
    position_open = False
    entry_price = None
    for t in range(slow, len(prices)):
        fast_ma = prices[t - fast:t].mean()
        slow_ma = prices[t - slow:t].mean()
        price = prices[t]
        if position_open and entry_price:
            change = (price - entry_price) / entry_price
            if (stop_loss_pct and change <= -stop_loss_pct) or (take_profit_pct and change >= take_profit_pct):
                portfolio.sell(symbol, price, portfolio.positions.get(symbol, 0.0))
                position_open, entry_price = False, None
                equity_curve.append(portfolio.mark_to_market({symbol: price}))
                continue
        if fast_ma > slow_ma and not position_open:
            shares = (portfolio.cash * 0.95) / price
            portfolio.buy(symbol, price, shares)
            position_open = True
            entry_price = price
        elif fast_ma < slow_ma and position_open:
            portfolio.sell(symbol, price, portfolio.positions.get(symbol, 0.0))
            position_open = False
            entry_price = None
        equity_curve.append(portfolio.mark_to_market({symbol: price}))
    equity_curve = np.array(equity_curve)
    running_max = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve - running_max) / running_max
    max_drawdown_pct = float(drawdown.min() * 100.0)
    perf = portfolio.performance({symbol: prices[-1]})
    perf["max_drawdown_pct"] = max_drawdown_pct
    perf["equity_curve"] = equity_curve.tolist()
    perf["buy_and_hold_pnl_pct"] = 100.0 * (prices[-1] - prices[slow]) / prices[slow]
    if len(equity_curve) > 1:
        rets = np.diff(equity_curve) / equity_curve[:-1]
        perf["sharpe_ratio"] = float(rets.mean() / rets.std()) if rets.std() > 0 else None
    else:
        perf["sharpe_ratio"] = None
    return perf
