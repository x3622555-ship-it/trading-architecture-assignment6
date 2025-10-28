# src/models.py
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

@dataclass
class Instrument:
    symbol: str
    name: str
    instrument_type: str
    attributes: Dict = field(default_factory=dict)

    def __repr__(self):
        return f"<{self.instrument_type} {self.symbol}>"

@dataclass
class Stock(Instrument):
    instrument_type: str = "Stock"

@dataclass
class Bond(Instrument):
    instrument_type: str = "Bond"

@dataclass
class ETF(Instrument):
    instrument_type: str = "ETF"

@dataclass
class Position:
    instrument: Instrument
    quantity: float
    avg_price: float

    def market_value(self, price: float) -> float:
        return self.quantity * price

@dataclass
class Portfolio:
    owner: str
    positions: List[Position] = field(default_factory=list)

    def add_position(self, pos: Position):
        self.positions.append(pos)

    def total_value(self, price_map: dict) -> float:
        return sum(pos.market_value(price_map.get(pos.instrument.symbol, pos.avg_price)) for pos in self.positions)