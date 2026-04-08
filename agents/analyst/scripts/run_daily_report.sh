#!/bin/bash
# AI 深度日报 Cron 任务脚本
# 运行时间：每天 08:00

cd /Users/bjd/Desktop/ZhugeDengpao-Team/agents/analyst/scripts

# 激活虚拟环境
source venv/bin/activate

# 运行报告生成脚本
python3 ai_daily_report.py >> /tmp/ai_daily_report.log 2>&1
