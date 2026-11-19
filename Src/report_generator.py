"""
report_generator.py
Exports:
1. Processed CSV dataset with calculated indicators -> outputs/
2. Human-readable Executive Financial Summary Report -> reports/
"""

import os
from datetime import datetime
import pandas as pd


def save_processed_csv(df: pd.DataFrame, ticker: str, output_dir: str = "outputs") -> str:
    """Saves the enriched DataFrame (prices + returns + SMAs + drawdown) to CSV."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{ticker}_analyzed_data.csv")
    df.to_csv(filepath)
    return filepath


def generate_text_report(metrics: dict, chart_paths: list[str], report_dir: str = "reports") -> str:
    """Generates a formatted text/markdown executive summary report."""
    os.makedirs(report_dir, exist_ok=True)
    ticker = metrics["ticker"]
    filepath = os.path.join(report_dir, f"{ticker}_summary_report.txt")

    report_content = f"""
====================================================================
           STOCK MARKET DATA ANALYZER — EXECUTIVE REPORT
====================================================================
Generated On      : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Ticker Symbol     : {ticker}
Data Source       : {metrics["data_source"]}
Analysis Period   : {metrics["start_date"]} to {metrics["end_date"]} ({metrics["trading_days"]} trading days)

--------------------------------------------------------------------
1. PRICE PERFORMANCE SUMMARY
--------------------------------------------------------------------
Starting Close    : ${metrics["start_price"]}
Ending Close      : ${metrics["end_price"]}
Total Return      : {metrics["total_return_pct"]:+.2f}%
Period High       : ${metrics["highest_price"]} (on {metrics["highest_date"]})
Period Low        : ${metrics["lowest_price"]} (on {metrics["lowest_date"]})

--------------------------------------------------------------------
2. TREND & MOVING AVERAGES
--------------------------------------------------------------------
Latest 20-Day SMA : {f"${metrics['latest_sma20']}" if metrics["latest_sma20"] is not None else "N/A"}
Latest 50-Day SMA : {f"${metrics['latest_sma50']}" if metrics["latest_sma50"] is not None else "N/A"}
Trend Signal      : {metrics["trend_signal"]}

--------------------------------------------------------------------
3. RETURN & RISK ANALYSIS
--------------------------------------------------------------------
Avg Daily Return  : {metrics["avg_daily_return_pct"]:+.4f}%
Best Single Day   : {metrics["best_day_pct"]:+.2f}%
Worst Single Day  : {metrics["worst_day_pct"]:+.2f}%
Daily Volatility  : {metrics["daily_volatility_pct"]:.2f}%
Annualized Vol    : {metrics["annualized_volatility_pct"]:.2f}%
Max Drawdown      : {metrics["max_drawdown_pct"]:.2f}%
Risk Assessment   : {metrics["risk_level"]}

--------------------------------------------------------------------
4. GENERATED VISUALIZATIONS
--------------------------------------------------------------------
{chr(10).join(f"- {path}" for path in chart_paths)}

--------------------------------------------------------------------
DISCLAIMER: This report is generated for educational and analytical
purposes only and does NOT constitute financial or investment advice.
====================================================================
""".strip()

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(report_content)

    return filepath