import yfinance as yf

def test_yahoo_connection(ticker="AAPL"):
    try:
        data = yf.download(ticker, period="1mo")
        if data.empty:
            print("Yahoo Finance returned no data.")
            return False
        else:
            latest_price = data["Adj Close"].iloc[-1]
            print(f"Yahoo Finance API working. Latest {ticker} price: ${latest_price:.2f}")
            return True
    except Exception as e:
        print(f"Error connecting to Yahoo Finance: {e}")
        return False

# Run test
if __name__ == "__main__":
    test_yahoo_connection()
