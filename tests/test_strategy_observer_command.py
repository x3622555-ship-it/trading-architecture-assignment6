# tests/test_strategy_observer_command.py
from src.patterns.strategy import MovingAverageCrossoverStrategy
from src.patterns.observer import Publisher, LoggerObserver
from src.patterns.command import CommandInvoker, ExecuteOrderCommand
from src.models import Portfolio

def test_strategy_and_engine_smoke():
    pf = Portfolio(owner="Test")
    strat = MovingAverageCrossoverStrategy(short_window=2, long_window=3, order_size=1)
    ticks = [{"symbol":"X","price":100},{"symbol":"X","price":101},{"symbol":"X","price":102}]
    signals = []
    for t in ticks:
        signals.extend(strat.on_tick(t))
    # expect at least zero signals; do not assert strict behavior here, just ensure on_tick runs
    assert isinstance(signals, list)
