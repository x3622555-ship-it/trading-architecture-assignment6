# tests/test_singleton.py
from src.patterns.singleton import Config
import json, tempfile

def test_singleton_reads(tmp_path):
    cfg = tmp_path/"cfg.json"
    cfg.write_text('{"x":1}')
    c1 = Config(str(cfg))
    c2 = Config(str(cfg))
    assert c1 is c2
    assert c1.get("x") == 1
