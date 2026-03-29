#!/bin/bash
# 每3小时对比sanwan.ai和dengpao.pages.dev的Cron脚本
# 执行时间: 0,3,6,9,12,15,18,21点

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
LOG_FILE="memory/cron-site-compare-${DATE}.md"

echo "=== Site Compare Cron: ${DATE} ${TIME} ===" > "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 使用curl获取页面标题和关键内容做对比
echo "## sanwan.ai 页面信息" >> "$LOG_FILE"
curl -s -L --max-time 15 "https://sanwan.ai" | grep -o '<title>[^<]*</title>' | head -1 >> "$LOG_FILE" 2>/dev/null || echo "无法访问sanwan.ai" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "## dengpao.pages.dev 页面信息" >> "$LOG_FILE"
curl -s -L --max-time 15 "https://dengpao.pages.dev" | grep -o '<title>[^<]*</title>' | head -1 >> "$LOG_FILE" 2>/dev/null || echo "无法访问dengpao.pages.dev" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "## 对比分析时间: ${TIME}" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 检查两个站点的meta description
echo "### Meta Description 对比" >> "$LOG_FILE"
echo "sanwan.ai:" >> "$LOG_FILE"
curl -s -L --max-time 15 "https://sanwan.ai" | grep -o '<meta[^>]*description[^>]*>' | head -1 >> "$LOG_FILE" 2>/dev/null || echo "无法获取" >> "$LOG_FILE"
echo "dengpao.pages.dev:" >> "$LOG_FILE"
curl -s -L --max-time 15 "https://dengpao.pages.dev" | grep -o '<meta[^>]*description[^>]*>' | head -1 >> "$LOG_FILE" 2>/dev/null || echo "无法获取" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 检查关键内容块
echo "### 页面结构对比" >> "$LOG_FILE"
echo "sanwan.ai h1标签:" >> "$LOG_FILE"
curl -s -L --max-time 15 "https://sanwan.ai" | grep -o '<h1[^>]*>[^<]*</h1>' | head -3 >> "$LOG_FILE" 2>/dev/null || echo "无法获取" >> "$LOG_FILE"
echo "dengpao.pages.dev h1标签:" >> "$LOG_FILE"
curl -s -L --max-time 15 "https://dengpao.pages.dev" | grep -o '<h1[^>]*>[^<]*</h1>' | head -3 >> "$LOG_FILE" 2>/dev/null || echo "无法获取" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 简单检查链接数量
echo "### 链接数量对比" >> "$LOG_FILE"
echo "sanwan.ai 链接数: $(curl -s -L --max-time 15 'https://sanwan.ai' | grep -o '<a[^>]*href' | wc -l)" >> "$LOG_FILE"
echo "dengpao.pages.dev 链接数: $(curl -s -L --max-time 15 'https://dengpao.pages.dev' | grep -o '<a[^>]*href' | wc -l)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "### 初步差距分析" >> "$LOG_FILE"
echo "需进一步使用浏览器访问两个站点进行详细对比" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "--- Cron执行完成: ${DATE} ${TIME} ---" >> "$LOG_FILE"

echo "Cron对比脚本执行完成，日志保存到: $LOG_FILE"
