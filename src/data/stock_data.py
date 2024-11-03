import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from yahoo_fin import stock_info as si


class StockDataAPI:
    """Enhanced class to handle all stock data API calls and indicators"""

    @staticmethod
    def fetch_stock_data_with_indicators(
        symbol: str, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """
        Fetch comprehensive stock data and indicators from Yahoo Finance.
        Updated to use non-deprecated methods.
        """
        try:
            # Create Ticker object
            stock = yf.Ticker(symbol)

            # Get historical data with maximum available indicators
            df = stock.history(
                start=start_date, end=end_date, interval="1d", actions=True
            )

            # Add basic moving averages
            df["SMA_20"] = df["Close"].rolling(window=20).mean()
            df["SMA_50"] = df["Close"].rolling(window=50).mean()
            df["SMA_200"] = df["Close"].rolling(window=200).mean()
            df["Volume_SMA_20"] = df["Volume"].rolling(window=20).mean()

            # Get income statement data instead of deprecated earnings
            try:
                income_stmt = stock.income_stmt
                net_income = (
                    income_stmt.loc["Net Income"].to_dict()
                    if not income_stmt.empty
                    else {}
                )
            except:
                net_income = {}

            # Get all available additional data
            additional_data = {
                "data": df,
                "info": stock.info,
                "financials": {
                    "income_statement": stock.income_stmt,
                    "balance_sheet": stock.balance_sheet,
                    "cash_flow": stock.cash_flow,
                    "quarterly_income_statement": stock.quarterly_income_stmt,
                    "quarterly_balance_sheet": stock.quarterly_balance_sheet,
                    "quarterly_cash_flow": stock.quarterly_cash_flow,
                    "net_income": net_income,
                },
            }

            # Add optional data if available
            try:
                additional_data["recommendations"] = stock.recommendations
            except:
                additional_data["recommendations"] = None

            try:
                additional_data["institutional_holders"] = stock.institutional_holders
            except:
                additional_data["institutional_holders"] = None

            try:
                additional_data["major_holders"] = stock.major_holders
            except:
                additional_data["major_holders"] = None

            return additional_data

        except Exception as e:
            print(f"Error fetching comprehensive stock data: {e}")
            return None

    @staticmethod
    def get_key_stats(symbol: str) -> Dict:
        """Get key statistics from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            # Get the most recent income statement data
            income_stmt = stock.income_stmt
            latest_quarter = income_stmt.columns[0] if not income_stmt.empty else None

            return {
                "valuation": {
                    "market_cap": info.get("marketCap"),
                    "enterprise_value": info.get("enterpriseValue"),
                    "pe_ratio": info.get("trailingPE"),
                    "forward_pe": info.get("forwardPE"),
                    "price_to_book": info.get("priceToBook"),
                },
                "financials": {
                    "revenue": info.get("totalRevenue"),
                    "gross_margins": info.get("grossMargins"),
                    "operating_margins": info.get("operatingMargins"),
                    "profit_margins": info.get("profitMargins"),
                    "net_income": (
                        income_stmt.loc["Net Income", latest_quarter]
                        if latest_quarter
                        else None
                    ),
                },
                "shares": {
                    "shares_outstanding": info.get("sharesOutstanding"),
                    "float_shares": info.get("floatShares"),
                    "held_percent_institutions": info.get("heldPercentInstitutions"),
                    "held_percent_insiders": info.get("heldPercentInsiders"),
                },
                "dividends": {
                    "dividend_rate": info.get("dividendRate"),
                    "dividend_yield": info.get("dividendYield"),
                    "payout_ratio": info.get("payoutRatio"),
                },
            }
        except Exception as e:
            print(f"Error fetching key stats: {e}")
            return None

    @staticmethod
    def get_analyst_ratings(symbol: str) -> Dict:
        """Get analyst ratings and price targets"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            return {
                "analyst_price_target": {
                    "current": info.get("currentPrice"),
                    "target_mean": info.get("targetMeanPrice"),
                    "target_high": info.get("targetHighPrice"),
                    "target_low": info.get("targetLowPrice"),
                    "number_of_analysts": info.get("numberOfAnalystOpinions"),
                }
            }
        except Exception as e:
            print(f"Error fetching analyst ratings: {e}")
            return None

    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> Dict:
        """Calculate key financial metrics."""
        metrics = {}
        if df is not None and not df.empty:
            latest_close = df["Close"].iloc[-1]
            prev_close = df["Close"].iloc[-2]

            metrics.update(
                {
                    "current_price": latest_close,
                    "daily_change": ((latest_close - prev_close) / prev_close * 100),
                    "current_volume": df["Volume"].iloc[-1],
                    "avg_volume": df["Volume"].mean(),
                    "avg_volume_20d": df["Volume"].rolling(window=20).mean().iloc[-1],
                    "price_52_week_high": df["High"].rolling(window=252).max().iloc[-1],
                    "price_52_week_low": df["Low"].rolling(window=252).min().iloc[-1],
                }
            )

            # Calculate period changes
            periods = {
                "weekly_change": 5,
                "monthly_change": 20,
                "quarterly_change": 63,
                "yearly_change": 252,
            }

            for period_name, period_length in periods.items():
                if len(df) >= period_length:
                    period_close = df["Close"].iloc[-period_length]
                    metrics[period_name] = (
                        (latest_close - period_close) / period_close * 100
                    )
                else:
                    metrics[period_name] = 0

            # Volatility metrics
            metrics["volatility_20d"] = (
                df["Close"].pct_change().rolling(window=20).std().iloc[-1]
                * (252**0.5)
                * 100
            )

        return metrics
    
    def get_moving_averages(ticker: str, period: str = "1mo") -> str:
        msft = yf.Ticker(ticker)
        hist = msft.history(period=period)
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['EMA_20'] = hist['Close'].ewm(span=20, adjust=False).mean()
        return hist[['Close', 'SMA_20', 'EMA_20']].to_string()

    def get_rsi(ticker: str, period: str = "1mo", window = 14) -> str:
        msft = yf.Ticker(ticker)
        hist = msft.history(period=period)

        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        hist['RSI'] = rsi
        return hist[['Close', 'RSI']].to_string()
    
    def get_dividends_and_splits(ticker: str) -> str:
        msft = yf.Ticker(ticker)
        dividends = msft.dividends
        splits = msft.splits
        return f"Dividends:\n{dividends}\n\nStock Splits:\n{splits}"
    
    def get_analyst_recommendations(ticker: str) -> str:
        msft = yf.Ticker(ticker)
        recommendations = msft.recommendations
        price_targets = msft.analyst_price_targets
        return f"Analyst Recommendations:\n{recommendations}\n\nAnalyst Price Targets:\n{price_targets}"