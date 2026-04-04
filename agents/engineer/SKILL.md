# SKILL.md - 代码侠

## 核心技能：网站开发与部署

### 修复网站问题
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
# 本地修改后 push
git add .
git commit -m "fix: [描述]"
git push origin main
```

### 触发CF Pages部署
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
printf 'y\n' | npx wrangler pages deploy . --project-name=dengpao
```

### 常用文件路径
- 首页：`index.html`
- 导航栏：各HTML文件内的 `<nav>`
- trading页面：`trading.html`（数据官负责）
- CSS：`css/` 目录

### 常见修复
- 导航栏加链接 → 修改 `index.html`
- 样式问题 → 修改对应CSS
- JS报错 → 检查浏览器Console

### 技术约束
- 不碰 trading.html（数据官负责）
- 不碰 portfolio.json
- 新增页面 → 告知小花审批
