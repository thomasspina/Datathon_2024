import streamlit as st
from src.visualization import company


class MainComponent():
    def __init__(self):
        self.init_state()
        st.set_page_config(page_title="Stock Analysis Tool", layout="wide")

        st.sidebar.title("History")
        controls, _ = st.columns([2, 4])
        with controls:
            self.add_dashboard_controls()
            
        for symbol, company in st.session_state.history:
            if st.sidebar.button(company) or st.session_state.symbol == symbol:
                self.navigate(symbol)

                
    
    def init_state(self):
        if "symbol" not in st.session_state:
            st.session_state.symbol = "NA.TO"
        if "history" not in st.session_state:
            st.session_state.history = [("AMZN", "Amazon"), ("NA.TO", "Banque Nationale")]

    
    def navigate(self, symbol):
        st.session_state.symbol = symbol
        company.CompanyComponent()


    def add_dashboard_controls(self):
        st.text_input(
            "Enter Stock Symbol",
            key="symbol_input",
            value=st.session_state.symbol,
            on_change=self.update_history,
        ).upper()

    def update_history(self):
        st.session_state.symbol = st.session_state.symbol_input
        if st.session_state.symbol not in [x for x, _ in st.session_state.history]:
            st.session_state.history.append((st.session_state.symbol, st.session_state.symbol))


if __name__ == "__main__":
    MainComponent()
