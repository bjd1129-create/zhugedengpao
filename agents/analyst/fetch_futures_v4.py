#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期货数据源 v4.0 - 多数据源整合
- 主数据源：Yahoo Finance + Binance
- 补充数据源：CoinPaprika（加密货币）、Twelve Data、Alpha Vantage
- 目标：覆盖更多品种，提高数据可靠性
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

# === 数据源配置 ===
DATA_SOURCES = {
    "yahoo": {
        "name": "Yahoo Finance",
        "base_url": "https://query1.finance.yahoo.com/v8/finance/chart",
        "proxy": True,
        "rate_limit": "5 次/分钟",
        "coverage": ["美股期货", "能源", "金属", "农产品", "外汇"]
    },
    "binance": {
        "name": "Binance",
        "base_url": "https://fapi.binance.com/fapi/v1",
        "proxy": True,
        "rate_limit": "IP 限流",
        "coverage": ["加密货币期货"]
    },
    "coinpaprika": {
        "name": "CoinPaprika",
        "base_url": "https://api.coinpaprika.com/v1",
        "proxy": False,
        "rate_limit": "免费",
        "coverage": ["加密货币现货"]
    },
    "coingecko": {
        "name": "CoinGecko",
        "base_url": "https://api.coingecko.com/api/v3",
        "proxy": False,
        "rate_limit": "10-50 次/分钟",
        "coverage": ["加密货币现货"]
    }
}

# === 新增品种配置 ===
ADDITIONAL_FUTURES = {
    # 欧洲指数
    "DAX=F": {"name": "DAX", "category": "indices", "desc": "德国 DAX"},
    "UKX=F": {"name": "UKX", "category": "indices", "desc": "英国富时 100"},
    "CAC=F": {"name": "CAC", "category": "indices", "desc": "法国 CAC40"},
    "NKX=F": {"name": "NKX", "category": "indices", "desc": "日经 225"},
    "HSI=F": {"name": "HSI", "category": "indices", "desc": "恒生指数"},
    
    # 中国商品期货（通过 Yahoo）
    "AU=F": {"name": "AU", "category": "metals", "desc": "沪金"},
    "AG=F": {"name": "AG", "category": "metals", "desc": "沪银"},
    "CU=F": {"name": "CU", "category": "metals", "desc": "沪铜"},
    "AL=F": {"name": "AL", "category": "metals", "desc": "沪铝"},
    
    # 更多商品
    "LBS=F": {"name": "LBS", "category": "materials", "desc": "木材"},
    "ZR=F": {"name": "ZR", "category": "agriculture", "desc": "稻米"},
    "MW=F": {"name": "MW", "category": "agriculture", "desc": "小麦（明尼阿波利斯）"},
}

# 加密货币补充数据源
CRYPTO_ALTERNATIVES = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "cardano": "ADA",
    "ripple": "XRP",
    "dogecoin": "DOGE",
    "avalanche": "AVAX",
    "chainlink": "LINK",
    "polkadot": "DOT",
    "uniswap": "UNI",
    "litecoin": "LTC",
    "cosmos": "ATOM",
    "ethereum-classic": "ETC",
    "polygon": "MATIC",
    "binance-coin": "BNB",
}

def get_timestamp():
    return datetime.now().astimezone().isoformat()

def fetch_yahoo(symbol, retry=3):
    """Yahoo Finance 数据抓取"""
    for attempt in range(retry):
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=60d"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
            }
            
            if attempt == 0:
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.get(url, headers=headers, proxies=PROXY, timeout=10)
            
            if response.status_code == 429:
                if attempt < retry - 1:
                    time.sleep(3)
                    continue
                return {"error": "限流"}
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get("chart", {}).get("result"):
                return {"error": "无数据"}
            
            result = data["chart"]["result"][0]
            quotes = result["indicators"]["quote"][0]
            closes = [c for c in quotes.get("close", []) if c is not None]
            
            if len(closes) < 2:
                return {"error": "数据不足"}
            
            current = closes[-1]
            previous = closes[-2]
            change_pct = ((current - previous) / previous) * 100
            
            return {
                "price": round(current, 2),
                "change_pct": round(change_pct, 2),
                "raw_quotes": closes[-50:]
            }
            
        except Exception as e:
            if attempt < retry - 1:
                time.sleep(1)
            else:
                return {"error": str(e)}
    return None

