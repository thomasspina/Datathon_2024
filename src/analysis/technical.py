import pandas as pd
import numpy as np
from typing import Dict, Any


class TechnicalAnalysis:
    """Technical analysis calculations"""

    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate all technical indicators"""
        indicators = {}

        # Moving Averages
        ma_periods = [20, 50, 200]
        for period in ma_periods:
            indicators[f"SMA_{period}"] = df["Close"].rolling(window=period).mean()
            indicators[f"EMA_{period}"] = (
                df["Close"].ewm(span=period, adjust=False).mean()
            )

        # RSI
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        indicators["RSI"] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = df["Close"].ewm(span=12, adjust=False).mean()
        exp2 = df["Close"].ewm(span=26, adjust=False).mean()
        indicators["MACD"] = exp1 - exp2
        indicators["Signal_Line"] = indicators["MACD"].ewm(span=9, adjust=False).mean()
        indicators["MACD_Histogram"] = indicators["MACD"] - indicators["Signal_Line"]

        # Bollinger Bands
        sma_20 = df["Close"].rolling(window=20).mean()
        std_20 = df["Close"].rolling(window=20).std()
        indicators["BB_Upper"] = sma_20 + (std_20 * 2)
        indicators["BB_Middle"] = sma_20
        indicators["BB_Lower"] = sma_20 - (std_20 * 2)

        # Volume Indicators
        indicators["Volume_SMA_20"] = df["Volume"].rolling(window=20).mean()
        indicators["Volume_SMA_50"] = df["Volume"].rolling(window=50).mean()

        return indicators

    @staticmethod
    def get_signals(
        df: pd.DataFrame, indicators: Dict[str, pd.Series]
    ) -> Dict[str, str]:
        """Generate trading signals based on indicators"""
        signals = {}

        # RSI Signals
        current_rsi = indicators["RSI"].iloc[-1]
        if current_rsi < 30:
            signals["RSI"] = ("Oversold", "green")
        elif current_rsi > 70:
            signals["RSI"] = ("Overbought", "red")
        else:
            signals["RSI"] = ("Neutral", "gray")

        # MACD Signals
        if indicators["MACD"].iloc[-1] > indicators["Signal_Line"].iloc[-1]:
            signals["MACD"] = ("Bullish", "green")
        else:
            signals["MACD"] = ("Bearish", "red")

        # Trend Signals
        current_price = df["Close"].iloc[-1]
        if current_price > indicators["SMA_200"].iloc[-1]:
            signals["Trend"] = ("Uptrend", "green")
        else:
            signals["Trend"] = ("Downtrend", "red")

        # Bollinger Bands Signals
        if current_price > indicators["BB_Upper"].iloc[-1]:
            signals["BB"] = ("Overbought", "red")
        elif current_price < indicators["BB_Lower"].iloc[-1]:
            signals["BB"] = ("Oversold", "green")
        else:
            signals["BB"] = ("Normal", "gray")

        return signals