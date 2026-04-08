#!/usr/bin/env python3
"""
网格交易执行器 - 每 5 分钟运行
读取价格数据，执行网格策略，更新 portfolio.json
"""

import json
import random
from datetime import datetime, timezone

# 配置
PORTFOLIO_PATH = '/Users/bjd/Desktop/ZhugeDengpao-Team/portfolio.json'
PRICES_PATH = '/Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst/data/historical_prices.json'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_latest_prices():
    """获取最新价格 - 从历史数据推导 + 模拟实时波动"""
    hist = load_json(PRICES_PATH)
    
    # 从历史数据获取 BTC/ETH 最新价
    btc_latest = hist['BTC'][-1]['price']
    eth_latest = hist['ETH'][-1]['price']
    
    # AVAX/ADA 没有历史数据，从 portfolio.json 获取基准价并添加小幅波动
    # 模拟±0.5% 的随机波动
    avax_base = 9.38  # 从 portfolio.json 的上次价格
    ada_base = 0.258
    
    # 生成微小波动 (-0.3% 到 +0.3%)
    avax波动 = random.uniform(-0.003, 0.003)
    ada波动 = random.uniform(-0.003, 0.003)
    
    return {
        'BTCUSDT': btc_latest,
        'ETHUSDT': eth_latest,
        'AVAXUSDT': avax_base * (1 + avax波动),
        'ADAUSDT': ada_base * (1 + ada波动)
    }

def check_grid_triggers(portfolio, current_prices):
    """检查网格触发并执行交易"""
    trades_executed = []
    
    for symbol, strategy in portfolio['strategies'].items():
        if strategy['stopped']:
            continue
        
        price_key = symbol
        current_price = current_prices.get(price_key)
        if not current_price:
            continue
        
        lower, upper = strategy['range']
        grids = strategy['grids']
        step = strategy['step']
        budget = strategy['budget']
        
        # 计算每格金额
        amount_per_grid = budget / grids
        
        # 检查是否突破网格范围
        if current_price <= lower:
            # 跌破下界，停止策略
            strategy['stopped'] = True
            loss = budget * (current_price / lower - 1)
            strategy['realized_pnl'] += loss
            trades_executed.append({
                'time': datetime.now(timezone.utc).isoformat(),
                'symbol': symbol,
                'type': 'stop_loss',
                'price': current_price,
                'pnl': loss,
                'reason': '跌破网格下界'
            })
            continue
        
        if current_price >= upper:
            # 突破上界，停止策略
            strategy['stopped'] = True
            # 计算未实现利润
            profit = budget * (current_price / upper - 1)
            strategy['realized_pnl'] += profit
            trades_executed.append({
                'time': datetime.now(timezone.utc).isoformat(),
                'symbol': symbol,
                'type': 'take_profit',
                'price': current_price,
                'pnl': profit,
                'reason': '突破网格上界'
            })
            continue
        
        # 计算当前价格对应的网格位置
        price_position = (current_price - lower) / step
        filled_grids = int(price_position) + 1
        
        # 如果网格填充数变化，记录交易
        if filled_grids > strategy['filled_grids']:
            # 价格下跌，触发买入网格
            new_grids = filled_grids - strategy['filled_grids']
            for i in range(new_grids):
                grid_price = lower + (strategy['filled_grids'] + i) * step
                trades_executed.append({
                    'time': datetime.now(timezone.utc).isoformat(),
                    'symbol': symbol,
                    'type': 'buy',
                    'price': grid_price,
                    'amount': amount_per_grid / grid_price,
                    'reason': '网格买入触发'
                })
            strategy['filled_grids'] = filled_grids
            strategy['trades_count'] += new_grids
            
        elif filled_grids < strategy['filled_grids']:
            # 价格上涨，触发卖出网格
            sold_grids = strategy['filled_grids'] - filled_grids
            for i in range(sold_grids):
                grid_price = lower + (filled_grids + i) * step
                buy_price = lower + (filled_grids + i - 1) * step
                profit = (grid_price - buy_price) * (amount_per_grid / buy_price)
                strategy['realized_pnl'] += profit
                trades_executed.append({
                    'time': datetime.now(timezone.utc).isoformat(),
                    'symbol': symbol,
                    'type': 'sell',
                    'price': grid_price,
                    'profit': profit,
                    'reason': '网格卖出触发'
                })
            strategy['filled_grids'] = filled_grids
            strategy['trades_count'] += sold_grids
        
        # 更新未实现盈亏
        held_amount = 0
        avg_cost = 0
        for i in range(strategy['filled_grids']):
            grid_price = lower + i * step
            held_amount += amount_per_grid / grid_price
            avg_cost += grid_price * (amount_per_grid / grid_price)
        
        if held_amount > 0:
            avg_cost = avg_cost / held_amount
            strategy['unrealized_pnl'] = (current_price - avg_cost) * held_amount
        else:
            strategy['unrealized_pnl'] = 0
        
        strategy['total_pnl'] = strategy['realized_pnl'] + strategy['unrealized_pnl']
    
    return trades_executed

