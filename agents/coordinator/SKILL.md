# SKILL.md - 协调官

## 核心技能：团队协调与内容运营

### 团队巡检
```bash
# 检查各Agent状态
ls agents/*/memory/*.md 2>/dev/null | head -20
# 检查配色师进度
ls images/ | grep comic | wc -l
# 检查GitHub状态
cd /Users/bjd/Desktop/ZhugeDengpao-Team && git status --short
```

### GitHub操作
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
# 凭证在 agents/coordinator/.env
source agents/coordinator/.env
# Push
git add . && git commit -m "协调官: 更新 $(date +%Y-%m-%d)" && git push origin main
```

### 向小花汇报
```python
sessions_send(
    sessionKey="agent:main:main",
    message="🦞 [协调官日报] YYYY-MM-DD\n\n✅ 完成：\n- xxx\n\n🔄 进行中：\n- xxx\n\n⚠️ 待处理：\n- xxx"
)
```

### 审批内容发布
- 配色师漫画完成 → 检查质量 → push发布
- 文案君文章完成 → 检查质量 → push发布
- 高光日记（22:00）→ 自动执行

## 汇报节奏
- 18:00 晚间汇报（发飞书给小花的user id）
- 有重大阻塞 → 立即汇报
- 正常 → 不打扰
