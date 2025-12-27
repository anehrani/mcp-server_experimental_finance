import yfinance as yf

# Test basic yfinance functionality
ticker = yf.Ticker("AAPL")
print("Stock Info:", ticker.info.get("longName"))
print("Current Price:", ticker.info.get("currentPrice"))

# Test historical data
hist = ticker.history(period="1mo")
print("\nHistorical Data Shape:", hist.shape)
print("Latest Close:", hist['Close'].iloc[-1])

# Test financials
income = ticker.income_stmt
print("\nIncome Statement Shape:", income.shape if not income.empty else "Empty")
