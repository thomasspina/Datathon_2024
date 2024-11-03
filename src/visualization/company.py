import streamlit as st
from datetime import datetime, timedelta
from src.data.stock_data import StockDataAPI
from src.visualization.dashboard import Dashboard
from src.analysis.technical import TechnicalAnalysis


class CompanyComponent():
    def __init__(self, symbol, history_callback):

        st.title("📈 Stock Analysis")

        # Dashboard controls
        controls, metrics = st.columns([1, 4])
        with controls:
            st.text_input(
                "Enter Stock Symbol (e.g., AAPL)",
                value=symbol,
                key="symbol_input",
                on_change=history_callback
            ).upper()

            start_date = st.date_input(
                "Select Start Date", value=datetime.now() - timedelta(days=365)
            )

            interval = st.selectbox("Interval", options=["1d", "1wk", "1mo"], index=0)
