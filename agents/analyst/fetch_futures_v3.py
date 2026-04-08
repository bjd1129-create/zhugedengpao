#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期货数据抓取脚本 v3.0 - 全品种覆盖
- 美股指数期货：ES, NQ, YM, RTY
- 能源期货：CL, BZ, NG, HO, RB
- 金属期货：GC, SI, HG, PL, PA
- 农产品期货：ZC, ZW, ZS, KC, SB, CT, CC, OJ
- 外汇期货：6E, 6J, 6B, 6C, 6A
- 加密货币：BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, LINK, MATIC
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

# 完整的期货品种配置
FUTURES_CONFIG = {
    # === 美股指数期货 ===
    "ES=F": {"name": "ES", "category": "indices", "desc": "标普 500 期货"},
    "NQ=F": {"name": "NQ", "category": "indices", "desc": "纳斯达克 100 期货"},
    "YM=F": {"name": "YM", "category": "indices", "desc": "道琼斯 30 期货"},
    "RTY=F": {"name": "RTY", "category": "indices", "desc": "罗素 2000 期货"},
    
    # === 中国股指期货 ===
    "IH2505.FV": {"name": "IH", "category": "cn_indices", "desc": "上证 50 股指期货"},
    "IF2505.FV": {"name": "IF", "category": "cn_indices", "desc": "沪深 300 股指期货"},
    "IC2505.FV": {"name": "IC", "category": "cn_indices", "desc": "中证 500 股指期货"},
    "IM2505.FV": {"name": "IM", "category": "cn_indices", "desc": "中证 1000 股指期货"},
    
    # === 美股现货指数 ===
    "^GSPC": {"name": "SPX", "category": "indices_spot", "desc": "标普 500 现货"},
    "^NDX": {"name": "NDX", "category": "indices_spot", "desc": "纳斯达克 100 现货"},
    "^DJI": {"name": "DJI", "category": "indices_spot", "desc": "道琼斯 30 现货"},
    "^RUT": {"name": "RUT", "category": "indices_spot", "desc": "罗素 2000 现货"},
    "^VIX": {"name": "VIX", "category": "indices_spot", "desc": "恐慌指数"},
    
    # === 科技七巨头 ===
    "AAPL": {"name": "AAPL", "category": "stocks", "desc": "苹果"},
    "MSFT": {"name": "MSFT", "category": "stocks", "desc": "微软"},
    "NVDA": {"name": "NVDA", "category": "stocks", "desc": "英伟达"},
    "GOOGL": {"name": "GOOGL", "category": "stocks", "desc": "谷歌 A"},
    "META": {"name": "META", "category": "stocks", "desc": "Meta"},
    "AMZN": {"name": "AMZN", "category": "stocks", "desc": "亚马逊"},
    "TSLA": {"name": "TSLA", "category": "stocks", "desc": "特斯拉"},
    
    # === 板块 ETF ===
    "XLK": {"name": "XLK", "category": "etfs", "desc": "科技 ETF"},
    "XLE": {"name": "XLE", "category": "etfs", "desc": "能源 ETF"},
    "XLF": {"name": "XLF", "category": "etfs", "desc": "金融 ETF"},
    "XLV": {"name": "XLV", "category": "etfs", "desc": "医疗 ETF"},
    "XLI": {"name": "XLI", "category": "etfs", "desc": "工业 ETF"},
    "XLP": {"name": "XLP", "category": "etfs", "desc": "消费 ETF"},
    "SOXX": {"name": "SOXX", "category": "etfs", "desc": "半导体 ETF"},
    
    # === 能源期货 ===
    "CL=F": {"name": "CL", "category": "energy", "desc": "WTI 原油"},
    "BZ=F": {"name": "BZ", "category": "energy", "desc": "布伦特原油"},
    "NG=F": {"name": "NG", "category": "energy", "desc": "天然气"},
    "HO=F": {"name": "HO", "category": "energy", "desc": "取暖油"},
    "RB=F": {"name": "RB", "category": "energy", "desc": "汽油"},
    
    # === 金属期货 ===
    "GC=F": {"name": "GC", "category": "metals", "desc": "黄金"},
    "SI=F": {"name": "SI", "category": "metals", "desc": "白银"},
    "HG=F": {"name": "HG", "category": "metals", "desc": "铜"},
    "PL=F": {"name": "PL", "category": "metals", "desc": "铂金"},
    "PA=F": {"name": "PA", "category": "metals", "desc": "钯金"},
    
    # === 农产品期货 ===
    "ZC=F": {"name": "ZC", "category": "agriculture", "desc": "玉米"},
    "ZW=F": {"name": "ZW", "category": "agriculture", "desc": "小麦"},
    "ZS=F": {"name": "ZS", "category": "agriculture", "desc": "大豆"},
    "ZM=F": {"name": "ZM", "category": "agriculture", "desc": "豆粕"},
    "ZL=F": {"name": "ZL", "category": "agriculture", "desc": "豆油"},
    "KC=F": {"name": "KC", "category": "agriculture", "desc": "咖啡"},
    "SB=F": {"name": "SB", "category": "agriculture", "desc": "糖"},
    "CT=F": {"name": "CT", "category": "agriculture", "desc": "棉花"},
    "CC=F": {"name": "CC", "category": "agriculture", "desc": "可可"},
    "OJ=F": {"name": "OJ", "category": "agriculture", "desc": "橙汁"},
    "LE=F": {"name": "LE", "category": "agriculture", "desc": "活牛"},
    "GF=F": {"name": "GF", "category": "agriculture", "desc": "饲牛"},
    
    # === 外汇期货 ===
    "6E=F": {"name": "6E", "category": "forex", "desc": "欧元"},
    "6J=F": {"name": "6J", "category": "forex", "desc": "日元"},
    "6B=F": {"name": "6B", "category": "forex", "desc": "英镑"},
    "6C=F": {"name": "6C", "category": "forex", "desc": "加元"},
    "6A=F": {"name": "6A", "category": "forex", "desc": "澳元"},
    "6S=F": {"name": "6S", "category": "forex", "desc": "瑞郎"},
}

