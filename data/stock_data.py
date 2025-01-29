import yfinance as yf
import pandas as pd

class StockDataFetcher:
    @staticmethod
    def get_stock_data(symbol: str, period: str = "1mo"):
        """Fetch stock data using yfinance"""
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        return hist
    
    @staticmethod
    def get_company_info(symbol: str):
        """Fetch company information"""
        stock = yf.Ticker(symbol)
        return {
            "info": stock.info,
            "news": stock.news,
            "recommendations": stock.recommendations,
            "financials": stock.financials
        } 