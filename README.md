# 📈 Stock Market Data Analyzer

An automated Python financial data analytics pipeline and interactive dashboard that ingests historical stock market data, computes quantitative return & risk metrics, detects trend signals using moving averages, generates publication-ready charts, and exports executive summary reports.

---

## 🎯 Problem Statement
Retail investors, finance students, and junior analysts often rely on manual spreadsheets to analyze stock performance—an approach that is slow, error-prone, and difficult to scale across multiple tickers. **Stock Market Data Analyzer** solves this by automating data collection, cleaning, technical indicator engineering, risk evaluation, and executive reporting in a single modular Python workflow.

---

## 🏢 Industry Relevance
This project mirrors core workflows used across:
- **Investment Research & Asset Management:** Screening equities, tracking trend reversals, and evaluating risk-adjusted behavior.
- **FinTech & WealthTech Platforms:** Powering automated portfolio analytics and user-facing performance charts.
- **Financial & Data Analyst Roles:** Building reproducible ETL pipelines from noisy time-series APIs into clean KPI reports.

---

## ✨ Key Features
- **Resilient Data Ingestion:** Fetches live historical OHLCV data via Yahoo Finance (`yfinance`) with an automatic local CSV fallback & offline synthetic data generator.
- **Automated Data Cleaning:** Handles `yfinance` MultiIndex columns, datetime indexing, sorting, deduplication, and missing values.
- **Technical & Quantitative Metrics:**
  - Daily & Cumulative Returns (%)
  - 20-Day & 50-Day Simple Moving Averages (`SMA_20`, `SMA_50`)
  - Automated Trend Signal Classification (Bullish / Bearish / Consolidation)
  - Daily & Annualized Volatility ($\sigma \times \sqrt{252}$) + Risk Rating
  - Period High/Low & Maximum Drawdown (%)
- **Automated Visualizations:** Exports 3 high-DPI charts (`Price Trend`, `Moving Averages`, `Return Distribution`).
- **Executive Reporting:** Generates enriched CSV files (`outputs/`) and plain-English financial summary reports (`reports/`).
- **Interactive Web App:** Optional `Streamlit` dashboard (`app.py`) for visual exploration and CSV downloads.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Data Processing & Math:** `pandas`, `numpy`
- **Market Data API:** `yfinance`
- **Visualization:** `matplotlib`, `seaborn`
- **Interactive UI:** `streamlit`

---

## 📁 Folder Structure
```text
Stock-Market-Data-Analyzer/
├── data/               # Raw & fallback CSV datasets
├── src/                # Core modular Python package
│   ├── data_loader.py
│   ├── analyzer.py
│   ├── visualizer.py
│   └── report_generator.py
├── outputs/            # Enriched CSV datasets with indicators
├── images/             # Saved charts & dashboard screenshots
├── reports/            # Generated executive text reports
├── notebooks/          # Exploratory Jupyter notebooks
├── docs/               # Architecture & interview notes
├── app.py              # Streamlit interactive dashboard
├── main.py             # CLI pipeline entry point
├── requirements.txt    # Dependencies
└── README.md

## Authors

* **GitHub:** [nandiniverma2009](https://github.com)
* **LinkedIn:** [NandiniVerma](https://linkedin.com)

