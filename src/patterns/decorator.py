# src/patterns/decorator.py
from abc import ABC, abstractmethod
from typing import Dict, List
import statistics
import math

# Simple interface: object must provide price_series (list of floats) and symbol
class InstrumentComponent(ABC):
    @abstractmethod
    def get_metrics(self) -> Dict:
        """Return a dict of computed metrics."""
        pass

class BasicInstrument(InstrumentComponent):
    def __init__(self, symbol: str, price_series: List[float]):
        self.symbol = symbol
        self.price_series = list(price_series)

    def get_metrics(self):
        # Basic metrics
        return {
            "symbol": self.symbol,
            "first_price": self.price_series[0] if self.price_series else None,
            "last_price": self.price_series[-1] if self.price_series else None,
            "n_points": len(self.price_series)
        }

class DecoratorBase(InstrumentComponent):
    def __init__(self, wrapped: InstrumentComponent):
        self._wrapped = wrapped

    def get_metrics(self):
        # start with wrapped metrics
        return dict(self._wrapped.get_metrics())

class VolatilityDecorator(DecoratorBase):
    def get_metrics(self):
        m = super().get_metrics()
        ps = getattr(self._wrapped, "price_series", []) or []
        if len(ps) < 2:
            m["volatility"] = 0.0
        else:
            returns = [(ps[i]/ps[i-1] - 1.0) for i in range(1, len(ps))]
            m["volatility"] = statistics.pstdev(returns)
        return m

class MaxDrawdownDecorator(DecoratorBase):
    def get_metrics(self):
        m = super().get_metrics()
        ps = getattr(self._wrapped, "price_series", []) or []
        peak = -math.inf
        max_dd = 0.0
        for p in ps:
            if p > peak:
                peak = p
            if peak > 0:
                dd = (peak - p) / peak
                if dd > max_dd:
                    max_dd = dd
        m["max_drawdown"] = max_dd
        return m

class SimpleBetaDecorator(DecoratorBase):
    def __init__(self, wrapped, market_series):
        super().__init__(wrapped)
        self.market_series = list(market_series)

    def get_metrics(self):
        m = super().get_metrics()
        ps = getattr(self._wrapped, "price_series", []) or []
        if len(ps) < 2 or len(self.market_series) < 2:
            m["beta"] = None
            return m
        # align lengths (use min length from the end)
        L = min(len(ps), len(self.market_series))
        asset_returns = [(ps[i]/ps[i-1]-1) for i in range(-L+1, 0)]
        market_returns = [(self.market_series[i]/self.market_series[i-1]-1) for i in range(-L+1, 0)]
        # covariance / variance
        mean_a = statistics.mean(asset_returns)
        mean_m = statistics.mean(market_returns)
        cov = sum((a-mean_a)*(b-mean_m) for a,b in zip(asset_returns, market_returns)) / len(asset_returns)
        var_m = statistics.pstdev(market_returns) ** 2
        beta = cov / var_m if var_m != 0 else None
        m["beta"] = beta
        return m
