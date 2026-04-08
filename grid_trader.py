#!/usr/bin/env python3
"""
网格交易执行器 — 每 5 分钟运行
读取实时价格，执行网格策略，更新 portfolio.json
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 导入交易模拟器
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trading_simulator import TradingSimulator, create_default_strategy

# 配置
WORKSPACE = Path("/Users/bjd/Desktop/ZhugeDengpao-Team")
PORTFOLIO_FILE = WORKSPACE / "portfolio.json"
TRADES_LOG = WORKSPACE / "trades_log.json"

def fetch_prices() -> dict:
    """从 Binance 获取实时价格"""
    import urllib.request
    import ssl
    
    # 绕过 SSL 验证（用于本地环境）
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    symbols = ['BTCUSDT', 'ETHUSDT', 'AVAXUSDT', 'ADAUSDT']
    prices = {}
    
    for symbol in symbols:
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            with urllib.request.urlopen(url, timeout=5, context=ssl_context) as response:
                data = json.loads(response.read().decode())
                prices[symbol] = float(data['price'])
        except Exception as e:
            print(f"⚠️  获取 {symbol} 价格失败：{e}")
            prices[symbol] = None
    
    return prices


def load_portfolio() -> dict:
    """加载投资组合状态"""
    if PORTFOLIO_FILE.exists():
        with open(PORTFOLIO_FILE, 'r') as f:
            return json.load(f)
    return None


def save_portfolio(portfolio: dict):
    """保存投资组合状态"""
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=2, ensure_ascii=False)


def append_trades(new_trades: list):
    """追加交易记录到日志"""
    trades = []
    if TRADES_LOG.exists():
        with open(TRADES_LOG, 'r') as f:
            trades = json.load(f)
    
    trades.extend(new_trades)
    
    # 只保留最近 1000 条
    if len(trades) > 1000:
        trades = trades[-1000:]
    
    with open(TRADES_LOG, 'w') as f:
        json.dump(trades, f, indent=2, ensure_ascii=False)


def run_grid_trading():
    """执行网格交易"""
    print(f"🕒 [{datetime.now().isoformat()}] 开始执行网格交易...")
    
    # 获取实时价格
    prices = fetch_prices()
    print(f"📊 当前价格:")
    for symbol, price in prices.items():
        if price:
            print(f"   {symbol}: ${price:.4f}")
    
    # 检查价格是否获取成功
    if not all(prices.values()):
        print("⚠️  部分价格获取失败，使用缓存或跳过本次执行")
        portfolio = load_portfolio()
        if portfolio:
            portfolio['last_update'] = datetime.now().isoformat()
            portfolio['status'] = 'partial_data'
            save_portfolio(portfolio)
        return
    
    # 创建策略
    sim = create_default_strategy()
    
    # 加载现有投资组合（如果有）
    portfolio = load_portfolio()
    
    if portfolio and 'grid_states' in portfolio:
        # TODO: 恢复之前的网格状态（需要扩展 trading_simulator 支持状态序列化）
        print("📁 检测到现有投资组合，将合并状态...")
    
    # 运行模拟
    results = sim.run_simulation(prices)
    
    # 计算实际盈亏 = 已实现盈亏 + 持有盈亏（网格未部署时不计入）
    total_pnl = 0.0
    for symbol, strategy in sim.strategies.items():
        total_pnl += strategy.realized_pnl  # 网格已实现盈亏
    for symbol, holding in sim.holdings.items():
        if symbol in prices:
            total_pnl += holding.get_pnl(prices[symbol])  # 持有盈亏
    
    # 收集新交易
    new_trades = []
    for symbol, strategy in sim.strategies.items():
        for trade in strategy.trades:
            trade['symbol'] = symbol
            new_trades.append(trade)
    
    # 追加交易记录
    if new_trades:
        append_trades(new_trades)
        print(f"✅ 新增 {len(new_trades)} 条交易记录")
    
    # 构建投资组合状态
    portfolio = {
        'last_update': datetime.now().isoformat(),
        'status': 'success',
        'total_capital': sim.total_capital,
        'cash': sim.cash,
        'total_pnl': total_pnl,
        'total_pnl_pct': total_pnl / sim.total_capital * 100,
        'prices': prices,
        'strategies': {},
        'holdings': {},
        'summary': {
            'grid_count': len(sim.strategies),
            'hold_count': len(sim.holdings),
            'total_trades': len(new_trades)
        }
    }
    
    # 添加网格策略状态
    for symbol, strategy in sim.strategies.items():
        portfolio['strategies'][symbol] = {
            'budget': strategy.budget,
            'range': [strategy.lower, strategy.upper],
            'grids': strategy.grid_count,
            'step': strategy.grid_step,
            'realized_pnl': strategy.realized_pnl,
            'unrealized_pnl': strategy.unrealized_pnl,
            'total_pnl': strategy.realized_pnl + strategy.unrealized_pnl,
            'trades_count': len(strategy.trades),
            'stopped': strategy.stopped,
            'filled_grids': sum(1 for g in strategy.grids if g['filled'])
        }
    
    # 添加持有策略状态
    for symbol, holding in sim.holdings.items():
        if symbol in prices:
            pnl = holding.get_pnl(prices[symbol])
            portfolio['holdings'][symbol] = {
                'amount': holding.amount,
                'entry_price': holding.entry_price,
                'current_price': prices[symbol],
                'stop_loss': holding.stop_loss,
                'pnl': pnl,
                'pnl_pct': pnl / holding.amount * 100,
                'stopped': holding.stopped,
                'exit_price': holding.exit_price
            }
    
    # 保存投资组合
    save_portfolio(portfolio)
    
    # 输出摘要
    print(f"\n{'='*50}")
    print(f"✅ 网格交易执行完成")
    print(f"{'='*50}")
    print(f"总盈亏：${total_pnl:.2f} ({total_pnl/sim.total_capital*100:.2f}%)")
    print(f"新增交易：{len(new_trades)} 笔")
    print(f"投资组合已更新：{PORTFOLIO_FILE}")
    
    return portfolio


if __name__ == '__main__':
    try:
        run_grid_trading()
    except Exception as e:
        print(f"❌ 执行失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
