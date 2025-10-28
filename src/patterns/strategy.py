# src/patterns/strategy.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from collections import deque
import statistics

class Signal:
    def __init__(self, symbol: str, side: str, qty: float, price: float, info: Dict = None):
        self.symbol = symbol
        self.side = side  # "BUY" or "SELL"
        self.qty = qty
        self.price = price
        self.info = info or {}

    def __repr__(self):
        return f"<Signal {self.side} {self.qty} {self.symbol} @{self.price}>"

class Strategy(ABC):
    @abstractmethod
    def on_tick(self, tick: Dict) -> List[Signal]:
        """Accepts a tick dict {'timestamp', 'symbol', 'price'} and returns 0..n Signals"""
        pass

class MovingAverageCrossoverStrategy(Strategy):
    def __init__(self, short_window=5, long_window=20, order_size=1.0):
        self.short_w = short_window
        self.long_w = long_window
        self.order_size = order_size
        self.history = {}  # symbol -> deque

    def _get_series(self, symbol):
        if symbol not in self.history:
            self.history[symbol] = deque(maxlen=self.long_w)
        return self.history[symbol]

    def on_tick(self, tick):
        sym = tick['symbol']
        price = float(tick['price'])
        dq = self._get_series(sym)
        dq.append(price)
        signals = []
        if len(dq) >= self.long_w:
            series = list(dq)
            short_ma = statistics.mean(series[-self.short_w:])
            long_ma = statistics.mean(series)
            if short_ma > long_ma:
                signals.append(Signal(sym, "BUY", self.order_size, price, {"short_ma": short_ma, "long_ma": long_ma}))
            elif short_ma < long_ma:
                signals.append(Signal(sym, "SELL", self.order_size, price, {"short_ma": short_ma, "long_ma": long_ma}))
        return signals

class MeanReversionStrategy(Strategy):
    def __init__(self, lookback=20, threshold=0.02, order_size=1.0):
        self.lookback = lookback
        self.threshold = threshold
        self.order_size = order_size
        self.history = {}

    def _get_series(self, symbol):
        if symbol not in self.history:
            from collections import deque
            self.history[symbol] = deque(maxlen=self.lookback)
        return self.history[symbol]

    def on_tick(self, tick):
        sym = tick['symbol']
        price = float(tick['price'])
        dq = self._get_series(sym)
        dq.append(price)
        signals = []
        if len(dq) >= self.lookback:
            mean = statistics.mean(dq)
            dev = (price - mean) / mean
            if dev > self.threshold:
                signals.append(Signal(sym, "SELL", self.order_size, price, {"dev": dev, "mean": mean}))
            elif dev < -self.threshold:
                signals.append(Signal(sym, "BUY", self.order_size, price, {"dev": dev, "mean": mean}))
        return signals
