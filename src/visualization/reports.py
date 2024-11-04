from time import sleep
import uuid
import streamlit as st
from src.models import bedrock_agent as ba
from src.prompts import prompts as pr
from config import settings


class ReportGrid():
    def __init__(self, symbol):
        st.title(f"{symbol} Generated Report")
        
        with st.spinner("Generating report... this may take a few minutes"):

            while not settings.sync_finished:
                sleep(1)
            # generate board of directors report
            session_id = str(uuid.uuid4())
            for i in range(1, 4):
                prompt = f"For this stock {symbol}, do the following: " + pr.get_board_of_directors_prompt(i)
                response = ba.invoke_agent(session_id, prompt)
                st.markdown(response)

            # generate top shareholders report
            session_id = str(uuid.uuid4())
            for i in range(1, 2):
                prompt = f"For this stock {symbol}, do the following: " + pr.get_top_shareholders_prompt(i)
                response = ba.invoke_agent(session_id, prompt)
                st.markdown(response)

            # generate financials report
            session_id = str(uuid.uuid4())
            for i in range(1, 2):
                prompt = f"For this stock {symbol}, do the following: " + pr.get_financials_prompt(i)
                response = ba.invoke_agent(session_id, prompt)
                st.markdown(response)


        # Create a grid to display the reports