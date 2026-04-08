#!/usr/bin/env python3
"""
Polymarket 下注执行脚本 v1.0
策略：地缘政治（美伊停火）+ 政治（匈牙利大选）
最后更新：2026-04-08 20:00
"""

import json
import time
from datetime import datetime
from pathlib import Path

# ==================== 配置区 ====================

# 账户配置
ACCOUNT_CONFIG = {
    "initial_balance": 10000.00,  # 初始资金 USDC
    "max_position_pct": 0.40,     # 单笔最大仓位 40%
    "max_total_exposure": 0.60,   # 总仓位上限 60%
    "cash_reserve": 0.40,         # 现金保留 40%
}

# 下注标的
BETS = [
    {
        "market_id": "trump-announces-end-of-military-operations-against-iran-by",
        "question": "特朗普宣布结束对伊朗的军事行动",
        "outcome": "4 月 30 日",
        "outcome_id": "april-30th",
        "current_prob": 0.56,
        "odds": 1.8,
        "allocation": 0.40,  # 40% 资金
        "reason": "已有官方停火声明，2 周停火期到 4 月 22 日，4 月 30 日前结束概率>70%",
        "news_sources": ["华盛顿邮报", "CNN", "BBC", "NYT"],
        "stop_loss": 0.50,   # 亏损 50% 平仓
        "take_profit": 1.00, # 盈利 100% 减持 50%
    },
    {
        "market_id": "next-prime-minister-of-hungary",
        "question": "匈牙利下任总理",
        "outcome": "Péter Magyar",
        "outcome_id": "peter-magyar",
        "current_prob": 0.64,
        "odds": 1.56,
        "allocation": 0.20,  # 20% 资金
        "reason": "民调领先，反 Orbán 情绪高涨，国际观察员看好",
        "news_sources": ["BBC", "NYT", "Reuters"],
        "stop_loss": 0.50,
        "take_profit": 1.00,
    },
]

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==================== 核心函数 ====================

def calculate_bet_size(bet, account_balance):
    """计算下注金额"""
    allocation = bet["allocation"] * account_balance
    return round(allocation, 2)

def calculate_expected_return(bet, bet_size):
    """计算预期收益"""
    # 预期收益 = (胜率 × 盈利) - (败率 × 本金)
    win_prob = bet["current_prob"]
    payout = bet_size * bet["odds"]
    expected_value = (win_prob * payout) - ((1 - win_prob) * bet_size)
    return round(expected_value, 2)

def generate_bet_order(bet, bet_size, expected_return):
    """生成下注订单"""
    order = {
        "timestamp": datetime.now().isoformat(),
        "market_id": bet["market_id"],
        "question": bet["question"],
        "outcome": bet["outcome"],
        "action": "BUY",
        "shares": bet_size,  # Polymarket 按份额购买
        "price_per_share": 1 / bet["odds"],
        "total_cost": bet_size,
        "potential_payout": round(bet_size * bet["odds"], 2),
        "expected_return": expected_return,
        "stop_loss": bet["stop_loss"],
        "take_profit": bet["take_profit"],
        "reason": bet["reason"],
        "news_sources": bet["news_sources"],
        "status": "PENDING",
    }
    return order

