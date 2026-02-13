import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.data_loader import DataLoader
from src.portfolio import Portfolio
from src.stress import stress_test, example_shocks
from src.time_series import rolling_stats

st.set_page_config(page_title="Multi-Asset Risk Platform", layout="wide")
st.title("Multi-Asset Risk Platform Dashboard")

# ------------------
# Sidebar - Data
# ------------------
st.sidebar.header("Data Settings")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2010-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-01-01"))

loader = DataLoader()
prices, returns = loader.load_processed_data(
    start=start_date.strftime("%Y-%m-%d"),
    end=end_date.strftime("%Y-%m-%d")
)
st.sidebar.success(f"Loaded {len(prices.columns)} assets: {list(prices.columns)}")

# ------------------
# Portfolio
# ------------------
port = Portfolio(prices, returns)
metrics = port.performance_comparison()

st.header("Performance Comparison Table")
st.dataframe(pd.DataFrame(metrics).T, use_container_width=True)

# ------------------
# Stress Testing
# ------------------
st.header("Stress Testing")

# Generate example shock scenarios
shocks = example_shocks(prices)
scenario = st.selectbox("Select Scenario", list(shocks.keys()))

# Default to equal-weight portfolio
weights, _ = port.equal_weight()

# Run stress test using prices & weights
stressed_portfolio = stress_test(prices, weights, shocks[scenario])

# Display chart
st.line_chart(stressed_portfolio, width="stretch")



# ------------------
# Rolling Stats
# ------------------
st.header("Rolling Portfolio Statistics")
window = st.slider("Rolling Window (days)", 10, 120, 60)
portfolio_returns = returns.dot(weights).to_frame(name="Portfolio")
rolling = rolling_stats(portfolio_returns, window=window)

st.subheader("Rolling Mean")
st.line_chart(rolling["Rolling Mean"])
st.subheader("Rolling Volatility")
st.line_chart(rolling["Rolling Volatility"])
st.subheader("Rolling Sharpe Ratio")
st.line_chart(rolling["Rolling Sharpe"])
