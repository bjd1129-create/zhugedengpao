#!/usr/bin/env python3
"""
股票实时监控脚本
- 监控 A 股 + 港股 + 美股
- RSI/MACD/布林带多指标分析
- 自动推送买卖信号
- 非交易时段静默
"""

import sys
import time
import yaml
import logging
from datetime import datetime, time as dt_time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path.home() / 'clawd' / 'quant-trading'))

try:
    import pandas as pd
    import numpy as np
    from akshare import stock_zh_a_hist, stock_hk_hist, stock_us_hist
    import requests
except ImportError as e:
    print(f"缺少依赖：{e}")
    print("请安装：pip install pandas numpy akshare requests pyyaml")
    sys.exit(1)

# 配置
CONFIG_PATH = Path.home() / 'clawd' / 'quant-trading' / 'config.yaml'
LOG_PATH = Path.home() / 'clawd' / 'quant-trading' / 'logs' / 'monitor.log'

# 确保日志目录存在
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_config():
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        logger.warning(f"配置文件不存在：{CONFIG_PATH}，使用默认配置")
        return {
            'symbols': ['600519.SS', '0700.HK', 'AAPL'],
            'push': {'feishu': {'enabled': False}}
        }
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def is_trading_time(market='A'):
    """
    检查当前是否为交易时间
    
    Args:
        market: 'A' (A 股), 'HK' (港股), 'US' (美股)
    
    Returns:
        bool: 是否在交易时段
    """
    now = datetime.now()
    weekday = now.weekday()
    
    # 周末休市
    if weekday >= 5:
        return False
    
    current_time = now.time()
    
    if market == 'A':
        # A 股：09:30-11:30, 13:00-15:00
        morning = dt_time(9, 30) <= current_time <= dt_time(11, 30)
        afternoon = dt_time(13, 0) <= current_time <= dt_time(15, 0)
        return morning or afternoon
    
    elif market == 'HK':
        # 港股：09:30-12:00, 13:00-16:00
        morning = dt_time(9, 30) <= current_time <= dt_time(12, 0)
        afternoon = dt_time(13, 0) <= current_time <= dt_time(16, 0)
        return morning or afternoon
    
    elif market == 'US':
        # 美股（美东时间）：21:30-次日 04:00（考虑夏令时/冬令时）
        # 简化处理：北京时间 21:30-次日 04:00
        us_start = dt_time(21, 30)
        us_end = dt_time(4, 0)
        return current_time >= us_start or current_time <= us_end
    
    return False


def calculate_rsi(prices, period=14):
    """计算 RSI 指标"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    with np.errstate(divide='ignore', invalid='ignore'):
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
    
    return rsi.iloc[-1] if len(rsi) > 0 else 50


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """计算 MACD 指标"""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd_bar = (dif - dea) * 2
    
    return {
        'dif': dif.iloc[-1] if len(dif) > 0 else 0,
        'dea': dea.iloc[-1] if len(dea) > 0 else 0,
        'bar': macd_bar.iloc[-1] if len(macd_bar) > 0 else 0,
        'prev_dif': dif.iloc[-2] if len(dif) > 1 else 0,
        'prev_dea': dea.iloc[-2] if len(dea) > 1 else 0
    }


def calculate_bollinger(prices, period=20, std_dev=2):
    """计算布林带"""
    middle = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = middle + (std_dev * std)
    lower = middle - (std_dev * std)
    
    current_price = prices.iloc[-1] if len(prices) > 0 else 0
    
    return {
        'upper': upper.iloc[-1] if len(upper) > 0 else 0,
        'middle': middle.iloc[-1] if len(middle) > 0 else 0,
        'lower': lower.iloc[-1] if len(lower) > 0 else 0,
        'price': current_price,
        'position': (current_price - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1]) if len(upper) > 0 and len(lower) > 0 else 0.5
    }


def fetch_stock_data(symbol):
    """
    获取股票历史数据
    
    Args:
        symbol: 股票代码 (如 600519.SS, 0700.HK, AAPL)
    
    Returns:
        pd.DataFrame: 包含 OHLCV 数据
    """
    try:
        if '.SS' in symbol or '.SZ' in symbol:
            # A 股
            df = stock_zh_a_hist(symbol.replace('.SS', '').replace('.SZ', ''), period="daily")
        elif '.HK' in symbol:
            # 港股
            df = stock_hk_hist(symbol.replace('.HK', ''), period="daily")
        else:
            # 美股
            df = stock_us_hist(symbol, period="daily")
        
        # 标准化列名
        df = df.rename(columns={
            '日期': 'date',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume'
        })
        
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df = df.dropna(subset=['close'])
        
        return df
    
    except Exception as e:
        logger.error(f"获取 {symbol} 数据失败：{e}")
        return None


def generate_signal(rsi, macd, bollinger):
    """
    生成交易信号
    
    Returns:
        tuple: (signal, confidence, reason)
            signal: 'buy', 'sell', 'hold'
            confidence: 0-1
            reason: 信号原因
    """
    buy_signals = 0
    sell_signals = 0
    reasons = []
    
    # RSI 信号
    if rsi < 30:
        buy_signals += 1
        reasons.append(f"RSI 超卖 ({rsi:.1f})")
    elif rsi > 70:
        sell_signals += 1
        reasons.append(f"RSI 超买 ({rsi:.1f})")
    
    # MACD 信号
    if macd['dif'] > macd['dea'] and macd['prev_dif'] <= macd['prev_dea']:
        buy_signals += 1
        reasons.append("MACD 金叉")
    elif macd['dif'] < macd['dea'] and macd['prev_dif'] >= macd['prev_dea']:
        sell_signals += 1
        reasons.append("MACD 死叉")
    
    # 布林带信号
    if bollinger['position'] < 0.1:
        buy_signals += 1
        reasons.append("布林带下轨")
    elif bollinger['position'] > 0.9:
        sell_signals += 1
        reasons.append("布林带上轨")
    
    # 生成最终信号
    if buy_signals >= 2:
        confidence = min(buy_signals / 3, 1.0)
        return 'buy', confidence, ', '.join(reasons)
    elif sell_signals >= 2:
        confidence = min(sell_signals / 3, 1.0)
        return 'sell', confidence, ', '.join(reasons)
    else:
        return 'hold', 0, '无明确信号'


def push_signal(symbol, signal, confidence, reason, price, rsi, macd, bollinger):
    """推送交易信号"""
    config = load_config()
    push_config = config.get('push', {})
    
    message = None
    
    if signal == 'buy':
        emoji = '🟢' if confidence > 0.6 else '🟡'
        message = f"""{emoji} 买入信号
