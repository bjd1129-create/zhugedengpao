# 推送渠道配置

## 支持的推送渠道

### 飞书 (Feishu)
```yaml
feishu:
  enabled: true
  webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  mention_users: ["ou_xxx"]  # 可选，@特定用户
```

### 微信 (WeChat)
```yaml
wechat:
  enabled: false
  corp_id: "xxx"
  agent_id: "xxx"
  secret: "xxx"
```

### Telegram
```yaml
telegram:
  enabled: false
  bot_token: "xxx"
  chat_id: "xxx"
```

### 邮件 (Email)
```yaml
email:
  enabled: false
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender: "alert@example.com"
  recipients: ["user@example.com"]
  username: "xxx"
  password: "xxx"
```

## 配置位置

`~/clawd/quant-trading/config.yaml`

## 推送模板

### 买入信号
```
🟢 买入信号
股票代码：{symbol}
当前价格：{price}
RSI: {rsi}
MACD: {macd_signal}
布林带：{bollinger_position}
时间：{timestamp}
```

### 卖出信号
```
🔴 卖出信号
股票代码：{symbol}
当前价格：{price}
RSI: {rsi}
MACD: {macd_signal}
布林带：{bollinger_position}
时间：{timestamp}
```

### 预警提示
```
🟡 预警提示
股票代码：{symbol}
预警类型：{alert_type}  # 超买/超卖
当前值：{current_value}
阈值：{threshold}
时间：{timestamp}
```
