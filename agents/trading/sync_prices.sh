#!/bin/bash
# 每分钟把最新的 price_aggregate.json 推送到 GitHub + 部署到 CF Pages
# 放在 crontab: * * * * * /Users/bjd/Desktop/ZhugeDengpao-Team/agents/trading/sync_prices.sh
cd /Users/bjd/Desktop/ZhugeDengpao-Team

FILE="data/trading/price_aggregate.json"
LOG="/tmp/price_sync.log"

# 检查文件是否存在且最近有更新（30秒内）
if [ -f "$FILE" ]; then
    AGE=$(($(date +%s) - $(stat -f %m "$FILE" 2>/dev/null || stat -c %Y "$FILE" 2>/dev/null)))
    if [ "$AGE" -lt 60 ]; then
        git add "$FILE" 2>/dev/null
        git commit -m "sync: prices $(date '+%H:%M')" 2>/dev/null
        git push origin main 2>/dev/null
        echo "[$(date '+%H:%M:%S')] synced (age=${AGE}s)" >> "$LOG"
    else
        echo "[$(date '+%H:%M:%S')] skipped (age=${AGE}s, server may be down)" >> "$LOG"
    fi
fi
