# src/engine.py
from typing import List, Dict
from src.patterns.observer import Publisher
from src.patterns.command import CommandInvoker, ExecuteOrderCommand
from src.patterns.strategy import Strategy

class BacktestEngine:
    def __init__(self, portfolio, strategies: List[Strategy], publisher: Publisher=None):
        self.portfolio = portfolio
        self.strategies = strategies
        self.publisher = publisher if publisher else Publisher()
        self.invoker = CommandInvoker()
        self.executions = []  # list of dicts for reporting

    def run(self, market_ticks: List[Dict]):
        """
        market_ticks: list of tick dicts with keys: timestamp, symbol, price
        processes ticks sequentially
        """
        for tick in market_ticks:
            # gather signals from each strategy
            for strat in self.strategies:
                signals = strat.on_tick(tick)
                for sig in signals:
                    # notify observers about signal
                    self.publisher.notify({"type":"signal","symbol":sig.symbol,"side":sig.side,"qty":sig.qty,"price":sig.price,"info":sig.info})
                    # create execute command
                    cmd = ExecuteOrderCommand(self.portfolio, sig.symbol, sig.qty if sig.side=="BUY" else -sig.qty, sig.price)
                    res = self.invoker.execute_cmd(cmd)
                    # publish execution event
                    exec_event = {"type":"execution","symbol":sig.symbol,"side":sig.side,"qty":sig.qty,"price":sig.price}
                    self.executions.append(exec_event)
                    self.publisher.notify(exec_event)
        return {"executions": self.executions, "portfolio": self.portfolio}
