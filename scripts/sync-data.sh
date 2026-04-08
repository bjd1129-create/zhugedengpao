#!/bin/bash
# 数据同步脚本 - 将分析师数据复制到前端目录

ANALYST_DATA="/Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst/data"
FRONTEND_DATA="/Users/bjd/Desktop/ZhugeDengpao-Team/agents/engineer/website/public/data"

echo "📊 同步期货数据..."
cp "$ANALYST_DATA/futures_prices.json" "$FRONTEND_DATA/"
cp "$ANALYST_DATA/technical_indicators.json" "$FRONTEND_DATA/"
cp "$ANALYST_DATA/historical_prices.json" "$FRONTEND_DATA/"

echo "✅ 数据已同步到 $FRONTEND_DATA"
echo "📝 文件列表:"
ls -lh "$FRONTEND_DATA"/*.json

echo ""
echo "🚀 如需部署，执行:"
echo "   cd agents/engineer/website && git add public/data/ && git commit -m 'chore: sync data' && git push"
