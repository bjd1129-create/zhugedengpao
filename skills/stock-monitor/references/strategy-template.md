# 策略开发模板

## 策略文件结构

```python
# strategies/my_strategy.py

class MyStrategy:
    """自定义策略类"""
    
    def __init__(self, config):
        self.config = config
        self.name = "my_strategy"
    
    def analyze(self, df):
        """
        分析行情数据
        
        Args:
            df: DataFrame，包含 OHLCV 数据
            
        Returns:
            dict: 分析结果，包含信号和指标值
        """
        # 计算指标
        rsi = self.calculate_rsi(df)
        macd = self.calculate_macd(df)
        bollinger = self.calculate_bollinger(df)
        
        # 生成信号
        signal = self.generate_signal(rsi, macd, bollinger)
        
        return {
            'signal': signal,  # 'buy', 'sell', 'hold'
            'rsi': rsi,
            'macd': macd,
            'bollinger': bollinger,
            'confidence': self.calculate_confidence(rsi, macd, bollinger)
        }
    
    def calculate_rsi(self, df, period=14):
        """计算 RSI 指标"""
        # TODO: 实现 RSI 计算
        pass
    
    def calculate_macd(self, df, fast=12, slow=26, signal=9):
        """计算 MACD 指标"""
        # TODO: 实现 MACD 计算
        pass
    
    def calculate_bollinger(self, df, period=20, std_dev=2):
        """计算布林带"""
        # TODO: 实现布林带计算
        pass
    
    def generate_signal(self, rsi, macd, bollinger):
        """
        生成交易信号
        
        逻辑示例：
        - RSI < 30 且 MACD 金叉 → 买入
        - RSI > 70 且 MACD 死叉 → 卖出
        - 其他情况 → 持有
        """
        # TODO: 实现信号生成逻辑
        pass
    
    def calculate_confidence(self, rsi, macd, bollinger):
        """
        计算信号置信度 (0-1)
        
        多指标共振时置信度更高
        """
        # TODO: 实现置信度计算
        pass
```

## 回测接口

```python
from backtest import Backtest

# 初始化回测
bt = Backtest(
    strategy=MyStrategy,
    symbol='600519.SS',
    start_date='2023-01-01',
    end_date='2023-12-31',
    initial_capital=100000,
    commission=0.001  # 手续费 0.1%
)

# 运行回测
results = bt.run()

# 输出结果
print(f"总收益率：{results['total_return']:.2%}")
print(f"夏普比率：{results['sharpe_ratio']:.2f}")
print(f"最大回撤：{results['max_drawdown']:.2%}")
print(f"胜率：{results['win_rate']:.2%}")
```

## 指标计算参考

### RSI 计算公式
```python
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

### MACD 计算公式
```python
def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd_bar = (dif - dea) * 2
    return {'dif': dif, 'dea': dea, 'bar': macd_bar}
```

### 布林带计算公式
```python
def calculate_bollinger(prices, period=20, std_dev=2):
    middle = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = middle + (std_dev * std)
    lower = middle - (std_dev * std)
    return {'upper': upper, 'middle': middle, 'lower': lower}
```

## 策略优化建议

1. **参数调优**: 使用网格搜索或贝叶斯优化寻找最优参数
2. **止损止盈**: 添加止损止盈逻辑控制风险
3. **仓位管理**: 实现动态仓位调整（如凯利公式）
4. **多品种分散**: 在多个股票/市场测试策略稳健性
5. **避免过拟合**: 使用交叉验证，保留样本外测试集

## 常用策略示例

### RSI 均值回归
```python
def generate_signal(self, rsi, macd, bollinger):
    if rsi['current'] < 30:
        return 'buy'
    elif rsi['current'] > 70:
        return 'sell'
    else:
        return 'hold'
```

### MACD 趋势跟踪
```python
def generate_signal(self, rsi, macd, bollinger):
    if macd['dif'] > macd['dea'] and macd['prev_dif'] <= macd['prev_dea']:
        return 'buy'  # 金叉
    elif macd['dif'] < macd['dea'] and macd['prev_dif'] >= macd['prev_dea']:
        return 'sell'  # 死叉
    else:
        return 'hold'
```

### 多指标融合
```python
def generate_signal(self, rsi, macd, bollinger):
    buy_signals = 0
    sell_signals = 0
    
    # RSI 信号
    if rsi['current'] < 30:
        buy_signals += 1
    elif rsi['current'] > 70:
        sell_signals += 1
    
    # MACD 信号
    if macd['dif'] > macd['dea']:
        buy_signals += 1
    else:
        sell_signals += 1
    
    # 布林带信号
    if bollinger['price'] < bollinger['lower']:
        buy_signals += 1
    elif bollinger['price'] > bollinger['upper']:
        sell_signals += 1
    
    # 多指标共振
    if buy_signals >= 2:
        return 'buy'
    elif sell_signals >= 2:
        return 'sell'
    else:
        return 'hold'
```
