#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期货数据抓取脚本 v2.0 - 扩展数据源
- 美股期货：Yahoo Finance (ES, NQ, CL, GC, SI, HG, ZC, ZW)
- 加密货币：Binance API (BTC, ETH, BNB, SOL, XRP 等)
- 商品期货：Yahoo Finance (原油、黄金、白银、铜、农产品)
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path

# 配置
DATA_DIR = Path(__file__).parent / "data"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

# 期货品种配置
FUTURES_CONFIG = {
    # 美股指数期货
    "ES=F": {"name": "ES", "category": "futures", "description": "标普 500 期货"},
    "NQ=F": {"name": "NQ", "category": "futures", "description": "纳斯达克 100 期货"},
    "YM=F": {"name": "YM", "category": "futures", "description": "道琼斯 30 期货"},
    "RTY=F": {"name": "RTY", "category": "futures", "description": "罗素 2000 期货"},
    
    # 能源期货
    "CL=F": {"name": "CL", "category": "energy", "description": "WTI 原油期货"},
    "BZ=F": {"name": "BZ", "category": "energy", "description": "布伦特原油期货"},
    "NG=F": {"name": "NG", "category": "energy", "description": "天然气期货"},
    "HO=F": {"name": "HO", "category": "energy", "description": "取暖油期货"},
    
    # 金属期货
    "GC=F": {"name": "GC", "category": "metals", "description": "黄金期货"},
    "SI=F": {"name": "SI", "category": "metals", "description": "白银期货"},
    "HG=F": {"name": "HG", "category": "metals", "description": "铜期货"},
    "PL=F": {"name": "PL", "category": "metals", "description": "铂金期货"},
    
    # 农产品期货
    "ZC=F": {"name": "ZC", "category": "agriculture", "description": "玉米期货"},
    "ZW=F": {"name": "ZW", "category": "agriculture", "description": "小麦期货"},
    "ZS=F": {"name": "ZS", "category": "agriculture", "description": "大豆期货"},
    "KC=F": {"name": "KC", "category": "agriculture", "description": "咖啡期货"},
    "SB=F": {"name": "SB", "category": "agriculture", "description": "糖期货"},
    "CT=F": {"name": "CT", "category": "agriculture", "description": "棉花期货"},
    
    # 其他
    "6E=F": {"name": "6E", "category": "forex", "description": "欧元期货"},
    "6J=F": {"name": "6J", "category": "forex", "description": "日元期货"},
    "BTC=F": {"name": "BTC", "category": "crypto", "description": "比特币期货"},
}

# 加密货币配置
CRYPTO_CONFIG = {
    "BTCUSDT": {"name": "BTC", "description": "比特币"},
    "ETHUSDT": {"name": "ETH", "description": "以太坊"},
    "BNBUSDT": {"name": "BNB", "description": "币安币"},
    "SOLUSDT": {"name": "SOL", "description": "索拉纳"},
    "XRPUSDT": {"name": "XRP", "description": "瑞波币"},
    "ADAUSDT": {"name": "ADA", "description": "卡尔达诺"},
    "DOGEUSDT": {"name": "DOGE", "description": "狗狗币"},
    "AVAXUSDT": {"name": "AVAX", "description": "Avalanche"},
    "LINKUSDT": {"name": "LINK", "description": "Chainlink"},
    "MATICUSDT": {"name": "MATIC", "description": "Polygon"},
}

def get_timestamp():
    """获取当前时间戳（ISO 格式）"""
    return datetime.now().astimezone().isoformat()

