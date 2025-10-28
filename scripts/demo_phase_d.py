# scripts/demo_phase_d.py
from src.models import Portfolio
from src.patterns.strategy import MovingAverageCrossoverStrategy
from src.patterns.observer import Publisher, LoggerObserver
from src.engine import BacktestEngine
import csv

# load market ticks quickly from data/market_data.csv
ticks=[]
with open("data/market_data.csv","r") as f:
    reader = csv.DictReader(f)
    for r in reader:
        ticks.append({"timestamp": r["timestamp"], "symbol": r["symbol"], "price": float(r["price"])})

# setup
pf = Portfolio(owner="Demo")
strat = MovingAverageCrossoverStrategy(short_window=3, long_window=10, order_size=1)
pub = Publisher()
logger = LoggerObserver()
pub.attach(logger)

engine = BacktestEngine(pf, [strat], publisher=pub)
res = engine.run(ticks[:200])  # run first 200 ticks

print("Executions:", len(res["executions"]))
print("Logger records:", len(logger.records))
print("Portfolio positions:", [(p.instrument.symbol, p.quantity) for p in pf.positions])
