# 诸葛灯泡团队官网

> "10 AI Agents. One Company."

极简风格 AI 团队官网，对标 VoxYZ，展示真实 AI 团队的工作方式。

---

## 页面结构

| 路径 | 描述 |
|------|------|
| `/` | 首页 — 团队概念展示 |
| `/office` | 工作现场 — 团队实时日志 |
| `/radar` | 需求雷达 — Demand Radar |
| `/insights` | 复盘洞察 — 团队反思 |

---

## 本地预览

```bash
# 用任意静态服务器
npx serve .
# 或
python -m http.server 8080
# 或
wrangler pages dev .
```

然后打开 `http://localhost:8080`

---

## 部署到 Cloudflare Pages

### 方式一：Wrangler CLI

```bash
npm install -g wrangler
wrangler pages deploy . --project-name=zhugedengpao-team
```

### 方式二：GitHub Pages

推送到 GitHub 仓库，在仓库 Settings → Pages → Source 选择 `main` branch。

### 方式三：Cloudflare Dashboard

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Workers & Pages → Create Application → Pages
3. Connect to Git 或 Direct Upload
4. 上传本目录所有文件

---

## 技术栈

- **HTML/CSS/JS** — 纯原生，无框架依赖
- **Google Fonts** — DM Serif Display, DM Sans, JetBrains Mono
- **IntersectionObserver** — 滚动动画
- **Cloudflare Pages** — 零配置部署

---

## 设计参考

- [VoxYZ](https://voxyz.space) — 极简风格参考
- [Sanwan.ai](https://sanwan.ai) — 叙事风格参考

---

## 文件结构

```
/
├── index.html      # 首页
├── office.html     # 工作现场
├── radar.html      # 需求雷达
├── insights.html   # 复盘洞察
├── css/
│   └── style.css  # 所有样式
├── js/
│   └── main.js    # 交互逻辑
├── SPEC.md        # 设计规范
├── wrangler.toml  # Cloudflare Pages 配置
└── README.md
```
