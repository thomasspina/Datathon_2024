import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Tuple, Optional, Dict


class StockDataAPI:
    """Class to handle all stock data API calls"""

    @staticmethod
    def fetch_stock_data(
        symbol: str, start_date: datetime, end_date: datetime
    ) -> Tuple[Optional[pd.DataFrame], Optional[Dict]]:
        """Fetch stock data from Yahoo Finance."""
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(start=start_date, end=end_date)
            return df, stock.info
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None, None

    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> Dict:
        """Calculate key financial metrics."""
        metrics = {}
        if df is not None and not df.empty:
            # Daily change
            metrics["daily_change"] = (
                (df["Close"][-1] - df["Close"][-2]) / df["Close"][-2] * 100
            )

            # Weekly change
            if len(df) >= 5:
                metrics["weekly_change"] = (
                    (df["Close"][-1] - df["Close"][-5]) / df["Close"][-5] * 100
                )
            else:
                metrics["weekly_change"] = 0

            # Monthly change
            if len(df) >= 20:
                metrics["monthly_change"] = (
                    (df["Close"][-1] - df["Close"][-20]) / df["Close"][-20] * 100
                )
            else:
                metrics["monthly_change"] = 0

            # Average volume
            metrics["avg_volume"] = df["Volume"].mean()

            # Current price
            metrics["current_price"] = df["Close"][-1]

            # Current volume
            metrics["current_volume"] = df["Volume"][-1]

        return metrics
