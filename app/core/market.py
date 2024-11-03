# app/services/market_service.py
from typing import Dict, Optional, Any
import yfinance as yf
from dataclasses import dataclass
from datetime import datetime
from urllib.error import HTTPError


@dataclass
class StockData:
    symbol: str
    company_name: str
    current_price: float
    market_cap: float
    pe_ratio: Optional[float]
    volume: int
    fifty_two_week_high: float
    fifty_two_week_low: float
    sector: str
    industry: str
    business_summary: str
    recommendation: str
    target_mean_price: float
    updated_at: datetime


class MarketService:
    def __init__(self):
        self._cache = {}  # Simple cache implementation
        self.ticker = None

    def fetch_ticker(self, symbol: str):
        try:
            self.ticker = yf.Ticker(symbol)
        except Exception as e:
            raise ValueError(f"Error fetching data for {symbol}: {str(e)}")

    def get_news_data(self) -> list:
        """
        Get news data for a given symbol.
        """
        news_list = self.ticker.news if self.ticker else []
        parsed_news = []
        for article in news_list:
            parsed_news.append(
                {
                    "title": article.get("title"),
                    "published_date": article.get("providerPublishTime"),
                }
            )
        return parsed_news

    def get_market_data(self) -> StockData:
        """
        Get stock data for a given symbol.
        Raises ValueError if symbol is invalid.
        """
        try:
            info = self.ticker.info

            return StockData(
                symbol=info.get("symbol", ""),
                company_name=info.get("longName", ""),
                current_price=info.get("currentPrice", 0.0),
                market_cap=info.get("marketCap", 0),
                pe_ratio=info.get("forwardPE"),
                volume=info.get("volume", 0),
                fifty_two_week_high=info.get("fiftyTwoWeekHigh", 0),
                fifty_two_week_low=info.get("fiftyTwoWeekLow", 0),
                sector=info.get("sector", ""),
                industry=info.get("industry", ""),
                business_summary=info.get("longBusinessSummary", ""),
                recommendation=info.get("recommendationKey", ""),
                target_mean_price=info.get("targetMeanPrice", 0.0),
                updated_at=datetime.now(),
            )

        except Exception as e:
            raise ValueError(f"Error fetching data for {symbol}: {str(e)}")

    def get_historical_data(self, symbol: str, period: str = "1y") -> Dict:
        """
        Get historical data for a given symbol.
        period: Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        """
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period=period)
            return history.to_dict()
        except Exception as e:
            raise ValueError(f"Error fetching historical data for {symbol}: {str(e)}")

    def is_valid_symbol(self, symbol: str) -> bool:
        """Check if a symbol exists"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            # If we can get currentPrice (or regularMarketPrice), the symbol exists
            return "regularMarketPrice" in info or "currentPrice" in info
        except:  # If any error occurs during the fetch, symbol doesn't exist
            return False
