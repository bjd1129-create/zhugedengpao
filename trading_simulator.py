#!/usr/bin/env python3
"""
交易模拟器 — 双币种网格 v2.0
策略：AVAX主网格 + ADA辅助网格 + BTC/ETH持有止损
作者：策略师 (2026-04-04)
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class GridStrategy:
    """网格策略"""
    
    def __init__(self, symbol: str, budget: float, lower: float, upper: float, 
                 grid_count: int, stop_loss: float):
        self.symbol = symbol
        self.budget = budget  # 总预算
        self.lower = lower    # 网格下界
        self.upper = upper    # 网格上界
        self.grid_count = grid_count  # 格数
        self.stop_loss = stop_loss  # 止损价
        
        # 计算每格参数
        self.grid_step = (upper - lower) / grid_count
        self.amount_per_grid = budget / grid_count
        
        # 初始化网格状态
        self.grids = []
        for i in range(grid_count):
            price = lower + i * self.grid_step
            self.grids.append({
                'price': price,
                'amount': self.amount_per_grid / price,  # 币数量
                'filled': False,
                'side': 'buy' if price < (lower + upper) / 2 else 'sell'
            })
        
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0
        self.trades = []
        self.stopped = False
    
    def simulate(self, current_price: float, price_history: List[float]):
        """模拟网格交易"""
        if self.stopped:
            return
        
        # 检查止损
        if current_price <= self.stop_loss:
            self.stopped = True
            loss = self.budget * (current_price / self.grids[0]['price'] - 1)
            self.realized_pnl += loss
            self.trades.append({
                'type': 'stop_loss',
                'price': current_price,
                'pnl': loss,
                'time': datetime.now().isoformat()
            })
            return
        
        # 检查网格触发
        for i, grid in enumerate(self.grids):
            if grid['side'] == 'buy' and current_price <= grid['price'] and not grid['filled']:
                # 买入触发
                grid['filled'] = True
                self.trades.append({
                    'type': 'buy',
                    'price': grid['price'],
                    'amount': grid['amount'],
                    'time': datetime.now().isoformat()
                })
            elif grid['side'] == 'sell' and current_price >= grid['price'] and grid['filled']:
                # 卖出触发（需要先有买入）
                buy_grid = self.grids[i-1] if i > 0 else None
                if buy_grid and buy_grid['filled']:
                    profit = (grid['price'] - buy_grid['price']) * buy_grid['amount']
                    self.realized_pnl += profit
                    buy_grid['filled'] = False  # 重置以便下次交易
                    self.trades.append({
                        'type': 'sell',
                        'price': grid['price'],
                        'profit': profit,
                        'time': datetime.now().isoformat()
                    })
        
        # 计算未实现盈亏
        self.unrealized_pnl = 0.0
        for grid in self.grids:
            if grid['filled']:
                self.unrealized_pnl += (current_price - grid['price']) * grid['amount']
    
    def get_summary(self) -> Dict:
        return {
            'symbol': self.symbol,
            'budget': self.budget,
            'range': f"${self.lower:.2f} ~ ${self.upper:.2f}",
            'grids': self.grid_count,
            'step': f"${self.grid_step:.3f}",
            'realized_pnl': self.realized_pnl,
            'unrealized_pnl': self.unrealized_pnl,
            'total_pnl': self.realized_pnl + self.unrealized_pnl,
            'trades_count': len(self.trades),
            'stopped': self.stopped
        }


class HoldStrategy:
    """持有策略（带止损）"""
    
    def __init__(self, symbol: str, amount: float, entry_price: float, stop_loss: float):
        self.symbol = symbol
        self.amount = amount  # USD金额
        self.entry_price = entry_price
        self.stop_loss = stop_loss
        self.quantity = amount / entry_price
        self.stopped = False
        self.exit_price = None
    
    def simulate(self, current_price: float):
        if self.stopped:
            return
        
        if current_price <= self.stop_loss:
            self.stopped = True
            self.exit_price = current_price
    
    def get_pnl(self, current_price: float) -> float:
        if self.stopped and self.exit_price:
            return (self.exit_price - self.entry_price) * self.quantity
        return (current_price - self.entry_price) * self.quantity
    
    def get_summary(self, current_price: float) -> Dict:
        pnl = self.get_pnl(current_price)
        return {
            'symbol': self.symbol,
            'amount': self.amount,
            'entry': self.entry_price,
            'current': current_price,
            'stop_loss': self.stop_loss,
            'pnl': pnl,
            'pnl_pct': pnl / self.amount * 100,
            'stopped': self.stopped
        }


class TradingSimulator:
    """交易模拟器主类"""
    
    def __init__(self, total_capital: float = 10000.0):
        self.total_capital = total_capital
        self.strategies = {}
        self.holdings = {}
        self.cash = 0.0
        self.initial_prices = {}
    
    def add_grid(self, symbol: str, budget: float, lower: float, upper: float,
                 grid_count: int, stop_loss: float):
        """添加网格策略"""
        self.strategies[symbol] = GridStrategy(
            symbol, budget, lower, upper, grid_count, stop_loss
        )
    
    def add_hold(self, symbol: str, amount: float, entry_price: float, stop_loss: float):
        """添加持有策略"""
        self.holdings[symbol] = HoldStrategy(symbol, amount, entry_price, stop_loss)
        self.initial_prices[symbol] = entry_price
    
    def set_cash(self, cash: float):
        self.cash = cash
    
    def run_simulation(self, prices: Dict[str, float], history: Dict[str, List[float]] = None):
        """运行模拟"""
        if history is None:
            history = {sym: [price] for sym, price in prices.items()}
        
        results = {}
        
        # 运行网格策略
        for symbol, strategy in self.strategies.items():
            if symbol in prices:
                strategy.simulate(prices[symbol], history.get(symbol, []))
                results[symbol] = strategy.get_summary()
        
        # 运行持有策略
        for symbol, holding in self.holdings.items():
            if symbol in prices:
                holding.simulate(prices[symbol])
                results[symbol] = holding.get_summary(prices[symbol])
        
        return results
    
    def get_total_pnl(self, prices: Dict[str, float]) -> float:
        """计算总盈亏"""
        total = self.cash  # 现金部分
        
        # 网格策略盈亏
        for symbol, strategy in self.strategies.items():
            total += strategy.realized_pnl + strategy.unrealized_pnl
        
        # 持有策略盈亏
        for symbol, holding in self.holdings.items():
            if symbol in prices:
                total += holding.get_pnl(prices[symbol])
        
        return total - self.total_capital
    
    def get_report(self, prices: Dict[str, float]) -> str:
        """生成报告"""
        results = self.run_simulation(prices)
        total_pnl = self.get_total_pnl(prices)
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║           交易模拟器报告 — 双币种网格 v2.0               ║
╚══════════════════════════════════════════════════════════╝

当前价格:
"""
        for symbol, price in prices.items():
            report += f"  {symbol}: ${price:.4f}\n"
        
        report += f"\n总盈亏: ${total_pnl:.2f} ({total_pnl/self.total_capital*100:.2f}%)\n"
        report += f"初始资金: ${self.total_capital:.2f}\n"
        report += f"现金保留: ${self.cash:.2f}\n"
        
        report += "\n━━━ 网格策略 ━━━\n"
        for symbol, strategy in self.strategies.items():
            summary = strategy.get_summary()
            report += f"""
{symbol}网格:
  预算: ${summary['budget']:.0f} | 范围: {summary['range']} | 格数: {summary['grids']}
  已实现盈亏: ${summary['realized_pnl']:.2f}
  未实现盈亏: ${summary['unrealized_pnl']:.2f}
  总盈亏: ${summary['total_pnl']:.2f}
  成交次数: {summary['trades_count']}
  止损触发: {'是 ⚠️' if summary['stopped'] else '否'}
"""
        
        report += "\n━━━ 持有策略 ━━━\n"
        for symbol, holding in self.holdings.items():
            if symbol in results:
                summary = results[symbol]
                report += f"""
{symbol}持有:
  金额: ${summary['amount']:.0f} | 入场: ${summary['entry']:.2f} | 当前: ${summary['current']:.2f}
  盈亏: ${summary['pnl']:.2f} ({summary['pnl_pct']:.2f}%)
  止损价: ${summary['stop_loss']:.2f}
  止损触发: {'是 ⚠️' if summary['stopped'] else '否'}
"""
        
        return report


