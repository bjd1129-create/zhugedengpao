#!/usr/bin/env python3
"""
Binance Grid Trading Simulator
Uses real Binance prices (production public API), simulates account locally.
"""
import requests
import json
import time
import os
from datetime import datetime

# Use production public API for prices (no auth needed)
PRICE_URL = "https://api.binance.com/api/v3/ticker/price"

PORTFOLIO_PATH = os.path.expanduser("~/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json")

INITIAL_BALANCE = 10000.0
GRID_SPACING = 0.02
POSITION_PER_GRID = INITIAL_BALANCE / 10

def get_price(symbol):
    try:
        r = requests.get(PRICE_URL, params={"symbol": symbol}, timeout=10)
        if r.status_code == 200:
            return float(r.json()["price"])
    except Exception as e:
        print(f"Price fetch error: {e}")
    return None

def load_portfolio():
    with open(PORTFOLIO_PATH, 'r') as f:
        return json.load(f)

def save_portfolio(p):
    with open(PORTFOLIO_PATH, 'w') as f:
        json.dump(p, f, indent=2, ensure_ascii=False)

def simulate_trades(portfolio, btc_price, eth_price):
    """Run grid logic on current prices."""
    holdings = {h['symbol']: h for h in portfolio['holdings']}
    trades = portfolio.get('recentTrades', [])
    cash = portfolio['account'].get('cashBalance', INITIAL_BALANCE)
    
    for sym, price in [('BTC', btc_price), ('ETH', eth_price)]:
        if sym not in holdings:
            continue
        h = holdings[sym]
        
        if h['amount'] == 0 and cash >= POSITION_PER_GRID:
            # First grid entry - BUY
            buy_amount = POSITION_PER_GRID / price
            h['amount'] = buy_amount
            h['avgPrice'] = price
            h['currentPrice'] = price
            h['value'] = buy_amount * price
            cash -= POSITION_PER_GRID
            trades.insert(0, {
                "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                "side": "BUY", "symbol": sym,
                "amount": round(buy_amount, 6),
                "price": round(price, 2),
                "note": "grid level 1"
            })
    
    # Update holdings
    for h in holdings.values():
        if h['amount'] > 0:
            h['currentPrice'] = {'BTC': btc_price, 'ETH': eth_price}.get(h['symbol'], h['currentPrice'])
            h['value'] = h['amount'] * h['currentPrice']
            h['pnl'] = (h['currentPrice'] - h['avgPrice']) * h['amount']
            h['pnlPercent'] = (h['currentPrice'] - h['avgPrice']) / h['avgPrice'] if h['avgPrice'] > 0 else 0
    
    # Total value
    holdings_value = sum(h['value'] for h in holdings.values())
    total = cash + holdings_value
    
    portfolio['holdings'] = list(holdings.values())
    portfolio['recentTrades'] = trades[:20]
    portfolio['account']['totalValue'] = round(total, 2)
    portfolio['account']['cashBalance'] = round(cash, 2)
    portfolio['account']['totalPnL'] = round(total - INITIAL_BALANCE, 2)
    portfolio['account']['totalPnLPercent'] = round((total - INITIAL_BALANCE) / INITIAL_BALANCE * 100, 2)
    portfolio['account']['totalTrades'] = len(trades)
    portfolio['lastUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    
    # Equity curve
    today = datetime.now().strftime("%Y-%m-%d")
    equity = portfolio.get('equityCurve', [])
    if equity and equity[-1]['date'] == today:
        equity[-1]['value'] = round(total, 2)
    else:
        equity.append({"date": today, "value": round(total, 2)})
    portfolio['equityCurve'] = equity[-30:]
    
    return portfolio

def main():
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"[{ts}] Trading simulator...")
    
    btc = get_price("BTCUSDT")
    eth = get_price("ETHUSDT")
    
    if not btc or not eth:
        print("Price unavailable")
        return
    
    print(f"BTC: ${btc:,.2f} | ETH: ${eth:,.2f}")
    
    p = load_portfolio()
    p = simulate_trades(p, btc, eth)
    save_portfolio(p)
    
    acc = p['account']
    print(f"Value: ${acc['totalValue']:,.2f} | PnL: {acc['totalPnLPercent']:+.2f}% | Trades: {acc['totalTrades']}")

if __name__ == "__main__":
    main()
