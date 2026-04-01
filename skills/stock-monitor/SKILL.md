---
name: stock-monitor
description: 股票实时监控和交易信号推送。使用当需要：(1) 监控 A 股/港股/美股实时行情，(2) 分析 RSI/MACD/布林带等技术指标，(3) 接收买卖信号自动推送，(4) 执行策略回测验证，(5) 设置超买超卖预警。支持交易时段自动运行，非交易时段静默。
---

# 股票监控技能

## 快速启动

### 实时监控

```bash
cd ~/clawd/stock-assistant
source venv/bin/activate  # Linux/Mac
# 或 .\venv\Scripts\Activate.ps1  # Windows

python3 ~/clawd/quant-trading/realtime_monitor.py
```

**监控时段：**
- A 股 + 港股：09:00-16:00（工作日）
- 美股：20:30-次日 05:00（美东时间）

**功能：**
- 多指标融合分析（RSI/MACD/布林带）
- 买入/卖出信号自动推送
- 超买/超卖预警
- 非交易时段自动静默

### 策略回测

```bash
python3 ~/clawd/quant-trading/backtest.py --strategy <策略名> --symbol <股票代码> --period <回测周期>
```

**示例：**
```bash
# 回测茅台的 RSI 策略（过去一年）
python3 ~/clawd/quant-trading/backtest.py --strategy rsi --symbol 600519.SS --period 1y

# 回测腾讯的多指标策略（过去 6 个月）
python3 ~/clawd/quant-trading/backtest.py --strategy multi --symbol 0700.HK --period 6m
```

## 核心指标

### RSI（相对强弱指标）
- **超买区**: RSI > 70 → 考虑卖出
- **超卖区**: RSI < 30 → 考虑买入
- **中性区**: 30 ≤ RSI ≤ 70

### MACD（移动平均收敛散度）
- **金叉**: DIF 上穿 DEA → 买入信号
- **死叉**: DIF 下穿 DEA → 卖出信号
- **背离**: 价格新高但 MACD 未新高 → 反转预警

### 布林带（Bollinger Bands）
- **触及上轨**: 可能超买，关注回调
- **触及下轨**: 可能超卖，关注反弹
- **带宽收缩**: 波动率降低，即将变盘

## 信号推送配置

推送渠道配置见 `references/channels.md`。

**信号等级：**
- 🔴 **红色**: 强烈买卖信号（多指标共振）
- 🟡 **黄色**: 单一指标信号（需确认）
- 🟢 **绿色**: 预警提示（超买/超卖）

## 自定义策略

创建新策略参考 `references/strategy-template.md`。

**策略文件位置**: `~/clawd/quant-trading/strategies/`

## 注意事项

1. **交易时段检查**: 脚本自动检测当前是否为交易时段，非交易时段不推送信号
2. **数据延迟**: 实时数据可能有 15 分钟延迟（免费 API）
3. **风险提示**: 技术指标仅供参考，不构成投资建议
4. **回测局限**: 历史表现不代表未来收益

## 相关文件

- **监控脚本**: `~/clawd/quant-trading/realtime_monitor.py`
- **回测脚本**: `~/clawd/quant-trading/backtest.py`
- **策略目录**: `~/clawd/quant-trading/strategies/`
- **配置文件**: `~/clawd/quant-trading/config.yaml`

## 故障排查

**问题**: 监控脚本无法启动
- 检查虚拟环境是否激活
- 确认数据 API key 有效
- 查看日志 `~/clawd/quant-trading/logs/monitor.log`

**问题**: 信号推送失败
- 检查推送渠道配置
- 确认网络连接
- 验证推送 token/密钥
