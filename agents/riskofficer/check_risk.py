#!/usr/bin/env python3
"""Risk Officer - Quick risk check, no AI needed."""
import json
import os
from datetime import datetime

PORTFOLIO = os.path.expanduser("~/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json")
MEMORY = os.path.expanduser("~/Desktop/ZhugeDengpao-Team/agents/riskofficer/MEMORY.md")

with open(PORTFOLIO) as f:
    p = json.load(f)

total = p['account']['totalValue']
initial = p['account']['initialBalance']
cash = p['account']['cashBalance']

if total <= initial * 0.95:
    status = "🔴"
    msg = f"止损! 总值=${total:.2f}"
elif total <= initial * 0.98:
    status = "🟡"
    msg = f"警告! 总值=${total:.2f}"
elif total >= initial * 1.05:
    status = "🎯"
    msg = f"止盈! 总值=${total:.2f}"
else:
    status = "🟢"
    msg = f"正常 总值=${total:.2f}"

now = datetime.now().strftime("%Y-%m-%d %H:%M")
with open(MEMORY) as f:
    content = f.read()

new = f"# RiskOfficer | {now}\n{status} {msg}\nCash=${cash:.2f}\n\n---\n\n" + content[:2000]
with open(MEMORY, 'w') as f:
    f.write(new)

print(f"[{now}] {status} {msg}")
