# src/patterns/observer.py
from abc import ABC, abstractmethod
from typing import List, Dict

class Observer(ABC):
    @abstractmethod
    def update(self, event: Dict):
        pass

class Publisher:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, obs: Observer):
        if obs not in self._observers:
            self._observers.append(obs)

    def detach(self, obs: Observer):
        if obs in self._observers:
            self._observers.remove(obs)

    def notify(self, event: Dict):
        for o in list(self._observers):
            try:
                o.update(event)
            except Exception:
                # best-effort; do not stop others
                pass

# Concrete observers
class LoggerObserver(Observer):
    def __init__(self):
        self.records = []

    def update(self, event):
        self.records.append(event)

class AlertObserver(Observer):
    def __init__(self, threshold_value=10000):
        self.alerts = []
        self.threshold_value = threshold_value

    def update(self, event):
        # if event is order executed and value exceeds threshold -> alert
        if event.get("type") == "execution":
            value = event.get("qty",0) * event.get("price",0)
            if value >= self.threshold_value:
                self.alerts.append({"symbol": event.get("symbol"), "value": value})
