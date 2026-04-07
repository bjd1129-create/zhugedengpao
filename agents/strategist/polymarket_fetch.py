#!/usr/bin/env python3
"""Polymarket数据获取脚本 - 直接调用官方Gamma API，无需API Key"""
import requests, json, sys
from datetime import datetime

OUT_FILE = "/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/polymarket_data.json"
API = "https://gamma-api.polymarket.com"

def fetch_markets(limit=50):
    """获取热门市场"""
    r = requests.get(f"{API}/markets", params={"limit": limit, "closed": "false"}, timeout=10)
    r.raise_for_status()
    return r.json()

def analyze_market(m):
    """分析单个市场，返回结构化数据"""
    try:
        prices = json.loads(m.get('outcomePrices', '[]'))
        vol = float(m.get('volume24hr', 0))
        liquidity = float(m.get('liquidity', 0))
        question = m.get('question', '')
        
        # 找出Yes/No概率
        yes_price = float(prices[0]) if prices else 0
        no_price = float(prices[1]) if len(prices) > 1 else 0
        
        return {
            'id': m.get('id', ''),
            'question': question,
            'yes_price': yes_price,
            'no_price': no_price,
            'yes_prob': yes_price,
            'no_prob': no_price,
            'volume_24h': vol,
            'liquidity': liquidity,
            'url': f"https://polymarket.com/event/{m.get('slug', '')}",
            'updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
        }
    except:
        return None

def main():
    print("[Polymarket] 获取热门市场...")
    markets = fetch_markets(50)
    
    # 分析所有市场
    analyzed = []
    for m in markets:
        result = analyze_market(m)
        if result:
            analyzed.append(result)
    
    # 按24h成交量排序
    by_vol = sorted(analyzed, key=lambda x: x['volume_24h'], reverse=True)
    
    # 取Top20
    top20 = by_vol[:20]
    
    # 提取关键词标签
    tags = set()
    for m in markets:
        for t in m.get('tags', []):
            tags.add(t)
    
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'),
        'total_markets': len(markets),
        'top_20': top20,
        'available_tags': list(tags)[:20],
        'summary': {
            'total_tracked': len(top20),
            'highest_volume': top20[0]['volume_24h'] if top20 else 0,
        }
    }
    
    # 保存
    with open(OUT_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"[Polymarket] ✅ 获取{len(top20)}个热门市场")
    for m in top20[:5]:
        print(f"  [{m['volume_24h']:.0f}] {m['question'][:50]}... → YES={m['yes_prob']:.1%}")
    
    return data

if __name__ == '__main__':
    main()
