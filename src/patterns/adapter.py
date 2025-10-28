# src/patterns/adapter.py
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, Any

# simple normalized representation
def _parse_iso(ts_str):
    try:
        # accept "YYYY-MM-DD HH:MM:SS" or ISO with T
        return datetime.fromisoformat(ts_str.replace("T", " "))
    except Exception:
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")

class YahooJSONAdapter:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_all(self) -> Dict[str, list]:
        """
        Example JSON schema (flexible). We'll read a list of quotes:
        [{"timestamp": "...", "symbol":"AAPL", "price": 150.0}, ...]
        Returns dict: symbol -> list of normalized dicts
        """
        with open(self.filepath) as fh:
            data = json.load(fh)
        out = {}
        for entry in data:
            sym = entry.get("symbol")
            ts = _parse_iso(entry.get("timestamp"))
            price = float(entry.get("price"))
            out.setdefault(sym, []).append({"timestamp": ts, "symbol": sym, "price": price})
        return out

class BloombergXMLAdapter:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_all(self):
        """
        Example simple XML:
        <feed>
          <quote><symbol>AAPL</symbol><time>2024-01-01T09:30:00</time><price>150.0</price></quote>
          ...
        </feed>
        """
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        out = {}
        for q in root.findall(".//quote"):
            sym = q.findtext("symbol")
            ts = _parse_iso(q.findtext("time"))
            price = float(q.findtext("price"))
            out.setdefault(sym, []).append({"timestamp": ts, "symbol": sym, "price": price})
        return out
