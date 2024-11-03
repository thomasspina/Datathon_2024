import streamlit as st
from src.data.stock_data import StockDataAPI
from src.models.bedrock_agent import BedrockAgent
import uuid

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
            if StockDataAPI.symbolHasChanged:
                StockDataAPI.fetch_yahoo_api(st.session_state.symbol)
                StockDataAPI.calculate_key_stats()
                StockDataAPI.parse_news()

                # Making a new session id for the agent
                BedrockAgent.set_session_id(str(uuid.uuid4()))

                # Feeding the model with the latest news
                BedrockAgent.ask_claude(f"Here are the latest news titles for the {StockDataAPI.symbol}: {StockDataAPI.news}")

                # Feeding the model with the latest stats
                BedrockAgent.ask_claude(f"Here are the key stats for the {StockDataAPI.symbol}: {StockDataAPI.key_stats}")
                StockDataAPI.symbolHasChanged = False
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
        StockDataAPI.symbolHasChanged = True
        if st.session_state.symbol not in [x for x, _ in st.session_state.history]:
            st.session_state.history.append((st.session_state.symbol, st.session_state.symbol))


    def add_dashboard_metrics(self):
        pass

    def add_dashboard_information(self):
        

        if not StockDataAPI.key_stats:
            st.error("Couldn't fetch data for this symbol")
            return
        
        def format_metric(value, format_type='number'):
            if value is None or value == 'N/A':
                return "N/A"
            try:
                if format_type == 'currency':
                    return "${:,.0f}".format(value)
                elif format_type == 'percent':
                    return "{:.1%}".format(value)
                else:  # number
                    return "{:.2f}".format(value)
            except (ValueError, TypeError):
                return "N/A"
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Valuation")
            metrics = StockDataAPI.key_stats["valuation"]
            st.metric("Market Cap", format_metric(metrics.get('market_cap'), 'currency'))
            st.metric("P/E Ratio", format_metric(metrics.get('pe_ratio')))
            st.metric("Price to Book", format_metric(metrics.get('price_to_book')))

        with col2:
            st.subheader("Financials")
            metrics = StockDataAPI.key_stats["financials"]
            st.metric("Revenue", format_metric(metrics.get('revenue'), 'currency'))
            st.metric("Profit Margin", format_metric(metrics.get('profit_margins'), 'percent'))
            st.metric("Operating Margin", format_metric(metrics.get('operating_margins'), 'percent'))

        with col3:
            st.subheader("Shares")
            metrics = StockDataAPI.key_stats["shares"]
            st.metric("Shares Outstanding", format_metric(metrics.get('shares_outstanding'), 'currency'))
            st.metric("Institutional Holdings", format_metric(metrics.get('held_percent_institutions'), 'percent'))
            st.metric("Insider Holdings", format_metric(metrics.get('held_percent_insiders'), 'percent'))

        with col4:
            st.subheader("Dividends")
            metrics = StockDataAPI.key_stats["dividends"]
            st.metric("Dividend Rate", format_metric(metrics.get('dividend_rate'), 'currency'))
            st.metric("Dividend Yield", format_metric(metrics.get('dividend_yield'), 'percent'))
            st.metric("Payout Ratio", format_metric(metrics.get('payout_ratio'), 'percent'))

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
                    response = BedrockAgent.ask_claude(st.session_state.get(f"prompt_input_{message_number}"))
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