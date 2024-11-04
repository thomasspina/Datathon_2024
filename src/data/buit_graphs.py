
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
            rows=1,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.4],
            subplot_titles=("Price & Indicators"),
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
        colors = ["orange", "blue"]
        periods = [20, 50]
        for period, color in zip(periods, colors):
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=indicators.get(f"SMA_{period}", pd.Series([None]*len(df))),
                    name=f"{period}-day MA",
                    line=dict(color=color),
                ),
                row=1,
                col=1,
            )

        fig.update_layout(
            height=1000,
            showlegend=True,
            yaxis_title="Price",
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
        st.subheader("Company Information")
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


    @staticmethod
    def display_cash_flow(df: pd.DataFrame):
        st.subheader("Cash Flow Chart")
        cash_flow = {
            'Free Cash Flow': df['cash_flow'].loc['Free Cash Flow'],
            'Operating Cash Flow': df['cash_flow'].loc['Operating Cash Flow'],
            'Net Income From Continuing Operations': df['cash_flow'].loc['Net Income From Continuing Operations'],
            'Capital Expenditure': df['cash_flow'].loc['Capital Expenditure'],
        }

        income_statement = {
            'total_revenue' : df['income_statement'].loc['Total Revenue']
        }

        # Create a new DataFrame for easier plotting
        cash_flow_df = pd.DataFrame(cash_flow)
        income_statement_df = pd.DataFrame(income_statement)

        # Plotting
        fig = go.Figure()

        # Add traces for each selected metric
        for metric, data in cash_flow_df.items():
            fig.add_trace(go.Scatter(x=cash_flow_df.index, y=data, mode='lines+markers', name=metric))

        # Update layout
        fig.update_layout(
            xaxis_title='Time Period',
            yaxis_title='Value',
            legend_title='Metrics',
            template='plotly_white',
            height=600
        )

        return fig
