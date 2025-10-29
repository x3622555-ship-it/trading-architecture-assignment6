# src/reporting.py
import pandas as pd
import numpy as np

def compute_equity_curve(trades: list, starting_cash: float = 0.0):
    """
    trades: list of dicts with keys: timestamp, symbol, side, qty, price
    returns: pandas.Series index=timestamp -> equity (cumulative P&L + starting cash)
    This is a simplified P&L runner assuming immediate execution and no slippage.
    """
    if not trades:
        return pd.Series(dtype=float)

    # build DataFrame
    df = pd.DataFrame(trades)
    # compute trade pnl: BUY reduces cash (negative), SELL increases cash (positive)
    df['signed'] = df['qty'].where(df['side']=='SELL', -df['qty'])
    df['cash_flow'] = -df['signed'] * df['price'] * -1  # simplified: BUY reduces cash
    # Actually: We'll compute cumulative cash by treating BUY as negative cash, SELL positive
    df['cash_effect'] = df.apply(lambda r: -r['qty']*r['price'] if r['side']=='BUY' else r['qty']*r['price'], axis=1)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').set_index('timestamp')
    equity = df['cash_effect'].cumsum() + starting_cash
    return equity

def total_return_from_equity(equity: pd.Series):
    if equity.empty:
        return 0.0
    start = equity.iloc[0]
    end = equity.iloc[-1]
    if start == 0:
        # If starting cash =0, return absolute change
        return float(end)
    return float((end - start) / abs(start) * 100.0)

def sharpe_ratio_from_returns(equity: pd.Series, periods_per_year: int = 252):
    if equity.empty or len(equity) < 2:
        return 0.0
    rets = equity.pct_change().dropna()
    mean = rets.mean()
    std = rets.std()
    if std == 0 or np.isnan(std):
        return 0.0
    sharpe = (mean / std) * (periods_per_year ** 0.5)
    return float(sharpe)
