import csv
from datetime import datetime
from pathlib import Path
from models import MarketDataPoint

def load_market_data(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{path} not found")
    rows = []
    with p.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            ts = datetime.fromisoformat(r['timestamp'])
            rows.append(MarketDataPoint(timestamp=ts, symbol=r['symbol'], price=float(r['price'])))
    return rows
