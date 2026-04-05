#!/usr/bin/env python3
"""
老虎证券模拟盘数据更新脚本
从 Tiger OpenAPI 获取账户数据，写入 website/data/trading/tiger_us_paper.json
"""
import sys
import json
import datetime
sys.path.insert(0, '/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader')
from tiger_connection import get_assets, get_positions, get_orders

OUTPUT = '/Users/bjd/Desktop/ZhugeDengpao-Team/website/data/trading/tiger_us_paper.json'

# 价值定投策略配置
STRATEGY_ALLOCATION = {
    "SPY": {"name": "SPDR S&P 500 ETF", "target": 0.40, "mode": "月定投"},
    "QQQ": {"name": "Invesco QQQ Trust", "target": 0.30, "mode": "月定投"},
    "VTI": {"name": "Vanguard Total Stock Market", "target": 0.20, "mode": "月定投"},
    "BND": {"name": "Vanguard Total Bond Market", "target": 0.10, "mode": "月定投"},
}

def main():
    result = {
        "updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "account": "21639635499102726",
        "type": "PAPER",
        "currency": "USD",
        "strategy": {
            "name": "价值定投策略 v1.0",
            "description": "月定投 $10,000 · 季度再平衡 · 股息复利 · 再平衡阈值 5%",
            "allocation": STRATEGY_ALLOCATION,
        },
        "quotes": {},
        "positions": [],
        "orders": [],
    }

    # 账户资产
    assets_data = get_assets()
    items = json.loads(assets_data["data"])["items"]
    for a in items:
        net_liq = a.get("netLiquidation", 0)
        cash = a.get("cashValue", 0)
        buying_power = a.get("buyingPower", 0)
        realized_pnl = a.get("realizedPnL", 0)
        unrealized_pnl = a.get("unrealizedPnL", 0)
        gross_pos_value = 0
        for seg in a.get("segments", []):
            if seg.get("category") == "S":
                gross_pos_value = seg.get("grossPositionValue", 0)
        
        result["account"] = {
            "net_liquidation": net_liq,
            "cash": cash,
            "gross_position_value": gross_pos_value,
            "realized_pnl": realized_pnl,
            "unrealized_pnl": unrealized_pnl,
            "buying_power": buying_power,
        }
        # 兼容字段（直接放顶层）
        result["net_liquidation"] = net_liq
        result["cash_value"] = cash
        result["position_value"] = gross_pos_value
        result["realized_pnl"] = realized_pnl
        result["unrealized_pnl"] = unrealized_pnl

    # 持仓
    positions_data = get_positions()
    pos_items = json.loads(positions_data["data"]).get("items", [])
    for p in pos_items:
        contract = p.get("contract", {})
        sym = contract.get("symbol", "") if isinstance(contract, dict) else ""
        result["positions"].append({
            "symbol": sym,
            "quantity": p.get("quantity", 0),
            "market_value": p.get("market_value", 0),
            "avg_cost": p.get("average_cost", 0),
            "unrealized_pnl": p.get("unrealized_pnl", 0),
            "unrealized_pnl_ratio": p.get("unrealized_pnl_percent", 0),
        })
        # 如果有持仓，从Yahoo Finance补充行情（需要单独实现）
        if sym:
            result["quotes"][sym] = {"last": p.get("market_price", 0), "change_pct": 0}

    # 订单
    orders_data = get_orders(limit=20)
    ord_items = json.loads(orders_data["data"]).get("items", [])
    for o in ord_items:
        contract = o.get("contract", {})
        result["orders"].append({
            "order_id": o.get("order_id", ""),
            "symbol": contract.get("symbol", "") if isinstance(contract, dict) else "",
            "action": o.get("action", ""),
            "quantity": o.get("quantity", 0),
            "order_type": o.get("order_type", ""),
            "status": o.get("status", ""),
            "filled_qty": o.get("filled", 0),
            "order_time": o.get("order_time", ""),
        })

    with open(OUTPUT, 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已更新 {OUTPUT}")
    print(f"   净值: ${result.get('net_liquidation', 0):,.2f} | 现金: ${result.get('cash_value', 0):,.2f} | 持仓: {len(result['positions'])}个")

if __name__ == "__main__":
    main()
