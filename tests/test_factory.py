# tests/test_factory.py
import pytest
from src.patterns.factory import InstrumentFactory
from src.models import Stock, Bond, ETF

def test_factory_creates_stock():
    data = {"type":"stock","symbol":"AAPL","name":"Apple Inc.","attributes":{"sector":"Tech"}}
    inst = InstrumentFactory.create_instrument(data)
    assert isinstance(inst, Stock)
    assert inst.symbol == "AAPL"
    assert inst.attributes["sector"] == "Tech"

def test_factory_creates_bond_etf():
    assert isinstance(InstrumentFactory.create_instrument({"type":"bond","symbol":"B1","name":"Bond"}), Bond)
    assert isinstance(InstrumentFactory.create_instrument({"type":"etf","symbol":"E1","name":"ETF"}), ETF)
