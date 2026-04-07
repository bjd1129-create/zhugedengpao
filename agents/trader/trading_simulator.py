#!/usr/bin/env python3
"""
Grid Trading Simulator v4.2 — 多平台密集网格
- BTC/ETH: 持有不动（各$3000）
- AVAX/ADA: 密集网格20格×0.5%（各$2000预算）
- 初始资金: $10,000
"""
import requests, json, os
from datetime import datetime

PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or None
INITIAL_BALANCE = 10_000.0
PATH = os.path.expanduser('~/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json')
STOP_LOSS = 0.90
TAKE_PROFIT = 1.15

# 策略配置
STRATEGY = {
    'BTC':  {'mode': 'hold', 'budget': 3000},
    'ETH':  {'mode': 'hold', 'budget': 3000},
    'AVAX': {'mode': 'grid', 'budget': 2000, 'spacing': 0.005, 'levels': 20},
    'ADA':  {'mode': 'grid', 'budget': 2000, 'spacing': 0.005, 'levels': 20},
}


SYMBOL_MAP = {'BTC':'bitcoin','ETH':'ethereum','AVAX':'avalanche-2','ADA':'cardano'}

def get_price(symbol):
    # 优先Binance，失败则CoinGecko
    try:
        kwargs = {"params": {"symbol": symbol + "USDT"}, "timeout": 10}
        if PROXY: kwargs["proxies"] = {"https": PROXY}
        r = requests.get("https://api.binance.com/api/v3/ticker/price", **kwargs)
        if r.status_code == 200: return float(r.json()["price"])
    except: pass
    # Fallback: CoinGecko
    try:
        cid = SYMBOL_MAP.get(symbol, symbol.lower())
        r2 = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd", timeout=10)
        if r2.status_code == 200:
            data = r2.json()
            return float(data[cid]['usd'])
    except: pass
    return None


def build_grid(center, spacing, count):
    half = count // 2
    return [round(center * (1 + spacing)**i, 4) for i in range(-half+1, half+1)]


def get_grid_idx(price, levels):
    for i in range(len(levels)-1):
        if levels[i] <= price < levels[i+1]: return i
    return len(levels)-1


def load():
    try:
        with open(PATH) as f: return json.load(f)
    except:
        p = {
            "account": {"cashBalance": INITIAL_BALANCE, "totalValue": INITIAL_BALANCE,
                        "initialBalance": INITIAL_BALANCE, "totalPnL": 0, "totalPnLPercent": 0,
                        "totalTrades": 0, "todayPnL": 0, "todayPnLPercent": 0},
            "holdings": [{"symbol": k, "name": n} for k, n in
                         [('BTC','Bitcoin'),('ETH','Ethereum'),('AVAX','Avalanche'),('ADA','Cardano')]],
            "gridState": {}, "recentTrades": [], "equityCurve": [],
            "lastUpdated": "", "strategy": {"name": "密集网格v4.2", "version": "4.2"}
        }
        with open(PATH, 'w') as f: json.dump(p, f, indent=2, ensure_ascii=False)
        return p


def save(p):
    with open(PATH, 'w') as f: json.dump(p, f, indent=2, ensure_ascii=False)


