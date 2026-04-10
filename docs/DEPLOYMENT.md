# 部署情况汇总

最后更新：2026-04-09 16:42

---

## 一、官网（dengpao.pages.dev）

### 部署平台
- **Cloudflare Pages**（`.pages.dev` 域名）
- 源码仓库：GitHub `bjd1129-create/zhugedengpao`

### 问题（2026-04-09 发现）

**现状**：访问 `https://dengpao.pages.dev/` 显示深蓝色页面（React 仪表盘空壳），而非真正的静态官网。

**根本原因**：

| 问题 | 说明 |
|------|------|
| 目录结构冲突 | `website/` 目录同时包含 React 源码（`src/`）和静态官网文件（`pages/`） |
| Cloudflare 指向错误 | Cloudflare Pages 指向 `website/` 根目录 → 触发 Vite build → 输出到 `dist/` → 覆盖静态文件 |
| Vercel 配置存在 | `website/.vercel/project.json` 存在，但 Vercel 已非当前部署平台 |
| `website/` 未加入 Git | 静态文件从未 commit，无法被 Cloudflare Pages 拉取 |

**技术细节**：
- `website/index.html` → React 根组件（`<div id="root">`）
- `website/package.json` → Vite + React 项目
- `website/pages/index.html` → 真正的静态首页（老庄与小花）
- Cloudflare Pages 构建输出 `dist/` → 覆盖整个 `website/` 目录

### 修复方案

1. 将 React 仪表盘移至 `dashboard/` 子目录（✅ 已完成）
2. `website/` 恢复为纯静态目录
3. Cloudflare Pages 改为指向 `website/pages/` 输出

---

## 二、记忆网站（memory-site.pages.dev）

### 部署平台
- **Cloudflare Pages**（`.pages.dev` 域名）
- 源码仓库：GitHub `bjd1129-create/zhugedengpao`（`memory-site/` 目录）

### 配置

**wrangler.toml**（Cloudflare Pages）：
```toml
name = "memory-site"
compatibility_date = "2024-01-01"

[site]
bucket = "."

[build]
command = "echo static"

[[redirects]]
from = "/*"
to = "/index.html"
status = 200
```

### 状态
- ✅ 正常运行
- ✅ 纯静态，无构建冲突

---

## 三、两个网站对比

| | 官网 dengpao.pages.dev | 记忆网站 memory-site.pages.dev |
|---|---|---|
| 平台 | Cloudflare Pages | Cloudflare Pages |
| 问题 | ❌ 目录冲突，静态文件被覆盖 | ✅ 正常 |
| 静态目录 | `website/pages/` | `memory-site/` 根目录 |
| 构建配置 | 无（Vite 项目干扰） | `wrangler.toml` |
| 加入 Git | ❌ 未加入 | ✅ 已加入 |
| 状态 | 需修复 | 正常 |

---

## 四、部署链路

```
GitHub push (main branch)
       │
       ├──→ GitHub Actions (CI 质量检查)
       └──→ Cloudflare Pages (自动触发)
                  │
                  ├── 官网 → 指向 website/ → 跑 Vite build → 输出 dist/ → ❌ 覆盖
                  └── 记忆网站 → 指向 memory-site/ → echo static → ✅ 正常
```

---

## 五、修复行动计划

### Phase 1：隔离 React 仪表盘 ✅
```bash
mkdir -p dashboard/
mv website/src website/dist website/package.json \
   website/vite.config.js website/tailwind.config.js \
   website/postcss.config.js dashboard/
```

### Phase 2：修复 website/ 静态结构
- [x] React 项目已移出 `website/`
- [ ] 确认 `website/` 目录加入 Git
- [ ] 清理 Vite 构建残留（`node_modules/` 等）
- [ ] `website/index.html` 改为静态首页内容

### Phase 3：修复 Cloudflare Pages 配置
- [ ] 登录 Cloudflare Dashboard
- [ ] 官网项目 → 构建配置 → 构建命令改为 `echo static`，输出目录改为 `pages`

### Phase 4：验证部署
- [ ] 访问 dengpao.pages.dev → 应显示"老庄与小花"
- [ ] 检查所有内页

---

## 六、相关链接

| 链接 | 状态 |
|------|------|
| https://dengpao.pages.dev | ❌ 显示错误 |
| https://memory-site.pages.dev | ✅ 正常 |
| https://github.com/bjd1129-create/zhugedengpao | 源码仓库 |

---

## 七、负责人

| 网站 | 负责人 | 说明 |
|------|--------|------|
| 官网 dengpao.pages.dev | 工程师 🔧 | 当前需修复 |
| 记忆网站 memory-site.pages.dev | 工程师 🔧 | 正常 |

---

_工程师 | 2026-04-09_

---

## 八、修复记录（2026-04-09 16:50）

### 问题根因
`website/` 目录同时包含 React 源码和静态文件，Cloudflare Pages 跑 Vite build 覆盖了静态内容。

### 修复措施
1. 将 React 源码移至 `dashboard/`
2. `pages/` 静态文件移到 `website/` 根目录
3. 删除 Vite 相关文件（package.json、node_modules、vercel.json、.vercel/）
4. 通过 `wrangler pages deploy` 直接部署新版本

### 部署结果
- 新部署：https://e2cdf58f.dengpao.pages.dev ✅
- 正式域名：https://dengpao.pages.dev ✅

### 待后续处理
- [ ] 清理 `dashboard/` 目录（React 仪表盘源码）
- [ ] 确认 GitHub push 是否也能触发正确部署
- [ ] 清理旧的 Cloudflare Pages deployment
