#!/usr/bin/env python3
"""
Multi-Platform Grid Trading Simulator
Binance + OKX + Bybit 并行运行
策略：v4.1 密集网格
"""
import requests, json, os, time
from datetime import datetime

PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or None

PLATFORMS = {
    'Binance': {
        'price_url': 'https://api.binance.com/api/v3/ticker/price',
        'symbols': {'BTC': 'BTCUSDT', 'ETH': 'ETHUSDT', 'AVAX': 'AVAXUSDT', 'ADA': 'ADAUSDT'},
        'note': '最成熟'
    },
    'OKX': {
        'price_url': 'https://www.okx.com/api/v5/market/ticker',
        'symbols': {'BTC': 'BTC-USDT', 'ETH': 'ETH-USDT', 'AVAX': 'AVAX-USDT', 'ADA': 'ADA-USDT'},
        'note': '费率低'
    },
    'Bybit': {
        'price_url': 'https://api-testnet.bybit.com/v5/market/tickers',
        'symbols': {'BTC': 'BTCUSDT', 'ETH': 'ETHUSDT', 'AVAX': 'AVAXUSDT', 'ADA': 'ADAUSDT'},
        'category': 'spot',
        'note': '永续合约强'
    }
}


def get_price_binance(symbol):
    try:
        r = requests.get('https://api.binance.com/api/v3/ticker/price',
            params={'symbol': symbol}, proxies={'https': PROXY} if PROXY else {}, timeout=10)
        return float(r.json()['price']) if r.status_code == 200 else None
    except: return None

def get_price_okx(symbol):
    try:
        r = requests.get('https://www.okx.com/api/v5/market/ticker',
            params={'instId': symbol}, proxies={'https': PROXY} if PROXY else {}, timeout=10)
        d = r.json().get('data', [{}])[0]
        return float(d.get('last', 0)) if d.get('last') else None
    except: return None

def get_price_bybit(symbol, category='spot'):
    try:
        r = requests.get('https://api-testnet.bybit.com/v5/market/tickers',
            params={'category': category, 'symbol': symbol}, proxies={'https': PROXY} if PROXY else {}, timeout=10)
        d = r.json().get('list', [{}])[0]
        return float(d.get('lastPrice', 0)) if d.get('lastPrice') else None
    except: return None


def run_platform(platform, config, initial=10000):
    """运行单个平台，返回结果"""
    prices = {}
    for sym_key, api_sym in config['symbols'].items():
        if platform == 'Binance':
            p = get_price_binance(api_sym)
        elif platform == 'OKX':
            p = get_price_okx(api_sym)
        elif platform == 'Bybit':
            p = get_price_bybit(api_sym)
        prices[sym_key] = p
    
    return {
        'platform': platform,
        'prices': prices,
        'note': config['note'],
        'timestamp': datetime.now().strftime('%H:%M')
    }


def main():
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"\n[🕐 {ts}] ═══ 三平台实时价格对比 ═══")
    
    results = []
    for platform, config in PLATFORMS.items():
        r = run_platform(platform, config)
        results.append(r)
        price_strs = [f"{k}: ${v:,.2f}" if v else f"{k}: ❌" for k, v in r['prices'].items()]
        print(f"  [{platform}] {' | '.join(price_strs)}")
    
    # Save latest comparison
    save_path = os.path.expanduser('~/Desktop/ZhugeDengpao-Team/data/trading/multi_platform.json')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w') as f:
        json.dump({'timestamp': ts, 'results': results}, f, indent=2)
    
    print(f"\n  ✅ 已保存到 multi_platform.json")


if __name__ == '__main__':
    main()
