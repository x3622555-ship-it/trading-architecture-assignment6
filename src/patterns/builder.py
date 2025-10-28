# src/patterns/builder.py
from ..models import Portfolio, Position, Stock

class PortfolioBuilder:
    def __init__(self, owner: str = "Unknown"):
        self.owner = owner
        self.positions = []

    def set_owner(self, owner: str):
        self.owner = owner
        return self

    def add_stock(self, symbol: str, quantity: float, avg_price: float, name: str = ""):
        # For simplicity we create Stock instrument; extend as needed
        inst = Stock(symbol=symbol, name=name or symbol)
        pos = Position(instrument=inst, quantity=quantity, avg_price=avg_price)
        self.positions.append(pos)
        return self

    def add_position(self, position):
        self.positions.append(position)
        return self

    def build(self) -> Portfolio:
        p = Portfolio(owner=self.owner)
        for pos in self.positions:
            p.add_position(pos)
        return p
