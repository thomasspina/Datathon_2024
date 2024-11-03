import streamlit as st
import json
import uuid
from datetime import datetime, timedelta
from src.data.stock_data import StockDataAPI
from src.visualization.dashboard import Dashboard
from src.models import bedrock_agent


def init_state():
    """Initialize session state variables"""
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.citations = []
    st.session_state.trace = {}


def main():
    # Page configuration
    st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

    # Initialize session state
    if len(st.session_state.items()) == 0:
        init_state()

    # Create two columns: left for chat, right for dashboard
    chat_col, dashboard_col = st.columns([1, 2])

    # Left Column - Chat Interface
    with chat_col:
        st.title("💬 Stock Assistant")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"], unsafe_allow_html=True)

        # Chat input
        if prompt := st.chat_input("Ask about stocks..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                placeholder.markdown("...")
                response = bedrock_agent.invoke_agent(
                    st.session_state.session_id, prompt
                )
                output_text = response["output_text"]

                # Add citations
                if len(response["citations"]) > 0:
                    citation_num = 1
                    num_citation_chars = 0
                    citation_locs = ""
                    for citation in response["citations"]:
                        end_span = (
                            citation["generatedResponsePart"]["textResponsePart"][
                                "span"
                            ]["end"]
                            + 1
                        )
                        for retrieved_ref in citation["retrievedReferences"]:
                            citation_marker = f"[{citation_num}]"
                            output_text = (
                                output_text[: end_span + num_citation_chars]
                                + citation_marker
                                + output_text[end_span + num_citation_chars :]
                            )
                            citation_locs = (
                                citation_locs
                                + "\n<br>"
                                + citation_marker
                                + " "
                                + retrieved_ref["location"]["s3Location"]["uri"]
                            )
                            citation_num = citation_num + 1
                            num_citation_chars = num_citation_chars + len(
                                citation_marker
                            )
                        output_text = (
                            output_text[: end_span + num_citation_chars]
                            + "\n"
                            + output_text[end_span + num_citation_chars :]
                        )
                        num_citation_chars = num_citation_chars + 1
                    output_text = output_text + "\n" + citation_locs

                placeholder.markdown(output_text, unsafe_allow_html=True)
                st.session_state.messages.append(
                    {"role": "assistant", "content": output_text}
                )
                st.session_state.citations = response["citations"]
                st.session_state.trace = response["trace"]

    # Right Column - Dashboard
    with dashboard_col:
        st.title("📈 Stock Analysis")

        # Dashboard controls in a horizontal layout
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            symbol = st.text_input(
                "Enter Stock Symbol (e.g., AAPL)", value="AAPL"
            ).upper()
        with col2:
            start_date = st.date_input(
                "Select Start Date", value=datetime.now() - timedelta(days=365)
            )
        with col3:
            interval = st.selectbox("Interval", options=["1d", "1wk", "1mo"], index=0)

        # Initialize API and Dashboard
        stock_api = StockDataAPI()
        dashboard = Dashboard()

        # Fetch and display data
        if symbol:
            with st.spinner("Fetching stock data..."):
                df, stock_info = stock_api.fetch_stock_data(
                    symbol, start_date, datetime.now()
                )

                if df is not None and not df.empty:
                    # Calculate and display metrics
                    metrics = stock_api.calculate_metrics(df)
                    dashboard.display_metrics(metrics)

                    # Display stock chart
                    st.plotly_chart(
                        dashboard.create_stock_chart(df), use_container_width=True
                    )

                    # Company info and raw data in expanders
                    if stock_info:
                        dashboard.display_company_info(stock_info)
                    dashboard.display_raw_data(df, symbol)

            with chat_col:
                # Send prompt to assistant with stock information
                prompt = f"Provide consise information about the company {symbol}."
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    placeholder.markdown("...")
                    response = bedrock_agent.ask_claude(
                        prompt
                    )
                    placeholder.markdown(response, unsafe_allow_html=True)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )


if __name__ == "__main__":
    main()
