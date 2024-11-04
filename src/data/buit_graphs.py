
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

def display_cash_flow(financials: pd.DataFrame):
    
    # Define the key metrics to extract from each statement
    income_metrics = ["Total Revenue", "Net Income", "Diluted EPS"]
    balance_metrics = ["Net Debt"]
    cash_flow_metrics = ["Free Cash Flow", "Operating Cash Flow", "Capital Expenditure"]

    # Extract the relevant metrics from each financial statement DataFrame
    income_df = financials["income_statement"].loc[income_metrics]
    balance_df = financials["balance_sheet"].loc[balance_metrics]
    cash_flow_df = financials["cash_flow"].loc[cash_flow_metrics]

    st.subheader("Income Statement Metrics")
    fig = go.Figure()

    # Convert dates to strings for the x-axis
    date_strings = income_df.columns.astype(str)

    # Add traces for Total Revenue and Net Income
    fig.add_trace(
        go.Bar(
            x=date_strings,
            y=income_df.loc["Total Revenue"],
            name="Total Revenue",
            marker_color='blue'
        )
    )
    fig.add_trace(
        go.Bar(
            x=date_strings,
            y=income_df.loc["Net Income"],
            name="Net Income",
            marker_color='green'
        )
    )

    # Add a line for Diluted EPS on the secondary y-axis
    fig.add_trace(
        go.Scatter(
            x=date_strings,
            y=income_df.loc["Diluted EPS"],
            name="Diluted EPS",
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='red', width=2)
        )
    )

    # Update layout for the dual axes plot
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue and Net Income",
        yaxis=dict(title='Revenue and Net Income', side='left', showgrid=True),
        yaxis2=dict(title='Diluted EPS', side='right', overlaying='y', showgrid=False),
        barmode='group',
        legend_title="Metrics",
        template="plotly_dark"
    )

    # Render the plot in the Streamlit app
    st.plotly_chart(fig)
    st.dataframe(income_df)

    # Display Cash Flow Metrics
    st.subheader("Cash Flow Metrics")

    cash_fig = go.Figure()

    for metric in ["Free Cash Flow", "Operating Cash Flow"]:
        cash_fig.add_trace(
            go.Bar(
                x=date_strings,  # Dates as strings
                y=cash_flow_df.loc[metric],  # Metric data for each date
                name=metric  # Label for the legend
            )
        )

    # Update layout for the cash flow metrics plot
    cash_fig.update_layout(
        title="Cash Flow Metrics Over Years",
        xaxis_title="Date",
        yaxis_title="Value",
        barmode="group",
        legend_title="Metrics",
        template="plotly_dark"
    )
    st.plotly_chart(cash_fig)
    st.dataframe(cash_flow_df)

    # Display Balance Sheet Metrics
    st.subheader("Balance Sheet Metrics")
    st.dataframe(balance_df)
    return 

def display_compare(df):
    df.set_index('name', inplace=True)
    companies = df.index
    ytd_return = df['ytd return']

    # Create the figure
    fig = go.Figure()

    # Add traces for each metric
    fig.add_trace(
        go.Bar(
            x=companies,
            y=ytd_return,
            name='YTD Return',
            marker_color='blue'
        )
    )

    # Update layout
    fig.update_layout(
        title='Comparison of Companies in same industry',
        xaxis_title='Companies',
        yaxis_title='Value',
        barmode='group',
        legend_title='Metrics',
        template='plotly_dark'
    )

    # Render the plot in Streamlit
    st.plotly_chart(fig)
