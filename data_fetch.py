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

def get_price_return(ticker: str, months: int = 6) -> float:
    """
    Fetches price return over the past `months` using yfinance.
    Falls back to static value if any issue occurs.
    """
    try:
        period = f"{months}mo"
        data = yf.download(ticker, period=period)
        if len(data) < 2:
            raise ValueError("Insufficient data returned")

        start_price = data['Adj Close'].iloc[0]
        end_price = data['Adj Close'].iloc[-1]
        pct_return = (end_price - start_price) / start_price

        return round(pct_return, 4)  # e.g., 0.045 for 4.5%
    except Exception as e:
        print(f"⚠️ Using fallback for {ticker}: {e}")
        return fallback_returns.get(ticker, 0.01)

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
