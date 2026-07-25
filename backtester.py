# Portfolio class chunk 1
from database import get_connection
from dataclasses import dataclass, field
from typing import Dict
import pandas as pd
import numpy as np

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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute (""" SELECT fetched_at, price FROM prices WHERE ticker = %s ORDER BY fetched_at ASC""", (ticker,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows, columns=["date", "price"])
    df.set_index("date", inplace = True) #inplace modifies th original dataframe instead of creating a new one
    return df

#backtesting function to simulate trading based on historical data
def run_backtest(ticker:str, strategy):
    print(f"\nRunning backtest for {ticker}...")
    df = load_price(ticker)
    portfolio = Portfolio()

    

    for i in range(20,len(df)):
        window = df.iloc[:i]
        current_price = df.iloc[i]["price"]
        current_prices = {ticker: current_price}
        signal = strategy(window, ticker)

        if signal == "buy" and portfolio.positions.get(ticker, 0) == 0:
            quantity = int(portfolio.cash // current_price)
            portfolio.buy(ticker, current_price, quantity)
        elif signal == "sell":
            portfolio.sell(ticker, current_price)

        portfolio.history.append(portfolio.total_value(current_prices))

    return portfolio

#Chunk 3 calculate metrics
def calculate_metrics(portfolio: Portfolio, initial_cash: float = 10000.0) -> Dict[str, float]:
    final_value = portfolio.history[-1]
    total_return = (final_value - initial_cash) / initial_cash * 100

    daily_returns = pd.Series(portfolio.history).pct_change().dropna()
    sharpe = daily_returns.mean() / daily_returns.std() * (252 ** 0.5)

    peak = pd.Series(portfolio.history).cummax()
    drawdown = (pd.Series(portfolio.history) - peak) / peak
    max_drawdown = drawdown.min() * 100
    
    print(f"\n--- Results ---")
    print(f"Starting cash:  ${initial_cash:,.2f}")
    print(f"Final value:    ${final_value:,.2f}")
    print(f"Total return:   {total_return:.2f}%")
    print(f"Sharpe ratio:   {sharpe:.2f}")
    print(f"Max drawdown:   {max_drawdown:.2f}%")

    return {
        "total_return": total_return,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "final_value": final_value
    }
#moving average crossover strategy function
def moving_average_strategy (window: pd.DataFrame, ticker:str) -> str:
    if len(window) < 20:
        return "hold"
    short_ma = window["price"].tail(5).mean()
    long_ma = window["price"].tail(20).mean()

    if short_ma > long_ma:
        return "buy"
    elif short_ma < long_ma:
        return "sell"
    return "hold"


#Mean reversion strategy function
def mean_reversion_strategy(window: pd.DataFrame, ticker:str) -> str:
    if len(window) < 20:
        return "hold"
    mean = window["price"].tail(20).mean()
    std = window["price"].tail(20).std()
    current_price = window["price"].iloc[-1]
    if current_price < mean - std:
        return "buy"
    elif current_price > mean + std:
        return "sell"
    return "hold"
#momentum strategy function
def momentum_strategy(window: pd.DataFrame, ticker:str) -> str:
    if len(window) < 20:
        return "hold"
    returns = window["price"].pct_change().tail(10)
    if returns.mean() > 0.001:
        return "buy"
    elif returns.mean() < -0.001:
        return "sell"
    return "hold"

if __name__ == "__main__":
    strategies = {
        "Moving Average": moving_average_strategy,
        "Mean Reversion": mean_reversion_strategy,
        "Momentum": momentum_strategy
    }

    for name, strategy in strategies.items():
        print(f"\n{'='*40}")
        print(f"Strategy: {name}")
        print(f"{'='*40}")
        portfolio = run_backtest("AAPL", strategy)
        calculate_metrics(portfolio)