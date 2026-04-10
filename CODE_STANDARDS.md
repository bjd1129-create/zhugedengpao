# 代码规范速查表

## 🚀 快速开始

```bash
# 安装依赖
npm install

# 格式化代码 (推荐在提交前运行)
npm run format

# 检查代码规范
npm run lint
```

## 📁 文件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| JavaScript | camelCase | `imageLoader.js` |
| CSS | kebab-case | `responsive-images.css` |
| HTML | kebab-case | `about-page.html` |
| 组件 | PascalCase | `PhotoCard.tsx` |

## 🎨 CSS 规范

### 变量命名 (Design Tokens)

```css
/* 颜色 */
--color-primary: #4A2508;
--color-secondary: #E5A853;
--color-background: #f5f3ee;
--color-text: #222;
--color-muted: #888;

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
```

### BEM 命名

```css
/* Block */
.card { }

/* Element */
.card__title { }
.card__image { }
.card__button { }

/* Modifier */
.card--featured { }
.card__button--primary { }
```

## 📜 JavaScript 规范

### 变量声明

```javascript
// ✅ 推荐: 使用 const
const config = { apiKey: 'xxx' };
const MAX_RETRIES = 3;

// ✅ 必要时使用 let
let count = 0;
count++;

// ❌ 避免: var
var name = 'old'; // 旧式写法
```

### 函数

```javascript
// ✅ 箭头函数
const fetchData = async (url) => {
  const response = await fetch(url);
  return response.json();
};

// ✅ 默认参数
function createElement(tag = 'div', options = {}) {
  // ...
}
```

### 字符串

```javascript
// ✅ 使用单引号
const message = 'Hello World';

// ✅ 模板字符串
const greeting = `Welcome, ${username}!`;
```

## 🔍 Code Review 清单

提交前自检:

- [ ] 代码已格式化 (Prettier)
- [ ] 无 ESLint 错误
- [ ] 无 console.log (调试代码已删除)
- [ ] 变量命名有意义
- [ ] 关键代码有注释
- [ ] 相关文档已更新

## 📝 Commit Message 示例

```
feat(website): 添加 PWA 离线支持
fix(api): 修复评论接口超时
docs: 更新部署文档
style(css): 优化响应式布局
refactor(components): 重构图片加载逻辑
perf(lazy-load): 提升首屏加载速度 40%
```

## 🆘 常见问题

### Q: Prettier 和 ESLint 冲突?

```bash
# 安装兼容包
npm install -D eslint-config-prettier

# 在 .eslintrc.json 中添加
{
  "extends": ["prettier"]
}
```

### Q: 如何跳过检查强制提交?

```bash
# ⚠️ 慎用! 仅紧急情况
git commit -m "fix: hotfix" --no-verify
```

### Q: 如何配置 IDE?

**VS Code**: 安装扩展 `ESLint` + `Prettier`

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

---

*有问题? 找资深开发者 🦞*
