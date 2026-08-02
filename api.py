from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backtester import run_backtest, calculate_metrics, moving_average_strategy, mean_reversion_strategy, momentum_strategy
from database import get_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STRATEGIES = {
    "moving_average": moving_average_strategy,
    "mean_reversion": mean_reversion_strategy,
    "momentum": momentum_strategy
}

class BacktestRequest(BaseModel):
    ticker: str
    strategy: str   

@app.get("/strategies")
def get_strategies():
    return list(STRATEGIES.keys())

@app.get("/prices/{ticker}")
def get_prices(ticker:str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fetched_at, price FROM prices
        WHERE ticker = %s
        ORDER BY fetched_at ASC
    """, (ticker,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"ticker": ticker, "prices": [{"date": str(r[0]), "price": r[1]} for r in rows]}

@app.post("/backtest")
def run_backtest_endpoint(request: BacktestRequest):
    strategy = STRATEGIES.get(request.strategy)
    if not strategy:
        return {"error": "Invalid strategy"}
    portfolio = run_backtest(request.ticker, strategy)
    metrics = calculate_metrics(portfolio)

    return {
        "ticker": request.ticker,
        "strategy": request.strategy,
        "metrics": metrics,
        "equity_curve": portfolio.history
    }
    