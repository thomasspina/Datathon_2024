import streamlit as st
from src.visualization.chat import ChatBox


class CompanyComponent():
    def __init__(self, history_callback):
        controls, _ = st.columns([2, 4])
        with controls:
            self.add_dashboard_controls(history_callback)


        data, chat = st.columns([2, 4])
        with data:
            self.add_dashboard_information()
            self.add_dashboard_metrics()

        with chat:
            self.add_company_resume()
            self.add_chat_box()



    def add_dashboard_controls(self, history_callback):
        st.text_input(
            "Enter Stock Symbol",
            key="symbol_input",
            value=st.session_state.symbol,
            on_change=history_callback
        ).upper()


    def add_dashboard_metrics(self):
        pass


    def add_dashboard_information(self):
        pass


    def add_company_resume(self):
        pass

    def add_chat_box(self):
        ChatBox()
