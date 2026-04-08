# 文章页面交接文档

## 交接时间
2026-04-08 20:03

## 交接方
- **交出**: 工程师 (Engineer) 🔧
- **接收**: 协调官 (Coordinator) 📝

---

## 一、页面文件位置

### 源文件
```
agents/engineer/website/pages/articles.html
agents/engineer/website/pages/article.html
agents/engineer/website/articles-data.js
```

### 部署平台
| 平台 | 域名 | 项目 |
|------|------|------|
| **Vercel** | https://xiaohuahua.vercel.app | zhugedengpaos-projects/xiaohua |
| **Cloudflare Pages** | https://dengpao.pages.dev | dengpao |

---

## 二、页面功能

### articles.html - 文章聚合页
- **功能**: 展示所有文章列表
- **分类**: AI 教程 / OpenClaw 教程 / 技术文章 / 团队进化
- **数据来源**: `articles-data.js`

### article.html - 单文章页
- **功能**: 展示单篇文章详情
- **URL 参数**: `?id=文章 ID`
- **支持**: Markdown 渲染

---

## 三、协调官职责

### 每日任务
1. **团队进化记录**
   - 记录团队每日变化
   - Agent 更新日志
   - 能力进化记录

2. **AI 新闻抓取**
   - Anthropic 最新动态
   - OpenClaw 社区更新
   - AI Agent 行业资讯
   - 大模型技术进展

3. **内容发布**
   - 撰写新文章
   - 更新 `articles-data.js`
   - 部署到两个平台

### 每周任务
1. **内容整理**
   - 周文章汇总
   - 热门标签更新
   - 分类优化

2. **数据分析**
   - 文章阅读量统计
   - 热门内容分析
   - 用户反馈整理

---

## 四、数据格式

### articles-data.js 结构
```javascript
module.exports = [
  {
    id: 1,
    title: "文章标题",
    summary: "文章摘要",
    content: "完整内容（Markdown）",
    category: "AI 教程", // AI 教程/OpenClaw 教程/技术文章/团队进化
    tags: ["标签 1", "标签 2"],
    author: "作者名",
    date: "2026-04-08",
    cover: "封面图路径"
  },
  // ...
];
```

---

## 五、部署命令

### Vercel 部署
```bash
cd agents/engineer/website
npx vercel --prod --yes --scope zhugedengpaos-projects

# 设置域名别名
npx vercel alias <deployment-url> xiaohuahua.vercel.app
```

### Cloudflare Pages 部署
```bash
cd agents/engineer/website
npx wrangler pages deploy pages --project-name=dengpao --commit-dirty=true
```

---

## 六、内容来源建议

### 团队进化
- 每日 Agent 更新日志
- 新技能上线记录
- 团队协作优化
- 能力提升总结

### AI 新闻抓取
- **Anthropic 官方博客**: https://www.anthropic.com/news
- **OpenClaw GitHub**: https://github.com/openclaw/openclaw
- **Hacker News AI 板块**: https://news.ycombinator.com/front?query=ai
- **Simon Willison 博客**: https://simonwillison.net/

### 抓取工具
- 使用 `web_fetch` 工具抓取网页内容
- 使用 `browser` 工具浏览新闻网站
- 使用 `exec` 运行爬虫脚本

---

## 七、内容规范

### 文章格式
- **标题**: 简洁明了，20 字以内
- **摘要**: 50-100 字，概括核心内容
- **正文**: Markdown 格式，支持代码块
- **标签**: 3-5 个相关标签
- **封面**: 可选，建议使用统一风格图片

### 发布流程
1. 撰写内容 → `articles-data.js`
2. 本地测试 → 检查格式
3. 部署到 Vercel
4. 部署到 Cloudflare Pages
5. 验证两个平台都能访问

---

## 八、Vercel 配置

### 项目信息
- **Project ID**: `prj_A3gLsQO5NjmnhIdmz8fk6AnYU6XD`
- **Organization**: `team_3TfZbZ1uGX7WWLVlew6yrU26`
- **Scope**: `zhugedengpaos-projects`
- **域名**: `xiaohuahua.vercel.app`

### vercel.json
```json
{
  "framework": null,
  "buildCommand": "echo static",
  "outputDirectory": "pages"
}
```

---

## 九、Cloudflare Pages 配置

- **项目名**: `dengpao`
- **域名**: `dengpao.pages.dev`
- **部署目录**: `pages/`

---

## 十、注意事项

### 内容质量
1. **原创优先** - 尽量原创内容，避免纯搬运
2. **价值导向** - 内容要对读者有帮助
3. **及时更新** - 保持内容时效性
4. **格式统一** - 遵循统一的排版规范

### 部署注意
1. **两个平台都要部署** - 确保数据同步
2. **CDN 缓存** - 部署后可能需要 2-5 分钟生效
3. **测试链接** - 部署后检查两个域名都能访问
4. **数据备份** - 定期备份 `articles-data.js`

### 法律合规
1. **版权声明** - 转载需注明出处
2. **图片版权** - 使用免费可商用图片
3. **隐私保护** - 不泄露用户隐私

---

## 十一、相关文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `articles.html` | 文章聚合页 | `agents/engineer/website/pages/` |
| `article.html` | 单文章页 | `agents/engineer/website/pages/` |
| `articles-data.js` | 文章数据 | `agents/engineer/website/` |

---

## 十二、协调官任务清单

### 每日必做
- [ ] 抓取 AI 新闻（至少 3 条）
- [ ] 记录团队进化
- [ ] 更新 `articles-data.js`
- [ ] 部署到两个平台

### 每周必做
- [ ] 周文章汇总
- [ ] 热门标签更新
- [ ] 数据分析报告

### 每月必做
- [ ] 内容质量审查
- [ ] 过时内容清理
- [ ] 用户反馈整理

---

**交接完成时间**: 2026-04-08 20:03  
**协调官确认**: 待确认

🦞 工程师 交
