# tests/test_models.py
from src.models import Stock, Position, Portfolio

def test_models_basic():
    s = Stock(symbol="TST", name="TestCorp")
    pos = Position(instrument=s, quantity=10, avg_price=100)
    pf = Portfolio(owner="Alice")
    pf.add_position(pos)
    assert pf.total_value({"TST": 110}) == 1100