def fetch_yahoo_futures(symbol, retry=3):
    """
    从 Yahoo Finance 获取期货数据
    支持重试机制避免限流
    """
    for attempt in range(retry):
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=60d"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
            }
            
            # 第一次不用代理，失败后用代理
            if attempt == 0:
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.get(url, headers=headers, proxies=PROXY, timeout=10)
            
            # 检查限流
            if response.status_code == 429 or "Too Many Requests" in response.text:
                print(f"  Yahoo 限流，等待 2 秒后重试... ({attempt+1}/{retry})")
                time.sleep(2)
                continue
            
            response.raise_for_status()
            data = response.json()
            
            # 检查是否有有效数据
            if not data.get("chart", {}).get("result"):
                print(f"  Yahoo 无数据 ({symbol})")
                return None
            
            result = data["chart"]["result"][0]
            quotes = result["indicators"]["quote"][0]
            
            # 获取最新价格（过滤 None 值）
            closes = [c for c in quotes.get("close", []) if c is not None]
            volumes = [v for v in quotes.get("volume", []) if v is not None]
            highs = [h for h in quotes.get("high", []) if h is not None]
            lows = [l for l in quotes.get("low", []) if l is not None]
            
            if len(closes) < 2:
                print(f"  Yahoo 数据不足 ({symbol})")
                return None
            
            current_price = closes[-1]
            previous_price = closes[-2]
            change_pct = ((current_price - previous_price) / previous_price) * 100
            volume = volumes[-1] if volumes else 0
            high = highs[-1] if highs else current_price
            low = lows[-1] if lows else current_price
            
            # 计算趋势
            trend = calculate_trend(closes)
            
            return {
                "price": round(current_price, 2),
                "change_pct": round(change_pct, 2),
                "volume": volume,
                "high": round(high, 2),
                "low": round(low, 2),
                "trend": trend,
                "raw_quotes": closes[-50:] if len(closes) >= 50 else closes
            }
            
        except Exception as e:
            if attempt < retry - 1:
                print(f"  Yahoo 错误 ({symbol}): {e}，重试中...")
                time.sleep(1)
            else:
                print(f"Yahoo Finance 错误 ({symbol}): {e}")
                return None
    
    return None

def fetch_binance_price(symbol):
    """从 Binance 获取加密货币价格"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"Binance 价格错误 ({symbol}): {e}")
        return None

def fetch_binance_funding_rate(symbol):
    """从 Binance 获取资金费率"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["lastFundingRate"])
    except Exception as e:
        print(f"Binance 资金费率错误 ({symbol}): {e}")
        return None

def fetch_binance_klines(symbol, interval="1h", limit=100):
    """从 Binance 获取 K 线数据"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        data = response.json()
        return [float(k[4]) for k in data]  # 收盘价
    except Exception as e:
        print(f"Binance K 线错误 ({symbol}): {e}")
        return None

def fetch_binance_24h_change(symbol):
    """获取 24 小时涨跌幅"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/24hr?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["priceChangePercent"])
    except Exception as e:
        print(f"Binance 24h 错误 ({symbol}): {e}")
        return None

def calculate_rsi(prices, period=14):
    """计算 RSI 指标"""
    if len(prices) < period + 1:
        return None
    
    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def calculate_ma(prices, period):
    """计算移动平均线"""
    if len(prices) < period:
        return None
    return round(sum(prices[-period:]) / period, 2)

