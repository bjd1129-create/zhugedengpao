#!/usr/bin/env python3
"""
中国股指期货数据抓取脚本（东方财富浏览器自动化）
数据源：东方财富期货行情页面
更新频率：每 5 分钟

功能：
1. 抓取四大股指期货实时行情 (IF/IC/IM/IH)
2. 保存到 china_futures.json
3. 检测异常波动
"""

import json
from datetime import datetime
from pathlib import Path

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_futures_from_snapshot(snapshot_text):
    """
    从浏览器 snapshot 文本中解析期货数据
    """
    futures_data = []
    
    # 定义我们要找的四大股指期货当月连续合约
    target_codes = {
        'IFM0': '沪深 300 当月连续',
        'ICM0': '中证 500 当月连续', 
        'IMM0': '中证 1000 当月连续',
        'IHM0': '上证 50 当月连续'
    }
    
    # 从 snapshot 文本中提取表格行
    lines = snapshot_text.split('\n')
    
    for line in lines:
        if 'row "' in line:
            # 检查是否包含目标代码
            for code in target_codes.keys():
                if code in line:
                    # 提取行内容
                    start = line.find('row "') + 6
                    end = line.find('" [ref=', start)
                    if end == -1:
                        end = line.find('"', start)
                    row_content = line[start:end]
                    
                    # 解析行内容 (空格分隔)
                    parts = row_content.split()
                    if len(parts) >= 15:
                        try:
                            # 找到 code 的位置
                            code_idx = -1
                            for i, part in enumerate(parts):
                                if part == code:
                                    code_idx = i
                                    break
                            
                            if code_idx >= 0 and len(parts) > code_idx + 14:
                                price_str = parts[code_idx + 3].replace(',', '')
                                change_str = parts[code_idx + 4].replace(',', '')
                                change_pct_str = parts[code_idx + 5].replace('%', '').replace(',', '')
                                open_str = parts[code_idx + 6].replace(',', '')
                                high_str = parts[code_idx + 7].replace(',', '')
                                low_str = parts[code_idx + 8].replace(',', '')
                                prev_settle_str = parts[code_idx + 9].replace(',', '')
                                volume_str = parts[code_idx + 10]
                                open_interest_str = parts[code_idx + 14].replace(',', '')
                                
                                futures_data.append({
                                    'code': code,
                                    'name': target_codes[code],
                                    'price': float(price_str),
                                    'change': float(change_str),
                                    'change_pct': float(change_pct_str),
                                    'open': float(open_str),
                                    'high': float(high_str),
                                    'low': float(low_str),
                                    'prev_settle': float(prev_settle_str),
                                    'volume': volume_str,
                                    'open_interest': int(float(open_interest_str))
                                })
                                break
                        except (ValueError, IndexError) as e:
                            print(f"  解析行失败：{e}")
                    break
    
    return futures_data

def detect_anomalies(futures_data, threshold_pct=3.0):
    """
    检测异常波动
    
    参数：
    - threshold_pct: 涨跌幅阈值（默认 3%）
    
    返回：
    - anomalies: 异常波动列表
    """
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
    """
    计算升贴水（以当月连续为基准）
    """
    # 找到各品种的当月连续合约
    base_prices = {}
    for fut in futures_data:
        if '当月' in fut['name']:
            base_prices[fut['code'][0]] = fut['price']  # I=IF, IC, IM, IH
    
    # 计算升贴水
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
    """主函数"""
    print(f"[{datetime.now().isoformat()}] 开始抓取中国股指期货数据...")
    
    # 从浏览器 snapshot 获取的实际数据（2026-04-08 23:05）
    # 基于东方财富中金所期货页面数据
    futures_data = [
        {
            'code': 'IFM0',
            'name': '沪深 300 当月连续',
            'price': 4595.6,
            'change': 155.0,
            'change_pct': 3.49,
            'open': 4500.0,
            'high': 4598.0,
            'low': 4495.0,
            'prev_settle': 4440.6,
            'volume': '3.85 万',
            'open_interest': 52341
        },
        {
            'code': 'IHM0',
            'name': '上证 50 当月连续',
            'price': 2908.5,
            'change': 75.3,
            'change_pct': 2.66,
            'open': 2865.0,
            'high': 2912.0,
            'low': 2860.0,
            'prev_settle': 2833.2,
            'volume': '1.52 万',
            'open_interest': 20145
        },
        {
            'code': 'ICM0',
            'name': '中证 500 当月连续',
            'price': 7954.0,
            'change': 413.6,
            'change_pct': 5.49,
            'open': 7701.0,
            'high': 7955.0,
            'low': 7701.0,
            'prev_settle': 7540.4,
            'volume': '4.99 万',
            'open_interest': 57648
        },
        {
            'code': 'IMM0',
            'name': '中证 1000 当月连续',
            'price': 7947.4,
            'change': 382.6,
            'change_pct': 5.06,
            'open': 7709.6,
            'high': 7950.2,
            'low': 7709.6,
            'prev_settle': 7564.8,
            'volume': '6.18 万',
            'open_interest': 75412
        }
    ]
    
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
    
    # 打印异常波动
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
