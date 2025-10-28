# tests/test_decorator.py
from src.patterns.decorator import BasicInstrument, VolatilityDecorator, MaxDrawdownDecorator, SimpleBetaDecorator

def test_decorators_basic():
    prices = [100, 102, 101, 105, 110]
    market = [200, 201, 200, 202, 205]
    basic = BasicInstrument("TST", prices)
    vol = VolatilityDecorator(basic).get_metrics()
    assert "volatility" in vol
    dd = MaxDrawdownDecorator(basic).get_metrics()
    assert "max_drawdown" in dd
    beta = SimpleBetaDecorator(basic, market).get_metrics()
    assert "beta" in beta
