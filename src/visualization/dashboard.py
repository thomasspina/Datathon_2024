import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict


class Dashboard:
    """Class to handle all dashboard visualization logic"""

    @staticmethod
    def create_technical_chart(
        df: pd.DataFrame, indicators: Dict[str, pd.Series]
    ) -> go.Figure:
        """Create comprehensive technical analysis chart"""
        fig = make_subplots(
            rows=4,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.4, 0.2, 0.2, 0.2],
            subplot_titles=("Price & Indicators", "Volume", "RSI", "MACD"),
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
        colors = ["orange", "blue", "red"]
        periods = [20, 50, 200]
        for period, color in zip(periods, colors):
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=indicators[f"SMA_{period}"],
                    name=f"{period}-day MA",
                    line=dict(color=color),
                ),
                row=1,
                col=1,
            )

        # Add Bollinger Bands
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=indicators["BB_Upper"],
                name="BB Upper",
                line=dict(color="gray", dash="dash"),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=indicators["BB_Lower"],
                name="BB Lower",
                line=dict(color="gray", dash="dash"),
                fill="tonexty",
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

        # RSI
        fig.add_trace(
            go.Scatter(x=df.index, y=indicators["RSI"], name="RSI"), row=3, col=1
        )

        # Add RSI lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3)

        # MACD
        fig.add_trace(
            go.Scatter(x=df.index, y=indicators["MACD"], name="MACD"), row=4, col=1
        )
        fig.add_trace(
            go.Scatter(x=df.index, y=indicators["Signal_Line"], name="Signal Line"),
            row=4,
            col=1,
        )

        # MACD Histogram
        fig.add_trace(
            go.Bar(x=df.index, y=indicators["MACD_Histogram"], name="MACD Histogram"),
            row=4,
            col=1,
        )

        fig.update_layout(
            height=1000,
            showlegend=True,
            xaxis4_title="Date",
            yaxis_title="Price",
            yaxis2_title="Volume",
            yaxis3_title="RSI",
            yaxis4_title="MACD",
        )

        return fig

    @staticmethod
    def display_metrics(metrics: Dict, signals: Dict[str, tuple]):
        """Display key metrics and signals in the dashboard."""
        # Market Metrics
        st.subheader("Market Metrics")
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

        # Technical Signals
        st.subheader("Technical Signals")
        sig_col1, sig_col2, sig_col3, sig_col4 = st.columns(4)

        with sig_col1:
            signal, color = signals["RSI"]
            st.markdown(
                f"**RSI Signal:** <span style='color:{color}'>{signal}</span>",
                unsafe_allow_html=True,
            )

        with sig_col2:
            signal, color = signals["MACD"]
            st.markdown(
                f"**MACD Signal:** <span style='color:{color}'>{signal}</span>",
                unsafe_allow_html=True,
            )

        with sig_col3:
            signal, color = signals["Trend"]
            st.markdown(
                f"**Trend Signal:** <span style='color:{color}'>{signal}</span>",
                unsafe_allow_html=True,
            )

        with sig_col4:
            signal, color = signals["BB"]
            st.markdown(
                f"**Bollinger Bands:** <span style='color:{color}'>{signal}</span>",
                unsafe_allow_html=True,
            )

    # Your existing methods remain the same...
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
