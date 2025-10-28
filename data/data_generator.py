import csv, random
from datetime import datetime, timedelta
from pathlib import Path

def generate_market_csv(filename="data/market_data.csv", symbol="TEST", start_price=100.0, n=300):
    p = Path(filename)
    p.parent.mkdir(parents=True, exist_ok=True)
    base = datetime(2024,1,1,9,30)
    price = start_price
    with p.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","symbol","price"])
        for i in range(n):
            price *= 1 + random.uniform(-0.01, 0.01)
            writer.writerow([(base + timedelta(minutes=i)).isoformat(sep=" "), symbol, round(price,2)])
    print("Generated", filename)
