# tests/test_factory.py
from src.patterns.factory import InstrumentFactory
from src.models import Stock, Bond, ETF

def test_factory_types():
    assert isinstance(InstrumentFactory.create_instrument({"type":"stock","symbol":"A","name":"A"}), Stock)
    assert isinstance(InstrumentFactory.create_instrument({"type":"bond","symbol":"B","name":"B"}), Bond)
    assert isinstance(InstrumentFactory.create_instrument({"type":"etf","symbol":"E","name":"E"}), ETF)
