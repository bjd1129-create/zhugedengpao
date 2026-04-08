# TOOLS.md - 工程师工具配置

## 官网目录（权限隔离）

**官网部署目录**：`agents/engineer/website/`

```
agents/engineer/website/
├── pages/          # HTML 页面（39 个页面）
├── images/         # 图片资源（114 个文件）
├── data/           # 数据文件
├── docs/           # 文档
├── .vercel/        # Vercel 部署配置
└── vercel.json     # Vercel 配置
```

**软链接**：`/Users/bjd/Desktop/ZhugeDengpao-Team/website` → `agents/engineer/website/`

---

## 权限隔离规则（2026-04-08 起）

| Agent | website/权限 | 说明 |
|-------|------------|------|
| 工程师 | ✅ 完全控制 | 读/写/删除 |
| 小花 | ✅ 完全控制 | 主 Agent，拥有所有权限 |
| 交易员 | 🟡 数据维护 | 只能维护 trading.html 数据 |
| 协调官 | ❌ 无权限 | 只能分配任务 |
| 数据分析师 | ❌ 无权限 | 只能提供数据 |

**其他 Agent 需要修改官网时**：
1. 向小花提出需求
2. 小花分配任务给工程师（或小花直接修改）
3. 工程师执行修改

---

## 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| HTML/CSS/JS | 页面开发 | 原生 |
| Tailwind CSS | 样式框架 | CDN |
| Next.js | 部分页面 | 16 |
| GitHub Pages | 部署 | - |
| Vercel | 自动部署 | - |

---

## Git 配置

- **工作目录**：`/Users/bjd/Desktop/ZhugeDengpao-Team`
- **分支**：main
- **提交规范**：`engineer: 描述`
- **部署**：push 后 GitHub Actions 自动部署到 Vercel

---

## 重要文件路径

| 文件 | 用途 | 路径 |
|------|------|------|
| 交易数据 | 加密组合 | `website/data/trading/portfolio.json` |
| 美股数据 | 老虎证券 | `website/data/trading/tiger_us_paper.json` |
| 文章数据 | 文章列表 | `website/articles-data.js` |
| Vercel 配置 | 部署配置 | `website/vercel.json` |

---

## 内容文件

| 文件 | 用途 | 路径 |
|------|------|------|
| 给桐桐的信 | 工程师内容 | `content/给桐桐的信.md` |

---

## 脚本工具

| 脚本 | 用途 | 状态 |
|------|------|------|
| `tongtong-letter.sh` | 桐桐信件处理 | 待配置 |

---

_工程师 | 2026-04-08 权限隔离_
