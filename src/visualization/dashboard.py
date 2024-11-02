import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict


class Dashboard:
    """Class to handle all dashboard visualization logic"""

    @staticmethod
    def create_stock_chart(df: pd.DataFrame) -> go.Figure:
        """Create stock price chart with volume."""
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3],
        )

        # Candlestick chart
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

        # Add Moving Averages
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"].rolling(window=20).mean(),
                name="20-day MA",
                line=dict(color="orange"),
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"].rolling(window=50).mean(),
                name="50-day MA",
                line=dict(color="blue"),
            ),
            row=1,
            col=1,
        )

        # Volume chart
        colors = [
            "red" if row["Open"] - row["Close"] >= 0 else "green"
            for index, row in df.iterrows()
        ]

        fig.add_trace(
            go.Bar(x=df.index, y=df["Volume"], name="Volume", marker_color=colors),
            row=2,
            col=1,
        )

        fig.update_layout(
            title="Stock Price and Volume Analysis",
            yaxis_title="Price",
            yaxis2_title="Volume",
            xaxis2_title="Date",
            height=800,
        )

        return fig

    @staticmethod
    def display_metrics(metrics: Dict):
        """Display key metrics in the dashboard."""
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Current Price",
                f"${metrics['current_price']:.2f}",
                f"{metrics['daily_change']:.2f}%",
            )

        with col2:
            st.metric(
                "Trading Volume",
                f"{metrics['current_volume']:,.0f}",
                f"Avg: {metrics['avg_volume']:,.0f}",
            )

        with col3:
            st.metric("Weekly Change", f"{metrics['weekly_change']:.2f}%")

        with col4:
            st.metric("Monthly Change", f"{metrics['monthly_change']:.2f}%")

    @staticmethod
    def display_company_info(stock_info: Dict):
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

    @staticmethod
    def display_raw_data(df: pd.DataFrame, symbol: str):
        """Display raw data with download option."""
        with st.expander("Raw Data"):
            st.dataframe(df)

            st.download_button(
                label="Download Data as CSV",
                data=df.to_csv().encode("utf-8"),
                file_name=f"{symbol}_stock_data.csv",
                mime="text/csv",
            )