# ════════════════════════════════════════════════════════════
# 策略配置 — 双币种网格 v2.0 (2026-04-04)
# ════════════════════════════════════════════════════════════

def create_default_strategy() -> TradingSimulator:
    """创建默认策略配置"""
    simulator = TradingSimulator(total_capital=10000.0)
    
    # AVAX网格 (主战场)
    simulator.add_grid(
        symbol='AVAXUSDT',
        budget=3000.0,
        lower=8.00,
        upper=9.80,
        grid_count=10,
        stop_loss=7.80
    )
    
    # ADA网格 (辅助)
    simulator.add_grid(
        symbol='ADAUSDT',
        budget=2000.0,
        lower=0.21,
        upper=0.28,
        grid_count=8,
        stop_loss=0.205
    )
    
    # BTC持有 (带止损)
    simulator.add_hold(
        symbol='BTCUSDT',
        amount=3500.0,
        entry_price=67102.54,  # 2026-04-04 收盘价
        stop_loss=64000.0
    )
    
    # ETH持有 (带止损)
    simulator.add_hold(
        symbol='ETHUSDT',
        amount=1000.0,
        entry_price=2850.0,  # 假设入场价
        stop_loss=2700.0
    )
    
    # 现金保留
    simulator.set_cash(500.0)
    
    return simulator


# ════════════════════════════════════════════════════════════
# 测试运行
# ════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # 创建策略
    sim = create_default_strategy()
    
    # 当前市场价格 (2026-04-04 21:00)
    current_prices = {
        'AVAXUSDT': 8.87,
        'ADAUSDT': 0.2441,
        'BTCUSDT': 67102.54,
        'ETHUSDT': 2850.0
    }
    
    # 生成报告
    print(sim.get_report(current_prices))
    
    # 压力测试：价格下跌10%
    print("\n\n⚠️  压力测试：价格下跌10%")
    stress_prices = {
        'AVAXUSDT': 8.87 * 0.9,
        'ADAUSDT': 0.2441 * 0.9,
        'BTCUSDT': 67102.54 * 0.9,
        'ETHUSDT': 2850.0 * 0.9
    }
    print(sim.get_report(stress_prices))