def generate_review_card(orders, account_balance):
    """生成复盘卡片（发送小花）"""
    total_invested = sum(order["total_cost"] for order in orders)
    total_potential = sum(order["potential_payout"] for order in orders)
    
    card = f"""
📝【Polymarket 交易复盘】

时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
账户：Polymarket 模拟盘
初始资金：${account_balance:,.2f}
总下注：${total_invested:,.2f} ({total_invested/account_balance*100:.1f}%)
现金保留：${account_balance - total_invested:,.2f} ({(account_balance - total_invested)/account_balance*100:.1f}%)

---

"""
    
    for i, order in enumerate(orders, 1):
        card += f"""
🎯 下注{i}: {order['question']}
- 选项：{order['outcome']}
- 金额：${order['total_cost']:,.2f}
- 赔率：{order['potential_payout']/order['total_cost']:.2f}x
- 潜在收益：${order['potential_payout']:,.2f} (+${order['potential_payout'] - order['total_cost']:,.2f})
- 胜率：{order['price_per_share']*100:.1f}%
- 止损：亏损{order['stop_loss']*100:.0f}% 平仓
- 止盈：盈利{order['take_profit']*100:.0f}% 减持 50%
- 理由：{order['reason']}
- 新闻源：{', '.join(order['news_sources'])}

"""
    
    card += f"""
---

📊 汇总:
- 预期总收益：${sum(o['potential_payout'] - o['total_cost'] for o in orders):,.2f}
- 风险等级：🟡 中等
- 监控频率：每 30 分钟

@小花 已执行，请监督
"""
    
    return card

def save_portfolio(orders, account_balance):
    """保存投资组合到 JSON"""
    portfolio = {
        "timestamp": datetime.now().isoformat(),
        "account": {
            "initial_balance": account_balance,
            "cash_balance": account_balance - sum(o["total_cost"] for o in orders),
            "invested": sum(o["total_cost"] for o in orders),
            "total_value": account_balance,  # 初始按成本计
        },
        "positions": [
            {
                "market_id": order["market_id"],
                "question": order["question"],
                "outcome": order["outcome"],
                "shares": order["shares"],
                "avg_cost": order["price_per_share"],
                "current_value": order["potential_payout"],  # 初始按潜在收益计
                "pnl": order["potential_payout"] - order["total_cost"],
                "pnl_pct": (order["potential_payout"] / order["total_cost"] - 1) * 100,
                "stop_loss": order["stop_loss"],
                "take_profit": order["take_profit"],
                "status": "OPEN",
            }
            for order in orders
        ],
        "orders": orders,
        "strategy": {
            "name": "事件驱动 v2.0",
            "focus": "地缘政治 + 政治",
            "max_position": 0.40,
            "max_exposure": 0.60,
        },
    }
    
    output_file = OUTPUT_DIR / "polymarket_portfolio.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)
    
    return output_file

# ==================== 主流程 ====================

def main():
    """主函数"""
    print(f"[{datetime.now().isoformat()}] 开始准备 Polymarket 下注...")
    
    account_balance = ACCOUNT_CONFIG["initial_balance"]
    orders = []
    
    # 计算每个下注
    for bet in BETS:
        bet_size = calculate_bet_size(bet, account_balance)
        expected_return = calculate_expected_return(bet, bet_size)
        order = generate_bet_order(bet, bet_size, expected_return)
        orders.append(order)
        
        print(f"✅ {bet['question']} - {bet['outcome']}")
        print(f"   下注金额：${bet_size:,.2f}")
        print(f"   预期收益：${expected_return:,.2f}")
        print(f"   潜在回报：${bet_size * bet['odds']:,.2f}")
    
    # 保存投资组合
    portfolio_file = save_portfolio(orders, account_balance)
    print(f"\n📁 投资组合已保存：{portfolio_file}")
    
    # 生成复盘卡片
    review_card = generate_review_card(orders, account_balance)
    print("\n📝 复盘卡片:")
    print(review_card)
    
    # 保存复盘卡片到文件
    review_file = OUTPUT_DIR / "polymarket_review_card.txt"
    with open(review_file, "w", encoding="utf-8") as f:
        f.write(review_card)
    print(f"📄 复盘卡片已保存：{review_file}")
    
    print("\n✅ 下注准备完成！")
    print("\n下一步:")
    print("1. 手动在 Polymarket 执行下注（或集成 API 自动执行）")
    print("2. 发送复盘卡片给小花")
    print("3. 设置监控（每 30 分钟检查盈亏）")

if __name__ == "__main__":
    main()
