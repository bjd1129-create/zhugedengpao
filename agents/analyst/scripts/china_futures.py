#!/usr/bin/env python3
"""
中国股指期货数据抓取脚本
数据源：新浪财经 API（免费）
"""

import requests
import json
from datetime import datetime

def get_index_futures():
    """获取四大股指期货实时行情"""
    url = "https://hq.sinajs.cn/rn=hq_sina_jss&list=IF0,IC0,IM0,IH0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://finance.sina.com.cn/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'gbk'  # 新浪财经返回 GBK 编码
        
        data = {}
        for line in response.text.split('\n'):
            if '=' in line and '"' in line:
                name, value = line.split('=')
                code = name.split('_')[-1]
                fields = value.strip('";\n').split(',')
                
                if len(fields) >= 15:
                    data[code] = {
                        'name': fields[0],
                        'date': fields[1],
                        'open': float(fields[2]) if fields[2] else 0,
                        'high': float(fields[3]) if fields[3] else 0,
                        'low': float(fields[4]) if fields[4] else 0,
                        'price': float(fields[5]) if fields[5] else 0,
                        'volume': int(fields[10]) if fields[10] else 0,
                        'open_interest': int(fields[12]) if fields[12] else 0,
                    }
        
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}

def save_to_json(data, filepath):
    """保存数据到 JSON 文件"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'source': '新浪财经',
        'futures': data
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to {filepath}")

def print_summary(data):
    """打印行情摘要"""
    print("\n=== 中国股指期货实时行情 ===")
    print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    code_map = {
        'IF0': '沪深 300',
        'IC0': '中证 500',
        'IM0': '中证 1000',
        'IH0': '上证 50'
    }
    
    for code, info in data.items():
        name = code_map.get(code, info['name'])
        print(f"{code} ({name}): {info['price']:.1f}  "
              f"涨跌：{info['open'] - info['price']:.1f}  "
              f"持仓：{info['open_interest']}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("正在获取中国股指期货数据...")
    data = get_index_futures()
    
    if data:
        print_summary(data)
        save_to_json(data, 'data/china_futures_prices.json')
    else:
        print("获取数据失败")