# 加密货币配置
CRYPTO_CONFIG = {
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
    "BNBUSDT": "BNB",
    "SOLUSDT": "SOL",
    "XRPUSDT": "XRP",
    "ADAUSDT": "ADA",
    "DOGEUSDT": "DOGE",
    "AVAXUSDT": "AVAX",
    "LINKUSDT": "LINK",
    "MATICUSDT": "MATIC",
    "DOTUSDT": "DOT",
    "UNIUSDT": "UNI",
    "LTCUSDT": "LTC",
    "ATOMUSDT": "ATOM",
    "ETCUSDT": "ETC",
}

def get_timestamp():
    return datetime.now().astimezone().isoformat()

def fetch_yahoo(symbol, retry=3):
    """从 Yahoo Finance 获取数据，带重试机制"""
    for attempt in range(retry):
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=60d"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json",
            }
            
            # 第一次不用代理，失败后用代理
            if attempt == 0:
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.get(url, headers=headers, proxies=PROXY, timeout=10)
            
            # 检查限流
            if response.status_code == 429 or "Too Many Requests" in response.text:
                if attempt < retry - 1:
                    print(f"    ⏳ 限流，等待 3 秒... ({attempt+1}/{retry})")
                    time.sleep(3)
                    continue
                else:
                    return {"error": "限流"}
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get("chart", {}).get("result"):
                return {"error": "无数据"}
            
            result = data["chart"]["result"][0]
            quotes = result["indicators"]["quote"][0]
            
            # 提取数据（过滤 None）
            closes = [c for c in quotes.get("close", []) if c is not None]
            volumes = [v for v in quotes.get("volume", []) if v is not None]
            
            if len(closes) < 2:
                return {"error": "数据不足"}
            
            current = closes[-1]
            previous = closes[-2]
            change_pct = ((current - previous) / previous) * 100
            volume = volumes[-1] if volumes else 0
            
            # 计算趋势
            ma5 = sum(closes[-5:]) / 5 if len(closes) >= 5 else current
            trend = "上涨" if current > ma5 else "下跌" if current < ma5 else "横盘"
            
            return {
                "price": round(current, 2),
                "change_pct": round(change_pct, 2),
                "volume": volume,
                "trend": trend,
                "raw_quotes": closes[-50:] if len(closes) >= 50 else closes
            }
            
        except Exception as e:
            if attempt < retry - 1:
                time.sleep(1)
            else:
                return {"error": str(e)}
    
    return None

