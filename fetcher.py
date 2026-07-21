import yfinance as yf
from database import save_price

def get_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    price = stock.fast_info["last_price"]
    return price

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

for ticker in tickers:
    price = get_price(ticker)
    save_price(ticker, price)