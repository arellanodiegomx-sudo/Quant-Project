# Portfolio class chunk 1
import psycopg2
from database import get_connection
from dataclasses import dataclass, field
from typing import Dict
import pandas as pd

@dataclass
class Portfolio:
    cash: float = 10000.0
    positions: Dict[str, int] = field(default_factory=dict)
    history: list = field(default_factory=list)
#Buy function to buy stocks
    def buy(self, ticker: str, price: float, quantity: int = 1):
        cost = price * quantity
        if cost > self.cash: #check if there is enough cash to buy the stock
            return
        self.cash -= cost
        self.positions[ticker] = self.positions.get(ticker, 0) + quantity #update the position of the stock in the portfolio
        print(f"BUY {quantity} {ticker} @ ${price:.2f}")
#sell function to sell stocks
    def sell(self, ticker:str, price:float, quantity:int = 1):
        if ticker not in self.positions or self.positions[ticker] == 0: #check if the stock is in the portfolio and if there are enough shares to sell
            return
        quantity = self.positions[ticker]
        self.cash += price * quantity
        self.positions[ticker] = 0
        print(f"SELL {quantity} {ticker} @ ${price:.2f}")
# function to get the total value of the portfolio
    def total_value(self, current_prices: Dict[str, float]) -> float:
        stock_value = sum( self.positions.get(ticker, 0) * price for ticker, price in current_prices.items())
        return self.cash + stock_value
    
# data loader function to load historical data from the database
def load_price(ticker: str) -> pd.DataFrame:
    conn = get_connection
    cursor = conn.cursor()
    cursor.execute (""" SELECT fetched_at, price FROM prices WHERE ticker = %s ORDER BY fetched_at ASC""", (ticker,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows, columns=["date", "price"])
    df.set_index("date", inplace = True) #inplace modifies th original dataframe instead of creating a new one
    return df

#backtesting function to simulate trading based on historical data
def backtest(ticker:str, strategy):
    print(f"\nRunning backtest for {ticker}...")
    df = load_price(ticker)
    portfolio = Portfolio()
    for i in range(20,len(df)):
        window = df.iloc[:i]
        current_price = df.iloc[i]["price"]
        current_prices = {ticker: current_price}
        signal = strategy(window, ticker)

        if signal == "buy":
            quantity = int(portfolio.cash // current_price)
            portfolio.buy(ticker, current_price, quantity)
        elif signal == "sell":
            portfolio.sell(ticker, current_price)

        portfolio.history.append(portfolio.total_value(current_prices))

    return portfolio



