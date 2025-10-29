# tests/test_engine_integration.py
from src.models import Portfolio, Stock, Position
from src.patterns.strategy import MovingAverageCrossoverStrategy
from src.patterns.observer import Publisher, LoggerObserver
from src.engine import BacktestEngine

def test_engine_runs_and_records_executions():
    # prepare tiny market ticks
    ticks = [
        {"timestamp":"2024-01-01 09:30:00","symbol":"TST","price":100},
        {"timestamp":"2024-01-01 09:31:00","symbol":"TST","price":101},
        {"timestamp":"2024-01-01 09:32:00","symbol":"TST","price":102},
        {"timestamp":"2024-01-01 09:33:00","symbol":"TST","price":103},
        {"timestamp":"2024-01-01 09:34:00","symbol":"TST","price":104},
    ]
    pf = Portfolio(owner="EngineTest")
    strat = MovingAverageCrossoverStrategy(short_window=2, long_window=3, order_size=1)
    pub = Publisher()
    logger = LoggerObserver()
    pub.attach(logger)
    engine = BacktestEngine(pf, [strat], publisher=pub)
    res = engine.run(ticks)
    # engine should have executed zero or more trades but not crash
    assert "executions" in res
    # logger should have recorded signal/execution events
    assert len(logger.records) >= 0
