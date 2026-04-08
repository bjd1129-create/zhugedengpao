#!/bin/bash
# 数据自动同步脚本
# 将 analyst/data/ 的数据文件同步到 engineer/website/public/data/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

SOURCE_DIR="$PROJECT_ROOT/analyst/data"
TARGET_DIR="$PROJECT_ROOT/engineer/website/public/data"

echo "📊 数据同步脚本 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "源目录：$SOURCE_DIR"
echo "目标目录：$TARGET_DIR"
echo ""

# 同步数据文件
for file in futures_prices.json technical_indicators.json historical_prices.json; do
  if [ -f "$SOURCE_DIR/$file" ]; then
    cp "$SOURCE_DIR/$file" "$TARGET_DIR/$file"
    echo "✅ 同步：$file"
  else
    echo "⚠️  跳过：$file (不存在)"
  fi
done

echo ""
echo "✅ 数据同步完成"
