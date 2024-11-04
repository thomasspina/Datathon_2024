
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def display_cash_flow(financials: pd.DataFrame):
    
    # Define the key metrics to extract from each statement
    income_metrics = ["Total Revenue", "Net Income", "Diluted EPS"]
    cash_flow_metrics = ["Free Cash Flow", "Operating Cash Flow", "Capital Expenditure"]

    # Extract the relevant metrics from each financial statement DataFrame
    income_df = financials["income_statement"].loc[income_metrics]
    balance_df = financials["balance_sheet"]
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
        yaxis_title='YTD Return',
        barmode='group',
        legend_title='Metrics',
        template='plotly_dark'
    )

    # Render the plot in Streamlit
    st.plotly_chart(fig)
