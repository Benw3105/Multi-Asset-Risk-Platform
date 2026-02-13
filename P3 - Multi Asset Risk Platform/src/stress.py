import pandas as pd
import numpy as np

def apply_shock(prices, shocks):
    """
    Apply shocks to asset prices.
    
    prices : pd.DataFrame
        Historical prices (rows = dates, columns = assets)
    shocks : dict
        Asset: shock factor (e.g., -0.1 for -10%)
    """
    shocked_prices = prices.copy()
    for asset, shock in shocks.items():
        if asset in shocked_prices.columns:
            shocked_prices[asset] = shocked_prices[asset] * (1 + shock)
        else:
            raise ValueError(f"Asset {asset} not in price data.")
    return shocked_prices

def portfolio_value(weights, prices):
    """
    Compute portfolio value given weights and price data.
    
    weights : array-like
        Portfolio weights (sum=1)
    prices : pd.DataFrame
        Asset prices
    """
    return (prices * weights).sum(axis=1)

def stress_test(prices, weights, shocks):
    """
    Run stress test on portfolio.
    
    prices : pd.DataFrame
        Historical prices
    weights : array-like
        Portfolio weights
    shocks : dict
        Asset shocks
    """
    shocked_prices = apply_shock(prices, shocks)
    stressed_portfolio = portfolio_value(weights, shocked_prices)
    return stressed_portfolio

def example_shocks(prices):
    """Return example scenarios for testing."""
    return {
        "down_10": {col: -0.10 for col in prices.columns},
        "up_10": {col: 0.10 for col in prices.columns},
        "mixed": {col: (-0.1 if i % 2 == 0 else 0.05) for i, col in enumerate(prices.columns)}
    }

# --- Wrapper so app.py can import ---
def run_stress_test(prices: pd.DataFrame, weights: np.ndarray, shocks: dict) -> pd.Series:
    """
    Apply a shock scenario to portfolio prices and return portfolio value as a pd.Series.
    """
    shocked_prices = prices.copy()
    for asset, shock in shocks.items():
        if asset in shocked_prices.columns:
            shocked_prices[asset] = shocked_prices[asset] * (1 + shock)
        else:
            raise ValueError(f"Asset {asset} not in price data.")
    
    stressed_portfolio = (shocked_prices * weights).sum(axis=1)
    return stressed_portfolio

