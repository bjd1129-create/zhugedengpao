#!/usr/bin/env python3
"""
策略回测脚本
- 支持多策略回测
- 计算收益率、夏普比率、最大回撤等指标
- 可视化回测结果
"""

import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path.home() / 'clawd' / 'quant-trading'))

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from akshare import stock_zh_a_hist, stock_hk_hist, stock_us_hist
except ImportError as e:
    print(f"缺少依赖：{e}")
    print("请安装：pip install pandas numpy matplotlib akshare")
    sys.exit(1)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Backtest:
    """回测引擎"""
    
    def __init__(self, strategy, symbol, start_date, end_date, 
                 initial_capital=100000, commission=0.001):
        """
        初始化回测
        
        Args:
            strategy: 策略类
            symbol: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            initial_capital: 初始资金
            commission: 手续费率
        """
        self.strategy = strategy
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.commission = commission
        
        self.capital = initial_capital
        self.position = 0  # 持仓数量
        self.trades = []  # 交易记录
        self.portfolio_values = []  # 组合价值
        
    def fetch_data(self):
        """获取历史数据"""
        logger.info(f"获取 {self.symbol} 数据 ({self.start_date} ~ {self.end_date})")
        
        try:
            if '.SS' in self.symbol or '.SZ' in self.symbol:
                df = stock_zh_a_hist(
                    self.symbol.replace('.SS', '').replace('.SZ', ''),
                    period="daily",
                    start_date=self.start_date.replace('-', ''),
                    end_date=self.end_date.replace('-', '')
                )
            elif '.HK' in self.symbol:
                df = stock_hk_hist(
                    self.symbol.replace('.HK', ''),
                    period="daily",
                    start_date=self.start_date.replace('-', ''),
                    end_date=self.end_date.replace('-', '')
                )
            else:
                df = stock_us_hist(
                    self.symbol,
                    period="daily",
                    start_date=self.start_date.replace('-', ''),
                    end_date=self.end_date.replace('-', '')
                )
            
            # 标准化列名
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume'
            })
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            df = df.sort_index()
            
            # 转换数值类型
            for col in ['open', 'close', 'high', 'low', 'volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df = df.dropna()
            
            logger.info(f"获取到 {len(df)} 条数据")
            return df
        
        except Exception as e:
            logger.error(f"获取数据失败：{e}")
            return None
    
    def run(self):
        """运行回测"""
        df = self.fetch_data()
        if df is None or len(df) < 30:
            logger.error("数据不足，无法回测")
            return None
        
        # 初始化策略
        if callable(self.strategy):
            strategy_instance = self.strategy({})
        else:
            strategy_instance = self.strategy
        
        logger.info(f"开始回测...")
        
        # 逐日回测
        for i in range(30, len(df)):
            # 获取历史数据用于计算指标
            hist_df = df.iloc[:i]
            current_price = df.iloc[i]['close']
            current_date = df.index[i]
            
            # 计算指标
            if hasattr(strategy_instance, 'analyze'):
                result = strategy_instance.analyze(hist_df)
                signal = result.get('signal', 'hold')
            else:
                # 默认策略：简单移动平均
                ma_short = hist_df['close'].rolling(10).mean().iloc[-1]
                ma_long = hist_df['close'].rolling(30).mean().iloc[-1]
                signal = 'buy' if ma_short > ma_long else 'sell'
            
            # 执行交易
            if signal == 'buy' and self.position == 0:
                # 买入
                shares = int(self.capital * 0.95 / current_price)  # 使用 95% 资金
                if shares > 0:
                    cost = shares * current_price * (1 + self.commission)
                    self.capital -= cost
                    self.position = shares
                    self.trades.append({
                        'date': current_date,
                        'type': 'buy',
                        'price': current_price,
                        'shares': shares,
                        'cost': cost
                    })
            
            elif signal == 'sell' and self.position > 0:
                # 卖出
                revenue = self.position * current_price * (1 - self.commission)
                self.capital += revenue
                self.trades.append({
                    'date': current_date,
                    'type': 'sell',
                    'price': current_price,
                    'shares': self.position,
                    'revenue': revenue
                })
                self.position = 0
            
            # 记录组合价值
            portfolio_value = self.capital + (self.position * current_price if self.position > 0 else 0)
            self.portfolio_values.append({
                'date': current_date,
                'value': portfolio_value
            })
        
        # 平仓
        if self.position > 0:
            final_price = df.iloc[-1]['close']
            revenue = self.position * final_price * (1 - self.commission)
            self.capital += revenue
            self.trades.append({
                'date': df.index[-1],
                'type': 'sell',
                'price': final_price,
                'shares': self.position,
                'revenue': revenue
            })
            self.position = 0
        
        # 计算结果
        results = self.calculate_results(df)
        return results
    
    def calculate_results(self, df):
        """计算回测结果"""
        portfolio_df = pd.DataFrame(self.portfolio_values)
        portfolio_df = portfolio_df.set_index('date')
        
        # 总收益率
        final_value = self.capital
        total_return = (final_value - self.initial_capital) / self.initial_capital
        
        # 计算每日收益率
        daily_returns = portfolio_df['value'].pct_change().dropna()
        
        # 年化收益率
        trading_days = len(df)
        years = trading_days / 252
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 夏普比率 (假设无风险利率 3%)
        risk_free_rate = 0.03
        if len(daily_returns) > 0 and daily_returns.std() != 0:
            sharpe_ratio = (annual_return - risk_free_rate) / (daily_returns.std() * np.sqrt(252))
        else:
            sharpe_ratio = 0
        
        # 最大回撤
        peak = portfolio_df['value'].cummax()
        drawdown = (portfolio_df['value'] - peak) / peak
        max_drawdown = drawdown.min()
        
        # 胜率
        buy_trades = [t for t in self.trades if t['type'] == 'buy']
        sell_trades = [t for t in self.trades if t['type'] == 'sell']
        
        winning_trades = 0
        for i, sell in enumerate(sell_trades):
            if i < len(buy_trades):
                if sell['price'] > buy_trades[i]['price']:
                    winning_trades += 1
        
        win_rate = winning_trades / len(sell_trades) if len(sell_trades) > 0 else 0
        
        results = {
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'final_value': final_value,
            'total_trades': len(self.trades),
            'portfolio_values': portfolio_df
        }
        
        # 打印结果
        print("\n" + "=" * 50)
        print(f"回测结果：{self.symbol}")
        print(f"回测区间：{self.start_date} ~ {self.end_date}")
        print("=" * 50)
        print(f"初始资金：¥{self.initial_capital:,.2f}")
        print(f"最终价值：¥{final_value:,.2f}")
        print(f"总收益率：{total_return:.2%}")
        print(f"年化收益率：{annual_return:.2%}")
        print(f"夏普比率：{sharpe_ratio:.2f}")
        print(f"最大回撤：{max_drawdown:.2%}")
        print(f"胜率：{win_rate:.2%}")
        print(f"交易次数：{len(self.trades)}")
        print("=" * 50)
        
        return results
    
    def plot(self, results):
        """绘制回测结果"""
        if results is None:
            return
        
        portfolio_df = results['portfolio_values']
        
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # 组合价值曲线
        axes[0].plot(portfolio_df.index, portfolio_df['value'], label='Portfolio Value')
        axes[0].axhline(y=self.initial_capital, color='r', linestyle='--', label='Initial Capital')
        axes[0].set_title(f'Portfolio Value ({self.symbol})')
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Value (¥)')
        axes[0].legend()
        axes[0].grid(True)
        
        # 回撤曲线
        drawdown = (portfolio_df['value'] - portfolio_df['value'].cummax()) / portfolio_df['value'].cummax()
        axes[1].fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
        axes[1].set_title('Drawdown')
        axes[1].set_xlabel('Date')
        axes[1].set_ylabel('Drawdown')
        axes[1].grid(True)
        
        plt.tight_layout()
        plt.show()


# 默认策略（简单移动平均）
class SimpleMAStrategy:
    """简单移动平均策略"""
    
    def __init__(self, config):
        self.short_period = config.get('short_period', 10)
        self.long_period = config.get('long_period', 30)
    
    def analyze(self, df):
        prices = df['close']
        ma_short = prices.rolling(self.short_period).mean()
        ma_long = prices.rolling(self.long_period).mean()
        
        if ma_short.iloc[-1] > ma_long.iloc[-1] and ma_short.iloc[-2] <= ma_long.iloc[-2]:
            return {'signal': 'buy'}
        elif ma_short.iloc[-1] < ma_long.iloc[-1] and ma_short.iloc[-2] >= ma_long.iloc[-2]:
            return {'signal': 'sell'}
        else:
            return {'signal': 'hold'}


# RSI 策略
class RSIStrategy:
    """RSI 策略"""
    
    def __init__(self, config):
        self.period = config.get('period', 14)
        self.overbought = config.get('overbought', 70)
        self.oversold = config.get('oversold', 30)
    
    def analyze(self, df):
        prices = df['close']
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        with np.errstate(divide='ignore', invalid='ignore'):
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
        
        current_rsi = rsi.iloc[-1]
        
        if current_rsi < self.oversold:
            return {'signal': 'buy', 'rsi': current_rsi}
        elif current_rsi > self.overbought:
            return {'signal': 'sell', 'rsi': current_rsi}
        else:
            return {'signal': 'hold', 'rsi': current_rsi}


def main():
    parser = argparse.ArgumentParser(description='策略回测')
    parser.add_argument('--strategy', type=str, default='ma', 
                        choices=['ma', 'rsi', 'multi'],
                        help='策略类型：ma(移动平均), rsi, multi(多指标)')
    parser.add_argument('--symbol', type=str, required=True, 
                        help='股票代码 (如 600519.SS, 0700.HK, AAPL)')
    parser.add_argument('--start', type=str, default='2023-01-01',
                        help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default='2023-12-31',
                        help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--capital', type=float, default=100000,
                        help='初始资金')
    parser.add_argument('--commission', type=float, default=0.001,
                        help='手续费率')
    parser.add_argument('--plot', action='store_true',
                        help='绘制结果图表')
    
    args = parser.parse_args()
    
    # 选择策略
    if args.strategy == 'ma':
        strategy = SimpleMAStrategy
    elif args.strategy == 'rsi':
        strategy = RSIStrategy
    else:
        # 多指标策略（需要导入）
        strategy = SimpleMAStrategy  # 默认使用 MA
    
    # 运行回测
    bt = Backtest(
        strategy=strategy,
        symbol=args.symbol,
        start_date=args.start,
        end_date=args.end,
        initial_capital=args.capital,
        commission=args.commission
    )
    
    results = bt.run()
    
    if results and args.plot:
        bt.plot(results)


if __name__ == '__main__':
    main()
