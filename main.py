"""
main.py
CLI Entry Point for the Stock Market Data Analyzer.
Usage:
    python main.py --ticker AAPL --start 2023-01-01 --end 2025-01-01
    python main.py  (uses interactive defaults)
"""

import argparse
from datetime import datetime, timedelta

from src.data_loader import fetch_stock_data
from src.analyzer import enrich_with_indicators, compute_summary_metrics
from src.visualizer import (
    plot_price_trend,
    plot_moving_averages,
    plot_return_distribution,
)
from src.report_generator import save_processed_csv, generate_text_report


def parse_arguments():
    default_end = datetime.today().strftime("%Y-%m-%d")
    default_start = (datetime.today() - timedelta(days=365 * 2)).strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser(description="Stock Market Data Analyzer CLI")
    parser.add_argument("--ticker", type=str, default="AAPL", help="Stock ticker symbol (e.g., AAPL, MSFT, TSLA, RELIANCE.NS)")
    parser.add_argument("--start", type=str, default=default_start, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=default_end, help="End date (YYYY-MM-DD)")
    parser.add_argument("--csv", type=str, default=None, help="Optional path to local CSV file")
    return parser.parse_args()


def main():
    args = parse_arguments()
    ticker = args.ticker.strip().upper()

    print("\n====================================================")
    print(f"   STOCK MARKET DATA ANALYZER | TICKER: {ticker}")
    print("====================================================")

    # Step 1: Load & Clean Data
    raw_df, data_source = fetch_stock_data(
        ticker=ticker,
        start_date=args.start,
        end_date=args.end,
        csv_fallback_path=args.csv,
    )

    # Step 2: Enrich Indicators & Compute Summary KPIs
    enriched_df = enrich_with_indicators(raw_df)
    metrics = compute_summary_metrics(enriched_df, ticker=ticker, data_source=data_source)

    # Step 3: Generate Visualizations
    chart_1 = plot_price_trend(enriched_df, ticker)
    chart_2 = plot_moving_averages(enriched_df, ticker)
    chart_3 = plot_return_distribution(enriched_df, ticker)
    chart_paths = [chart_1, chart_2, chart_3]

    # Step 4: Save Processed CSV & Executive Report
    csv_output = save_processed_csv(enriched_df, ticker)
    report_output = generate_text_report(metrics, chart_paths)

    # Step 5: Display Terminal Summary
    print(f"\n[SUCCESS] Analysis Complete for {ticker} ({data_source})")
    print(f"  Period          : {metrics['start_date']} -> {metrics['end_date']} ({metrics['trading_days']} days)")
    print(f"  Price Movement  : ${metrics['start_price']} -> ${metrics['end_price']} ({metrics['total_return_pct']:+.2f}%)")
    print(f"  High / Low      : ${metrics['highest_price']} / ${metrics['lowest_price']}")
    print(f"  Trend Signal    : {metrics['trend_signal']}")
    print(f"  Annualized Vol  : {metrics['annualized_volatility_pct']:.2f}% ({metrics['risk_level']})")
    print(f"  Max Drawdown    : {metrics['max_drawdown_pct']:.2f}%")
    print("\n[OUTPUT FILES]")
    print(f"  Processed Data  : {csv_output}")
    print(f"  Summary Report  : {report_output}")
    for c in chart_paths:
        print(f"  Chart Saved     : {c}")
    print("====================================================\n")


if __name__ == "__main__":
    main()