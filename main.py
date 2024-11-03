import streamlit as st
import src.models.bedrock_agent as bedrock_agent

class MainComponent():
    def __init__(self):
        self.init_state()
        st.set_page_config(page_title="Stock Analysis Tool", layout="wide")

        st.sidebar.title("History")

        # Sidebar buttons for company history
        for symbol, company in st.session_state.history:
            if st.sidebar.button(company, key=f"button_{symbol}"):
                st.session_state.symbol = symbol

        controls, _ = st.columns([2, 4])
        with controls:
            self.add_dashboard_controls()

        # Display the main components based on selected symbol
        if "symbol" in st.session_state:
            data, chat, reports = st.tabs(["Financial Analysis", "Chat", "Reports"])
            with data:
                self.add_dashboard_information()
                self.add_dashboard_metrics()

            with chat:
                self.add_company_resume()
                self.add_chat_box()

            with reports:
                pass

    def init_state(self):
        if "symbol" not in st.session_state:
            st.session_state.symbol = "NA.TO"
        if "history" not in st.session_state:
            st.session_state.history = [("AMZN", "Amazon"), ("NA.TO", "Banque Nationale")]
        if "messages" not in st.session_state:
            st.session_state.messages = []



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


    def add_dashboard_metrics(self):
        pass

    def add_dashboard_information(self):
        pass


    def add_company_resume(self):
        pass

    def add_chat_box(self):
        st.title("💬 Stock Assistant")

        # Display existing messages for the current symbol
        for message in st.session_state.messages:
            if message["symbol"] == st.session_state.symbol:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        message_number = [x["symbol"] for x in st.session_state.messages].count(st.session_state.symbol)

        # Check if there is a new input from the chat input box
        if st.session_state.get(f"prompt_input_{message_number}"):
            # Add user message to session state
            st.session_state.messages.append({
                "symbol": st.session_state.symbol, 
                "role": "user",
                "content": st.session_state.get(f"prompt_input_{message_number}"),
            })

            # Display user message in chat
            with st.chat_message("user"):
                st.markdown(st.session_state.get(f"prompt_input_{message_number}"))

            # Process assistant's response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = bedrock_agent.ask_claude(st.session_state.get(f"prompt_input_{message_number}"))
                st.markdown(response)
                st.session_state.messages.append({
                    "symbol": st.session_state.symbol, 
                    "role": "assistant",
                    "content": response,
                })

            # Clear the input field after processing
            st.session_state.prompt_input = ""

        st.chat_input("What is up?", key=f"prompt_input_{message_number}")


if __name__ == "__main__":
    MainComponent()