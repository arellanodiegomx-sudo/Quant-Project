import yfinance as yf
import psycopg2
from database import get_connection

#Dowload Historical datat function
def download_historical_data(ticker: str, period: str = "2y"):
    print(f"Downloading historical data for {ticker}...")
    stock = yf.Ticker(ticker)
    df = stock.history(period = period)
    return df

#Save historical data to database function
def save_historical_data(ticker:str, df):
    conn = get_connection()
    cursor = conn.cursor()

    for date, row in df.iterrows():
        cursor.execute("""
            INSERT INTO prices(ticker, price, fetched_at) VALUES(%s, %s, %s) ON CONFLICT DO NOTHING""", 
            (ticker, float(row['Close']), date))
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Saved {len(df)} rows for {ticker}")

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

for ticker in tickers:
    df = download_historical_data(ticker)
    save_historical_data(ticker, df)


