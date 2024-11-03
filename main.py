import streamlit as st
import json
import uuid
from datetime import datetime, timedelta
from src.data.stock_data import StockDataAPI
from src.visualization.dashboard import Dashboard
from src.models import bedrock_agent
from src.analysis.technical import TechnicalAnalysis


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

        # Chat interface code remains the same...
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"], unsafe_allow_html=True)

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

                # Citations handling remains the same...
                if len(response["citations"]) > 0:
                    # ... citation code remains the same ...
                    pass

                placeholder.markdown(output_text, unsafe_allow_html=True)
                st.session_state.messages.append(
                    {"role": "assistant", "content": output_text}
                )
                st.session_state.citations = response["citations"]
                st.session_state.trace = response["trace"]

    # Right Column - Dashboard
    with dashboard_col:
        st.title("📈 Stock Analysis")

        # Dashboard controls
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            symbol = st.text_input(
                "Enter Stock Symbol (e.g., AAPL)", value="AAPL"
            ).upper()
        with col2:
            unformatted_start_date = st.date_input(
                "Select Start Date", value=datetime.now().date() - timedelta(days=365)
            )
            start_date = unformatted_start_date.strftime("%Y-%m-%d")

        with col3:
            interval = st.selectbox("Interval", options=["1d", "1wk", "1mo"], index=0)

        # Initialize components
        stock_api = StockDataAPI()
        dashboard = Dashboard()
        technical_analysis = TechnicalAnalysis()

        # Fetch and display data
        if symbol:
            with st.spinner("Fetching stock data..."):
                # Get comprehensive stock data
                stock_data = stock_api.fetch_stock_data_with_indicators(
                    symbol, start_date, datetime.now().strftime("%Y-%m-%d")
                )

                if stock_data is not None:
                    df = stock_data["data"]
                    stock_info = stock_data["info"]

                    # Calculate metrics
                    metrics = stock_api.calculate_metrics(df)

                    # Calculate technical indicators
                    indicators = technical_analysis.calculate_all_indicators(df)
                    signals = technical_analysis.get_signals(df, indicators)

                    # Display metrics and signals
                    dashboard.display_metrics(metrics, signals)

                    # Display technical analysis chart
                    st.plotly_chart(
                        dashboard.create_technical_chart(df, indicators),
                        use_container_width=True,
                    )

                    # Display company information
                    dashboard.display_company_info(stock_info)

                    # Display financial metrics
                    with st.expander("Financial Metrics"):
                        stats = stock_api.get_key_stats(symbol)
                        if stats:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("### Valuation Metrics")
                                for key, value in stats["valuation"].items():
                                    st.write(
                                        f"**{key.replace('_', ' ').title()}:** {value}"
                                    )
                            with col2:
                                st.write("### Financial Metrics")
                                for key, value in stats["financials"].items():
                                    st.write(
                                        f"**{key.replace('_', ' ').title()}:** {value}"
                                    )

                    # Display analyst ratings
                    with st.expander("Analyst Ratings"):
                        ratings = stock_api.get_analyst_ratings(symbol)
                        if ratings and ratings.get("analyst_price_target"):
                            pt = ratings["analyst_price_target"]
                            st.write(f"**Current Price:** ${pt.get('current', 'N/A')}")
                            st.write(
                                f"**Mean Target:** ${pt.get('target_mean', 'N/A')}"
                            )
                            st.write(
                                f"**High Target:** ${pt.get('target_high', 'N/A')}"
                            )
                            st.write(f"**Low Target:** ${pt.get('target_low', 'N/A')}")
                            st.write(
                                f"**Number of Analysts:** {pt.get('number_of_analysts', 'N/A')}"
                            )

                    # Display raw data
                    dashboard.display_raw_data(df, symbol)

                    # Technical Analysis Details
                    with st.expander("Technical Analysis Details"):
                        st.write("### Current Indicator Values")
                        detail_col1, detail_col2 = st.columns(2)

                        with detail_col1:
                            st.write(f"**RSI (14):** {indicators['RSI'].iloc[-1]:.2f}")
                            st.write(f"**MACD:** {indicators['MACD'].iloc[-1]:.2f}")
                            st.write(
                                f"**Signal Line:** {indicators['Signal_Line'].iloc[-1]:.2f}"
                            )

                        with detail_col2:
                            st.write(
                                f"**20-day SMA:** ${indicators['SMA_20'].iloc[-1]:.2f}"
                            )
                            st.write(
                                f"**50-day SMA:** ${indicators['SMA_50'].iloc[-1]:.2f}"
                            )
                            st.write(
                                f"**200-day SMA:** ${indicators['SMA_200'].iloc[-1]:.2f}"
                            )
                else:
                    st.error(
                        "Failed to fetch stock data. Please check the symbol and try again."
                    )

    # Sidebar settings
    # with st.sidebar:
    #     if st.button("Reset Session"):
    #         init_state()

    #     st.title("Settings")
    #     with st.expander("Technical Analysis Parameters"):
    #         st.slider("RSI Period", 7, 21, 14)
    #         st.slider("MACD Fast Period", 8, 16, 12)
    #         st.slider("MACD Slow Period", 20, 30, 26)
    #         st.slider("MACD Signal Period", 5, 13, 9)


if __name__ == "__main__":
    main()
