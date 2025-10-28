# src/patterns/command.py
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass

class ExecuteOrderCommand(Command):
    def __init__(self, portfolio, symbol, qty, price):
        self.portfolio = portfolio  # a Portfolio object
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self._executed = False

    def execute(self):
        # simplistic: append or update position
        from src.models import Instrument, Position, Stock
        # find position
        for p in self.portfolio.positions:
            if p.instrument.symbol == self.symbol:
                # update avg price and quantity (simplified)
                total_qty = p.quantity + self.qty
                if total_qty == 0:
                    p.quantity = 0
                    self._executed = True
                    return {"status":"ok"}
                p.avg_price = (p.avg_price * p.quantity + self.price * self.qty) / total_qty
                p.quantity = total_qty
                self._executed = True
                return {"status":"ok"}
        # if not found create a new Stock position
        new_inst = Stock(symbol=self.symbol, name=self.symbol)
        new_pos = Position(instrument=new_inst, quantity=self.qty, avg_price=self.price)
        self.portfolio.add_position(new_pos)
        self._executed = True
        return {"status":"ok"}

    def undo(self):
        # naive undo: remove qty (not recomputing avg price precisely)
        for p in list(self.portfolio.positions):
            if p.instrument.symbol == self.symbol:
                p.quantity -= self.qty
                if p.quantity <= 0:
                    self.portfolio.positions.remove(p)
                self._executed = False
                return {"status":"undone"}
        return {"status":"nothing"}

class CommandInvoker:
    def __init__(self):
        self.history = []

    def execute_cmd(self, cmd: Command):
        res = cmd.execute()
        self.history.append(cmd)
        return res

    def undo_last(self):
        if not self.history:
            return None
        cmd = self.history.pop()
        return cmd.undo()
