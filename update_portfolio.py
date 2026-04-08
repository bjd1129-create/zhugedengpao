#!/usr/bin/env python3
"""
网格交易执行脚本 - 每 5 分钟运行
更新价格数据，执行网格策略，更新 portfolio.json
"""

import json
from datetime import datetime

# 最新市场价格 (2026-04-08 22:00)
NEW_PRICES = {
    'BTCUSDT': 71393.0,    # 分析师数据 +4.00%
    'ETHUSDT': 2233.94,    # 分析师数据 +6.19%
    'AVAXUSDT': 8.87,      # CoinMarketCap
    'ADAUSDT': 0.2463      # CoinMarketCap
}

def load_portfolio(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)

def save_portfolio(path: str, data: dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def calculate_grid_pnl(symbol: str, strategy: dict, new_price: float) -> dict:
    """计算网格策略盈亏"""
    lower, upper = strategy['range']
    grids = strategy['grids']
    step = (upper - lower) / grids
    budget = strategy['budget']
    
    # 检查是否有网格触发
    filled_grids = strategy.get('filled_grids', 0)
    realized_pnl = strategy.get('realized_pnl', 0)
    
    # 简单的网格盈亏模拟
    # 如果价格在网格范围内，检查是否有买卖触发
    mid_price = (lower + upper) / 2
    
    # 计算当前应持有的网格数量
    if new_price <= lower:
        # 价格低于下界，全部买入
        target_filled = grids
    elif new_price >= upper:
        # 价格高于上界，全部卖出
        target_filled = 0
    else:
        # 价格在范围内，按比例计算
        ratio = (upper - new_price) / (upper - lower)
        target_filled = int(ratio * grids)
    
    # 模拟网格交易
    trades_this_run = 0
    if target_filled > filled_grids:
        # 买入触发
        grids_to_buy = target_filled - filled_grids
        buy_amount = grids_to_buy * (budget / grids)
        trades_this_run = grids_to_buy
    elif target_filled < filled_grids:
        # 卖出触发
        grids_to_sell = filled_grids - target_filled
        # 简化：假设每格利润为 step * (budget/grids/lower)
        avg_profit_per_grid = step * (budget / grids / lower) * 0.5
        profit = grids_to_sell * avg_profit_per_grid
        realized_pnl += profit
        trades_this_run = grids_to_sell
    
    # 计算未实现盈亏
    avg_entry = lower + (grids - target_filled) * step / 2 if target_filled > 0 else lower
    unrealized_pnl = 0
    if target_filled > 0:
        held_value = target_filled * (budget / grids)
        unrealized_pnl = held_value * (new_price - avg_entry) / avg_entry
    
    return {
        'realized_pnl': realized_pnl,
        'unrealized_pnl': unrealized_pnl,
        'total_pnl': realized_pnl + unrealized_pnl,
        'filled_grids': target_filled,
        'trades_count': strategy.get('trades_count', 0) + trades_this_run,
        'trades_this_run': trades_this_run
    }

def calculate_hold_pnl(symbol: str, holding: dict, new_price: float) -> dict:
    """计算持有策略盈亏"""
    amount = holding['amount']
    entry_price = holding['entry_price']
    stop_loss = holding['stop_loss']
    stopped = holding.get('stopped', False)
    
    if stopped:
        # 已止损
        exit_price = holding.get('exit_price', stop_loss)
        pnl = (exit_price - entry_price) * (amount / entry_price)
        pnl_pct = pnl / amount * 100
    else:
        # 检查是否触发止损
        if new_price <= stop_loss:
            stopped = True
            pnl = (stop_loss - entry_price) * (amount / entry_price)
            pnl_pct = pnl / amount * 100
        else:
            pnl = (new_price - entry_price) * (amount / entry_price)
            pnl_pct = pnl / amount * 100
    
    return {
        'pnl': pnl,
        'pnl_pct': pnl_pct,
        'stopped': stopped,
        'exit_price': holding.get('exit_price')
    }

def main():
    portfolio_path = '/Users/bjd/Desktop/ZhugeDengpao-Team/portfolio.json'
    
    # 加载现有组合
    portfolio = load_portfolio(portfolio_path)
    
    print(f"📊 网格交易执行 - {datetime.now().isoformat()}")
    print("=" * 50)
    
    # 更新价格
    old_prices = portfolio.get('prices', {})
    portfolio['prices'] = NEW_PRICES
    
    print("\n📈 价格更新:")
    for symbol, new_price in NEW_PRICES.items():
        old_price = old_prices.get(symbol, new_price)
        change = ((new_price - old_price) / old_price * 100) if old_price else 0
        print(f"  {symbol}: {old_price:.4f} → {new_price:.4f} ({change:+.2f}%)")
    
    # 更新网格策略
    print("\n🔲 网格策略:")
    total_grid_pnl = 0
    total_trades = 0
    
    for symbol, strategy in portfolio.get('strategies', {}).items():
        if symbol in NEW_PRICES:
            new_price = NEW_PRICES[symbol]
            result = calculate_grid_pnl(symbol, strategy, new_price)
            
            # 更新策略状态
            strategy['realized_pnl'] = result['realized_pnl']
            strategy['unrealized_pnl'] = result['unrealized_pnl']
            strategy['total_pnl'] = result['total_pnl']
            strategy['filled_grids'] = result['filled_grids']
            strategy['trades_count'] = result['trades_count']
            
            total_grid_pnl += result['total_pnl']
            total_trades += result['trades_this_run']
            
            print(f"  {symbol}:")
            print(f"    已实现盈亏：${result['realized_pnl']:.2f}")
            print(f"    未实现盈亏：${result['unrealized_pnl']:.2f}")
            print(f"    成交网格：{result['filled_grids']}/{strategy['grids']}")
            if result['trades_this_run'] > 0:
                print(f"    ⚡ 本次成交：{result['trades_this_run']} 格")
    
    # 更新持有策略
    print("\n💼 持有策略:")
    total_hold_pnl = 0
    
    for symbol, holding in portfolio.get('holdings', {}).items():
        if symbol in NEW_PRICES:
            new_price = NEW_PRICES[symbol]
            result = calculate_hold_pnl(symbol, holding, new_price)
            
            # 更新持有状态
            holding['current_price'] = new_price
            holding['pnl'] = result['pnl']
            holding['pnl_pct'] = result['pnl_pct']
            
            if result['stopped'] and not holding.get('stopped'):
                holding['stopped'] = True
                holding['exit_price'] = holding['stop_loss']
                print(f"  ⚠️ {symbol} 触发止损！")
            
            total_hold_pnl += result['pnl']
            
            status = "🛑 已止损" if holding.get('stopped') else "📊 持有中"
            print(f"  {symbol} {status}: ${result['pnl']:.2f} ({result['pnl_pct']:.2f}%)")
    
    # 计算总盈亏
    total_pnl = total_grid_pnl + total_hold_pnl
    portfolio['total_pnl'] = total_pnl
    portfolio['total_pnl_pct'] = total_pnl / portfolio['total_capital'] * 100
    
    # 更新现金（简化：现金 = 总资金 - 网格预算 - 持有金额 + 已实现盈亏）
    grid_budget = sum(s['budget'] for s in portfolio.get('strategies', {}).values())
    hold_amount = sum(h['amount'] for h in portfolio.get('holdings', {}).values())
    portfolio['cash'] = portfolio['total_capital'] - grid_budget - hold_amount + total_grid_pnl
    
    # 更新汇总
    portfolio['summary'] = {
        'grid_count': len(portfolio.get('strategies', {})),
        'hold_count': len([h for h in portfolio.get('holdings', {}).values() if not h.get('stopped')]),
        'total_trades': total_trades
    }
    
    # 保存更新
    portfolio['last_update'] = datetime.now().isoformat()
    portfolio['status'] = 'success'
    
    save_portfolio(portfolio_path, portfolio)
    
    print("\n" + "=" * 50)
    print(f"✅ 组合更新完成")
    print(f"   总盈亏：${total_pnl:.2f} ({portfolio['total_pnl_pct']:.2f}%)")
    print(f"   现金余额：${portfolio['cash']:.2f}")
    print(f"   本次成交：{total_trades} 格")
    print(f"   更新时间：{portfolio['last_update']}")

if __name__ == '__main__':
    main()
