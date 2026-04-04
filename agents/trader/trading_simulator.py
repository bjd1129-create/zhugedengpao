#!/usr/bin/env python3
"""
Binance Real Grid Trading Simulator v3.0 - Hybrid Strategy
- BTC/ETH: 持有不操作（长期）
- AVAX/ADA: 密集网格交易
- 止损：$9,500 | 止盈：$10,500
"""
import requests, json, os
from datetime import datetime

PRICE_URL = "https://api.binance.com/api/v3/ticker/price"
PORTFOLIO_PATH = os.path.expanduser("~/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json")
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or None
INITIAL_BALANCE = 10_000.0
STOP_LOSS = 0.95
TAKE_PROFIT = 1.05

# 币种配置
# mode: 'hold'=买入持有不操作 | 'grid'=网格交易
COINS = [
    {'symbol': 'BTC',  'name': 'Bitcoin',    'per_grid': 0,    'price_fmt': 2,  'mode': 'hold'},  # 持有不操作
    {'symbol': 'ETH',  'name': 'Ethereum',   'per_grid': 0,    'price_fmt': 2,  'mode': 'hold'},  # 持有不操作
    {'symbol': 'AVAX', 'name': 'Avalanche',  'per_grid': 250,  'price_fmt': 2,  'mode': 'grid', 'spacing': 0.015},  # ±1.5%密集网格
    {'symbol': 'ADA',  'name': 'Cardano',    'per_grid': 200,  'price_fmt': 4,  'mode': 'grid', 'spacing': 0.03},   # ±3%网格
]


def get_price(symbol):
    try:
        kwargs = {"params": {"symbol": symbol + "USDT"}, "timeout": 10}
        if PROXY: kwargs["proxies"] = {"https": PROXY}
        r = requests.get(PRICE_URL, **kwargs)
        if r.status_code == 200: return float(r.json()["price"])
    except Exception as e:
        print(f"  ⚠️ {symbol} 价格获取失败: {e}")
    return None


def load_portfolio():
    with open(PORTFOLIO_PATH) as f: return json.load(f)

def save_portfolio(p):
    with open(PORTFOLIO_PATH, 'w') as f: json.dump(p, f, indent=2, ensure_ascii=False)

def build_grid(center, spacing, count=8):
    half = count // 2
    return [round(center * (1 + spacing) ** i, 4) for i in range(-half + 1, half + 1)]

def get_grid_idx(price, levels):
    for i in range(len(levels) - 1):
        if levels[i] <= price < levels[i + 1]: return i
    return len(levels) - 1


def run_grid(portfolio, sym, price, per_grid, spacing):
    gs = portfolio['gridState'].setdefault(sym, {})
    levels = gs.get('levels', [])

    # 初始化网格
    if not levels:
        levels = build_grid(price, spacing)
        gs.update({'levels': levels, 'position': 0.0, 'avgPrice': 0.0, 'lastGridIdx': None, 'fills': []})
        portfolio['gridState'][sym] = gs
        print(f"  🟢 [{sym}] 网格启动: {levels[0]:.4f} ~ {levels[-1]:.4f}")
        return False, ""

    pos = gs['position']
    avg = gs['avgPrice']
    fills = gs['fills']
    last = gs.get('lastGridIdx')
    curr = get_grid_idx(price, levels)
    gs['lastGridIdx'] = curr
    trades = []

    if last is not None and curr != last:
        if curr < last and pos == 0:  # 下跌且无持仓 → 买入
            buy_amt = per_grid / price
            pos += buy_amt
            avg = (avg * (pos - buy_amt) + per_grid) / pos if pos > buy_amt else price
            fills.insert(0, {
                "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                "side": "BUY", "symbol": sym, "amount": round(buy_amt, 8),
                "price": round(price, 4), "note": f"grid-{curr} ↓"
            })
            trades.append(f"📈 买入 {sym} @ ${price:.4f}")
        elif curr > last and pos > 0:  # 上涨且持仓 → 卖出
            proceeds = pos * price
            pnl = (price - avg) * pos
            fills.insert(0, {
                "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                "side": "SELL", "symbol": sym, "amount": round(pos, 8),
                "price": round(price, 4), "note": f"grid-{last}↑ PnL:${pnl:+.2f}"
            })
            trades.append(f"📤 卖出 {sym} @ ${price:.4f} (${pnl:+.2f})")
            pos = 0
            avg = 0

    gs.update({'position': pos, 'avgPrice': avg, 'fills': fills[:30]})
    return bool(trades), " | ".join(trades) if trades else ""


