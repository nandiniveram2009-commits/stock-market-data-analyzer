"""
analyzer.py
Performs quantitative stock analysis:
- Daily & cumulative returns
- Moving averages (SMA-20, SMA-50)
- Volatility (daily & annualized)
- Highest/lowest prices & max drawdown
- Trend classification & risk rating
"""

import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def enrich_with_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds technical & return indicators to the cleaned OHLCV DataFrame.
    """
    data = df.copy()

    # 1. Daily Percentage Return
    data["Daily_Return"] = data["Close"].pct_change()

    # 2. Cumulative Return (growth of $1 invested - 1)
    data["Cumulative_Return"] = (1 + data["Daily_Return"].fillna(0)).cumprod() - 1

    # 3. Moving Averages
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["SMA_50"] = data["Close"].rolling(window=50).mean()

    # 4. Rolling 20-Day Annualized Volatility
    data["Rolling_Vol_20"] = data["Daily_Return"].rolling(window=20).std() * np.sqrt(TRADING_DAYS_PER_YEAR)

    # 5. Running Peak & Drawdown
    data["Running_Max"] = data["Close"].cummax()
    data["Drawdown"] = (data["Close"] - data["Running_Max"]) / data["Running_Max"]

    return data


def compute_summary_metrics(df: pd.DataFrame, ticker: str, data_source: str) -> dict:
    """
    Computes executive KPIs and market insights from the enriched DataFrame.
    """
    start_price = float(df["Close"].iloc[0])
    end_price = float(df["Close"].iloc[-1])
    total_return_pct = ((end_price - start_price) / start_price) * 100

    highest_price = float(df["High"].max()) if "High" in df.columns else float(df["Close"].max())
    highest_date = df["High"].idxmax().strftime("%Y-%m-%d") if "High" in df.columns else df["Close"].idxmax().strftime("%Y-%m-%d")

    lowest_price = float(df["Low"].min()) if "Low" in df.columns else float(df["Close"].min())
    lowest_date = df["Low"].idxmin().strftime("%Y-%m-%d") if "Low" in df.columns else df["Close"].idxmin().strftime("%Y-%m-%d")

    returns = df["Daily_Return"].dropna()
    avg_daily_return_pct = float(returns.mean() * 100) if not returns.empty else 0.0
    daily_volatility_pct = float(returns.std() * 100) if not returns.empty else 0.0
    annualized_volatility_pct = float(returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR) * 100) if not returns.empty else 0.0

    best_day_pct = float(returns.max() * 100) if not returns.empty else 0.0
    worst_day_pct = float(returns.min() * 100) if not returns.empty else 0.0
    max_drawdown_pct = float(df["Drawdown"].min() * 100)

    # Trend Identification via Moving Averages
    latest_sma20 = df["SMA_20"].iloc[-1]
    latest_sma50 = df["SMA_50"].iloc[-1]

    if pd.notna(latest_sma20) and pd.notna(latest_sma50):
        if end_price > latest_sma20 > latest_sma50:
            trend_signal = "Strong Bullish (Price > SMA-20 > SMA-50)"
        elif end_price < latest_sma20 < latest_sma50:
            trend_signal = "Strong Bearish (Price < SMA-20 < SMA-50)"
        elif latest_sma20 > latest_sma50:
            trend_signal = "Moderately Bullish (SMA-20 > SMA-50)"
        else:
            trend_signal = "Consolidation / Bearish Bias (SMA-20 <= SMA-50)"
    else:
        trend_signal = "Insufficient data for 50-day SMA crossover"

    # Risk Classification based on Annualized Volatility
    if annualized_volatility_pct < 20:
        risk_level = "Low Risk"
    elif annualized_volatility_pct < 35:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    return {
        "ticker": ticker.upper(),
        "data_source": data_source,
        "start_date": df.index[0].strftime("%Y-%m-%d"),
        "end_date": df.index[-1].strftime("%Y-%m-%d"),
        "trading_days": int(len(df)),
        "start_price": round(start_price, 2),
        "end_price": round(end_price, 2),
        "total_return_pct": round(total_return_pct, 2),
        "highest_price": round(highest_price, 2),
        "highest_date": highest_date,
        "lowest_price": round(lowest_price, 2),
        "lowest_date": lowest_date,
        "avg_daily_return_pct": round(avg_daily_return_pct, 4),
        "daily_volatility_pct": round(daily_volatility_pct, 2),
        "annualized_volatility_pct": round(annualized_volatility_pct, 2),
        "best_day_pct": round(best_day_pct, 2),
        "worst_day_pct": round(worst_day_pct, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "latest_sma20": round(float(latest_sma20), 2) if pd.notna(latest_sma20) else None,
        "latest_sma50": round(float(latest_sma50), 2) if pd.notna(latest_sma50) else None,
        "trend_signal": trend_signal,
        "risk_level": risk_level,
    }