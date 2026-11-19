"""
visualizer.py
Creates and saves analytical charts to the images/ folder:
1. Closing Price Trend + Peak/Trough Annotations
2. Moving Averages (Close vs SMA-20 vs SMA-50)
3. Daily Returns Distribution (Histogram + KDE)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd


sns.set_theme(style="whitegrid")


def plot_price_trend(df: pd.DataFrame, ticker: str, output_dir: str = "images") -> str:
    """Plots closing price trend with highest & lowest points highlighted."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{ticker}_price_trend.png")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Close"], color="#1f77b4", linewidth=2, label="Close Price")
    ax.fill_between(df.index, df["Close"], df["Close"].min() * 0.98, color="#1f77b4", alpha=0.08)

    # Annotate Peak and Trough
    max_idx = df["Close"].idxmax()
    min_idx = df["Close"].idxmin()
    ax.scatter(max_idx, df.loc[max_idx, "Close"], color="green", s=80, zorder=5, label=f"Peak: ${df.loc[max_idx, 'Close']:.2f}")
    ax.scatter(min_idx, df.loc[min_idx, "Close"], color="red", s=80, zorder=5, label=f"Low: ${df.loc[min_idx, 'Close']:.2f}")

    ax.set_title(f"{ticker} — Historical Closing Price Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Price ($)", fontsize=11)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate()
    ax.legend(loc="best")

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath


def plot_moving_averages(df: pd.DataFrame, ticker: str, output_dir: str = "images") -> str:
    """Plots Close Price against 20-Day and 50-Day Simple Moving Averages."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{ticker}_moving_averages.png")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Close"], color="#2c3e50", linewidth=1.6, alpha=0.85, label="Close Price")
    ax.plot(df.index, df["SMA_20"], color="#e67e22", linewidth=1.8, linestyle="--", label="20-Day SMA (Short-Term)")
    ax.plot(df.index, df["SMA_50"], color="#8e44ad", linewidth=2.0, label="50-Day SMA (Medium-Term)")

    ax.set_title(f"{ticker} — Price vs. Moving Averages (Trend Analysis)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Price ($)", fontsize=11)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.autofmt_xdate()
    ax.legend(loc="best")

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath


def plot_return_distribution(df: pd.DataFrame, ticker: str, output_dir: str = "images") -> str:
    """Plots daily return histogram with KDE curve and mean return marker."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{ticker}_return_distribution.png")

    returns_pct = df["Daily_Return"].dropna() * 100

    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.histplot(returns_pct, bins=40, kde=True, color="#16a085", edgecolor="white", ax=ax)

    mean_ret = returns_pct.mean()
    ax.axvline(mean_ret, color="#c0392b", linestyle="--", linewidth=2, label=f"Mean Return: {mean_ret:.3f}%")
    ax.axvline(0, color="black", linestyle=":", linewidth=1.2, label="Break-even (0%)")

    ax.set_title(f"{ticker} — Daily Returns Distribution & Volatility Profile", fontsize=14, fontweight="bold")
    ax.set_xlabel("Daily Return (%)", fontsize=11)
    ax.set_ylabel("Frequency (Trading Days)", fontsize=11)
    ax.legend(loc="best")

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close(fig)
    return filepath