股票代码：{symbol}
当前价格：{price:.2f}
置信度：{confidence:.1%}
RSI: {rsi:.1f}
MACD: {macd['dif']:.2f} / {macd['dea']:.2f}
布林带：{bollinger['position']:.1%}
原因：{reason}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    elif signal == 'sell':
        emoji = '🔴' if confidence > 0.6 else '🟡'
        message = f"""{emoji} 卖出信号
股票代码：{symbol}
当前价格：{price:.2f}
置信度：{confidence:.1%}
RSI: {rsi:.1f}
MACD: {macd['dif']:.2f} / {macd['dea']:.2f}
布林带：{bollinger['position']:.1%}
原因：{reason}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    if message and push_config.get('feishu', {}).get('enabled'):
        try:
            webhook_url = push_config['feishu'].get('webhook_url')
            if webhook_url:
                payload = {
                    "msg_type": "text",
                    "content": {"text": message}
                }
                requests.post(webhook_url, json=payload, timeout=10)
                logger.info(f"信号已推送：{symbol} {signal}")
        except Exception as e:
            logger.error(f"推送失败：{e}")
    
    # 打印到控制台
    print(message)
    print("-" * 50)


def monitor_symbol(symbol):
    """监控单只股票"""
    logger.info(f"分析 {symbol}...")
    
    df = fetch_stock_data(symbol)
    if df is None or len(df) < 30:
        logger.warning(f"{symbol} 数据不足，跳过")
        return
    
    prices = df['close']
    current_price = prices.iloc[-1]
    
    # 计算指标
    rsi = calculate_rsi(prices)
    macd = calculate_macd(prices)
    bollinger = calculate_bollinger(prices)
    
    # 生成信号
    signal, confidence, reason = generate_signal(rsi, macd, bollinger)
    
    # 只在有明确信号时推送
    if signal != 'hold' and confidence > 0.5:
        push_signal(symbol, signal, confidence, reason, current_price, rsi, macd, bollinger)
    else:
        logger.info(f"{symbol}: 持有 (RSI={rsi:.1f})")


def main():
    """主函数"""
    config = load_config()
    symbols = config.get('symbols', ['600519.SS', '0700.HK', 'AAPL'])
    
    logger.info("=" * 50)
    logger.info("股票监控启动")
    logger.info(f"监控标的：{symbols}")
    logger.info("=" * 50)
    
    while True:
        try:
            now = datetime.now()
            
            # 检查交易时段
            trading = False
            if is_trading_time('A') or is_trading_time('HK'):
                trading = True
                logger.info("A 股/港股交易时段")
            elif is_trading_time('US'):
                trading = True
                logger.info("美股交易时段")
            
            if trading:
                # 监控所有标的
                for symbol in symbols:
                    monitor_symbol(symbol)
                
                # 每 5 分钟检查一次
                logger.info("等待 5 分钟后再次检查...")
                time.sleep(300)
            else:
                # 非交易时段，静默等待
                next_check = 60  # 1 分钟后检查是否进入交易时段
                logger.info(f"非交易时段，{next_check}秒后检查...")
                time.sleep(next_check)
        
        except KeyboardInterrupt:
            logger.info("监控停止")
            break
        except Exception as e:
            logger.error(f"监控异常：{e}")
            time.sleep(60)


if __name__ == '__main__':
    main()
