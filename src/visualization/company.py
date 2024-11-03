import streamlit as st
from src.visualization.chat import ChatBox


class CompanyComponent():
    def __init__(self):
        data, chat = st.columns([2, 4])
        with data:
            self.add_dashboard_information()
            self.add_dashboard_metrics()

        with chat:
            self.add_company_resume()
            self.add_chat_box()


    def add_dashboard_metrics(self):
        pass


    def add_dashboard_information(self):
        pass


    def add_company_resume(self):
        pass

    def add_chat_box(self):
        ChatBox()
