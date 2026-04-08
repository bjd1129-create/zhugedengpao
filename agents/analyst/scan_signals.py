#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常信号扫描脚本
扫描价格波动、成交量异常、资金费率异常、RSI 超买超卖
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"

def load_data():
    """加载最新数据（优先 v3，回退到 v1）"""
    prices_file = DATA_DIR / "futures_prices_v3.json"
    indicators_file = DATA_DIR / "technical_indicators_v3.json"
    
    # 如果 v3 不存在，回退到 v1
    if not prices_file.exists():
        prices_file = DATA_DIR / "futures_prices.json"
    if not indicators_file.exists():
        indicators_file = DATA_DIR / "technical_indicators.json"
    
    with open(prices_file, "r", encoding="utf-8") as f:
        prices = json.load(f)
    
    with open(indicators_file, "r", encoding="utf-8") as f:
        indicators = json.load(f)
    
    return prices, indicators

def scan_signals():
    """扫描异常信号（支持 v3 数据结构）"""
    prices, indicators = load_data()
    signals = []
    
    print(f"[{datetime.now().isoformat()}] 开始扫描异常信号...")
    
    # 扫描所有期货类别（v3 结构）
    categories = ["indices", "energy", "metals", "agriculture", "forex"]
    
    for category in categories:
        for name, data in prices.get(category, {}).items():
            indicator = indicators.get("indicators", {}).get(name, {})
            change_pct = data.get("change_pct")
            
            # 1. 价格大幅波动
            if change_pct and abs(change_pct) > 3:
                direction = "暴涨" if change_pct > 0 else "暴跌"
                severity = "🔴 严重" if abs(change_pct) > 10 else "⚠️ 警告"
                signals.append({
                    "品种": name,
                    "类别": category,
                    "信号类型": f"价格{direction}",
                    "数值": f"{change_pct:+.2f}%",
                    "严重程度": severity,
                    "建议": "关注消息面，谨慎操作"
                })
            
            # 2. RSI 超买超卖
            rsi = indicator.get("rsi_14")
            if rsi:
                if rsi > 70:
                    severity = "🔴 严重" if rsi > 80 else "⚠️ 警告"
                    signals.append({
                        "品种": name,
                        "类别": category,
                        "信号类型": "RSI 超买",
                        "数值": f"RSI={rsi}",
                        "严重程度": severity,
                        "建议": "警惕回调风险，不宜追高"
                    })
                elif rsi < 30:
                    severity = "🔴 严重" if rsi < 20 else "⚠️ 警告"
                    signals.append({
                        "品种": name,
                        "类别": category,
                        "信号类型": "RSI 超卖",
                        "数值": f"RSI={rsi}",
                        "严重程度": severity,
                        "建议": "可能反弹机会，关注买入信号"
                    })
    
    # 扫描加密货币
    for name, data in prices.get("crypto", {}).items():
        indicator = indicators.get("indicators", {}).get(name, {})
        
        # 1. RSI 超买超卖
        rsi = indicator.get("rsi_14")
        if rsi:
            if rsi > 70:
                severity = "🔴 严重" if rsi > 80 else "⚠️ 警告"
                signals.append({
                    "品种": name,
                    "类别": "crypto",
                    "信号类型": "RSI 超买",
                    "数值": f"RSI={rsi}",
                    "严重程度": severity,
                    "建议": "警惕回调风险，不宜追高"
                })
            elif rsi < 30:
                severity = "🔴 严重" if rsi < 20 else "⚠️ 警告"
                signals.append({
                    "品种": name,
                    "类别": "crypto",
                    "信号类型": "RSI 超卖",
                    "数值": f"RSI={rsi}",
                    "严重程度": severity,
                    "建议": "可能反弹机会，关注买入信号"
                })
        
        # 2. 资金费率异常
        funding_rate = data.get("funding_rate")
        if funding_rate:
            fr_pct = funding_rate * 100
            if fr_pct > 0.1:
                signals.append({
                    "品种": name,
                    "类别": "crypto",
                    "信号类型": "资金费率过高",
                    "数值": f"{fr_pct:.4f}%",
                    "严重程度": "⚠️ 警告",
                    "建议": "多头过热，警惕回调"
                })
            elif fr_pct < -0.1:
                signals.append({
                    "品种": name,
                    "类别": "crypto",
                    "信号类型": "资金费率过低",
                    "数值": f"{fr_pct:.4f}%",
                    "严重程度": "⚠️ 警告",
                    "建议": "空头过热，可能反弹"
                })
        
        # 3. 价格大幅波动
        change_pct = data.get("change_pct")
        if change_pct and abs(change_pct) > 5:
            direction = "暴涨" if change_pct > 0 else "暴跌"
            signals.append({
                "品种": name,
                "类别": "crypto",
                "信号类型": f"价格{direction}",
                "数值": f"{change_pct:+.2f}%",
                "严重程度": "🔴 严重" if abs(change_pct) > 10 else "⚠️ 警告",
                "建议": "关注消息面，谨慎操作"
            })
    
    # 打印结果
    if signals:
        print(f"\n发现 {len(signals)} 个信号：\n")
        for sig in signals:
            print(f"{sig['严重程度']} {sig['品种']} - {sig['信号类型']}")
            print(f"  数值：{sig['数值']}")
            print(f"  建议：{sig['建议']}")
            print()
    else:
        print("\n✅ 无异常信号")
    
    # 保存扫描结果
    scan_result = {
        "scan_time": datetime.now().astimezone().isoformat(),
        "signals_count": len(signals),
        "signals": signals
    }
    
    scan_file = DATA_DIR / "signals.json"
    with open(scan_file, "w", encoding="utf-8") as f:
        json.dump(scan_result, f, indent=2, ensure_ascii=False)
    print(f"✓ 扫描结果已保存：{scan_file}")
    
    return signals

if __name__ == "__main__":
    scan_signals()
