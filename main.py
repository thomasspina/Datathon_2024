import streamlit as st
from src.visualization import company


class MainComponent():
    def __init__(self):
        self.init_state()
        st.set_page_config(page_title="Stock Analysis Tool", layout="wide")

        st.sidebar.title("History")
        for symbol, company in st.session_state.history:
            if st.sidebar.button(company):
                self.navigate(symbol)
                
    
    def init_state(self):
        if "symbol" not in st.session_state:
            st.session_state.symbol = "NA.TO"
        if "history" not in st.session_state:
            st.session_state.history = [("AMZN", "Amazon"), ("NA.TO", "Banque Nationale")]

    
    def navigate(self, symbol):
        st.session_state.selected = symbol
        company.CompanyComponent(symbol, self.update_history)

    def update_history(self):
        st.session_state.symbol = st.session_state.symbol_input
        print(st.session_state.symbol)
        if st.session_state.symbol not in [x for x, _ in st.session_state.history]:
            st.session_state.history.append((st.session_state.symbol, st.session_state.symbol))



if __name__ == "__main__":
    MainComponent()
