# tests/test_reporting.py
from src.reporting import compute_equity_curve, total_return_from_equity, sharpe_ratio_from_returns
import pandas as pd

def test_reporting_empty():
    eq = compute_equity_curve([])
    assert eq.empty
    assert total_return_from_equity(eq) == 0.0
    assert sharpe_ratio_from_returns(eq) == 0.0
