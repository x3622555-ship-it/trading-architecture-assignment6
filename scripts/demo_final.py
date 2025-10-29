import csv
from src.models import Portfolio
from src.patterns.strategy import MovingAverageCrossoverStrategy
from src.patterns.observer import Publisher, LoggerObserver
from src.engine import BacktestEngine
from src.reporting import compute_equity_curve, total_return_from_equity, sharpe_ratio_from_returns

# load ticks
ticks=[]
with open("data/market_data.csv") as f:
    reader = csv.DictReader(f)
    for i,r in enumerate(reader):
        if i>=300: break
        ticks.append({"timestamp": r["timestamp"], "symbol": r["symbol"], "price": float(r["price"])})

pf=Portfolio(owner="Demo")
strat=MovingAverageCrossoverStrategy(short_window=5,long_window=20,order_size=1)
pub=Publisher(); logger=LoggerObserver(); pub.attach(logger)
engine=BacktestEngine(pf,[strat],publisher=pub)
res=engine.run(ticks)

print("Executions:", len(res["executions"]))
print("Positions:", [(p.instrument.symbol,p.quantity) for p in pf.positions])
trades=[{"timestamp":e.get("timestamp"),"symbol":e.get("symbol"),"side":e.get("side"),"qty":e.get("qty"),"price":e.get("price")} for e in res["executions"]]
eq=compute_equity_curve(trades,0.0)
print("Total return:", total_return_from_equity(eq))
print("Sharpe:", sharpe_ratio_from_returns(eq))