def fetch_coinpaprika(coin_id):
    """CoinPaprika 加密货币数据"""
    try:
        url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        quotes = data.get("quotes", {})
        return {
            "price": quotes.get("USD", {}).get("price"),
            "volume_24h": quotes.get("USD", {}).get("volume_24h"),
            "market_cap": quotes.get("USD", {}).get("market_cap"),
            "change_24h": data.get("quotes", {}).get("USD", {}).get("percent_change_24h")
        }
    except Exception as e:
        return None

def fetch_coingecko(ids):
    """CoinGecko 批量加密货币数据"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(ids),
            "vs_currencies": "usd",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_market_cap": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  CoinGecko 错误：{e}")
        return None

def fetch_binance_futures(symbol):
    """Binance 期货数据"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except:
        return None

def fetch_binance_funding(symbol):
    """Binance 资金费率"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        return float(response.json()["lastFundingRate"])
    except:
        return None

def main():
    print(f"[{get_timestamp()}] 开始抓取多数据源期货数据 (v4.0)...")
    
    # 加载 v3 数据作为基础
    v3_file = DATA_DIR / "futures_prices_v3.json"
    if v3_file.exists():
        with open(v3_file, "r", encoding="utf-8") as f:
            base_data = json.load(f)
        print(f"  ✓ 已加载 v3 数据作为基础")
    else:
        base_data = {
            "update_time": get_timestamp(),
            "indices": {}, "energy": {}, "metals": {},
            "agriculture": {}, "forex": {}, "crypto": {}
        }
    
    # === 1. 添加新期货品种 ===
    print("\n=== 新增期货品种 ===")
    for symbol, info in ADDITIONAL_FUTURES.items():
        print(f"  {info['category']:12} {symbol:8} ({info['desc']})...", end=" ")
        
        result = fetch_yahoo(symbol)
        
        if result and "error" not in result:
            if info["category"] not in base_data:
                base_data[info["category"]] = {}
            
            base_data[info["category"]][info["name"]] = {
                "price": result["price"],
                "change_pct": result["change_pct"],
                "desc": info["desc"],
                "source": "yahoo"
            }
            print(f"${result['price']:>12,} ({result['change_pct']:+.2f}%)")
        else:
            error = result.get("error", "失败") if result else "失败"
            print(f"✗ {error}")
        
        time.sleep(1.2)
    
    # === 2. 补充加密货币数据（多数据源对比）===
    print("\n=== 补充加密货币数据 ===")
    print("  数据源：CoinGecko（批量）...")
    
    coingecko_data = fetch_coingecko(list(CRYPTO_ALTERNATIVES.keys()))
    
    if coingecko_data:
        for cg_id, name in CRYPTO_ALTERNATIVES.items():
            if cg_id in coingecko_data:
                data = coingecko_data[cg_id]
                if name in base_data.get("crypto", {}):
                    # 更新现有数据，添加数据源对比
                    base_data["crypto"][name]["coingecko_price"] = data.get("usd")
                    base_data["crypto"][name]["coingecko_vol"] = data.get("usd_24h_vol")
                    base_data["crypto"][name]["coingecko_change"] = data.get("usd_24h_change")
                    print(f"  ✓ {name}: Binance ${base_data['crypto'][name].get('price', 0):,.2f} vs CoinGecko ${data.get('usd', 0):,.2f}")
    
    # === 3. 数据源统计 ===
    print("\n=== 数据源统计 ===")
    source_stats = {}
    for category in ["indices", "energy", "metals", "agriculture", "forex", "crypto", "materials"]:
        for name, data in base_data.get(category, {}).items():
            source = data.get("source", "unknown")
            source_stats[source] = source_stats.get(source, 0) + 1
    
    for source, count in source_stats.items():
        print(f"  {source}: {count} 个品种")
    
    # === 4. 保存数据 ===
    output_file = DATA_DIR / "futures_prices_v4.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(base_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ 数据已保存：{output_file}")
    print(f"[{get_timestamp()}] 完成！")

if __name__ == "__main__":
    main()
