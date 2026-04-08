#!/usr/bin/env python3
"""
网格交易执行器 - 每 5 分钟运行
读取价格数据，检查网格触发，更新 portfolio.json
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 路径配置
TRADING_DIR = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading")
PORTFOLIO_FILE = TRADING_DIR / "portfolio.json"
PRICE_FILE = TRADING_DIR / "price_aggregate.json"
STOP_FLAG = TRADING_DIR / "STOP_TRADING.flag"

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_avg_price(prices):
    """计算多平台平均价格"""
    if not prices:
        return None
    return sum(prices.values()) / len(prices)

def check_grid_trigger(current_price, levels, position, last_idx):
    """检查是否触发网格交易"""
    if not levels:
        return None, position, last_idx
    
    # 找到当前价格附近的网格位置
    for i, level in enumerate(levels):
        # 买入触发：价格从上往下穿过网格线
        if current_price <= level and (last_idx is None or i > last_idx):
            return ('BUY', i), i, i
        # 卖出触发：价格从下往上穿过网格线
        elif current_price >= level and (last_idx is None or i < last_idx):
            return ('SELL', i), i, i
    
    return None, position, last_idx

def main():
    print(f"⏰ 网格交易检查 - {datetime.now().isoformat()}")
    
    # 检查是否停止交易
    if STOP_FLAG.exists():
        print("🔴 交易已停止 (STOP_TRADING.flag 存在)")
        with open(STOP_FLAG, 'r') as f:
            reason = f.read().strip() or "未知原因"
        print(f"   原因：{reason}")
        
        # 即使停止交易，也更新当前价格
        portfolio = load_json(PORTFOLIO_FILE)
        price_data = load_json(PRICE_FILE)
        
        # 更新持仓的当前价格
        for holding in portfolio.get('holdings', []):
            symbol = holding['symbol']
            if symbol in price_data.get('platforms', {}):
                platforms = price_data['platforms']
                prices = {p: platforms[p][symbol] for p in platforms if symbol in platforms[p]}
                if prices:
                    holding['currentPrice'] = get_avg_price(prices)
        
        portfolio['lastUpdated'] = datetime.now().astimezone().isoformat()
        save_json(PORTFOLIO_FILE, portfolio)
        print(f"📊 已更新价格数据 (净值：${portfolio['account']['totalValue']:.2f})")
        return
    
    # 加载数据
    portfolio = load_json(PORTFOLIO_FILE)
    price_data = load_json(PRICE_FILE)
    
    print(f"💰 当前现金：${portfolio['account']['cashBalance']:.2f}")
    print(f"📈 总交易次数：{portfolio['account']['totalTrades']}")
    
    # 获取当前价格
    platforms = price_data.get('platforms', {})
    trades = []
    
    # 检查每个币种的网格
    for symbol, grid_state in portfolio.get('gridState', {}).items():
        if symbol not in platforms:
            continue
        
        # 计算平均价格
        prices = {p: platforms[p][symbol] for p in platforms if symbol in platforms[p]}
        if not prices:
            continue
        
        current_price = get_avg_price(prices)
        levels = grid_state.get('levels', [])
        position = grid_state.get('position', 0)
        last_idx = grid_state.get('lastGridIdx')
        
        print(f"\n{symbol}: ${current_price:.4f} (网格：{len(levels)} 层，持仓：{position})")
        
        # 检查网格触发
        trigger, new_idx, new_last_idx = check_grid_trigger(current_price, levels, position, last_idx)
        
        if trigger:
            side, idx = trigger
            grid_price = levels[idx]
            print(f"  ⚡ 触发网格 {idx}: ${grid_price:.4f} ({side})")
            
            # 记录交易
            trade = {
                'time': datetime.now().astimezone().isoformat(),
                'side': side,
                'symbol': symbol,
                'price': grid_price,
                'note': f'grid-{idx}{"↑" if side == "SELL" else "↓"}'
            }
            trades.append(trade)
            
            # 更新网格状态
            grid_state['lastGridIdx'] = new_last_idx
            
            # TODO: 实际执行交易逻辑（模拟盘仅记录）
            if side == 'BUY':
                # 计算买入数量
                grid_value = 100  # 每格$100
                amount = grid_value / grid_price
                grid_state['position'] = position + amount
                
                # 更新现金
                portfolio['account']['cashBalance'] -= grid_value
                portfolio['account']['totalTrades'] += 1
                
                trade['amount'] = amount
                trade['note'] += f" {amount:.4f} {symbol}"
                
            elif side == 'SELL':
                # 计算卖出数量
                grid_value = 100
                amount = grid_value / grid_price
                grid_state['position'] = max(0, position - amount)
                
                # 更新现金
                portfolio['account']['cashBalance'] += grid_value
                portfolio['account']['totalTrades'] += 1
                
                trade['amount'] = amount
                pnl = grid_value * 0.02  # 假设 2% 利润
                if pnl > 0:
                    trade['pnl'] = pnl
                    trade['note'] += f" PnL:${pnl:.2f}"
    
    # 更新持仓价格
    for holding in portfolio.get('holdings', []):
        symbol = holding['symbol']
        if symbol in platforms:
            prices = {p: platforms[p][symbol] for p in platforms if symbol in platforms[p]}
            if prices:
                holding['currentPrice'] = get_avg_price(prices)
    
    # 计算总价值
    portfolio['account']['totalValue'] = portfolio['account']['cashBalance']
    for holding in portfolio.get('holdings', []):
        portfolio['account']['totalValue'] += holding['amount'] * holding['currentPrice']
    
    # 计算盈亏
    initial = portfolio['account']['initialBalance']
    total = portfolio['account']['totalValue']
    portfolio['account']['totalPnL'] = total - initial
    portfolio['account']['totalPnLPercent'] = (total - initial) / initial * 100
    
    # 添加交易记录
    if trades:
        portfolio['recentTrades'] = trades + portfolio.get('recentTrades', [])[:10]
    
    portfolio['lastUpdated'] = datetime.now().astimezone().isoformat()
    
    # 保存
    save_json(PORTFOLIO_FILE, portfolio)
    
    print(f"\n✅ 更新完成")
    print(f"   净值：${portfolio['account']['totalValue']:.2f}")
    print(f"   盈亏：${portfolio['account']['totalPnL']:.2f} ({portfolio['account']['totalPnLPercent']:.2f}%)")
    if trades:
        print(f"   成交：{len(trades)} 笔")

if __name__ == '__main__':
    main()
