#!/bin/bash
# 期货数据更新脚本
# 每 5 分钟更新一次期货价格和技术指标

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
DATA_DIR="$PROJECT_ROOT/analyst/data"
SYNC_SCRIPT="$SCRIPT_DIR/sync_data.sh"

echo "📊 数据更新 - $(date '+%Y-%m-%d %H:%M:%S')"

# 使用 Python 更新数据（需要创建 Python 脚本）
python3 "$SCRIPT_DIR/fetch_futures.py"

# 同步到 frontend
if [ -x "$SYNC_SCRIPT" ]; then
  "$SYNC_SCRIPT"
fi

echo "✅ 数据更新完成"
