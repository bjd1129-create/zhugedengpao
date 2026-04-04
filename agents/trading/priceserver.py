#!/usr/bin/env python3
"""
三平台实时价格服务
每30秒抓取 Binance + OKX + Bybit 价格
写到 data/trading/price_aggregate.json 给前端读取
"""
import requests, json, os, time
from datetime import datetime

PROXY = {'https': 'http://127.0.0.1:7897'}
OUT = '/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/price_aggregate.json'
SYMS = ['BTC', 'ETH', 'AVAX', 'ADA']


def fetch_all():
    result = {}
    # Binance
    bn = {}
    for s in SYMS:
        try:
            r = requests.get(f'https://api.binance.com/api/v3/ticker/price',
                params={'symbol': f'{s}USDT'}, proxies=PROXY, timeout=10)
            bn[s] = float(r.json()['price'])
        except:
            bn[s] = None
    result['Binance'] = bn

    # OKX
    okx = {}
    for s in ['BTC', 'ETH', 'AVAX', 'ADA']:
        try:
            r = requests.get('https://www.okx.com/api/v5/market/ticker',
                params={'instId': f'{s}-USDT'}, proxies=PROXY, timeout=10)
            okx[s] = float(r.json()['data'][0]['last'])
        except:
            okx[s] = None
    result['OKX'] = okx

    # Bybit
    by = {}
    for s in ['BTC', 'ETH', 'AVAX', 'ADA']:
        try:
            r = requests.get('https://api.bybit.com/v5/market/tickers',
                params={'category': 'spot', 'symbol': f'{s}USDT'}, proxies=PROXY, timeout=10)
            by[s] = float(r.json()['result']['list'][0]['lastPrice'])
        except:
            by[s] = None
    result['Bybit'] = by

    return result


if __name__ == '__main__':
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 价格服务启动，每30秒更新一次")
    while True:
        try:
            prices = fetch_all()
            data = {
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'),
                'platforms': prices
            }
            with open(OUT, 'w') as f:
                json.dump(data, f, ensure_ascii=False)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] OK: BTC=${prices['Binance']['BTC']:,.2f} | OKX=${prices['OKX'].get('BTC','?'):,.2f} | BY=${prices['Bybit'].get('BTC','?'):,.2f}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 错误: {e}")
        time.sleep(30)
