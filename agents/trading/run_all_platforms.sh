#!/bin/bash
# 三平台并行交易脚本
export HTTPS_PROXY="http://127.0.0.1:7897"
export http_proxy="http://127.0.0.1:7897"

LOG="/tmp/multi_platform.log"
BASE="/Users/bjd/Desktop/ZhugeDengpao-Team"

while true; do
    DATE=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$DATE]" >> $LOG
    
    # 三平台并行运行
    python3 "$BASE/agents/trading/binance_sim.py" >> $LOG 2>&1 &
    python3 "$BASE/agents/trading/okx_sim.py" >> $LOG 2>&1 &
    python3 "$BASE/agents/trading/bybit_sim.py" >> $LOG 2>&1 &
    
    wait
    
    echo "---" >> $LOG
    sleep 300  # 每5分钟
done
