# scripts/demo_phase_c.py
from src.patterns.decorator import BasicInstrument, VolatilityDecorator, MaxDrawdownDecorator
from src.patterns.adapter import YahooJSONAdapter
from src.patterns.composite import PositionLeaf, PortfolioGroup
from src.models import Stock, Position

# 1) create basic instrument and decorate
prices = [100, 102, 101, 105, 110]
basic = BasicInstrument("TST", prices)
decorated = MaxDrawdownDecorator(VolatilityDecorator(basic))
print("Decorator metrics:", decorated.get_metrics())

# 2) adapter example (if you have data/sample_yahoo.json)
# adapter = YahooJSONAdapter("data/sample_yahoo.json")
# d = adapter.load_all()
# print("Adapter loaded:", d)

# 3) composite example
s = Stock("TST", "Test")
p = Position(s, 10, 100)
leaf = PositionLeaf(p)
group = PortfolioGroup("root")
group.add(leaf)
print("Composite total:", group.total_value({"TST": 110}))
