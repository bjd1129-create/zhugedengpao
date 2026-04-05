#!/bin/bash
# 网站文案巡检脚本 - 每30分钟执行
# 检查官网文字健康状态

LOG="/Users/bjd/Desktop/ZhugeDengpao-Team/agents/writer/memory/site_guard.log"
mkdir -p $(dirname $LOG)

echo "=== $(date '+%Y-%m-%d %H:%M') 巡检开始 ===" >> $LOG

# 检查官网可访问性
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://dengpao.pages.dev/diary.html)
if [ "$STATUS" != "200" ]; then
    echo "⚠️ 官网不可访问 (HTTP $STATUS)" >> $LOG
else
    echo "✅ 官网可访问" >> $LOG
fi

# 记录巡检完成
echo "=== 巡检完成 ===" >> $LOG
