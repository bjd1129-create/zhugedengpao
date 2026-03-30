# 代码侠心跳配置

## 心跳间隔
30分钟

## 检查清单
1. 检查网站状态（dengpao.pages.dev）
2. 检查部署需求
3. 检查技术问题

## 静默期
23:00-07:00

## 技术栈
- Cloudflare Pages
- 部署命令：source .cloudflare.env && env -u http_proxy -u https_proxy npx wrangler pages deploy . --project-name=dengpao


## 任务完成记录规范
**重要：每次完成任务后，必须立即记录到 agents/engineer/MEMORY.md**

记录格式：
```
## 完成的任务
- YYYY-MM-DD：任务描述
```
不记录视为任务未完成。


## 🧬 自我进化规范（任务后必做）
每次完成任务后，必须在 agents/engineer/MEMORY.md 记录：

```
## 完成的任务
- YYYY-MM-DD [任务名]：成功✅ / 失败❌ / 教训🔍
```
**记录是进化的燃料，不记录=任务白做**
