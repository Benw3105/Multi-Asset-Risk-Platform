# src/risk.py
import numpy as np
import pandas as pd

def annualized_return(returns, periods_per_year=252):
    """Compute annualized return from daily returns."""
    cumulative = (1 + returns).prod()
    n_periods = len(returns)
    return cumulative**(periods_per_year / n_periods) - 1

def annualized_volatility(returns, periods_per_year=252):
    """Compute annualized volatility from daily returns."""
    return returns.std() * np.sqrt(periods_per_year)

def sharpe_ratio(returns, risk_free_rate=0, periods_per_year=252):
    ann_ret = annualized_return(returns, periods_per_year)
    ann_vol = annualized_volatility(returns, periods_per_year)
    return ann_ret / ann_vol if ann_vol != 0 else np.nan


def max_drawdown(returns):
    """Compute maximum drawdown from cumulative returns."""
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def portfolio_metrics(returns, periods_per_year=252):
    """Return all metrics in a dictionary."""
    return {
        "Annual Return": annualized_return(returns, periods_per_year),
        "Annual Volatility": annualized_volatility(returns, periods_per_year),
        "Sharpe Ratio": sharpe_ratio(returns, periods_per_year=periods_per_year),
        "Max Drawdown": max_drawdown(returns)
    }

# Alias for app.py compatibility
compute_risk_metrics = portfolio_metrics
