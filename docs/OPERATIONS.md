# 运维手册

**项目:** 老庄与小花团队网站
**版本:** 1.0
**更新:** 2026-04-10

---

## 一、日常运维

### 1.1 监控检查清单

```markdown
□ 访问 https://dengpao.pages.dev 确认正常
□ 访问 https://306alp.pages.dev 确认正常
□ 检查 GitHub Actions CI 状态
□ 检查 Cloudflare Analytics 有无异常
```

### 1.2 每月维护

```markdown
□ 清理不需要的文件和图片
□ 检查日志中的错误
□ 更新依赖包版本
□ 备份重要数据
```

---

## 二、部署指南

### 2.1 自动部署流程

```
开发者 Push → GitHub → GitHub Actions CI → Cloudflare Pages → 线上
```

**触发条件:**
- Push 到 main 分支
- Pull Request 合并

### 2.2 手动部署

```bash
# 1. 克隆仓库
git clone https://github.com/bjd1129-create/zhugedengpao.git
cd zhugedengpao

# 2. 安装 Wrangler CLI
npm install -g wrangler

# 3. 登录 Cloudflare
wrangler login

# 4. 部署官网
cd website
wrangler pages deploy . --project-name=dengpao

# 5. 部署记忆网站
cd ../memory-site
wrangler pages deploy . --project-name=memory-site
```

### 2.3 本地预览

```bash
# 使用 Cloudflare Pages 本地开发
npx wrangler pages dev ./website
```

---

## 三、故障排查

### 3.1 网站无法访问

**检查步骤:**

1. 检查 DNS 解析
   ```bash
   dig dengpao.pages.dev
   ```

2. 检查 Cloudflare Pages 状态
   - 登录 Cloudflare Dashboard
   - 查看 Pages 项目状态

3. 检查 GitHub Actions 部署日志
   - 查看最近的 deployment

### 3.2 PWA 无法离线

1. 清除浏览器缓存
2. 重新注册 Service Worker
   - Chrome: DevTools → Application → Service Workers → Unregister
3. 检查 manifest.json 是否正确加载

### 3.3 图片加载失败

1. 检查图片路径是否正确
2. 检查文件是否存在于仓库中
3. 检查 Cloudflare Cache 状态

---

## 四、安全指南

### 4.1 敏感信息管理

```bash
# 永远不要提交到 Git
.env
*.pem
*.key
secrets.json
```

### 4.2 GitHub Secrets

需要设置的 Secrets:

| Name | 说明 | 获取方式 |
|------|------|----------|
| CLOUDFLARE_API_TOKEN | Cloudflare API 令牌 | Cloudflare Dashboard |

### 4.3 应急响应

**发现安全漏洞:**

1. 立即评估影响范围
2. 修复并推送 (使用 `--no-verify` 如果需要)
3. 通知相关人员
4. 记录到安全事件日志

---

## 五、备份与恢复

### 5.1 备份策略

| 数据 | 频率 | 存储 |
|------|------|------|
| 代码仓库 | 自动 (Git) | GitHub |
| 网站文件 | 每次部署 | Cloudflare |
| 评论数据 | 每日 | 独立存储 |

### 5.2 恢复步骤

**场景: 需要回滚到之前版本**

```bash
# 1. 找到目标 commit
git log --oneline

# 2. 创建回滚分支
git checkout -b rollback-v1.2.3 <commit-hash>

# 3. 部署
wrangler pages deploy . --project-name=dengpao

# 4. 验证后合并到 main
git checkout main
git merge rollback-v1.2.3
```

---

## 六、性能优化

### 6.1 性能指标目标

| 指标 | 移动端 | 桌面端 |
|------|--------|--------|
| LCP | < 2.5s | < 1.5s |
| FID | < 100ms | < 50ms |
| CLS | < 0.1 | < 0.1 |

### 6.2 优化命令

```bash
# 检查图片体积
find . -name "*.jpg" -exec ls -lh {} \; | sort -k5 -h

# 生成缩略图 (需要 ImageMagick)
mogrify -resize 800x600 -quality 80 thumbnails/*.jpg

# 清理未使用的图片
git clone https://github.com/pre-commit/pre-commit-hooks
pre-commit run --all-files trim-trailing-whitespace
```

---

## 七、联系与支持

### 7.1 相关链接

| 服务 | 地址 |
|------|------|
| GitHub 仓库 | https://github.com/bjd1129-create/zhugedengpao |
| Cloudflare Dashboard | https://dash.cloudflare.com |
| 网站监控 | https://status.cloudflare.com |

### 7.2 紧急联系人

| 角色 | 职责 |
|------|------|
| 运维负责人 | 部署、故障处理 |
| 开发者 | 代码问题 |
| Cloudflare Support | 平台问题 |

---

*文档版本: 1.0 | 最后更新: 2026-04-10*
