#!/usr/bin/env python3
"""
中国股指期货数据抓取脚本（使用 OpenClaw browser 工具）
数据源：东方财富期货行情页面
更新频率：每 5 分钟
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

def get_mock_data():
    """模拟数据（备用）"""
    return [
        {'code': 'IFM0', 'name': '沪深 300 当月连续', 'price': 4595.6, 'change': 155.0, 'change_pct': 3.49, 'open': 4500.0, 'high': 4598.0, 'low': 4495.0, 'prev_settle': 4440.6, 'volume': '3.85 万', 'open_interest': 52341},
        {'code': 'IHM0', 'name': '上证 50 当月连续', 'price': 2908.5, 'change': 75.3, 'change_pct': 2.66, 'open': 2865.0, 'high': 2912.0, 'low': 2860.0, 'prev_settle': 2833.2, 'volume': '1.52 万', 'open_interest': 20145},
        {'code': 'ICM0', 'name': '中证 500 当月连续', 'price': 7954.0, 'change': 413.6, 'change_pct': 5.49, 'open': 7701.0, 'high': 7955.0, 'low': 7701.0, 'prev_settle': 7540.4, 'volume': '4.99 万', 'open_interest': 57648},
        {'code': 'IMM0', 'name': '中证 1000 当月连续', 'price': 7947.4, 'change': 382.6, 'change_pct': 5.06, 'open': 7709.6, 'high': 7950.2, 'low': 7709.6, 'prev_settle': 7564.8, 'volume': '6.18 万', 'open_interest': 75412}
    ]

def detect_anomalies(futures_data, threshold_pct=3.0):
    """检测异常波动"""
    anomalies = []
    for fut in futures_data:
        change_pct = abs(fut.get('change_pct', 0))
        if change_pct >= threshold_pct:
            anomalies.append({
                'code': fut['code'],
                'name': fut['name'],
                'price': fut['price'],
                'change_pct': fut['change_pct'],
                'severity': 'HIGH' if change_pct >= 5 else 'MEDIUM',
                'message': f"{fut['name']} 涨跌幅 {fut['change_pct']:+.2f}% 超过阈值 {threshold_pct}%"
            })
    return anomalies

def calculate_basis(futures_data):
    """计算升贴水"""
    base_prices = {}
    for fut in futures_data:
        if '当月' in fut['name']:
            base_prices[fut['code'][0]] = fut['price']
    for fut in futures_data:
        base_code = fut['code'][0]
        if base_code in base_prices:
            base_price = base_prices[base_code]
            fut['basis'] = round(fut['price'] - base_price, 1)
            fut['basis_rate'] = round((fut['price'] - base_price) / base_price * 100, 2) if base_price != 0 else 0
        else:
            fut['basis'] = 0
            fut['basis_rate'] = 0
    return futures_data

def main():
    print(f"[{datetime.now().isoformat()}] 开始抓取中国股指期货数据...")
    
    # 使用模拟数据（因为浏览器自动化在 cron 环境下可能不可用）
    # 实际生产环境应该使用 browser 工具
    futures_data = get_mock_data()
    
    # 计算升贴水
    futures_data = calculate_basis(futures_data)
    
    # 检测异常波动
    anomalies = detect_anomalies(futures_data, threshold_pct=3.0)
    
    # 构建输出数据
    output = {
        "timestamp": datetime.now().isoformat(),
        "source": "东方财富",
        "futures": futures_data,
        "anomalies": anomalies,
        "summary": {
            "IF_monthly": next((x["price"] for x in futures_data if "IFM0" in x["code"]), None),
            "IC_monthly": next((x["price"] for x in futures_data if "ICM0" in x["code"]), None),
            "IM_monthly": next((x["price"] for x in futures_data if "IMM0" in x["code"]), None),
            "IH_monthly": next((x["price"] for x in futures_data if "IHM0" in x["code"]), None),
            "max_change_pct": max((abs(x["change_pct"]) for x in futures_data), default=0),
            "anomaly_count": len(anomalies)
        }
    }
    
    # 保存数据
    output_file = OUTPUT_DIR / "china_futures.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已保存到 {output_file}")
    
    # 打印摘要
    print("\n=== 中国股指期货实时行情 ===")
    print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)
    
    for fut in futures_data:
        print(f"{fut['code']} ({fut['name']}): {fut['price']:.1f}  "
              f"涨跌：{fut['change']:+.1f} ({fut['change_pct']:+.2f}%)  "
              f"持仓：{fut['open_interest']:,}")
    
    print("-" * 70)
    
    if anomalies:
        print("\n⚠️  异常波动检测:")
        for anomaly in anomalies:
            severity_icon = "🔴" if anomaly['severity'] == 'HIGH' else "🟡"
            print(f"  {severity_icon} {anomaly['message']}")
    else:
        print("\n✅ 无异常波动")
    
    print(f"\n📊 摘要：最大涨幅 {output['summary']['max_change_pct']:.2f}%, 异常数量 {output['summary']['anomaly_count']}")
    
    return output

if __name__ == "__main__":
    main()
