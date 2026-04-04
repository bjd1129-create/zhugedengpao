# SKILL.md - 洞察者

## 核心技能：AI资讯研究与市场洞察

### 获取AI最新资讯
使用 `web_search` 工具：
```
搜索：AI tools news 2026
搜索：OpenClaw latest updates
```

### 写研究报告
```bash
# 写研究报告
cat > agents/洞察者/研究-YYYY-MM-DD.md << 'EOF'
# 研究主题

## 发现
- xxx

## 分析
- xxx

## 建议
- xxx
EOF
```

### 存档
研究报告保存到 `agents/洞察者/memory/` 目录

## 研究方向
- OpenClaw新功能
- AI行业动态
- 交易策略研究
- Self-Evolve进化进展

## 汇报节奏
- 每小时自动研究（cron）
- 有重大发现 → 发 sessions_send 通知小花
