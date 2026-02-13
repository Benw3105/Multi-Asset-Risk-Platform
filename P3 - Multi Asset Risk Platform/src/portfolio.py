import sys
import os
import numpy as np
import pandas as pd

# Ensure the project root is in sys.path so we can do absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Now absolute imports from src will work
from src.risk import portfolio_metrics
from src.time_series import rolling_stats
from src.stress import stress_test

class Portfolio:
    def __init__(self, prices, returns):
        self.prices = prices
        self.returns = returns
        self.assets = prices.columns.tolist()

    def equal_weight(self):
        n = len(self.assets)
        weights = np.ones(n) / n
        portfolio_value = (self.prices * weights).sum(axis=1)
        return weights, portfolio_value

    def equity_bond_weights(self, equity_idx=[0], bond_idx=[1]):
        weights = np.zeros(len(self.assets))
        n_eq = len(equity_idx)
        n_bond = len(bond_idx)
        for i in equity_idx:
            weights[i] = 0.6 / n_eq
        for i in bond_idx:
            weights[i] = 0.4 / n_bond
        portfolio_value = (self.prices * weights).sum(axis=1)
        return weights, portfolio_value

    def min_variance_weights(self):
        cov = self.returns.cov()
        inv_cov = np.linalg.pinv(cov.values)
        ones = np.ones(len(self.assets))
        weights = inv_cov.dot(ones) / ones.dot(inv_cov).dot(ones)
        portfolio_value = (self.prices * weights).sum(axis=1)
        return weights, portfolio_value

    def rolling_min_variance(self, window=60):
        rolled_portfolio = pd.Series(index=self.returns.index, dtype=float)
        for i in range(window, len(self.returns)):
            ret_window = self.returns.iloc[i-window:i]
            cov = ret_window.cov()
            inv_cov = np.linalg.pinv(cov.values)
            ones = np.ones(len(self.assets))
            weights = inv_cov.dot(ones) / ones.dot(inv_cov).dot(ones)
            rolled_portfolio.iloc[i] = (self.prices.iloc[i] * weights).sum()
        return rolled_portfolio.dropna()

    def performance_comparison(self):
        ew_w, ew_val = self.equal_weight()
        eq_w, eq_val = self.equity_bond_weights()
        mv_w, mv_val = self.min_variance_weights()
        rmv_val = self.rolling_min_variance()

        metrics = {
            "Equal Weight": portfolio_metrics(ew_val.pct_change().fillna(0)),
            "60/40": portfolio_metrics(eq_val.pct_change().fillna(0)),
            "Static Min Var": portfolio_metrics(mv_val.pct_change().fillna(0)),
            "Rolling Min Var": portfolio_metrics(rmv_val.pct_change().fillna(0)),
        }
        return metrics


# For testing directly
if __name__ == "__main__":
    # Generate dummy data
    dates = pd.date_range("2020-01-01", periods=100)
    prices = pd.DataFrame(
        np.cumprod(1 + np.random.randn(100, 6) * 0.01, axis=0),
        index=dates,
        columns=["SPY", "IEF", "GLD", "Brent", "NatGas", "DXY"]
    )
    returns = prices.pct_change().fillna(0)

    port = Portfolio(prices, returns)
    port.performance_comparison()
