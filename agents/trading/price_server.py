#!/usr/bin/env python3
"""
多平台实时行情聚合器
同时抓取 Binance + OKX + Bybit 实时价格
输出到 price_aggregate.json 给前端页面使用
"""
import requests, json, os
from datetime import datetime

PROXY = {'https': 'http://127.0.0.1:7897'}
OUT_PATH = os.path.expanduser('~/Desktop/ZhugeDengpao-Team/data/trading/price_aggregate.json')

SYMBOLS = ['BTC', 'ETH', 'AVAX', 'ADA']

def get_binance():
    prices = {}
    for sym in SYMBOLS:
        try:
            r = requests.get('https://api.binance.com/api/v3/ticker/price',
                params={'symbol': f'{sym}USDT'}, proxies=PROXY, timeout=10)
            prices[sym] = float(r.json()['price'])
        except: prices[sym] = None
    return prices

def get_okx():
    prices = {}
    for sym in ['BTC', 'ETH', 'AVAX', 'ADA']:
        inst = f'{sym}-USDT'
        try:
            r = requests.get('https://www.okx.com/api/v5/market/ticker',
                params={'instId': inst}, proxies=PROXY, timeout=10)
            prices[sym] = float(r.json()['data'][0]['last'])
        except: prices[sym] = None
    return prices

def get_bybit():
    prices = {}
    for sym in ['BTC', 'ETH', 'AVAX', 'ADA']:
        try:
            r = requests.get('https://api.bybit.com/v5/market/tickers',
                params={'category': 'spot', 'symbol': f'{sym}USDT'}, proxies=PROXY, timeout=10)
            prices[sym] = float(r.json()['result']['list'][0]['lastPrice'])
        except: prices[sym] = None
    return prices

def main():
    ts = datetime.now().strftime('%H:%M:%S')
    bn = get_binance()
    okx = get_okx()
    bybit = get_bybit()

    data = {
        'timestamp': ts,
        'updated': datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        'platforms': {
            'Binance': {'prices': bn, 'note': '最成熟'},
            'OKX': {'prices': okx, 'note': '费率低'},
            'Bybit': {'prices': bybit, 'note': '合约强'}
        },
        'best': {}  # 最佳买卖价
    }

    # 计算最佳价格（买价/卖价）
    for sym in SYMBOLS:
        valid = {k: v for k, v in {'Binance': bn.get(sym), 'OKX': okx.get(sym), 'Bybit': bybit.get(sym)}.items() if v}
        if valid:
            best_bid = max(valid, key=valid.get)
            best_ask = min(valid, key=valid.get)
            data['best'][sym] = {
                'lowestAsk': valid[best_ask],
                'highestBid': valid[best_bid],
                'spread': valid[best_ask] - valid[best_bid],
                'arb': '✅ 有套利空间' if valid[best_ask] < valid[best_bid] else '❌ 无套利'
            }

    with open(OUT_PATH, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[{ts}] 三平台价格聚合完成")
    for sym in SYMBOLS:
        bn_p = bn.get(sym)
        okx_p = okx.get(sym)
        by_p = bybit.get(sym)
        bn_s = f"${bn_p:,.2f}" if bn_p else "❌"
        okx_s = f"${okx_p:,.2f}" if okx_p else "❌"
        by_s = f"${by_p:,.2f}" if by_p else "❌"
        print(f"  {sym}: BN={bn_s} | OKX={okx_s} | BY={by_s}")

if __name__ == '__main__':
    main()
