"""
data_loader.py
Handles fetching stock market data from Yahoo Finance (yfinance),
providing an automatic local CSV fallback (or synthetic sample data if offline),
and cleaning/standardizing the dataset.
"""

import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import yfinance as yf


def generate_sample_csv(filepath: str, ticker: str = "DEMO", days: int = 252) -> str:
    """
    Generates realistic synthetic OHLCV stock data as a CSV fallback
    so the project can always be tested offline.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    np.random.seed(42)

    dates = pd.bdate_range(end=datetime.today(), periods=days)
    daily_returns = np.random.normal(loc=0.0006, scale=0.018, size=days)
    close_prices = 150.0 * np.cumprod(1 + daily_returns)

    open_prices = close_prices * (1 + np.random.normal(0, 0.005, size=days))
    high_prices = np.maximum(open_prices, close_prices) * (1 + np.abs(np.random.normal(0, 0.008, size=days)))
    low_prices = np.minimum(open_prices, close_prices) * (1 - np.abs(np.random.normal(0, 0.008, size=days)))
    volumes = np.random.randint(1_500_000, 8_000_000, size=days)

    df = pd.DataFrame({
        "Date": dates.strftime("%Y-%m-%d"),
        "Open": np.round(open_prices, 2),
        "High": np.round(high_prices, 2),
        "Low": np.round(low_prices, 2),
        "Close": np.round(close_prices, 2),
        "Volume": volumes,
    })
    df.to_csv(filepath, index=False)
    print(f"[INFO] Generated offline sample dataset for '{ticker}' at: {filepath}")
    return filepath


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw OHLCV data:
    - Flattens MultiIndex columns (common in newer yfinance versions)
    - Ensures DatetimeIndex sorted chronologically
    - Enforces numeric types and removes missing/invalid rows
    """
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty. Cannot clean stock data.")

    df = df.copy()

    # Flatten MultiIndex columns if present (e.g., ('Close', 'AAPL') -> 'Close')
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Move Date from column to index if needed
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df = df.set_index("Date")
    else:
        df.index = pd.to_datetime(df.index, errors="coerce")
        df = df[~df.index.isna()]

    df.index.name = "Date"

    # Standardize required numeric columns
    required_cols = ["Open", "High", "Low", "Close", "Volume"]
    for col in required_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort oldest -> newest and remove duplicate dates
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="first")]

    # Drop rows where Close price is missing, forward-fill minor gaps if any
    df = df.dropna(subset=["Close"])
    df = df.ffill().dropna()

    return df


def fetch_stock_data(
    ticker: str,
    start_date: str,
    end_date: str,
    csv_fallback_path: str | None = None,
    save_raw: bool = True,
) -> tuple[pd.DataFrame, str]:
    """
    Fetches historical stock data via yfinance.
    Falls back to a local CSV file (or generates a sample CSV) if the API fails.

    Returns:
        (cleaned_dataframe, data_source_label)
    """
    ticker = ticker.strip().upper()
    os.makedirs("data", exist_ok=True)
    raw_cache_path = os.path.join("data", f"{ticker}_raw.csv")

    # 1. Attempt live Yahoo Finance download
    try:
        print(f"[INFO] Downloading '{ticker}' data from Yahoo Finance ({start_date} to {end_date})...")
        raw_df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)

        if raw_df is not None and not raw_df.empty:
            cleaned_df = clean_stock_data(raw_df)
            if save_raw:
                cleaned_df.to_csv(raw_cache_path)
            return cleaned_df, "Yahoo Finance (yfinance)"
        else:
            print(f"[WARNING] No online records returned for '{ticker}'. Switching to CSV fallback...")
    except Exception as exc:
        print(f"[WARNING] Yahoo Finance fetch failed ({exc}). Switching to CSV fallback...")

    # 2. CSV Fallback Path
    fallback_file = csv_fallback_path or raw_cache_path
    if not os.path.exists(fallback_file):
        fallback_file = os.path.join("data", f"{ticker}_sample.csv")
        generate_sample_csv(fallback_file, ticker=ticker)

    print(f"[INFO] Loading stock data from CSV: {fallback_file}")
    csv_df = pd.read_csv(fallback_file)
    cleaned_df = clean_stock_data(csv_df)
    return cleaned_df, f"Local CSV ({os.path.basename(fallback_file)})"