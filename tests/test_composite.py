# tests/test_composite.py
from src.models import Stock, Position
from src.patterns.composite import PositionLeaf, PortfolioGroup

def test_composite_value():
    s = Stock(symbol="TST", name="Test")
    pos = Position(instrument=s, quantity=10, avg_price=100)
    leaf = PositionLeaf(pos)
    pg = PortfolioGroup("root")
    pg.add(leaf)
    assert pg.total_value({"TST": 110}) == 110*10
    assert len(pg.list_positions()) == 1
