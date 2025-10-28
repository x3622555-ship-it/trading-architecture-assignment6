# src/patterns/factory.py
from typing import Dict
from ..models import Stock, Bond, ETF, Instrument

class InstrumentFactory:
    @staticmethod
    def create_instrument(data: Dict) -> Instrument:
        """
        data: dict with keys 'type', 'symbol', 'name', and other attributes
        """
        typ = data.get("type", "").strip().lower()
        symbol = data.get("symbol", "")
        name = data.get("name", "")
        attrs = data.get("attributes", {})

        if typ == "stock":
            return Stock(symbol=symbol, name=name, attributes=attrs)
        if typ == "bond":
            return Bond(symbol=symbol, name=name, attributes=attrs)
        if typ == "etf":
            return ETF(symbol=symbol, name=name, attributes=attrs)

        # fallback generic Instrument
        return Instrument(symbol=symbol, name=name, instrument_type=typ or "Unknown", attributes=attrs)