def main():
    ts = datetime.now().strftime('%H:%M:%S')
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    print(f"\n[🕐 {ts}] ═══ v4.2 密集网格 ═══")

    prices = {}
    for sym in STRATEGY:
        prices[sym] = get_price(sym)
        if prices[sym]:
            mode = STRATEGY[sym]['mode']
            print(f"  {sym}: ${prices[sym]:,.4f} [{'持有' if mode=='hold' else '网格'}]")
        else:
            print(f"  {sym}: ❌ 价格获取失败")

    if not all(prices.values()):
        print("  ⚠️ 部分价格缺失，跳过")
        return

    p = load()
    p['lastUpdated'] = now
    cash = p['account']['cashBalance']
    trades = []

    for sym, cfg in STRATEGY.items():
        price = prices[sym]
        gs = p['gridState'].setdefault(sym, {})
        mode = cfg['mode']

        if mode == 'hold':
            pos = gs.get('position', 0)
            avg = gs.get('avgPrice', 0)

            # 首次买入
            if pos == 0 and cash >= cfg['budget']:
                amt = cfg['budget'] / price
                gs.update({'position': amt, 'avgPrice': price, 'levels': [], 'lastGridIdx': None, 'fills': []})
                cash -= cfg['budget']
                trades.append(f"💎 {sym} 买入 ${cfg['budget']} @ ${price:,.2f}")
            elif pos == 0 and cash < cfg['budget']:
                print(f"  ⚠️ {sym}: 现金不足，跳过 (${cash:.0f} < ${cfg['budget']})")

            pos = gs.get('position', 0)
            avg = gs.get('avgPrice', 0)

        else:  # grid
            spacing = cfg['spacing']
            levels_count = cfg['levels']
            per_grid = cfg['budget'] / (levels_count // 2)  # 每格可用金额

            levels = gs.get('levels', [])
            if not levels:
                levels = build_grid(price, spacing, levels_count)
                gs.update({'levels': levels, 'position': 0, 'avgPrice': 0, 'lastGridIdx': None, 'fills': []})
                print(f"  🟢 [{sym}] 网格: {levels[0]:.4f}~{levels[-1]:.4f} (20格×0.5%)")

            pos = gs['position']
            avg = gs['avgPrice']
            fills = gs['fills']
            last = gs.get('lastGridIdx')

            if price >= levels[0] and price <= levels[-1]:
                curr = get_grid_idx(price, levels)
                gs['lastGridIdx'] = curr

                if last is not None and curr != last:
                    if curr < last and cash >= per_grid:
                        # 价格下跌 → 买入
                        amt = per_grid / price
                        new_pos = pos + amt
                        new_avg = (pos * avg + per_grid) / new_pos if pos > 0 else price
                        fills.insert(0, {
                            "time": now, "side": "BUY", "symbol": sym,
                            "amount": round(amt, 8), "price": round(price, 4),
                            "note": f"grid-{curr}↓"
                        })
                        cash -= per_grid
                        trades.append(f"📈 {sym} @${price:.4f} (grid-{curr})")
                        pos, avg = new_pos, new_avg

                    elif curr > last and pos > 0:
                        # 价格上涨 → 卖出
                        proceeds = pos * price
                        pnl = (price - avg) * pos
                        fills.insert(0, {
                            "time": now, "side": "SELL", "symbol": sym,
                            "amount": round(pos, 8), "price": round(price, 4),
                            "pnl": round(pnl, 2),
                            "note": f"grid-{last}↑ PnL:${pnl:+.2f}"
                        })
                        cash += proceeds
                        trades.append(f"📤 {sym} @${price:.4f} PnL:${pnl:+.2f}")
                        pos, avg = 0, 0
            else:
                curr = get_grid_idx(price, levels) if price < levels[0] else len(levels)-1
                gs['lastGridIdx'] = curr

            gs.update({'position': pos, 'avgPrice': avg, 'fills': fills[:50]})

        # 更新持仓显示
        for h in p['holdings']:
            if h['symbol'] == sym:
                h['amount'] = round(gs.get('position', 0), 8)
                h['avgPrice'] = round(gs.get('avgPrice', 0), 4)
                h['currentPrice'] = round(price, 4)
                h['value'] = round(gs.get('position', 0) * price, 2)
                pnl = (price - gs.get('avgPrice', 0)) * gs.get('position', 0)
                h['pnl'] = round(pnl, 2)
                h['pnlPercent'] = round(pnl / (gs.get('avgPrice', 0) * gs.get('position', 0)) * 100, 2) if gs.get('avgPrice', 0) > 0 and gs.get('position', 0) > 0 else 0

    # 计算总资产
    holdings_value = sum(h.get('value', 0) for h in p['holdings'])
    total = cash + holdings_value
    p['account']['cashBalance'] = round(cash, 2)
    p['account']['totalValue'] = round(total, 2)
    p['account']['totalPnL'] = round(total - INITIAL_BALANCE, 2)
    p['account']['totalPnLPercent'] = round((total - INITIAL_BALANCE) / INITIAL_BALANCE * 100, 2)
    total_trades = 0
    for sym in STRATEGY:
        total_trades += len(p['gridState'].get(sym, {}).get('fills', []))
    p['account']['totalTrades'] = total_trades

    # 止损止盈
    if total <= INITIAL_BALANCE * STOP_LOSS:
        print(f"  🛑 止损! ${total:,.2f}")
    elif total >= INITIAL_BALANCE * TAKE_PROFIT:
        print(f"  🎯 止盈! ${total:,.2f}")

    # 收益曲线
    today = datetime.now().strftime("%Y-%m-%d")
    equity = p.get('equityCurve', [])
    if equity and equity[-1]['date'] == today:
        equity[-1]['value'] = round(total, 2)
    else:
        equity.append({"date": today, "value": round(total, 2)})
    p['equityCurve'] = equity[-30:]

    # 最近交易
    recent = []
    for sym in STRATEGY:
        for f in p['gridState'].get(sym, {}).get('fills', [])[:3]:
            recent.append(f)
    p['recentTrades'] = sorted(recent, key=lambda x: x['time'], reverse=True)[:20]

    save(p)

    # 输出
    print(f"\n  💰 总资产: ${total:,.2f} ({p['account']['totalPnLPercent']:+.2f}%) | 现金: ${cash:,.2f} | 交易: {total_trades}笔")
    for t in trades:
        print(f"  {t}")
    print(f"  持仓: BTC={p['holdings'][0]['amount']:.6f} ETH={p['holdings'][1]['amount']:.6f} AVAX={p['holdings'][2]['amount']:.4f} ADA={p['holdings'][3]['amount']:.6f}")


if __name__ == '__main__':
    # ==========小花添加：紧急停止开关（必须在main()之前）==========
    STOP_FILE = os.path.join(os.path.dirname(PATH), 'STOP_TRADING.flag')
    if os.path.exists(STOP_FILE):
        print("🛑 STOP_TRADING.flag 存在，仅更新价格，不交易")
        p = load()
        prices = {}
        for sym in STRATEGY:
            prices[sym] = get_price(sym)
            if prices[sym]:
                for h in p['holdings']:
                    if h['symbol'] == sym:
                        h['currentPrice'] = round(prices[sym], 4)
                        h['value'] = round(h['amount'] * prices[sym], 2)
        holdings_value = sum(h.get('value', 0) for h in p['holdings'])
        p['account']['totalValue'] = round(p['account']['cashBalance'] + holdings_value, 2)
        p['lastUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        save(p)
        print(f"  仅更新价格完成，总资产: ${p['account']['totalValue']:,.2f}")
        exit(0)
    # ==========停止开关结束==========
    main()

# 旧版停止开关（兼容保留）
STOP_FILE = os.path.join(os.path.dirname(PATH), 'STOP_TRADING.flag')
if os.path.exists(STOP_FILE):
    print("🛑 STOP_TRADING.flag 存在，仅更新价格，不交易")
    p = load()
    prices = {}
    for sym in STRATEGY:
        prices[sym] = get_price(sym)
        if prices[sym]:
            for h in p['holdings']:
                if h['symbol'] == sym:
                    h['currentPrice'] = round(prices[sym], 4)
                    h['value'] = round(h['amount'] * prices[sym], 2)
    holdings_value = sum(h.get('value', 0) for h in p['holdings'])
    p['account']['totalValue'] = round(p['account']['cashBalance'] + holdings_value, 2)
    p['lastUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    save(p)
    print(f"  仅更新价格完成，总资产: ${p['account']['totalValue']:,.2f}")
    exit(0)
# ==========停止开关结束==========
