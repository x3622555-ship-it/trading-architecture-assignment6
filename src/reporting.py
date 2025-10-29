"""
reporting.py
-------------
Handles performance computation and reporting for the trading backtester.
Includes equity curve, total return, and Sharpe ratio calculations.
"""

import pandas as pd
import numpy as np


def compute_equity_curve(executions, initial_capital=0.0):
    """
    Build an equity curve (cumulative portfolio value over time)
    from a list of executed trades.

    Parameters
    ----------
    executions : list[dict]
        List of executed trades, each containing 'timestamp', 'price', and 'qty'.
    initial_capital : float, optional
        Starting capital value. Default is 0.0.

    Returns
    -------
    pd.Series
        Pandas Series indexed by timestamp, representing cumulative equity value.
    """
    if not executions:
        return pd.Series(dtype=float)

    df = pd.DataFrame(executions)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["trade_value"] = df["price"] * df["qty"]
    df["cum_value"] = df["trade_value"].cumsum() + initial_capital
    df.set_index("timestamp", inplace=True)

    return df["cum_value"]


def total_return_from_equity(equity_series: pd.Series) -> float:
    """
    Calculate total return as (final_value / initial_value - 1).

    Parameters
    ----------
    equity_series : pd.Series
        Series of portfolio values over time.

    Returns
    -------
    float
        Total return (e.g. 0.05 = 5%)
    """
    if equity_series.empty or equity_series.iloc[0] == 0:
        return 0.0

    initial_val = equity_series.iloc[0]
    final_val = equity_series.iloc[-1]
    return (final_val / initial_val) - 1.0


def sharpe_ratio_from_returns(equity_series: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Compute annualized Sharpe ratio from daily equity curve.

    Parameters
    ----------
    equity_series : pd.Series
        Portfolio equity values indexed by time.
    risk_free_rate : float
        Annual risk-free rate, default = 0.0

    Returns
    -------
    float
        Sharpe ratio.
    """
    if equity_series.empty or len(equity_series) < 2:
        return 0.0

    # Compute periodic returns
    returns = equity_series.pct_change().dropna()
    if returns.std() == 0:
        return 0.0

    excess = returns - risk_free_rate / len(returns)
    sharpe = np.sqrt(252) * excess.mean() / excess.std()
    return round(float(sharpe), 2)


def export_equity_to_csv(equity_series: pd.Series, filename: str = "data/equity_curve.csv"):
    """
    Export equity curve to a CSV file for inspection.

    Parameters
    ----------
    equity_series : pd.Series
        Equity curve data.
    filename : str
        Output CSV file path.
    """
    equity_series.to_csv(filename, header=["equity"])
    print(f"✅ Equity curve exported to {filename}")
