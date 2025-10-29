# scripts/demo_phase_e.py
import csv
from src.models import Portfolio
from src.patterns.strategy import MovingAverageCrossoverStrategy
from src.patterns.observer import Publisher, LoggerObserver
from src.engine import BacktestEngine
from src.reporting import compute_equity_curve, total_return_from_equity, sharpe_ratio_from_returns
import matplotlib.pyplot as plt
import pandas as pd

# load market ticks (first N rows)
ticks = []
with open("data/market_data.csv", "r") as f:
    reader = csv.DictReader(f)
    for i, r in enumerate(reader):
        if i >= 500: break
        ticks.append({"timestamp": r["timestamp"], "symbol": r["symbol"], "price": float(r["price"])})

# setup
pf = Portfolio(owner="Demo")
strat = MovingAverageCrossoverStrategy(short_window=5, long_window=20, order_size=1)
pub = Publisher()
logger = LoggerObserver()
pub.attach(logger)

engine = BacktestEngine(pf, [strat], publisher=pub)
res = engine.run(ticks)

print("Executions:", len(res["executions"]))

# Build trade list for reporting (logger has events; filter executions)
trades = [e for e in res["executions"]]
equity = compute_equity_curve(trades, starting_cash=0.0)

print("Data points:", len(ticks))
print("Total Return:", total_return_from_equity(equity))
print("Sharpe Ratio:", sharpe_ratio_from_returns(equity))

# optional plot (only if matplotlib installed)
if not equity.empty:
    equity.plot(title="Equity Curve")
    plt.show()
