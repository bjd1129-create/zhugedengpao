# TOOLS.md - 数据官本地工具配置

## 核心工具

### Git
- 工作目录：`/Users/bjd/Desktop/ZhugeDengpao-Team`
- 分支：main
- 部署：Cloudflare Pages（dengpao.pages.dev）

### 文件路径
- trading.html：`/Users/bjd/Desktop/ZhugeDengpao-Team/trading.html`
- portfolio.json：`/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json`

### Wrangler（Cloudflare部署）
```bash
npx wrangler pages deploy . --project-name=dengpao
```

### 数据新鲜度检查
- 最后更新时间 > 10分钟 → 标记为⚠️
- 最后更新时间 > 30分钟 → 标记为🔴
