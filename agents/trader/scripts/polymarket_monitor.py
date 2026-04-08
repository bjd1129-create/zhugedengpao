# Polymarket 监控脚本 v1.0
**最后更新**: 2026-04-08 21:45
**功能**: 每 30 分钟检查持仓盈亏，触发告警

import json
import time
from datetime import datetime
from pathlib import Path

# 配置
CHECK_INTERVAL = 1800  # 30 分钟
STOP_LOSS_PCT = -0.50  # -50% 止损
TAKE_PROFIT_PCT = 1.00  # +100% 止盈

def load_portfolio():
    """加载投资组合"""
    portfolio_file = Path(__file__).parent.parent / "data" / "polymarket_portfolio.json"
    with open(portfolio_file, "r", encoding="utf-8") as f:
        return json.load(f)

def check_positions(portfolio):
    """检查持仓状态"""
    alerts = []
    
    for position in portfolio["positions"]:
        pnl_pct = position["pnl_pct"] / 100  # 转换为小数
        
        # 止损检查
        if pnl_pct <= STOP_LOSS_PCT:
            alerts.append({
                "type": "STOP_LOSS",
                "market": position["question"],
                "outcome": position["outcome"],
                "pnl_pct": pnl_pct * 100,
                "action": "立即平仓 50%"
            })
        
        # 止盈检查
        if pnl_pct >= TAKE_PROFIT_PCT:
            alerts.append({
                "type": "TAKE_PROFIT",
                "market": position["question"],
                "outcome": position["outcome"],
                "pnl_pct": pnl_pct * 100,
                "action": "减持 50%"
            })
    
    return alerts

def generate_alert_message(alerts, portfolio):
    """生成告警消息"""
    if not alerts:
        return None
    
    message = "🚨【Polymarket 监控告警】\n\n"
    
    for alert in alerts:
        message += f"""
{alert['type']} 触发:
- 市场：{alert['market']}
- 选项：{alert['outcome']}
- 盈亏：{alert['pnl_pct']:.1f}%
- 操作：{alert['action']}

"""
    
    # 添加账户汇总
    total_value = sum(p["current_value"] for p in portfolio["positions"])
    total_cost = portfolio["account"]["invested"]
    total_pnl = total_value - total_cost
    
    message += f"""
---

📊 账户汇总:
- 总投入：${total_cost:,.2f}
- 现值：${total_value:,.2f}
- 总盈亏：${total_pnl:,.2f} ({total_pnl/total_cost*100:.1f}%)

@交易员 请立即处理！
"""
    
    return message

def main():
    """主循环"""
    print(f"[{datetime.now().isoformat()}] Polymarket 监控启动...")
    print(f"检查间隔：{CHECK_INTERVAL}秒")
    print(f"止损线：{STOP_LOSS_PCT*100:.0f}%")
    print(f"止盈线：{TAKE_PROFIT_PCT*100:.0f}%")
    
    while True:
        try:
            portfolio = load_portfolio()
            alerts = check_positions(portfolio)
            
            if alerts:
                message = generate_alert_message(alerts, portfolio)
                print(f"\n[{datetime.now().isoformat()}] 告警触发:")
                print(message)
                # TODO: 发送到 sessions_send 或飞书
            else:
                print(f"[{datetime.now().isoformat()}] 无告警，持仓正常")
            
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] 错误：{e}")
            time.sleep(60)  # 错误时等待 1 分钟

if __name__ == "__main__":
    main()
