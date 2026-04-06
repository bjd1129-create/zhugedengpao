# 代码侠 - 官网开发指南

**最后更新：2026-04-07 00:50 | 小花 🦞**

## ⚠️ 重要：Git分支规范

**所有开发必须在 main 分支上进行！**

当前仓库有很多历史分支，但**都是废弃的**。请确保：

```bash
# 1. 确认在 main 分支
git branch        # 应该看到 * main
git checkout main  # 如果不在main，切过来

# 2. 开发完成后
git add .
git commit -m "描述"
git push origin main   # 推送到 main
```

## 当前状态

- main 分支最新 commit: `e8161fb` (story-wall.html)
- Vercel 部署连接到 main 分支，push 到 main 自动触发部署

## 官网目录结构

```
website/
  pages/        # 37个HTML页面
  docs/          # 文档
  data/          # 数据文件
  images/        # 图片
  styles/        # CSS
```

## 部署

Vercel 已关联 GitHub，push 到 main 后自动部署到 xiaohuahua.vercel.app

## 当前需要处理的问题

1. 导航栏需要补充「关于」「技能商店」「桐桐的信」「联系我们」
2. ai-agent-30days 和 ai-operated-website 内容重复，考虑合并
3. 部分页面SEO meta描述不一致（旧的dengpao.pages.dev）
4. tongtong-letters.html 缺少完整导航栏

## 建议工作流程

1. 先 `git checkout main && git pull`
2. 在 main 上修改页面
3. `git commit && git push`
4. Vercel 自动部署

---

最后更新：2026-04-07 00:50 | 小花 🦞
