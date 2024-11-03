# app/main.py
import streamlit as st
import uuid
from config import Config
from core.market import MarketService
from core.llm import BedrockAgent


class MainApp:
    def __init__(self):
        st.set_page_config(page_title="Stock Analysis", page_icon="📈", layout="wide")
        self.init_session_state()
        self.market_service = MarketService()
        self.bedrock_agent = BedrockAgent()
        print("init state")

    def init_session_state(self):
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        if "symbol" not in st.session_state:
            st.session_state.symbol = None
        if "market_data" not in st.session_state:
            st.session_state.market_data = None
        if "news_data" not in st.session_state:
            st.session_state.news_data = None
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def reset_session_state(self):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.symbol = None
        st.session_state.market_data = None
        st.session_state.news_data = None
        st.session_state.messages = []

    def render_search(self):
        st.title("Stock Analysis Tool")

        col1, col2 = st.columns([3, 1])
        with col1:
            symbol = st.text_input(
                "Enter stock symbol (e.g., AAPL)", key="symbol_input"
            )
        with col2:
            analyze_clicked = st.button(
                "Analyze", type="primary", use_container_width=True
            )
        if symbol and analyze_clicked:
            symbol = symbol.upper()
            if self.market_service.is_valid_symbol(symbol):
                self.reset_session_state()
                st.session_state.symbol = symbol
                self.market_service.fetch_ticker(symbol)
            else:
                st.error("Invalid symbol. Please try again.")

    def render_dashboard(self):
        with st.spinner("Fetching data..."):
            try:
                market_data = self.market_service.get_market_data()
                st.session_state.market_data = market_data

                news_data = self.market_service.get_news_data()
                st.session_state.news_data = news_data

                # if not st.session_state.analysis:
                #     st.session_state.analysis = get_analysis(
                #         st.session_state.market_data
                #     )

                chat_col, dashboard_col = st.columns([1, 2])

                with dashboard_col:
                    st.title("📈 Stock Analysis")

                    # Display data
                    st.header(f"{market_data.company_name} ({market_data.symbol})")
                    st.caption(f"{market_data.sector} | {market_data.industry}")

                    # Key metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Current Price", f"${market_data.current_price:.2f}")
                    with col2:
                        st.metric(
                            "Market Cap",
                            f"${market_data.market_cap/1e9:.1f}B",  # Convert to billions
                        )
                    with col3:
                        if market_data.pe_ratio:
                            st.metric("P/E Ratio", f"{market_data.pe_ratio:.2f}")
                    # Key Metrics - Second Row
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            "52W Range",
                            f"${market_data.fifty_two_week_low:.2f} - ${market_data.fifty_two_week_high:.2f}",
                        )
                    with col2:
                        st.metric(
                            "Target Price", f"${market_data.target_mean_price:.2f}"
                        )
                    with col3:
                        st.metric("Recommendation", market_data.recommendation.upper())

                    # Add a divider before AI Analysis
                    st.divider()

                    # AI Analysis Section
                    # st.subheader("AI Analysis")
                    # st.write(st.session_state.analysis)
                with chat_col:
                    # self.bedrock_agent.initialize_session()
                    st.title("💬 Stock Assistant")
                    # Chat interface code remains the same...
                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"], unsafe_allow_html=True)

                    if prompt := st.chat_input("Ask about stocks..."):
                        st.session_state.messages.append(
                            {"role": "user", "content": prompt}
                        )
                        with st.chat_message("user"):
                            st.write(prompt)
                        print("\n", st.session_state.market_data, "\n")

                        with st.chat_message("assistant"):
                            placeholder = st.empty()
                            placeholder.markdown("...")
                            response = self.bedrock_agent.invoke_agent(
                                st.session_state.session_id, prompt
                            )
                            output_text = response["output_text"]
                            print("\n", st.session_state.market_data, "\n")

                            # Citations handling remains the same...
                            # if len(response["citations"]) > 0:
                            # ... citation code remains the same ...
                            # pass

                            placeholder.markdown(output_text, unsafe_allow_html=True)
                            st.session_state.messages.append(
                                {"role": "assistant", "content": output_text}
                            )
                            # st.session_state.citations = response["citations"]
                            # st.session_state.trace = response["trace"]
                            print("\n", st.session_state.market_data, "\n")

            except Exception as e:
                st.error(f"Error analyzing stock: {str(e)}")

    def render(self):
        # Always show search at top
        self.render_search()

        # Show separator if we have a symbol
        if st.session_state.symbol:
            st.divider()
            self.render_dashboard()


if __name__ == "__main__":
    app = MainApp()
    print("app created")
    app.render()
