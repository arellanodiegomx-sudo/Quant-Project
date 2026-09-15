▄▄▄▄·  ▄▄▄·  ▄▄· ▄ •▄ ▄▄▄▄▄▄▄▄ ..▄▄ · ▄▄▄▄▄▄▄▄ .▄▄▄  
▐█ ▀█▪▐█ ▀█ ▐█ ▌▪█▌▄▌▪•██  ▀▄.▀·▐█ ▀. •██  ▀▄.▀·▀▄ █·
▐█▀▀█▄▄█▀▀█ ██ ▄▄▐▀▀▄· ▐█.▪▐▀▀▪▄▄▀▀▀█▄ ▐█.▪▐▀▀▪▄▐▀▀▄ 
██▄▪▐█▐█ ▪▐▌▐███▌▐█.█▌ ▐█▌·▐█▄▄▌▐█▄▪▐█ ▐█▌·▐█▄▄▌▐█•█▌
·▀▀▀▀  ▀  ▀ ·▀▀▀ ·▀  ▀ ▀▀▀  ▀▀▀  ▀▀▀▀  ▀▀▀  ▀▀▀ .▀  ▀

# Quant Backtester

An algorithmic trading research platform that simulates trading strategies on historical market data.

## What it does
- Fetches and stores historical price data for 5 stocks (AAPL, MSFT, GOOGL, AMZN, TSLA)
- Runs backtests using three strategies: Moving Average Crossover, Mean Reversion, and Momentum
- Enforces risk management rules: position sizing, stop loss, and max drawdown limits
- Visualizes results with an equity curve and performance metrics

## Tech stack
- **Backend**: Python, FastAPI, PostgreSQL, yfinance
- **Frontend**: React, Recharts, Vite
- **Deployment**: Render (backend + database), Vercel (frontend)

## Live demo
- Frontend: https://dashboard-tawny-eight-lzng7774jv.vercel.app
- API: https://quant-backend-xb53.onrender.com/docs

## How to run locally
1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the API: `uvicorn api:app --reload`
5. In a separate terminal run the React dashboard: `cd dashboard && npm run dev`

## Disclaimer:
This project is for educational purposes only and is not financial advice.