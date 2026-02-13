# Multi-Asset Risk Platform

A Python-powered dashboard for analyzing and stress-testing multi-asset portfolios.  
Built with **Streamlit**, this platform allows you to explore portfolio strategies, compute rolling statistics, and run stress scenarios on historical market data.

---

## Features

- **Portfolio Strategies**: Equal weight, 60/40 equity-bond, static minimum variance, and rolling minimum variance  
- **Rolling Statistics**: Mean, volatility, and Sharpe ratio over customizable windows  
- **Stress Testing**: Apply predefined or custom shocks to portfolio assets  
- **Data Sources**: Yahoo Finance ETFs (SPY, IEF, GLD) and FRED commodities/indices (Brent, NatGas, DXY)  
- **Interactive Dashboard**: Fully interactive charts and tables via Streamlit  

---

## Project Structure

```bash
Multi-Asset Risk Platform/
│
├── app.py                     # Streamlit dashboard
├── requirements.txt           # Project dependencies
├── README.md                  # Project overview and instructions
│
├── data/
│   ├── raw/                   # Raw downloaded CSVs
│   │   └── prices_raw.csv
│   └── processed/             # Cleaned and processed CSVs
│       ├── prices_clean.csv
│       └── returns.csv
│
└── src/                       # Source code
    ├── __init__.py
    ├── data_loader.py         # Data downloading and processing
    ├── portfolio.py           # Portfolio strategies and backtesting
    ├── risk.py                # Portfolio metrics and risk calculations
    ├── stress.py              # Stress test logic
    └── time_series.py         # Rolling statistics functions
```

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd "P3 - Multi Asset Risk Platform"
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```
