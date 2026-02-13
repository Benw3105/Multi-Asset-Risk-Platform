import os
from typing import Tuple

import numpy as np
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr

# Data sources
YF_TICKERS = ["SPY", "IEF", "GLD"]  # ETFs from Yahoo
FRED_SERIES = {
    "Brent": "DCOILBRENTEU",  # Brent Crude
    "NatGas": "DHHNGSP",      # Natural Gas
    "DXY": "DTWEXBGS",        # US Dollar Index
}


class DataLoader:
    """
    Download and process multi-asset price data:
      - Yahoo Finance tickers (via yfinance)
      - FRED series (via pandas_datareader)
      Saves raw and processed CSVs under the project folder.
    """

    def __init__(self, project_dir: str = None):
        # Default to the project folder
        if project_dir is None:
            project_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..")
            )
        self.raw_dir = os.path.join(project_dir, "data", "raw")
        self.processed_dir = os.path.join(project_dir, "data", "processed")
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    def fetch_yahoo(self, start: str, end: str = None) -> pd.DataFrame:
        dfs = {}
        for ticker in YF_TICKERS:
            tk = yf.Ticker(ticker)
            hist = tk.history(start=start, end=end, auto_adjust=True)
            prices = hist["Close"] if "Close" in hist else hist["Adj Close"]
            # Remove timezone info to avoid concat issues
            prices.index = prices.index.tz_localize(None)
            dfs[ticker] = prices.rename(ticker)
        return pd.concat(dfs.values(), axis=1)

    def fetch_fred(self, start: str, end: str = None) -> pd.DataFrame:
        series_list = {}
        for name, code in FRED_SERIES.items():
            s = pdr.DataReader(code, "fred", start, end)
            # Ensure tz-naive
            s.index = pd.to_datetime(s.index).tz_localize(None)
            series_list[name] = s.rename(columns={code: name})
        return pd.concat(series_list.values(), axis=1)

    def download_all(self, start: str = "2010-01-01", end: str = None) -> pd.DataFrame:
        yf_df = self.fetch_yahoo(start, end)
        fred_df = self.fetch_fred(start, end)
        df = pd.concat([yf_df, fred_df], axis=1)
        return df

    @staticmethod
    def clean_prices(prices: pd.DataFrame) -> pd.DataFrame:
        return prices.ffill().dropna()

    @staticmethod
    def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
        numeric = prices.apply(pd.to_numeric, errors="coerce")
        numeric = numeric.replace(0, np.nan)
        returns = np.log(numeric / numeric.shift(1))
        returns.iloc[0] = 0
        return returns.fillna(0)

    def load_processed_data(
        self, start: str = "2010-01-01", end: str = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        raw_file = os.path.join(self.raw_dir, "prices_raw.csv")
        clean_file = os.path.join(self.processed_dir, "prices_clean.csv")
        returns_file = os.path.join(self.processed_dir, "returns.csv")

        if os.path.exists(raw_file):
            prices = pd.read_csv(raw_file, index_col=0, parse_dates=True)
        else:
            prices = self.download_all(start=start, end=end)
            prices.to_csv(raw_file, index=True)

        prices_clean = self.clean_prices(prices)
        prices_clean.index = pd.to_datetime(prices_clean.index)
        prices_clean = prices_clean.dropna(how="any", axis=0).sort_index()
        returns = self.compute_log_returns(prices_clean)

        # Save processed CSVs
        prices_clean.to_csv(clean_file, index=True)
        returns.to_csv(returns_file, index=True)

        return prices_clean, returns


if __name__ == "__main__":
    loader = DataLoader()
    prices, returns = loader.load_processed_data(start="2010-01-01")
    print("Available tickers in data:", list(prices.columns))
    print("=== Prices (Top 5) ===")
    print(prices.head())
    print("=== Returns (Top 5) ===")
    print(returns.head())
