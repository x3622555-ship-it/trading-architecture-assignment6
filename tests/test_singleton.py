# tests/test_singleton.py
from src.patterns.singleton import Config

def test_singleton_reads_config(tmp_path):
    cfgfile = tmp_path / "cfg.json"
    cfgfile.write_text('{"k":"v"}')
    c1 = Config(str(cfgfile))
    c2 = Config(str(cfgfile))
    assert c1 is c2
    assert c1.get("k") == "v"
