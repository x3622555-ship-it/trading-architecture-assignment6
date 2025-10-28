# src/patterns/singleton.py
import json
from pathlib import Path
from typing import Any

class Config:
    _instance = None

    def __new__(cls, config_path: str = "data/config.json"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load(config_path)
        return cls._instance

    def _load(self, path: str):
        p = Path(path)
        if not p.exists():
            self._data = {}
            return
        with p.open() as fh:
            self._data = json.load(fh)

    def get(self, key: str, default: Any = None):
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value
