# Commit Message 规范

## 格式

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Type 类型

| Type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构 |
| perf | 性能优化 |
| test | 测试相关 |
| chore | 构建/工具变更 |

## Examples

```
feat(website): 添加 PWA 支持

添加 manifest.json 和 Service Worker 实现离线访问。

Closes #123
```

```
fix(api): 修复评论接口超时问题

原因: 未设置请求超时
解决方案: 添加 10s 超时控制

Closes #456
```

```
docs: 更新部署文档

新增 Cloudflare Pages 部署流程。
```

## 规则

1. Subject 不超过 72 字符
2. 使用祈使句："add" 而不是 "added"
3. Body 解释 "why" 而不是 "what"
4. Footer 引用相关 Issue
