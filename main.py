import streamlit as st
from src.data.stock_data import StockDataAPI
from src.models.bedrock_agent import BedrockAgent
import uuid

from src.data.buit_graphs import display_cash_flow, display_compare

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
                if st.session_state.symbol not in [x for x, _ in st.session_state.history]:
                    if StockDataAPI.stock.info.get("longName") is None:
                        st.error("Couldn't fetch data for this symbol")
                        return
                    
                    name = StockDataAPI.stock.info["longName"]
                    st.session_state.history.append((st.session_state.symbol, name))
                    st.sidebar.button(
                        name,
                        key=f"button_{st.session_state.symbol}"
                    )

                StockDataAPI.calculate_key_stats()
                StockDataAPI.parse_news()
                st.session_state.messages = []
                # Making a new session id for the agent
                BedrockAgent.set_session_id(str(uuid.uuid4()))

                BedrockAgent.send_news(StockDataAPI.symbol, StockDataAPI.news)

                BedrockAgent.send_stats(StockDataAPI.symbol, StockDataAPI.key_stats)
                
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
            st.session_state.history = [("AMZN", "Amazon.com, Inc."), ("NA.TO", "National Bank of Canada")]
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


    def add_dashboard_metrics(self):
        financials = StockDataAPI.get_financials()
        display_cash_flow(financials)
        industry = StockDataAPI.get_industry_info()
        display_compare(industry)
    

    def add_dashboard_information(self):
        st.title("📈 Stock Analysis")

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

        # Get messages for current symbol
        # symbol_messages = [
        #     msg for msg in st.session_state.messages 
        #     if msg["symbol"] == st.session_state.symbol
        # ]
        
        # Display existing messages
        for message in st.session_state.messages :
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        message_number = len(st.session_state.messages)

        # Handle new messages
        if prompt := st.chat_input("What is up?", key=f"prompt_input_{message_number}"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Add to session state
            
            # Get chat history for context
            # chat_history = [
            #     {"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}]}
            #     for msg in symbol_messages
            # ]

            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = BedrockAgent.talk_to_model(st.session_state.messages)
                st.markdown(response)

                
                
                # Add to session state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })


if __name__ == "__main__":
    MainComponent()