import streamlit as st
import src.models.bedrock_agent as bedrock_agent
from src.data.stock_data import StockDataAPI
from src.analysis.technical import TechnicalAnalysis
from src.data.buit_graphs import Dashboard
from datetime import datetime, timedelta

class MainComponent():
    def __init__(self):
        self.init_state()
        st.set_page_config(page_title="Stock Analysis Tool", layout="wide")

        st.sidebar.title("History")

        # Sidebar buttons for company history
        for symbol, company in st.session_state.history:
            if st.sidebar.button(company, key=f"button_{symbol}"):
                st.session_state.symbol = symbol


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

        st.title("📈 Stock Analysis")

        start_date = st.date_input(
            "Select Start Date", value=datetime.now() - timedelta(days=730)
        )

        # Initialize components
        stock_api = StockDataAPI()
        technical_analysis = TechnicalAnalysis()
        dashboard = Dashboard()

        # Fetch and display data
        if st.session_state.symbol:
            with st.spinner("Fetching stock data..."):
                # Get comprehensive stock data
                stock_data = stock_api.fetch_stock_data_with_indicators(
                    st.session_state.symbol, start_date, datetime.now()
                )

                if stock_data is not None:
                    df = stock_data["data"]
                    stock_info = stock_data["info"]
                    financials = stock_data['financials']

                    dashboard.display_company_info(stock_info)

                    # Calculate metrics
                    metrics = stock_api.calculate_metrics(df)

                    # Calculate technical indicators
                    indicators = technical_analysis.calculate_all_indicators(df)
                    signals = technical_analysis.get_signals(df, indicators)

                    # Display metrics and signals
                    dashboard.display_metrics(metrics, signals)

                    # Display cash flow
                    st.plotly_chart(dashboard.display_cash_flow(financials))

                    # Display technical analysis chart
                    st.plotly_chart(
                        dashboard.create_technical_chart(df, indicators),
                        use_container_width=True,
                    )

                    # Display financial metrics
                    with st.expander("Financial Metrics"):
                        stats = stock_api.get_key_stats(st.session_state.symbol)
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

                    # Display raw data
                    dashboard.display_raw_data(df, st.session_state.symbol)

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