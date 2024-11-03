import streamlit as st
import src.models.bedrock_agent as bedrock_agent

class ChatBox():
    def __init__(self, symbol):

        st.title("💬 Stock Assistant")
        st.session_state.messages = []



        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        prompt = st.chat_input("What is up?")
        if prompt :
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    print(prompt)
                    response = bedrock_agent.ask_claude(prompt)
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
