#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股指期货数据抓取脚本 - 从东方财富获取数据
每 5 分钟更新一次
"""

import json
import urllib.request
import urllib.error
import ssl
from datetime import datetime
from pathlib import Path

# 东方财富期货数据 API (使用 push2 接口)
EASTMONEY_API = "http://push2.eastmoney.com/api/qt/stock/get"

# 股指期货代码映射
FUTURE_CODES = {
    "IFM0": "沪深 300 当月连续",
    "IHM0": "上证 50 当月连续",
    "ICM0": "中证 500 当月连续",
    "IMM0": "中证 1000 当月连续",
}

# 异常检测阈值
ANOMALY_THRESHOLD = 3.0

def fetch_futures_data():
    """从东方财富获取股指期货数据"""
    futures_data = []
    
    # 使用东方财富的证券代码
    code_mapping = {
        "IFM0": "1.000300",  # 沪深 300 指数
        "IHM0": "1.000016",  # 上证 50 指数
        "ICM0": "1.000905",  # 中证 500 指数
        "IMM0": "1.000852",  # 中证 1000 指数
    }
    
    # 创建 SSL 上下文 (忽略证书验证)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    for code, name in FUTURE_CODES.items():
        try:
            secid = code_mapping.get(code, "")
            # 使用测试成功的 API 参数
            url = f"{EASTMONEY_API}?secid={secid}&fields=f43,f57,f169,f170,f46,f47,f48,f44,f49,f50,f51,f52"
            
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Referer": "http://quote.eastmoney.com/"
                }
            )
            
            # 尝试 HTTP (东方财富 API 支持 HTTP)
            try:
                with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                    data = json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 502:
                    # 502 错误，稍后重试
                    import time
                    time.sleep(1)
                    with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                        data = json.loads(response.read().decode("utf-8"))
                else:
                    raise
            
            if data.get("data"):
                fd = data["data"]
                price = fd.get("f43", 0) / 100 if fd.get("f43") else 0
                change = fd.get("f169", 0) / 100 if fd.get("f169") else 0
                change_pct = fd.get("f170", 0) / 100 if fd.get("f170") else 0
                
                futures_data.append({
                    "code": code,
                    "name": name,
                    "price": round(price, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                    "open": round(fd.get("f46", 0) / 100, 2) if fd.get("f46") else 0,
                    "high": 0,  # API 不返回 high
                    "low": 0,   # API 不返回 low
                    "prev_settle": round(fd.get("f44", 0) / 100, 2) if fd.get("f44") else 0,
                    "volume": str(fd.get("f49", "0")),
                    "open_interest": 0,
                    "basis": 0.0,
                    "basis_rate": 0.0
                })
                print(f"✓ 获取 {code} 成功：{price:.2f} ({change_pct:+.2f}%)")
                    
        except Exception as e:
            print(f"✗ 获取 {code} 数据失败：{e}")
    
    return futures_data

def fetch_alternative():
    """备用方案：尝试其他 API"""
    futures_data = []
    
    # 尝试新浪财经 API
    sina_codes = {
        "IFM0": "IF0000",
        "IHM0": "IH0000", 
        "ICM0": "IC0000",
        "IMM0": "IM0000",
    }
    
    for code, sina_code in sina_codes.items():
        try:
            url = f"http://hq.sinajs.cn/rn={int(datetime.now().timestamp()*1000)}&list=f_{sina_code}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                text = response.read().decode("gbk")
                # 解析格式：var hq_str_f_IF0000="名称，当前价，...，昨收，..."
                if '"' in text:
                    parts = text.split('"')[1].split(',')
                    if len(parts) >= 2:
                        name = parts[0]
                        price = float(parts[1]) if parts[1] else 0
                        prev_close = float(parts[2]) if len(parts) > 2 and parts[2] else 0
                        change_pct = ((price - prev_close) / prev_close * 100) if prev_close > 0 else 0
                        
                        futures_data.append({
                            "code": code,
                            "name": FUTURE_CODES.get(code, name),
                            "price": round(price, 2),
                            "change": round(price - prev_close, 2),
                            "change_pct": round(change_pct, 2),
                            "open": 0,
                            "high": 0,
                            "low": 0,
                            "prev_settle": round(prev_close, 2),
                            "volume": "0",
                            "open_interest": 0,
                            "basis": 0.0,
                            "basis_rate": 0.0
                        })
                        print(f"✓ 获取 {code} 成功 (新浪): {price:.2f}")
        except Exception as e:
            print(f"✗ 新浪 API 获取 {code} 失败：{e}")
    
    return futures_data

def detect_anomalies(current_data, previous_data):
    """检测异常波动"""
    anomalies = []
    
    for future in current_data:
        code = future["code"]
        change_pct = abs(future["change_pct"])
        
        if change_pct > ANOMALY_THRESHOLD:
            severity = "HIGH" if change_pct > 5.0 else "MEDIUM"
            anomalies.append({
                "code": code,
                "name": future["name"],
                "price": future["price"],
                "change_pct": future["change_pct"],
                "severity": severity,
                "message": f"{future['name']} 涨跌幅 {future['change_pct']:+.2f}% 超过阈值 {ANOMALY_THRESHOLD}%"
            })
        
        if previous_data:
            prev_future = next((f for f in previous_data if f["code"] == code), None)
            if prev_future and prev_future["price"] > 0:
                price_change = abs(future["price"] - prev_future["price"]) / prev_future["price"] * 100
                if price_change > 2.0:
                    if not any(a["code"] == code for a in anomalies):
                        anomalies.append({
                            "code": code,
                            "name": future["name"],
                            "price": future["price"],
                            "change_pct": round(price_change, 2),
                            "severity": "MEDIUM",
                            "message": f"{future['name']} 5 分钟内价格波动 {price_change:.2f}%"
                        })
    
    return anomalies

def main():
    data_dir = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/data")
    data_file = data_dir / "china_futures.json"
    
    # 读取历史数据
    previous_data = None
    if data_file.exists():
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                old_data = json.load(f)
                previous_data = old_data.get("futures", [])
                print(f"读取历史数据成功，时间：{old_data.get('timestamp', '未知')}")
        except Exception as e:
            print(f"读取历史数据失败：{e}")
    
    # 获取新数据
    print("\n正在获取股指期货数据...")
    futures_data = fetch_futures_data()
    
    if not futures_data:
        print("\n东方财富 API 失败，尝试新浪财经备用方案...")
        futures_data = fetch_alternative()
    
    if not futures_data:
        print("\n⚠️  所有数据源获取失败，保持原有数据")
        return
    
    # 检测异常
    anomalies = detect_anomalies(futures_data, previous_data)
    
    # 构建输出数据
    output = {
        "timestamp": datetime.now().isoformat(),
        "source": "东方财富" if len(futures_data) >= 2 else "新浪财经",
        "futures": futures_data,
        "anomalies": anomalies,
        "summary": {
            "IF_monthly": next((f["price"] for f in futures_data if f["code"] == "IFM0"), 0),
            "IC_monthly": next((f["price"] for f in futures_data if f["code"] == "ICM0"), 0),
            "IM_monthly": next((f["price"] for f in futures_data if f["code"] == "IMM0"), 0),
            "IH_monthly": next((f["price"] for f in futures_data if f["code"] == "IHM0"), 0),
            "max_change_pct": max((abs(f["change_pct"]) for f in futures_data), default=0),
            "anomaly_count": len(anomalies)
        }
    }
    
    # 保存数据
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据更新成功：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"更新合约数：{len(futures_data)}")
    print(f"异常检测：{len(anomalies)} 个")
    
    if anomalies:
        print("\n⚠️  异常波动提醒:")
        for a in anomalies:
            print(f"  - {a['name']}: {a['message']}")
    
    print("\n📊 股指期货快照:")
    for f in futures_data:
        print(f"  {f['name']}: {f['price']:.2f} ({f['change_pct']:+.2f}%)")

if __name__ == "__main__":
    main()
