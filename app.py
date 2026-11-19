"""
app.py
Interactive Streamlit Web Dashboard for the Stock Market Data Analyzer.
Run with: streamlit run app.py
"""

from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt

from src.data_loader import fetch_stock_data
from src.analyzer import enrich_with_indicators, compute_summary_metrics

st.set_page_config(page_title="Stock Market Data Analyzer", page_icon="📈", layout="wide")

st.title("📈 Stock Market Data Analyzer")
st.caption("Interactive FinTech & Quantitative Equity Analysis Dashboard (Educational Use Only)")

# Sidebar Controls
st.sidebar.header("Analysis Parameters")
ticker = st.sidebar.text_input("Stock Ticker Symbol", value="AAPL").strip().upper()
default_end = datetime.today().date()
default_start = default_end - timedelta(days=365 * 2)

start_date = st.sidebar.date_input("Start Date", value=default_start)
end_date = st.sidebar.date_input("End Date", value=default_end)

if st.sidebar.button("Run Analysis", type="primary") or ticker:
    with st.spinner(f"Analyzing {ticker}..."):
        df, source = fetch_stock_data(ticker, str(start_date), str(end_date))
        enriched_df = enrich_with_indicators(df)
        metrics = compute_summary_metrics(enriched_df, ticker, source)

    st.info(f"**Data Source:** {source} | **Period:** {metrics['start_date']} to {metrics['end_date']} ({metrics['trading_days']} trading days)")

    # Top KPI Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Close", f"${metrics['end_price']}", f"{metrics['total_return_pct']:+.2f}%")
    col2.metric("Period High / Low", f"${metrics['highest_price']}", f"Low: ${metrics['lowest_price']}")
    col3.metric("Annualized Volatility", f"{metrics['annualized_volatility_pct']}%", metrics["risk_level"])
    col4.metric("Max Drawdown", f"{metrics['max_drawdown_pct']}%", f"Avg Daily: {metrics['avg_daily_return_pct']:+.3f}%")

    st.success(f"**Detected Trend Signal:** {metrics['trend_signal']}")

    # Interactive Charts
    tab1, tab2, tab3, tab4 = st.tabs(["Price & Moving Averages", "Daily Returns", "Drawdown Risk", "Processed Data"])

    with tab1:
        st.subheader(f"{ticker} Closing Price & Moving Averages")
        st.line_chart(enriched_df[["Close", "SMA_20", "SMA_50"]])

    with tab2:
        st.subheader(f"{ticker} Daily Returns (%)")
        st.bar_chart(enriched_df["Daily_Return"] * 100)

    with tab3:
        st.subheader(f"{ticker} Historical Drawdown (%)")
        st.area_chart(enriched_df["Drawdown"] * 100)

    with tab4:
        st.subheader("Enriched Dataset (Latest 50 Rows)")
        st.dataframe(enriched_df.tail(50), use_container_width=True)
        csv_bytes = enriched_df.to_csv().encode("utf-8")
        st.download_button("Download Enriched CSV", data=csv_bytes, file_name=f"{ticker}_analyzed.csv", mime="text/csv")