def main():
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"\n[🕐 {ts}] ═══ 混合策略运行 ═══")

    prices = {c['symbol']: p for c in COINS if (p := get_price(c['symbol']))}
    if not prices:
        print("  ⚠️ 价格全部获取失败")
        return

    for sym, price in prices.items():
        coin = next((c for c in COINS if c['symbol'] == sym), {})
        print(f"  {sym}: ${price:,.{coin.get('price_fmt',2)}f} [{coin.get('mode','grid')}]")

    p = load_portfolio()
    p['lastUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    trade_notes = []
    cash = p['account'].get('cashBalance', INITIAL_BALANCE)

    # 处理每个币种
    for coin in COINS:
        sym, mode = coin['symbol'], coin['mode']
        price = prices.get(sym)
        if not price: continue

        if mode == 'hold':
            # 持有模式：买入一次，之后不操作
            gs = p['gridState'].setdefault(sym, {})
            if gs.get('position', 0) == 0 and cash >= coin['per_grid'] or (coin['per_grid'] > 0 and gs.get('position', 0) == 0):
                # 买入持有
                alloc = coin['per_grid']
                if alloc > 0 and cash >= alloc:
                    amt = alloc / price
                    gs.update({'position': amt, 'avgPrice': price, 'levels': [], 'lastGridIdx': None, 'fills': []})
                    cash -= alloc
                    p['account']['cashBalance'] = round(cash, 2)
                    print(f"  💎 买入 {sym} ${alloc:.0f} @ ${price:.2f} = {amt:.6f}")
            # 更新当前价格
            for h in p['holdings']:
                if h['symbol'] == sym:
                    h['amount'] = round(gs.get('position', 0), 8)
                    h['avgPrice'] = round(gs.get('avgPrice', price), 2)
                    h['currentPrice'] = round(price, coin['price_fmt'])
                    h['value'] = round(h['amount'] * price, 2)
                    h['pnl'] = round((price - h['avgPrice']) * h['amount'], 2)
                    h['pnlPercent'] = round((price - h['avgPrice']) / h['avgPrice'] * 100, 4) if h['avgPrice'] > 0 else 0

        else:  # grid mode
            traded, note = run_grid(p, sym, price, coin['per_grid'], coin['spacing'])
            if note: trade_notes.append(note)
            gs = p['gridState'].get(sym, {})
            pos, avg = gs.get('position', 0), gs.get('avgPrice', 0)
            for h in p['holdings']:
                if h['symbol'] == sym:
                    h['amount'] = round(pos, 8)
                    h['avgPrice'] = round(avg, 4)
                    h['currentPrice'] = round(price, coin['price_fmt'])
                    h['value'] = round(pos * price, 2)
                    h['pnl'] = round((price - avg) * pos, 2) if pos > 0 else 0
                    h['pnlPercent'] = round((price - avg) / avg * 100, 4) if avg > 0 else 0

    # 总资产
    holdings_value = sum(h['value'] for h in p['holdings'])
    total = cash + holdings_value
    p['account']['totalValue'] = round(total, 2)
    p['account']['cashBalance'] = round(cash, 2)
    p['account']['totalPnL'] = round(total - INITIAL_BALANCE, 2)
    p['account']['totalPnLPercent'] = round((total - INITIAL_BALANCE) / INITIAL_BALANCE * 100, 4)

    # 全局止损/止盈
    if total <= INITIAL_BALANCE * STOP_LOSS:
        print(f"  🛑 止损！总资产 ${total:.2f}")
    elif total >= INITIAL_BALANCE * TAKE_PROFIT:
        print(f"  🎯 止盈！总资产 ${total:.2f}")

    # 收益曲线
    today = datetime.now().strftime("%Y-%m-%d")
    equity = p.get('equityCurve', [])
    if equity and equity[-1]['date'] == today:
        equity[-1]['value'] = round(total, 2)
    else:
        equity.append({"date": today, "value": round(total, 2)})
    p['equityCurve'] = equity[-30:]

    p['account']['totalTrades'] = sum(
        len(p['gridState'].get(c['symbol'], {}).get('fills', [])) for c in COINS
    )

    recent = []
    for c in COINS:
        for f in p['gridState'].get(c['symbol'], {}).get('fills', [])[:2]:
            recent.append(f)
    p['recentTrades'] = sorted(recent, key=lambda x: x['time'], reverse=True)[:10]

    save_portfolio(p)
    acc = p['account']
    print(f"\n  💰 总资产: ${total:,.2f} ({acc['totalPnLPercent']:+.2f}%) | 现金: ${cash:,.2f} | 交易: {acc['totalTrades']}笔")
    for note in trade_notes:
        print(f"  {note}")


if __name__ == "__main__":
    main()