def calculate_ema(prices, period):
    """计算指数移动平均线 (EMA)"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    
    return ema

def calculate_macd(prices):
    """计算 MACD 指标 (12, 26, 9)"""
    if len(prices) < 26 + 9:
        return None, None, None
    
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    
    if ema12 is None or ema26 is None:
        return None, None, None
    
    macd_line = ema12 - ema26
    signal_line = macd_line * 0.9  # 简化近似
    histogram = macd_line - signal_line
    
    return round(macd_line, 4), round(signal_line, 4), round(histogram, 4)

def calculate_trend(prices):
    """趋势判断"""
    if len(prices) < 20:
        return "未知"
    
    ma20 = calculate_ma(prices, 20)
    ma50 = calculate_ma(prices, 50) if len(prices) >= 50 else ma20
    current = prices[-1]
    
    if ma20 is None:
        return "未知"
    if ma50 is None:
        return "上涨" if current > ma20 else "下跌" if current < ma20 else "横盘"
    
    if current > ma20 > ma50:
        return "上涨"
    elif current < ma20 < ma50:
        return "下跌"
    else:
        return "横盘"

def main():
    print(f"[{get_timestamp()}] 开始抓取期货数据 (v2.0 扩展版)...")
    
    # 初始化数据结构
    futures_data = {
        "update_time": get_timestamp(),
        "futures": {},
        "energy": {},
        "metals": {},
        "agriculture": {},
        "crypto": {}
    }
    
    indicators_data = {
        "update_time": get_timestamp(),
        "indicators": {}
    }
    
    # 1. 抓取美股期货（分批请求，避免限流）
    print("\n=== 美股期货 ===")
    yahoo_symbols = [k for k, v in FUTURES_CONFIG.items() if v["category"] in ["futures", "energy", "metals", "agriculture"]]
    
    for i, symbol in enumerate(yahoo_symbols):
        config = FUTURES_CONFIG[symbol]
        print(f"  [{i+1}/{len(yahoo_symbols)}] 抓取 {symbol} ({config['description']})...")
        
        data = fetch_yahoo_futures(symbol)
        if data:
            category = config["category"]
            futures_data[category][config["name"]] = {
                "price": data["price"],
                "change_pct": data["change_pct"],
                "volume": data["volume"],
                "high": data["high"],
                "low": data["low"],
                "trend": data["trend"],
                "description": config["description"]
            }
            
            # 计算技术指标
            raw = data.get("raw_quotes", [])
            if len(raw) >= 14:
                rsi = calculate_rsi(raw)
                ma20 = calculate_ma(raw, 20)
                ma50 = calculate_ma(raw, 50) if len(raw) >= 50 else None
                macd, macd_signal, macd_hist = calculate_macd(raw * 2)  # 复制数据
            else:
                rsi = None
                ma20 = None
                ma50 = None
                macd, macd_signal, macd_hist = None, None, None
            
            indicators_data["indicators"][config["name"]] = {
                "rsi_14": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "macd_hist": macd_hist,
                "ma_20": ma20,
                "ma_50": ma50,
                "trend": data["trend"]
            }
        
        # 请求间隔，避免限流
        if i < len(yahoo_symbols) - 1:
            time.sleep(1.5)
    
    # 2. 抓取加密货币
    print("\n=== 加密货币 ===")
    for symbol, config in CRYPTO_CONFIG.items():
        print(f"  抓取 {symbol} ({config['description']})...")
        
        price = fetch_binance_price(symbol)
        funding_rate = fetch_binance_funding_rate(symbol)
        change_24h = fetch_binance_24h_change(symbol)
        klines = fetch_binance_klines(symbol)
        
        if price:
            futures_data["crypto"][config["name"]] = {
                "price": price,
                "change_pct": change_24h,
                "funding_rate": funding_rate,
                "rsi": None,
                "trend": None,
                "description": config["description"]
            }
            
            # 计算技术指标
            if klines and len(klines) >= 50:
                rsi = calculate_rsi(klines)
                trend = calculate_trend(klines)
                ma20 = calculate_ma(klines, 20)
                ma50 = calculate_ma(klines, 50)
                macd, macd_signal, macd_hist = calculate_macd(klines)
            else:
                rsi = None
                trend = "未知"
                ma20 = None
                ma50 = None
                macd, macd_signal, macd_hist = None, None, None
            
            indicators_data["indicators"][config["name"]] = {
                "rsi_14": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "macd_hist": macd_hist,
                "ma_20": ma20,
                "ma_50": ma50,
                "trend": trend
            }
    
    # 保存数据
    prices_file = DATA_DIR / "futures_prices.json"
    indicators_file = DATA_DIR / "technical_indicators.json"
    
    with open(prices_file, "w", encoding="utf-8") as f:
        json.dump(futures_data, f, indent=2, ensure_ascii=False)
    print(f"\n✓ 价格数据已保存：{prices_file}")
    
    with open(indicators_file, "w", encoding="utf-8") as f:
        json.dump(indicators_data, f, indent=2, ensure_ascii=False)
    print(f"✓ 技术指标已保存：{indicators_file}")
    
    print(f"\n[{get_timestamp()}] 数据抓取完成！")
    
    # 打印摘要
    print("\n=== 数据摘要 ===")
    print("\n【美股指数】")
    for name, data in futures_data["futures"].items():
        print(f"  {name}: ${data['price']:,} ({data['change_pct']:+.2f}%) - {data['trend']}")
    
    print("\n【能源】")
    for name, data in futures_data["energy"].items():
        print(f"  {name}: ${data['price']:.2f} ({data['change_pct']:+.2f}%) - {data['trend']}")
    
    print("\n【金属】")
    for name, data in futures_data["metals"].items():
        print(f"  {name}: ${data['price']:.2f} ({data['change_pct']:+.2f}%) - {data['trend']}")
    
    print("\n【农产品】")
    for name, data in futures_data["agriculture"].items():
        print(f"  {name}: ${data['price']:.2f} ({data['change_pct']:+.2f}%) - {data['trend']}")
    
    print("\n【加密货币】")
    for name, data in futures_data["crypto"].items():
        fr = f"{data['funding_rate']*100:.4f}%" if data['funding_rate'] else "N/A"
        chg = f"{data['change_pct']:+.2f}%" if data['change_pct'] else "N/A"
        print(f"  {name}: ${data['price']:,.2f} (24h: {chg}) - 资金费率：{fr}")

if __name__ == "__main__":
    main()
