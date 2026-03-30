# TOOLS.md - Local Notes

## 🚀 官网部署

### 部署命令
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
source .cloudflare.env && env -u http_proxy -u https_proxy npx wrangler pages deploy . --project-name=dengpao --commit-dirty=true
```

### Cloudflare
- **项目名**: dengpao
- **生产 URL**: https://dengpao.pages.dev/
- **部署方式**: wrangler pages deploy（绕过 GitHub 直接部署）
- **GitHub App**: 已断开（Git Provider: No），但 wrangler deploy 可用
- **API Token**: 见 `.cloudflare.env`

### GitHub
- **Repo**: https://github.com/bjd1129-create/zhugedengpao
- **分支**: main（受保护，禁止直接 push）
- **功能分支**: feature/testing-ci（待推送）

---

## 🌐 其他部署

### Vercel
```bash
vercel --prod
```

### Netlify
- **URL**: https://dengpao-official.netlify.app
- **方式**: GitHub 自动部署

---

## 🔑 API Keys（存储位置）

| 服务 | Key | 位置 |
|------|-----|------|
| Cloudflare API Token | `cfut_TMaebBDML94a92I...` | `.cloudflare.env` |
| DashScope (阿里) | `sk-sp-b879148afe854...` | `.env` |
| MiniMax | 使用 OpenClaw 内置 | - |

---

## 📁 重要文件路径

### 研究报告
- **OpenClaw X热帖研究v2（含Hermes分析）**
  `/Users/bjd/Desktop/ZhugeDengpao-Team/agents/engineer/memory/openclaw-x-top100-v2-2026-03-29.md`

### 团队共享
- **团队共享记忆**
  `/Users/bjd/Desktop/ZhugeDengpao-Team/company/SHARED_MEMORY.md`

### 项目
- **官网项目**
  `/Users/bjd/Desktop/ZhugeDengpao-Team/`

### X.com 账号
- **已登录账号**: `@zhugedengpao_ai`
- **浏览器 session**: 保持中

---

## ⚠️ 注意事项

- **代理环境**: Git push 需要 `env -u http_proxy -u https_proxy` 绕过
- **wrangler deploy**: 不受 Git Provider 限制，直接更新生产环境
- **Git Hook**: `.git/hooks/pre-push` 阻止直接 push main

---

*更新: 2026-03-30*
