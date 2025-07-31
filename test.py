"""
test.py

Standalone script to test Yahoo Finance connectivity. Downloads recent stock data
for a given ticker and prints the latest adjusted close price to verify connection.

Usage:
- Run this file directly with `python3 test.py` to confirm data_fetch reliability.
"""

import yfinance as yf

def test_yahoo_connection(ticker="AAPL"):
    try:
        # Download historical data with explicit settings
        data = yf.download(ticker, period="1mo", auto_adjust=False, threads=False)
        
        # Ensure data isn't empty and has the required column
        if data.empty or "Adj Close" not in data.columns:
            raise ValueError("No usable data returned.")
        
        # Extract last non-null value
        series = data["Adj Close"].dropna()
        latest_price = float(series.iloc[-1])


        print(f"✅ Yahoo Finance API working. Latest {ticker} price: ${latest_price:.2f}")
        return True

    except Exception as e:
        print(f"❌ Error connecting to Yahoo Finance: {e}")
        print("🔁 Falling back to static data for demo.")
        return False

if __name__ == "__main__":
    test_yahoo_connection("AAPL")
