# tests/test_adapter.py
from src.patterns.adapter import YahooJSONAdapter, BloombergXMLAdapter

def test_yahoo_adapter(tmp_path):
    p = tmp_path/"y.json"
    p.write_text('[{"timestamp":"2024-01-01 09:30:00","symbol":"TST","price":100}]')
    adapter = YahooJSONAdapter(str(p))
    d = adapter.load_all()
    assert "TST" in d
    assert len(d["TST"]) == 1

def test_bloom_adapter(tmp_path):
    p = tmp_path/"b.xml"
    p.write_text('<feed><quote><symbol>TST</symbol><time>2024-01-01 09:30:00</time><price>100</price></quote></feed>')
    adapter = BloombergXMLAdapter(str(p))
    d = adapter.load_all()
    assert "TST" in d
