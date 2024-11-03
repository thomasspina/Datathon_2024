import streamlit as st
import json
import uuid
from datetime import datetime, timedelta
from src.data.stock_data import StockDataAPI
from src.visualization.dashboard import Dashboard
from src.models import bedrock_agent
from src.analysis.technical import TechnicalAnalysis


def init_state():
    """Initialize session state variables"""
    st.session_state.selected = "BNC"
    st.session_state.history = [("AMZN", "Amazon"), ("BNC", "Banque Nationale")]


def main():
    init_state()
    st.set_page_config(page_title="Stock Analysis Tool", layout="wide")

    # Define a function to set the navigation state
    def navigate(symbol):
        st.session_state.selected = symbol

    st.sidebar.title("History")

    for symbol, company in st.session_state.history:
        if st.sidebar.button(company):
            navigate(symbol)

        if st.session_state.selected == symbol:
            st.title(f"Analysis of {company}")
            st.write("Welcome to the home page!")


if __name__ == "__main__":
    main()
