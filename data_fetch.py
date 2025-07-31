"""
data_fetch.py

Handles retrieval of financial data such as stock price returns and sentiment scores.
Uses Yahoo Finance via the `yfinance` library. Includes fallback logic in case of
network errors or unavailable data.

Key functions:
- get_price_return(): Fetches recent price change as a return percentage.
- get_sentiment_score(): Placeholder for sentiment analysis (currently static).
- get_live_signals(): Combines return and sentiment data for a set of tickers.
"""

import yfinance as yf
import pandas as pd

# Optional fallback values for offline mode or demo stability
fallback_returns = {
    "AAPL": 0.03,
    "TSLA": 0.05,
    "GOOG": 0.02,
    "SPY": 0.01,
    "VOO": 0.015
}

# Optional fallback sentiment scores (can be refined later)
fallback_sentiments = {
    "AAPL": 0.6,
    "TSLA": 0.8,
    "GOOG": 0.5,
    "SPY": 0.9,
    "VOO": 0.85
}

def get_price_return(ticker, period="1mo"):
    try:
        data = yf.download(ticker, period=period, auto_adjust=False, threads=False)

        if data.empty or "Adj Close" not in data.columns:
            raise ValueError("Insufficient data returned")

        # Drop nulls and ensure enough data points
        prices = data["Adj Close"].dropna()
        if len(prices) < 2:
            raise ValueError("Not enough price points")

        pct_return = (prices.iloc[-1] / prices.iloc[0]) - 1
        return float(pct_return.iloc[0]) if isinstance(pct_return, pd.Series) else float(pct_return)


    except Exception as e:
        print(f"⚠️ Using fallback for {ticker}: {e}")
        return 0.02  # fallback return

def get_live_signals(tickers: list[str]) -> dict:
    """
    Combines returns + fallback sentiment for a list of tickers.
    """
    signals = {}
    for ticker in tickers:
        signals[ticker] = {
            "return": get_price_return(ticker),
            "sentiment": fallback_sentiments.get(ticker, 0.5)
        }
    return signals
