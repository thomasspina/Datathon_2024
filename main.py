import streamlit as st
from src.visualization import company


class MainPage():

    def __init__(self):
        st.set_page_config(page_title="Stock Analysis Tool", layout="wide")
        st.sidebar.title("History")

        self.init_state()

        for symbol, company in st.session_state.history:
            if st.sidebar.button(company):
                self.navigate(symbol)
                
    
    def init_state(self):
        """Initialize session state variables"""
        st.session_state.history = [("AMZN", "Amazon"), ("NA.TO", "Banque Nationale")]

        # go to where user left off
        if st.session_state.get("selected"):
            self.navigate(st.session_state.selected)


    
    def navigate(self, symbol):
        st.session_state.selected = symbol
        company.CompanyPage(symbol)


if __name__ == "__main__":
    MainPage()
