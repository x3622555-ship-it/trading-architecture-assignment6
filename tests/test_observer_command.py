# tests/test_observer_command.py
from src.patterns.observer import Publisher, LoggerObserver, AlertObserver
from src.patterns.command import ExecuteOrderCommand, CommandInvoker
from src.models import Portfolio, Stock, Position

def test_observer_and_command():
    # setup
    pub = Publisher()
    logger = LoggerObserver()
    alert = AlertObserver(threshold_value=200)
    pub.attach(logger)
    pub.attach(alert)

    # portfolio
    pf = Portfolio(owner="Test")
    inv = CommandInvoker()

    # execute a command
    cmd = ExecuteOrderCommand(pf, "TST", 1, 100)  # small trade
    res = inv.execute_cmd(cmd)
    # notify
    pub.notify({"type":"execution","symbol":"TST","qty":1,"price":100})
    assert len(logger.records) >= 1
    assert alert.alerts == []  # threshold not reached

    # big trade triggers alert
    cmd2 = ExecuteOrderCommand(pf, "BIG", 200, 100)  # value 20,000
    inv.execute_cmd(cmd2)
    pub.notify({"type":"execution","symbol":"BIG","qty":200,"price":100})
    assert len(alert.alerts) >= 1
