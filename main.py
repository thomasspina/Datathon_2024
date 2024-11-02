import streamlit as st
from datetime import datetime, timedelta
from src.data.stock_data import StockDataAPI
from src.visualization.dashboard import Dashboard


def main():
    # Page configuration
    st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

    # Title and description
    st.title("📈 Stock Analysis Dashboard")
    st.markdown(
        """
    This dashboard provides real-time stock data analysis and visualization.
    Enter a stock symbol and select a date range to begin.
    """
    )

    # Sidebar inputs
    st.sidebar.header("Dashboard Controls")

    # Stock symbol input
    symbol = st.sidebar.text_input(
        "Enter Stock Symbol (e.g., AAPL)", value="AAPL"
    ).upper()

    # Date range selection
    end_date = datetime.now()
    start_date = st.sidebar.date_input(
        "Select Start Date", value=end_date - timedelta(days=365)
    )

    # Interval selection
    st.sidebar.selectbox("Select Time Interval", options=["1d", "1wk", "1mo"], index=0)

    # Initialize API and Dashboard
    stock_api = StockDataAPI()
    dashboard = Dashboard()

    # Fetch data button
    if st.sidebar.button("Fetch Data"):
        with st.spinner("Fetching stock data..."):
            df, stock_info = stock_api.fetch_stock_data(symbol, start_date, end_date)

            if df is not None and not df.empty:
                # Calculate metrics
                metrics = stock_api.calculate_metrics(df)

                # Display metrics
                dashboard.display_metrics(metrics)

                # Display stock chart
                st.plotly_chart(
                    dashboard.create_stock_chart(df), use_container_width=True
                )

                # Display company information
                if stock_info:
                    dashboard.display_company_info(stock_info)

                # Display raw data
                dashboard.display_raw_data(df, symbol)
            else:
                st.error(
                    "Failed to fetch stock data. Please check the symbol and try again."
                )


if __name__ == "__main__":
    main()
