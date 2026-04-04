#!/usr/bin/env python3
"""
OKX Grid Trading Simulator v1.0
策略: 密集网格v4.1 (20格×0.5%)
"""
import requests, json, os
from datetime import datetime

P = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or None
INITIAL = 10_000.0
PATH = os.path.expanduser('~/Desktop/ZhugeDengpao-Team/data/trading/okx_portfolio.json')
STOP_LOSS = 0.95
TAKE_PROFIT = 1.05

SYMBOLS = {
    'BTC': {'okx': 'BTC-USDT', 'per_grid': 250, 'spacing': 0.005, 'levels': 20},
    'ETH': {'okx': 'ETH-USDT', 'per_grid': 150, 'spacing': 0.005, 'levels': 20},
    'AVAX': {'okx': 'AVAX-USDT', 'per_grid': 200, 'spacing': 0.005, 'levels': 20},
    'ADA': {'okx': 'ADA-USDT', 'per_grid': 200, 'spacing': 0.005, 'levels': 20},
}


def get_price(sym):
    try:
        r = requests.get('https://www.okx.com/api/v5/market/ticker',
            params={'instId': sym}, proxies={'https': P} if P else {}, timeout=10)
        d = r.json().get('data', [{}])[0]
        return float(d.get('last', 0)) if d.get('last') else None
    except: return None


def build_grid(center, spacing, count):
    h = count // 2
    return [round(center * (1 + spacing)**i, 4) for i in range(-h+1, h+1)]


def get_idx(price, levels):
    for i in range(len(levels)-1):
        if levels[i] <= price < levels[i+1]: return i
    return len(levels)-1


def main():
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"\n[🕐 {ts}] OKX 密集网格")
    
    prices = {k: get_price(v['okx']) for k, v in SYMBOLS.items()}
    print(f"  价格: {', '.join(f'{k}:${v:,.4f}' if v else f'{k}:❌' for k,v in prices.items())}")
    
    if not any(prices.values()):
        print("  ⚠️ 价格获取失败")
        return
    
    try:
        with open(PATH) as f: p = json.load(f)
    except:
        p = {'account': {'cashBalance': INITIAL, 'totalValue': INITIAL, 'initialBalance': INITIAL, 'totalPnL': 0, 'totalPnLPercent': 0, 'totalTrades': 0}, 'holdings': [{'symbol': k} for k in SYMBOLS], 'gridState': {}, 'lastUpdated': ''}
    
    p['lastUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    cash = p['account'].get('cashBalance', INITIAL)
    trades = []
    
    for sym, cfg in SYMBOLS.items():
        price = prices.get(sym)
        if not price: continue
        
        gs = p['gridState'].setdefault(sym, {})
        levels = gs.get('levels', [])
        
        if not levels:
            levels = build_grid(price, cfg['spacing'], cfg['levels'])
            gs.update({'levels': levels, 'position': 0.0, 'avgPrice': 0.0, 'lastGridIdx': None, 'fills': []})
            print(f"  🟢 [{sym}] 网格: {levels[0]:.4f}~{levels[-1]:.4f}")
            continue
        
        pos = gs['position']
        avg = gs['avgPrice']
        fills = gs['fills']
        last = gs.get('lastGridIdx')
        curr = get_idx(price, levels)
        gs['lastGridIdx'] = curr
        
        if last is not None and curr != last:
            pg = cfg['per_grid']
            if curr < last:
                amt = pg / price
                pos = pos + amt
                avg = (pos * avg + pg) / pos if pos > amt else price
                fills.insert(0, {'time': p['lastUpdated'], 'side': 'BUY', 'symbol': sym, 'amount': round(amt,8), 'price': round(price,4)})
                cash -= pg
                trades.append(f"📈 {sym} @${price:.4f}")
            elif curr > last and pos > 0:
                proceeds = pos * price
                pnl = (price - avg) * pos
                fills.insert(0, {'time': p['lastUpdated'], 'side': 'SELL', 'symbol': sym, 'amount': round(pos,8), 'price': round(price,4), 'pnl': round(pnl,2)})
                cash += proceeds
                pos = 0; avg = 0
                trades.append(f"📤 {sym} @${price:.4f} PnL:${pnl:+.2f}")
        
        gs.update({'position': pos, 'avgPrice': avg, 'fills': fills[:30]})
        for h in p['holdings']:
            if h['symbol'] == sym:
                h.update({'amount': round(pos,8), 'avgPrice': round(avg,4), 'currentPrice': round(price,4), 'value': round(pos*price,2)})
    
    hv = sum(h.get('value',0) for h in p['holdings'])
    total = cash + hv
    p['account'].update({'cashBalance': round(cash,2), 'totalValue': round(total,2), 'totalPnL': round(total-INITIAL,2), 'totalPnLPercent': round((total-INITIAL)/INITIAL*100,4), 'totalTrades': sum(len(p['gridState'].get(h['symbol'],{}).get('fills',[])) for h in p['holdings'])})
    
    if total <= INITIAL * STOP_LOSS: print(f"  🛑 止损 ${total:.2f}")
    elif total >= INITIAL * TAKE_PROFIT: print(f"  🎯 止盈 ${total:.2f}")
    
    with open(PATH, 'w') as f: json.dump(p, f, indent=2, ensure_ascii=False)
    
    print(f"  💰 总: ${total:,.2f} ({p['account']['totalPnLPercent']:+.2f}%) | {' '.join(trades) if trades else '无交易'}")


if __name__ == '__main__':
    main()
