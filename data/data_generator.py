# data/data_generator.py

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

def generate_market_csv(filename="data/market_data.csv", symbol="AAPL", start_price=150.0, n=500):
    """
    Generates fake market price data and saves it to a CSV file.

    :param filename: Path where the CSV will be saved
    :param symbol: Stock symbol (e.g., 'AAPL')
    :param start_price: Starting price
    :param n: Number of data points to generate
    """
    p = Path(filename)
    p.parent.mkdir(parents=True, exist_ok=True)

    current_time = datetime(2024, 1, 1, 9, 30)
    price = start_price

    with p.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "symbol", "price"])

        for _ in range(n):
            # Simulate small random price movement
            price *= 1 + random.uniform(-0.01, 0.01)
            price = round(price, 2)
            writer.writerow([current_time.isoformat(sep=" "), symbol, price])
            current_time += timedelta(minutes=1)

    print(f"✅ Generated {filename} with {n} rows of market data.")

# Run automatically if executed directly
if __name__ == "__main__":
    generate_market_csv()
