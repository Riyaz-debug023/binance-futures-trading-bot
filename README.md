# Binance Futures Testnet Trading Bot

## Features
- Market Orders
- Limit Orders
- BUY / SELL
- CLI Interface
- Logging
- Error Handling

## Setup
pip install -r requirements.txt

## Run

Market:
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

Limit:
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000

## Tech Stack
- Python
- Requests
- Binance Futures Testnet API
