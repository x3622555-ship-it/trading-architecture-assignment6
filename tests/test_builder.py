# tests/test_builder.py
from src.patterns.builder import PortfolioBuilder

def test_portfolio_builder():
    builder = PortfolioBuilder().set_owner("Alice").add_stock("AAPL", 10, 150).add_stock("MSFT", 5, 300)
    portfolio = builder.build()
    assert portfolio.owner == "Alice"
    assert len(portfolio.positions) == 2
    # check a position symbol
    assert portfolio.positions[0].instrument.symbol == "AAPL"
