import streamlit as st
import src.models.bedrock_agent as bedrock_agent

class ChatBox():
    def __init__(self):
        st.title("💬 Stock Assistant")
        self.init_state()

        if "prompt_input" not in st.session_state:
            st.chat_input(
                "What is up?",
                key="prompt_input",
            )

        if st.session_state.prompt_input:
            st.session_state.messages.append({
                "symbol": st.session_state.symbol, 
                "role": "user",
                "content": st.session_state.prompt_input,
            })

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(st.session_state.prompt_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = bedrock_agent.ask_claude(st.session_state.prompt_input)
                st.markdown(response)
                st.session_state.messages.append({
                    "symbol": st.session_state.symbol, 
                    "role": "assistant",
                    "content": response,
                })

    
    def init_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            if message["symbol"] == st.session_state.symbol:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
