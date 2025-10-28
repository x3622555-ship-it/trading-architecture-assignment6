# src/patterns/composite.py
from abc import ABC, abstractmethod
from typing import List
from ..models import Position  # expecting Position dataclass

class PortfolioComponent(ABC):
    @abstractmethod
    def total_value(self, price_map: dict) -> float:
        pass

    @abstractmethod
    def list_positions(self) -> List[Position]:
        pass

class PositionLeaf(PortfolioComponent):
    def __init__(self, position: Position):
        self.position = position

    def total_value(self, price_map: dict) -> float:
        price = price_map.get(self.position.instrument.symbol, self.position.avg_price)
        return self.position.market_value(price)

    def list_positions(self):
        return [self.position]

class PortfolioGroup(PortfolioComponent):
    def __init__(self, name: str):
        self.name = name
        self.children: List[PortfolioComponent] = []

    def add(self, comp: PortfolioComponent):
        self.children.append(comp)

    def total_value(self, price_map: dict) -> float:
        return sum(c.total_value(price_map) for c in self.children)

    def list_positions(self):
        out = []
        for c in self.children:
            out.extend(c.list_positions())
        return out