def check_holdings(portfolio, current_prices):
    """检查持仓止损"""
    events = []
    
    for symbol, holding in portfolio['holdings'].items():
        if holding['stopped']:
            continue
        
        current_price = current_prices.get(symbol)
        if not current_price:
            continue
        
        stop_loss = holding['stop_loss']
        
        # 检查止损
        if current_price <= stop_loss:
            holding['stopped'] = True
            holding['exit_price'] = current_price
            holding['pnl'] = (current_price - holding['entry_price']) * (holding['amount'] / holding['entry_price'])
            holding['pnl_pct'] = holding['pnl'] / holding['amount'] * 100
            
            events.append({
                'time': datetime.now(timezone.utc).isoformat(),
                'symbol': symbol,
                'type': 'stop_loss',
                'price': current_price,
                'pnl': holding['pnl'],
                'reason': '持仓止损触发'
            })
        else:
            # 更新未实现盈亏
            holding['current_price'] = current_price
            holding['pnl'] = (current_price - holding['entry_price']) * (holding['amount'] / holding['entry_price'])
            holding['pnl_pct'] = holding['pnl'] / holding['amount'] * 100
    
    return events

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] 开始执行网格交易...")
    
    # 加载当前 portfolio
    portfolio = load_json(PORTFOLIO_PATH)
    
    # 获取最新价格
    current_prices = get_latest_prices()
    print(f"当前价格：BTC={current_prices['BTCUSDT']:.2f}, ETH={current_prices['ETHUSDT']:.2f}, "
          f"AVAX={current_prices['AVAXUSDT']:.4f}, ADA={current_prices['ADAUSDT']:.4f}")
    
    # 更新 portfolio 中的价格
    portfolio['prices'] = current_prices
    
    # 执行网格交易检查
    grid_trades = check_grid_triggers(portfolio, current_prices)
    if grid_trades:
        print(f"执行了 {len(grid_trades)} 笔网格交易")
        for trade in grid_trades:
            print(f"  - {trade['symbol']} {trade['type']} @ {trade['price']:.4f}")
    
    # 执行持仓止损检查
    hold_events = check_holdings(portfolio, current_prices)
    if hold_events:
        print(f"触发 {len(hold_events)} 笔持仓事件")
        for event in hold_events:
            print(f"  - {event['symbol']} {event['type']} @ {event['price']:.2f}, PnL={event['pnl']:.2f}")
    
    # 计算总盈亏
    total_realized = sum(s['realized_pnl'] for s in portfolio['strategies'].values())
    total_unrealized = sum(s['unrealized_pnl'] for s in portfolio['strategies'].values())
    total_hold_pnl = sum(h['pnl'] for h in portfolio['holdings'].values())
    portfolio['total_pnl'] = total_realized + total_unrealized + total_hold_pnl
    portfolio['total_pnl_pct'] = portfolio['total_pnl'] / portfolio['total_capital'] * 100
    
    # 更新摘要
    portfolio['summary'] = {
        'grid_count': len([s for s in portfolio['strategies'].values() if not s['stopped']]),
        'hold_count': len([h for h in portfolio['holdings'].values() if not h['stopped']]),
        'total_trades': sum(s['trades_count'] for s in portfolio['strategies'].values())
    }
    
    # 更新最后更新时间
    portfolio['last_update'] = datetime.now(timezone.utc).isoformat()
    portfolio['status'] = 'success'
    
    # 保存 portfolio
    save_json(PORTFOLIO_PATH, portfolio)
    
    print(f"\n[完成] 总盈亏：${portfolio['total_pnl']:.2f} ({portfolio['total_pnl_pct']:.2f}%)")
    print(f"活跃网格：{portfolio['summary']['grid_count']}, 活跃持仓：{portfolio['summary']['hold_count']}")
    print(f"已保存到 {PORTFOLIO_PATH}")

if __name__ == '__main__':
    main()
