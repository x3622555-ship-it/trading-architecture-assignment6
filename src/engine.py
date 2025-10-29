# src/engine.py
from typing import List, Dict, Any
from src.patterns.observer import Publisher
from src.patterns.command import CommandInvoker, ExecuteOrderCommand
from src.patterns.strategy import Strategy, Signal
from src.models import Portfolio

class BacktestEngine:
    def __init__(self, portfolio: Portfolio, strategies: List[Strategy], publisher: Publisher = None):
        self.portfolio = portfolio
        self.strategies = strategies
        self.publisher = publisher or Publisher()
        self.invoker = CommandInvoker()
        self.executions: List[Dict[str, Any]] = []

    def run(self, market_ticks: List[Dict[str, Any]]):
        """
        market_ticks: list of dicts {timestamp, symbol, price}
        Returns: dict with executions list and portfolio reference
        """
        for tick in market_ticks:
            for strat in self.strategies:
                signals = strat.on_tick(tick)
                for sig in signals:
                    # 1) publish the signal
                    self.publisher.notify({
                        "type": "signal",
                        "timestamp": tick.get("timestamp"),
                        "symbol": sig.symbol,
                        "side": sig.side,
                        "qty": sig.qty,
                        "price": sig.price,
                        "info": getattr(sig, "info", {})
                    })
                    # 2) build command and execute
                    qty_signed = sig.qty if sig.side == "BUY" else -sig.qty
                    cmd = ExecuteOrderCommand(self.portfolio, sig.symbol, qty_signed, sig.price)
                    res = self.invoker.execute_cmd(cmd)
                    # 3) publish execution
                    exec_event = {
                        "type": "execution",
                        "timestamp": tick.get("timestamp"),
                        "symbol": sig.symbol,
                        "side": sig.side,
                        "qty": sig.qty,
                        "price": sig.price
                    }
                    self.executions.append(exec_event)
                    self.publisher.notify(exec_event)
        return {"executions": self.executions, "portfolio": self.portfolio}
