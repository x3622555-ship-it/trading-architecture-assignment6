# tests/test_strategies.py
from src.patterns.strategy import MovingAverageCrossoverStrategy, MeanReversionStrategy

def test_ma_crossover_generates_signals():
    s = MovingAverageCrossoverStrategy(short_window=2, long_window=3, order_size=2)
    ticks = [
        {'symbol':'TST','price':100},
        {'symbol':'TST','price':101},
        {'symbol':'TST','price':102},  # now long window filled -> short_ma > long_ma => BUY
    ]
    out = []
    for t in ticks:
        out.extend(s.on_tick(t))
    assert any(sig.side == "BUY" for sig in out)
