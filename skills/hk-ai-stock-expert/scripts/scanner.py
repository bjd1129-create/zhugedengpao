#!/usr/bin/env python3
"""
港股 AI 股票筛选器
- 根据 AI 纯度/成长性/估值/流动性筛选标的
- 输出符合标准的股票池
"""

import sys
import argparse
from datetime import datetime

try:
    import pandas as pd
    import akshare as ak
except ImportError as e:
    print(f"缺少依赖：{e}")
    print("请安装：pip install pandas akshare")
    sys.exit(1)


# 港股 AI 成分股列表
AI_STOCKS = [
    # 互联网巨头
    {'code': '00700', 'name': '腾讯控股', 'category': '互联网'},
    {'code': '09988', 'name': '阿里巴巴', 'category': '互联网'},
    {'code': '03690', 'name': '美团', 'category': '互联网'},
    {'code': '09618', 'name': '京东', 'category': '互联网'},
    {'code': '09888', 'name': '百度集团', 'category': '互联网'},
    {'code': '09999', 'name': '网易', 'category': '互联网'},
    {'code': '01810', 'name': '小米集团', 'category': '互联网'},
    
    # AI 纯玩家
    {'code': '00020', 'name': '商汤科技', 'category': 'AI 纯玩家'},
    {'code': '01357', 'name': '美图公司', 'category': 'AI 纯玩家'},
    
    # 企业 SaaS
    {'code': '00268', 'name': '金蝶国际', 'category': 'SaaS'},
    {'code': '00909', 'name': '明源云', 'category': 'SaaS'},
    {'code': '01024', 'name': '微盟集团', 'category': 'SaaS'},
    
    # 硬件/算力
    {'code': '00992', 'name': '联想集团', 'category': '硬件'},
    {'code': '00981', 'name': '中芯国际', 'category': '硬件'},
    {'code': '01347', 'name': '华虹半导体', 'category': '硬件'},
    {'code': '09698', 'name': '万国数据', 'category': '硬件'},
    
    # 智能汽车
    {'code': '09868', 'name': '小鹏汽车', 'category': '汽车'},
    {'code': '02015', 'name': '理想汽车', 'category': '汽车'},
    {'code': '09866', 'name': '蔚来', 'category': '汽车'},
    
    # 医疗 AI
    {'code': '00241', 'name': '阿里健康', 'category': '医疗'},
    {'code': '01833', 'name': '平安好医生', 'category': '医疗'},
]


def fetch_stock_data(code):
    """获取个股数据"""
    try:
        # 使用 akshare 获取港股实时行情
        df = ak.stock_hk_daily(symbol=code)
        if df is None or len(df) == 0:
            return None
        
        latest = df.iloc[-1]
        return {
            'code': code,
            'price': latest.get('close', 0),
            'change_pct': latest.get('change', 0),
            'volume': latest.get('volume', 0),
            'market_cap': latest.get('market_cap', 0),
        }
    except Exception as e:
        print(f"获取 {code} 数据失败：{e}")
        return None


def calculate_scores(stock_data):
    """计算综合评分"""
    # 简化评分逻辑
    scores = {
        'liquidity_score': min(stock_data.get('volume', 0) / 10000000, 10),  # 流动性
        'size_score': min(stock_data.get('market_cap', 0) / 10000000000, 10),  # 市值
    }
    scores['total_score'] = (scores['liquidity_score'] + scores['size_score']) / 2
    return scores


def screen_stocks(min_market_cap=50, min_volume=3000):
    """
    筛选股票
    
    Args:
        min_market_cap: 最小市值 (亿港元)
        min_volume: 最小日均成交 (万港元)
    
    Returns:
        DataFrame: 筛选结果
    """
    results = []
    
    for stock in AI_STOCKS:
        print(f"处理 {stock['code']} - {stock['name']}...")
        
        data = fetch_stock_data(stock['code'])
        if data is None:
            continue
        
        # 计算评分
        scores = calculate_scores(data)
        
        # 筛选条件
        if data.get('market_cap', 0) < min_market_cap * 1e8:
            continue
        if data.get('volume', 0) < min_volume * 1e4:
            continue
        
        results.append({
            '代码': stock['code'],
            '名称': stock['name'],
            '类别': stock['category'],
            '现价': round(data.get('price', 0), 2),
            '涨跌幅': f"{data.get('change_pct', 0):.2f}%",
            '成交量': f"{data.get('volume', 0)/1e4:.0f}万",
            '市值 (亿港元)': f"{data.get('market_cap', 0)/1e8:.1f}",
            '综合评分': f"{scores['total_score']:.1f}",
        })
    
    return pd.DataFrame(results)


def main():
    parser = argparse.ArgumentParser(description='港股 AI 股票筛选器')
    parser.add_argument('--min-cap', type=float, default=50,
                        help='最小市值 (亿港元，默认 50)')
    parser.add_argument('--min-volume', type=float, default=3000,
                        help='最小日均成交 (万港元，默认 3000)')
    parser.add_argument('--output', type=str, default='',
                        help='输出文件路径 (CSV 格式)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("港股 AI 股票筛选器")
    print(f"筛选条件：市值 ≥ {args.min_cap}亿港元，日均成交 ≥ {args.min_volume}万港元")
    print("=" * 60)
    
    # 执行筛选
    df = screen_stocks(min_market_cap=args.min_cap, min_volume=args.min_volume)
    
    if len(df) == 0:
        print("未找到符合条件的股票")
        return
    
    # 输出结果
    print(f"\n找到 {len(df)} 只符合条件的股票:\n")
    print(df.to_string(index=False))
    
    # 保存文件
    if args.output:
        df.to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存到：{args.output}")
    
    # 按类别统计
    print("\n按类别统计:")
    category_count = df.groupby('类别').size().reset_index(name='数量')
    print(category_count.to_string(index=False))


if __name__ == '__main__':
    main()
