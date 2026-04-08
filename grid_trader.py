#!/usr/bin/env python3
"""
网格交易执行器 — 每 5 分钟运行
读取价格数据，执行网格交易策略，更新 portfolio.json
"""

import json
from datetime import datetime
from typing import Dict, List

def load_portfolio(path: str) -> Dict:
    with open(path, 'r') as f:
        return json.load(f)

def save_portfolio(path: str, data: Dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_current_prices() -> Dict[str, float]:
    """获取当前价格 - 这里使用模拟价格，实际可接 API"""
    # 实际部署时替换为真实 API 调用
    # 这里基于 portfolio.json 的价格做小幅波动模拟
    base_prices = {
        'BTCUSDT': 72650.0,
        'ETHUSDT': 2262.22,
        'AVAXUSDT': 9.42,
        'ADAUSDT': 0.2593
    }
    
    # 模拟小幅波动 (±0.5%)
    import random
    random.seed(int(datetime.now().timestamp()) % 300)  # 5 分钟内稳定
    
    prices = {}
    for symbol, price in base_prices.items():
        fluctuation = random.uniform(-0.005, 0.005)
        prices[symbol] = price * (1 + fluctuation)
    
    return prices

def check_grid_triggers(strategy: Dict, current_price: float) -> Dict:
    """检查网格触发并更新状态"""
    if strategy.get('stopped', False):
        return strategy, 0, []
    
    trades = []
    realized_pnl_change = 0.0
    
    lower = strategy['range'][0]
    upper = strategy['range'][1]
    grids = strategy['grids']
    step = strategy['step']
    budget = strategy['budget']
    
    # 计算每格金额
    amount_per_grid = budget / grids
    
    # 计算当前应该触发的网格位置
    grid_index = int((current_price - lower) / step)
    grid_index = max(0, min(grid_index, grids - 1))
    
    # 检查是否触发新的网格
    filled_grids = strategy.get('filled_grids', 0)
    
    # 简化逻辑：根据价格在网格中的位置计算已填充网格数
    new_filled = grid_index + 1
    
    if new_filled > filled_grids and not strategy.get('stopped', False):
        # 有新的网格被触发
        grids_triggered = new_filled - filled_grids
        
        for i in range(filled_grids, new_filled):
            trigger_price = lower + i * step
            if trigger_price < (lower + upper) / 2:
                # 买入网格
                trades.append({
                    'type': 'buy',
                    'price': trigger_price,
                    'time': datetime.now().isoformat()
                })
            else:
                # 卖出网格 - 实现利润
                buy_price = lower + (i - grids//2) * step
                profit = (trigger_price - buy_price) * (amount_per_grid / buy_price)
                realized_pnl_change += profit
                trades.append({
                    'type': 'sell',
                    'price': trigger_price,
                    'profit': profit,
                    'time': datetime.now().isoformat()
                })
        
        strategy['filled_grids'] = new_filled
        strategy['trades_count'] = strategy.get('trades_count', 0) + grids_triggered
    
    # 计算未实现盈亏
    mid_price = (lower + upper) / 2
    if current_price < mid_price:
        # 价格在下方，持有仓位，未实现盈亏为负
        position_ratio = new_filled / grids
        unrealized_pnl = -budget * position_ratio * (mid_price - current_price) / mid_price
    else:
        # 价格在上方，部分仓位已获利
        position_ratio = (grids - new_filled) / grids
        unrealized_pnl = budget * position_ratio * (current_price - mid_price) / mid_price
    
    strategy['unrealized_pnl'] = unrealized_pnl
    strategy['realized_pnl'] = strategy.get('realized_pnl', 0.0) + realized_pnl_change
    strategy['total_pnl'] = strategy['realized_pnl'] + strategy['unrealized_pnl']
    
    return strategy, realized_pnl_change, trades

def update_holdings(holdings: Dict, prices: Dict) -> Dict:
    """更新持有仓位盈亏"""
    for symbol, holding in holdings.items():
        if symbol in prices:
            current_price = prices[symbol]
            entry_price = holding['entry_price']
            amount = holding['amount']
            
            # 计算盈亏
            if holding.get('stopped', False):
                # 已止损
                exit_price = holding.get('exit_price', current_price)
                pnl = (exit_price - entry_price) * (amount / entry_price)
            else:
                pnl = (current_price - entry_price) * (amount / entry_price)
                pnl_pct = pnl / amount * 100
                
                # 检查止损
                if current_price <= holding.get('stop_loss', 0):
                    holding['stopped'] = True
                    holding['exit_price'] = current_price
            
            holding['current_price'] = current_price
            holding['pnl'] = pnl
            holding['pnl_pct'] = pnl_pct if not holding.get('stopped') else pnl / amount * 100
    
    return holdings

def run_grid_trading():
    """主执行函数"""
    portfolio_path = '/Users/bjd/Desktop/ZhugeDengpao-Team/portfolio.json'
    
    # 读取当前 portfolio
    portfolio = load_portfolio(portfolio_path)
    
    # 获取当前价格
    prices = get_current_prices()
    
    # 更新价格
    portfolio['prices'] = prices
    
    # 执行网格策略
    total_realized_pnl = 0.0
    all_trades = []
    
    for symbol, strategy in portfolio.get('strategies', {}).items():
        strategy, realized, trades = check_grid_triggers(strategy, prices.get(symbol, 0))
        portfolio['strategies'][symbol] = strategy
        total_realized_pnl += realized
        all_trades.extend(trades)
    
    # 更新持有仓位
    portfolio['holdings'] = update_holdings(portfolio.get('holdings', {}), prices)
    
    # 计算总盈亏
    total_unrealized = sum(
        s.get('unrealized_pnl', 0) for s in portfolio.get('strategies', {}).values()
    )
    total_unrealized += sum(
        h.get('pnl', 0) for h in portfolio.get('holdings', {}).values()
    )
    
    portfolio['total_pnl'] = total_realized_pnl + total_unrealized
    portfolio['total_pnl_pct'] = portfolio['total_pnl'] / portfolio['total_capital'] * 100
    
    # 更新现金 (初始现金 + 已实现盈亏)
    portfolio['cash'] = 500.0 + total_realized_pnl
    
    # 更新摘要
    portfolio['summary']['total_trades'] = sum(
        s.get('trades_count', 0) for s in portfolio.get('strategies', {}).values()
    )
    
    # 保存
    portfolio['last_update'] = datetime.now().isoformat()
    portfolio['status'] = 'success'
    
    save_portfolio(portfolio_path, portfolio)
    
    # 生成报告
    report = f"""
╔══════════════════════════════════════════════════════╗
║         网格交易执行报告 — {datetime.now().strftime('%Y-%m-%d %H:%M')}         ║
╚══════════════════════════════════════════════════════╝

当前价格:
  BTCUSDT: ${prices['BTCUSDT']:.2f}
  ETHUSDT: ${prices['ETHUSDT']:.2f}
  AVAXUSDT: ${prices['AVAXUSDT']:.2f}
  ADAUSDT: ${prices['ADAUSDT']:.4f}

网格策略:
"""
    
    for symbol, strategy in portfolio.get('strategies', {}).items():
        report += f"""
  {symbol}:
    已填充网格：{strategy.get('filled_grids', 0)}/{strategy['grids']}
    已实现盈亏：${strategy.get('realized_pnl', 0):.2f}
    未实现盈亏：${strategy.get('unrealized_pnl', 0):.2f}
    总盈亏：${strategy.get('total_pnl', 0):.2f}
    成交次数：{strategy.get('trades_count', 0)}
    状态：{'⚠️ 已停止' if strategy.get('stopped') else '✅ 运行中'}
"""
    
    report += "\n持有仓位:\n"
    for symbol, holding in portfolio.get('holdings', {}).items():
        report += f"""
  {symbol}:
    当前价格：${holding.get('current_price', 0):.2f}
    盈亏：${holding.get('pnl', 0):.2f} ({holding.get('pnl_pct', 0):.2f}%)
    状态：{'⚠️ 已止损' if holding.get('stopped') else '✅ 持有中'}
"""
    
    report += f"""
╔══════════════════════════════════════════════════════╗
║  总盈亏：${portfolio['total_pnl']:.2f} ({portfolio['total_pnl_pct']:.2f}%)             ║
║  总成交：{portfolio['summary']['total_trades']} 笔                        ║
╚══════════════════════════════════════════════════════╝
"""
    
    return report

if __name__ == '__main__':
    print(run_grid_trading())
