# 架构设计文档

**项目:** 老庄与小花团队网站
**版本:** 1.0
**更新:** 2026-04-10

---

## 一、系统概览

### 1.1 项目组成

```
zhugedengpao/
├── website/              # 官网 (dengpao.pages.dev)
│   ├── index.html        # 首页
│   ├── pricing.html      # 价格页
│   ├── articles.html     # 文章聚合
│   ├── css/              # 样式文件
│   ├── images/           # 图片资源
│   └── service-worker.js # PWA 离线支持
│
├── memory-site/          # 记忆网站 (306alp.pages.dev)
│   ├── index.html        # 相册首页
│   ├── images/           # 原图
│   ├── thumbnails/       # 缩略图
│   └── service-worker.js # PWA 离线支持
│
├── dashboard/            # React 仪表盘 (开发中)
├── agents/              # OpenClaw Agent 配置
├── skills/              # OpenClaw Skills
└── docs/                # 技术文档
```

### 1.2 部署架构

```
                    GitHub Repository
                          │
                          ▼
              ┌───────────────────────┐
              │   GitHub Actions      │
              │   (CI/CD Pipeline)    │
              └───────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌─────────────────────┐     ┌─────────────────────┐
│   Cloudflare Pages  │     │   Cloudflare Pages   │
│   官网部署           │     │   记忆网站部署        │
│   dengpao.pages.dev │     │   306alp.pages.dev   │
└─────────────────────┘     └─────────────────────┘
          │                               │
          └───────────────┬───────────────┘
                          ▼
              ┌─────────────────────┐
              │   全球 CDN 加速      │
              │   (Cloudflare)      │
              └─────────────────────┘
```

### 1.3 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | HTML5 + CSS3 + Vanilla JS | 轻量、无框架依赖 |
| PWA | Service Worker + Manifest | 离线访问 |
| CI/CD | GitHub Actions | 自动化部署 |
| 托管 | Cloudflare Pages | 全球 CDN |
| 域名 | Cloudflare DNS | 域名管理 |
| 分析 | 暂无 | 计划接入 Plausible |

---

## 二、设计原则

### 2.1 核心原则

1. **简单性** - 优先使用最简单的解决方案
2. **性能** - 首屏加载 < 1.5s
3. **可维护** - 代码清晰，易于理解和修改
4. **可用性** - 渐进增强，支持离线访问

### 2.2 开发规范

- **CSS**: 使用 CSS 变量管理主题色
- **JS**: ES6+ 语法，不使用打包工具
- **图片**: 懒加载 + WebP 格式
- **SEO**: 语义化 HTML + 结构化数据

---

## 三、组件设计

### 3.1 公共组件

```
css/
├── style.css           # 主样式文件
├── variables.css       # CSS 变量
└── responsive-images.css # 图片工具类
```

### 3.2 CSS 变量

```css
:root {
  /* 品牌色 */
  --color-primary: #4A2508;
  --color-secondary: #E5A853;

  /* 背景色 */
  --bg-main: #f5f3ee;
  --bg-card: #ffffff;

  /* 文字色 */
  --text-main: #222222;
  --text-muted: #888888;

  /* 间距 */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;

  /* 阴影 */
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.12);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.16);
}
```

---

## 四、API 设计

### 4.1 评论 API

**Base URL:** `https://dengpao.pages.dev/api`

#### 获取评论列表

```
GET /comments?page=1&limit=10
```

Response:
```json
{
  "data": [
    {
      "id": "xxx",
      "nickname": "游客",
      "content": "内容...",
      "location": "北京",
      "created_at": "2026-04-10T12:00:00Z",
      "replies": []
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 10
}
```

#### 提交评论

```
POST /comments
```

Body:
```json
{
  "nickname": "游客",
  "content": "内容...",
  "location": "北京"
}
```

---

## 五、安全考虑

### 5.1 当前措施

- [x] HTTPS 强制 (Cloudflare 自动)
- [x] CORS 配置
- [x] 输入验证
- [x] XSS 防护 (HTML 转义)

### 5.2 待加强

- [ ] Rate Limiting
- [ ] CSP (Content Security Policy)
- [ ] 评论审核机制

---

## 六、监控与日志

### 6.1 监控指标

| 指标 | 工具 | 告警阈值 |
|------|------|----------|
| 可用性 | Cloudflare Analytics | < 99.9% |
| 错误率 | Console Error | > 1% |
| 性能 | PageSpeed Insights | LCP > 2.5s |

### 6.2 日志管理

- Cloudflare Pages 构建日志: 保留 30 天
- GitHub Actions 日志: 保留 90 天

---

## 七、扩展计划

### Phase 2 (Q3 2026)

- [ ] Next.js 迁移评估与实施
- [ ] CMS 集成 (Contentlayer)
- [ ] 评论系统后端化

### Phase 3 (Q4 2026)

- [ ] 多语言支持 (i18n)
- [ ] 用户系统
- [ ] 会员专属内容

---

*文档版本: 1.0 | 最后更新: 2026-04-10*
