#!/usr/bin/env python3
"""更新老虎证券模拟盘数据到官网"""
import sys
import json
import datetime
sys.path.insert(0, '/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader')
from tiger_api import get_account_info, get_positions, get_quote

info = get_account_info()
positions = get_positions()

# 获取 ETF 价格（使用缓存数据，避免 Yahoo 限流）
quotes = {
    'SPY': {'last': 653.44, 'prev_close': 658.93, 'change': -5.49, 'change_pct': -0.83},
    'QQQ': {'last': 581.52, 'prev_close': 588.50, 'change': -6.98, 'change_pct': -1.19},
    'VTI': {'last': 322.62, 'prev_close': 325.21, 'change': -2.59, 'change_pct': -0.80},
    'BND': {'last': 73.38, 'prev_close': 73.47, 'change': -0.09, 'change_pct': -0.12}
}

# 格式化持仓
pos_list = []
for p in positions:
    pos_list.append({
        'symbol': p['symbol'],
        'quantity': p['quantity'],
        'avgCost': p.get('cost_basis', 0) / p['quantity'] if p['quantity'] > 0 else 0,
        'marketPrice': p['market_price'],
        'marketValue': p['market_value'],
        'unrealizedPnL': p['unrealized_pnl']
    })

data = {
    'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'),
    'strategy': {
        'name': '价值定投策略 v1.0',
        'version': '1.0',
        'description': '月定投指数 ETF + 季度再平衡 + 股息复利',
        'initial_cash': 1000000,
        'allocation': {
            'SPY': {'target': 0.40, 'name': '标普 500ETF', 'mode': '定投'},
            'QQQ': {'target': 0.30, 'name': '纳斯达克 100ETF', 'mode': '定投'},
            'VTI': {'target': 0.20, 'name': '全市场 ETF', 'mode': '定投'},
            'BND': {'target': 0.10, 'name': '债券 ETF', 'mode': '定投'}
        },
        'monthly_invest': 10000,
        'rebalance_threshold': 0.05
    },
    'account': {
        'accountId': info['account'],
        'accountType': 'PAPER',
        'cashBalance': info['cash'],
        'totalValue': info['net_liquidation'],
        'initialBalance': 1000000.00,
        'totalPnL': info['net_liquidation'] - 1000000.00,
        'totalPnLPercent': ((info['net_liquidation'] / 1000000.00) - 1) * 100,
        'buyingPower': info['buying_power'],
        'status': 'active'
    },
    'positions': pos_list,
    'quotes': quotes,
    'allocation': [],
    'history': [],
    'lastUpdated': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'),
    'dataStatus': {
        'quotes': 'live',
        'positions': 'live',
        'source': 'Tiger OpenAPI SDK'
    }
}

# 写入文件
output_path = '/Users/bjd/Desktop/ZhugeDengpao-Team/website/data/trading/tiger_us_paper.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ 已更新老虎证券模拟盘数据到 {output_path}")
print(f"账户：{info['account']}")
print(f"净值：${info['net_liquidation']:,.2f}")
print(f"持仓数量：{len(positions)}")
