"""
demo_final.py — Phase F demonstration script for the Trading Backtester Project
Author: x3622555-ship-it
Description:
    Runs a mini backtest using the implemented design patterns
    (Factory, Singleton, Builder, Strategy, Observer, Command, Engine, Reporting)
    and prints performance summary results.
"""

import csv
import os
import datetime

from src.models import Portfolio
from src.patterns.strategy import MovingAverageCrossoverStrategy
from src.patterns.observer import Publisher, LoggerObserver, AlertObserver
from src.engine import BacktestEngine
from src.reporting import (
    compute_equity_curve,
    total_return_from_equity,
    sharpe_ratio_from_returns,
)

def load_market_data(path="data/market_data.csv", max_rows=300):
    """Simple CSV loader for demo purposes."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Please run data_generator first.")
    ticks = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for i, r in enumerate(reader):
            if i >= max_rows:
                break
            ticks.append(
                {
                    "timestamp": datetime.datetime.fromisoformat(r["timestamp"]),
                    "symbol": r["symbol"],
                    "price": float(r["price"]),
                }
            )
    return ticks


def main():
    print("🚀 Starting final backtest demo...\n")

    # Load small sample of generated data
    ticks = load_market_data("data/market_data.csv", max_rows=300)
    print(f"Loaded {len(ticks)} market ticks.\n")

    # Initialize key components
    portfolio = Portfolio(owner="DemoUser")
    strategy = MovingAverageCrossoverStrategy(short_window=5, long_window=20, order_size=1)

    publisher = Publisher()
    logger = LoggerObserver()
    alert = AlertObserver(threshold_value=20000)
    publisher.attach(logger)
    publisher.attach(alert)

    engine = BacktestEngine(portfolio, [strategy], publisher=publisher)

    # Run engine
    results = engine.run(ticks)
    executions = results.get("executions", [])
    print(f"✅ Backtest complete. Executions: {len(executions)}")

    # Compute performance
    equity = compute_equity_curve(executions, initial_capital=0.0)
    total_ret = total_return_from_equity(equity)
    sharpe = sharpe_ratio_from_returns(equity)

    print(f"\n📊 Performance Summary:")
    print(f"Total Return: {total_ret:.2%}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Number of Alerts: {len(alert.alerts)}\n")

    # Save summary to CSV
    summary_path = "data/results_summary.csv"
    os.makedirs("data", exist_ok=True)
    with open(summary_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["total_return", total_ret])
        writer.writerow(["sharpe_ratio", sharpe])
        writer.writerow(["executions", len(executions)])
    print(f"Results saved to {summary_path}")

    print("\n💡 Tip: View data/results_summary.csv to verify results or open in Excel.\n")


if __name__ == "__main__":
    main()