def fetch_binance_price(symbol):
    """获取加密货币价格"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        return float(response.json()["price"])
    except:
        return None

def fetch_binance_24h(symbol):
    """获取 24h 涨跌幅"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/ticker/24hr?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        return float(response.json()["priceChangePercent"])
    except:
        return None

def fetch_binance_funding(symbol):
    """获取资金费率"""
    try:
        url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
        response = requests.get(url, proxies=PROXY, timeout=5)
        response.raise_for_status()
        return float(response.json()["lastFundingRate"])
    except:
        return None

def calculate_rsi(prices, period=14):
    """计算 RSI"""
    if len(prices) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        gains.append(max(0, diff))
        losses.append(max(0, -diff))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    return round(100 - (100 / (1 + avg_gain/avg_loss)), 2)

def calculate_trend(prices):
    """趋势判断"""
    if len(prices) < 20:
        return "未知"
    ma20 = sum(prices[-20:]) / 20
    ma50 = sum(prices[-50:]) / 50 if len(prices) >= 50 else ma20
    current = prices[-1]
    if current > ma20 > ma50:
        return "上涨"
    elif current < ma20 < ma50:
        return "下跌"
    else:
        return "横盘"

def main():
    print(f"[{get_timestamp()}] 开始抓取全品种期货数据 (v3.0)...")
    print(f"  期货品种：{len(FUTURES_CONFIG)} 个")
    print(f"  加密货币：{len(CRYPTO_CONFIG)} 个")
    
    # 抓取中国股指期货（独立模块）
    try:
        from fetch_cn_indices_v2 import fetch_cn_indices_sina
        print("\n=== 中国股指期货 ===")
        cn_data = fetch_cn_indices_sina()
    except Exception as e:
        print(f"  中国股指期货抓取失败：{e}")
        cn_data = {}
    
    # 初始化数据结构
    data = {
        "update_time": get_timestamp(),
        "indices": {},
        "indices_spot": {},
        "cn_indices": {},
        "stocks": {},
        "etfs": {},
        "energy": {},
        "metals": {},
        "agriculture": {},
        "forex": {},
        "crypto": {}
    }
    
    indicators = {
        "update_time": get_timestamp(),
        "indicators": {}
    }
    
    # === 1. 抓取期货 ===
    print("\n=== 期货数据 ===")
    total = len(FUTURES_CONFIG)
    
    for i, (symbol, info) in enumerate(FUTURES_CONFIG.items()):
        print(f"  [{i+1}/{total}] {info['category']:12} {symbol:8} ({info['desc']})...", end=" ")
        
        result = fetch_yahoo(symbol)
        
        if result and "error" not in result:
            data[info["category"]][info["name"]] = {
                "price": result["price"],
                "change_pct": result["change_pct"],
                "volume": result["volume"],
                "trend": result["trend"],
                "desc": info["desc"]
            }
            
            # 计算技术指标
            raw = result.get("raw_quotes", [])
            rsi = calculate_rsi(raw) if len(raw) >= 14 else None
            trend = calculate_trend(raw) if len(raw) >= 20 else result["trend"]
            
            indicators["indicators"][info["name"]] = {
                "rsi_14": rsi,
                "trend": trend,
                "ma_20": round(sum(raw[-20:])/20, 2) if len(raw) >= 20 else None,
                "ma_50": round(sum(raw[-50:])/50, 2) if len(raw) >= 50 else None
            }
            
            # 打印结果
            chg_str = f"{result['change_pct']:+.2f}%"
            if result['change_pct'] > 3:
                chg_str = "📈 " + chg_str
            elif result['change_pct'] < -3:
                chg_str = "📉 " + chg_str
            print(f"${result['price']:>12,} {chg_str:>10} {result['trend']}")
        else:
            error_msg = result.get("error", "未知错误") if result else "未知错误"
            print(f"✗ {error_msg}")
        
        # 请求间隔，避免限流
        if i < total - 1:
            time.sleep(1.2)
    
    # === 2. 抓取加密货币 ===
    print("\n=== 加密货币 ===")
    for symbol, name in CRYPTO_CONFIG.items():
        print(f"  {symbol:12} ({name})...", end=" ")
        
        price = fetch_binance_price(symbol)
        change = fetch_binance_24h(symbol)
        funding = fetch_binance_funding(symbol)
        
        if price:
            data["crypto"][name] = {
                "price": price,
                "change_pct": change,
                "funding_rate": funding,
                "desc": name
            }
            
            chg_str = f"{change:+.2f}%" if change else "N/A"
            fr_str = f"{funding*100:.4f}%" if funding else "N/A"
            print(f"${price:>12,.2f} 24h:{chg_str:>8} 费率:{fr_str}")
        else:
            print("✗ 失败")
        
        time.sleep(0.3)
    
    # === 3. 添加中国股指期货数据 ===
    if cn_data:
        data["cn_indices"] = cn_data
        print(f"\n✓ 中国股指期货已添加：{len(cn_data)} 个品种")
    
    # === 4. 保存数据 ===
    prices_file = DATA_DIR / "futures_prices_v3.json"
    indicators_file = DATA_DIR / "technical_indicators_v3.json"
    
    with open(prices_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    with open(indicators_file, "w", encoding="utf-8") as f:
        json.dump(indicators, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ 数据已保存:")
    print(f"  - {prices_file}")
    print(f"  - {indicators_file}")
    
    # === 4. 打印摘要 ===
    print("\n" + "="*60)
    print("数据摘要")
    print("="*60)
    
    for category in ["indices", "indices_spot", "stocks", "etfs", "energy", "metals", "agriculture", "forex"]:
        if data[category]:
            cat_name = category.replace("_", " ").upper()
            print(f"\n【{cat_name}】")
            for name, d in data[category].items():
                chg = f"{d['change_pct']:+.2f}%"
                if d['change_pct'] > 3:
                    chg = "📈 " + chg
                elif d['change_pct'] < -3:
                    chg = "📉 " + chg
                print(f"  {name:8} ${d['price']:>12,} {chg:>10}")
    
    if data["crypto"]:
        print(f"\n【CRYPTO】")
        for name, d in data["crypto"].items():
            chg = f"{d['change_pct']:+.2f}%" if d['change_pct'] else "N/A"
            fr = f"{d['funding_rate']*100:.4f}%" if d['funding_rate'] else "N/A"
            print(f"  {name:6} ${d['price']:>12,.2f} 24h:{chg:>8} 费率:{fr}")
    
    # === 5. 打印摘要 ===
    print(f"\n[{get_timestamp()}] 完成！共抓取 {sum(len(v) for v in data.values())} 个品种")
    
    # 打印中国股指期货摘要
    if data.get("cn_indices"):
        print("\n【中国股指期货】")
        for name, d in data["cn_indices"].items():
            chg = f"{d['change_pct']:+.2f}%"
            print(f"  {name:6} ¥{d['price']:>10,.1f} {chg:>10} ({d['contract']})")

if __name__ == "__main__":
    main()
