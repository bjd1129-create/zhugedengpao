#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期货数据抓取脚本 v2.0 - 扩展数据源（简化测试版）
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

# 核心品种（优先）
CORE_FUTURES = {
    "ES=F": {"name": "ES", "desc": "标普 500"},
    "NQ=F": {"name": "NQ", "desc": "纳斯达克 100"},
    "CL=F": {"name": "CL", "desc": "WTI 原油"},
    "GC=F": {"name": "GC", "desc": "黄金"},
    "SI=F": {"name": "SI", "desc": "白银"},
}

CORE_CRYPTO = {
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
}

def get_timestamp():
    return datetime.now().astimezone().isoformat()

def fetch_yahoo(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=60d"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, proxies=PROXY, timeout=10)
        
        if response.status_code == 429:
            return {"error": "限流"}
        
        data = response.json()
        result = data["chart"]["result"][0]
        quotes = result["indicators"]["quote"][0]
        closes = [c for c in quotes.get("close", []) if c is not None]
        
        if len(closes) < 2:
            return None
        
        current = closes[-1]
        previous = closes[-2]
        change_pct = ((current - previous) / previous) * 100
        
        return {
            "price": round(current, 2),
            "change_pct": round(change_pct, 2),
            "trend": "上涨" if current > sum(closes[-5:])/5 else "下跌"
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_binance(symbol):
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        data = response.json()
        return float(data["price"])
    except:
        return None

def fetch_binance_24h(symbol):
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/24hr?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        data = response.json()
        return float(data["priceChangePercent"])
    except:
        return None

def fetch_binance_funding(symbol):
    try:
        url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        data = response.json()
        return float(data["lastFundingRate"])
    except:
        return None

def main():
    print(f"[{get_timestamp()}] 开始抓取核心品种数据...")
    
    data = {
        "update_time": get_timestamp(),
        "futures": {},
        "energy": {},
        "metals": {},
        "crypto": {}
    }
    
    # 美股期货
    print("\n=== 美股期货 ===")
    for symbol, info in CORE_FUTURES.items():
        print(f"  抓取 {symbol}...")
        result = fetch_yahoo(symbol)
        if result and "error" not in result:
            if symbol in ["ES=F", "NQ=F"]:
                data["futures"][info["name"]] = result
            elif symbol in ["CL=F"]:
                data["energy"][info["name"]] = result
            elif symbol in ["GC=F", "SI=F"]:
                data["metals"][info["name"]] = result
            print(f"    ✓ {info['name']}: ${result['price']:,} ({result['change_pct']:+.2f}%)")
        else:
            print(f"    ✗ {symbol}: {result}")
        time.sleep(1)
    
    # 加密货币
    print("\n=== 加密货币 ===")
    for symbol, name in CORE_CRYPTO.items():
        print(f"  抓取 {symbol}...")
        price = fetch_binance(symbol)
        change = fetch_binance_24h(symbol)
        funding = fetch_binance_funding(symbol)
        
        if price:
            data["crypto"][name] = {
                "price": price,
                "change_pct": change,
                "funding_rate": funding
            }
            chg_str = f"{change:+.2f}%" if change else "N/A"
            fr_str = f"{funding*100:.4f}%" if funding else "N/A"
            print(f"    ✓ {name}: ${price:,.2f} (24h: {chg_str}, 费率：{fr_str})")
        time.sleep(0.5)
    
    # 保存
    output_file = DATA_DIR / "futures_prices_v2.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ 数据已保存：{output_file}")
    print(f"[{get_timestamp()}] 完成！")

if __name__ == "__main__":
    main()
