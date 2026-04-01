# 团队Cron任务计划

> 创建时间：2026-03-30
> 需要在OpenClaw Gateway中创建这些定时任务

---

## 1. 安全官-网站监控（最高优先级）
```bash
openclaw cron add \
  --name "安全官-网站监控" \
  --interval "30m" \
  --agent support \
  --prompt "安全官执行网站状态检查：
1. 检查网站是否可访问（curl dengpao.pages.dev）
2. 检查Token消耗（阈值4500次/5小时，70%告警）
3. 检查sitemap.xml和robots.txt
4. 检查外链是否有死链
发现问题立即汇报给主Agent小花。"
```

## 2. 洞察者-竞品研究（每天3次）
```bash
openclaw cron add \
  --name "洞察者-竞品研究" \
  --interval "8h" \
  --agent researcher \
  --prompt "洞察者执行竞品研究：
1. 检查三万sanwan.ai有无新内容
2. 检查SEO关键词排名变化
3. 搜索"AI龙虾"、"AI助手"相关热词
4. 更新 content/竞品动态.md
有重大发现立即汇报给小花。"
```

## 3. 运营官-每日站会（每天3次）
```bash
openclaw cron add \
  --name "运营官-每日站会" \
  --interval "8h" \
  --agent scheduler \
  --prompt "运营官执行每日站会：
1. 检查P0/P1/P2任务队列状态
2. 清理已完成任务
3. 更新 memory/任务看板.md
4. 检查有无阻塞的任务需要协调
汇报给小花。"
```

## 4. 文案君-内容更新（每天2次）
```bash
openclaw cron add \
  --name "文案君-内容更新" \
  --interval "12h" \
  --agent writer \
  --prompt "文案君执行内容更新：
1. 检查官网内容是否有需要更新的
2. 更新日记页面（如果老庄有新的进展）
3. 检查用户反馈并草拟回复
汇报给小花。"
```

## 5. 代码侠-技术健康检查（每天2次）
```bash
openclaw cron add \
  --name "代码侠-技术检查" \
  --interval "12h" \
  --agent engineer \
  --prompt "代码侠执行技术健康检查：
1. 检查网站JS错误（浏览器控制台）
2. 检查图片/CDN是否正常加载
3. 检查网页加载速度
4. 检查移动端适配
有技术问题立即汇报给小花。"
```

## 6. 配色师-视觉巡查（每天1次）
```bash
openclaw cron add \
  --name "配色师-视觉巡查" \
  --interval "24h" \
  --agent designer \
  --prompt "配色师执行视觉巡查：
1. 截图检查官网整体视觉效果
2. 检查各页面字体/颜色/布局是否一致
3. 检查日记配图是否正常显示
发现视觉问题汇报给小花。"
```

## 7. 团队进化-深度进化（每5小时）
```bash
openclaw cron add \
  --name "团队-深度进化" \
  --interval "5h" \
  --agent researcher \
  --prompt "团队深度进化：
1. 分析过去5小时的错误和失败
2. 检查skills目录有无需要更新的
3. 更新 agents/researcher/MEMORY.md
4. 生成进化建议汇报给小花。"
```

---

## 快速创建命令

如果CLI挂起，可以尝试：
```bash
# 重启Gateway
openclaw gateway restart

# 或者直接编辑配置
openclaw cron list
```

## 静默期
所有Cron任务在 23:00-07:00 静默，不主动执行。

---

*小花记录于 2026-03-30*
