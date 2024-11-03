import streamlit as st
from src.visualization.chat import ChatBox
from src.visualization.stock_analysis import StockAnalysis


class CompanyPage():
    def __init__(self, symbol):

        tab1, tab2 = st.tabs(["Stock Analysis", "Chat"])

        with tab1:
            StockAnalysis(symbol)
        with tab2:
            ChatBox(symbol)

    def navigate_to_chat(self):
        print("navtochat")
        return None
    
    def navigate_to_stock(self):
        return None
