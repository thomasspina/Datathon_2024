import streamlit as st
from src.visualization import company


class MainPage():
    def __init__(self):
        self.init_state()
        st.set_page_config(page_title="Stock Analysis Tool", layout="wide")

        st.sidebar.title("History")

        for symbol, company in st.session_state.history:
            if st.sidebar.button(company):
                self.navigate(symbol)
                
    
    def init_state(self):
        """Initialize session state variables"""
        st.session_state.selected = "NA.TO"
        st.session_state.history = [("AMZN", "Amazon"), ("NA.TO", "Banque Nationale")]

    
    def navigate(self, symbol):
        st.session_state.selected = symbol
        company.CompanyPage(symbol)

if __name__ == "__main__":
    MainPage()
