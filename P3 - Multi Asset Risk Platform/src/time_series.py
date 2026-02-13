import pandas as pd
import numpy as np

def rolling_mean(returns, window=20):
    """Compute rolling mean of returns."""
    return returns.rolling(window=window).mean()

def rolling_volatility(returns, window=20):
    """Compute rolling volatility of returns."""
    return returns.rolling(window=window).std()

def rolling_sharpe(returns, window=20, risk_free_rate=0):
    """Compute rolling Sharpe ratio."""
    mean = rolling_mean(returns, window)
    vol = rolling_volatility(returns, window)
    return (mean - risk_free_rate) / vol

# --- Wrapper for app.py ---
def rolling_stats(returns: pd.DataFrame, window: int = 20):
    rolling_mean = returns.rolling(window).mean()
    rolling_vol = returns.rolling(window).std()
    rolling_sharpe = rolling_mean / rolling_vol.replace(0, np.nan)
    return {
        "Rolling Mean": rolling_mean,
        "Rolling Volatility": rolling_vol,
        "Rolling Sharpe": rolling_sharpe
    }

