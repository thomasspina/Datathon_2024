import streamlit as st
from src.visualization.chat import ChatBox
from src.visualization.stock_analysis import StockAnalysis
from src.visualization.reports import ReportGrid
import src.data.edgar as edgar
from src.models import bedrock_agent as ba
import threading


class CompanyPage():
    def __init__(self, symbol):

        # get recent SEC filings
        thread = threading.Thread(
            target=edgar.download_recent_sec_directory_to_s3,
            args=(symbol)
        )
        thread.start()

        tab1, tab2, tab3 = st.tabs(["Stock Analysis", "Chat", "Generated Reports"])

        with tab1:
            StockAnalysis(symbol)
        with tab2:
            ChatBox(symbol)
        with tab3:
            ReportGrid(symbol)
            

