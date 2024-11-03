import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from typing import Dict


class Dashboard:
    def create_technical_chart(self, df: pd.DataFrame) -> go.Figure:
        fig = make_subplots(
            rows=1,
            cols=1,
            shared_xaxes=True,
            row_heights=[1.2],
        )

        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Price",
            ),
            row=1,
            col=1,
        )

        return fig


    def display_metrics(self, metrics: Dict, signals: Dict[str, tuple]):
        # Define the stock symbol and period
        stock_symbol = "NA.TO"
        period = "1d"  # 1-day view similar to the chart in your image

        # Fetch the stock data
        data = yf.download(stock_symbol, period=period, interval="1m")  # 1-minute intervals for intraday data

        # Display the stock information
        st.title(f"{stock_symbol} Stock Price")
        st.write(f"As of {data.index[-1].strftime('%B %d at %I:%M %p EDT')}")
        current_price = data['Close'][-1]
        previous_close = data['Close'][0]
        price_change = current_price - previous_close
        percentage_change = (price_change / previous_close) * 100

        st.metric(label="Price", value=f"${current_price:.2f}", delta=f"{price_change:.2f} ({percentage_change:.2f}%)")

        # Create the line chart
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name=stock_symbol,
                line=dict(color='red', width=2)
            )
        )

        # Update layout to match a similar style as the reference image
        fig.update_layout(
            title=f"{stock_symbol} - Intraday Price",
            xaxis_title="Time",
            yaxis_title="Price (CAD)",
            template="plotly_white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="LightGray"),
            height=400,
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)


    def display_company_info(self, stock_info: Dict):
        """Display company information."""
        with st.expander("Company Information"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Sector:** {stock_info.get('sector', 'N/A')}")
                st.write(f"**Industry:** {stock_info.get('industry', 'N/A')}")
                st.write(f"**Market Cap:** ${stock_info.get('marketCap', 0)/1e9:.2f}B")

            with col2:
                st.write(
                    f"**52 Week High:** ${stock_info.get('fiftyTwoWeekHigh', 'N/A')}"
                )
                st.write(
                    f"**52 Week Low:** ${stock_info.get('fiftyTwoWeekLow', 'N/A')}"
                )
                st.write(f"**P/E Ratio:** {stock_info.get('trailingPE', 'N/A')}")


    def display_raw_data(self, df: pd.DataFrame, symbol: str):
        """Display raw data with download option."""
        with st.expander("Raw Data"):
            st.dataframe(df)

            st.download_button(
                label="Download Data as CSV",
                data=df.to_csv().encode("utf-8"),
                file_name=f"{symbol}_stock_data.csv",
                mime="text/csv",
            )
