# Agent Browser技能

> **技能获取时间:** 2026-03-18 20:05
> **技能来源:** 老庄发送
> **提供者:** Vercel Labs
> **作者:** Yossi Elkrief (@MaTriXy)

---

## 技能描述

无头浏览器自动化CLI，专为AI Agent优化，使用accessibility tree快照和ref-based元素选择，实现确定性浏览器自动化。

---

## 核心特点

| 特点 | 说明 |
|------|------|
| **Accessiblity Tree** | 使用可访问性树快照 |
| **Ref-based选择** | 确定性元素选择（@e1, @e2...） |
| **JSON输出** | 易于解析的结构化输出 |
| **会话隔离** | 支持多会话并行 |
| **状态持久化** | 保存/加载认证状态 |

---

## 安装方式

```bash
npm install -g agent-browser
agent-browser install              # 下载Chromium
agent-browser install --with-deps  # Linux: +系统依赖
```

---

## 与内置Browser工具对比

| 场景 | 推荐工具 |
|------|----------|
| **多步骤工作流自动化** | ✅ agent-browser |
| **确定性元素选择** | ✅ agent-browser |
| **性能敏感场景** | ✅ agent-browser |
| **复杂SPA应用** | ✅ agent-browser |
| **需要截图/PDF分析** | 内置browser |
| **需要视觉检查** | 内置browser |

---

## 核心命令

### 导航

```bash
agent-browser open https://example.com
agent-browser back | forward | reload | close
```

### 快照（推荐 -i --json）

```bash
agent-browser snapshot -i --json          # 交互元素 + JSON输出
agent-browser snapshot -i -c -d 5 --json  # +紧凑 +深度限制
agent-browser snapshot -s "#main" -i      # 限定选择器范围
```

### 交互（基于Ref）

```bash
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser type @e3 "text"
agent-browser hover @e4
agent-browser check @e5 | uncheck @e5
agent-browser select @e6 "value"
agent-browser press "Enter"
agent-browser scroll down 500
agent-browser drag @e7 @e8
```

### 获取信息

```bash
agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
agent-browser get count ".item" --json
```

### 检查状态

```bash
agent-browser is visible @e2 --json
agent-browser is enabled @e3 --json
agent-browser is checked @e4 --json
```

### 等待

```bash
agent-browser wait @e2                    # 等待元素
agent-browser wait 1000                   # 等待毫秒
agent-browser wait --text "Welcome"       # 等待文本
agent-browser wait --url "**/dashboard"   # 等待URL
agent-browser wait --load networkidle     # 等待网络空闲
agent-browser wait --fn "window.ready"    # 等待函数
```

### 会话（隔离浏览器）

```bash
agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
```

### 状态持久化

```bash
agent-browser state save auth.json        # 保存cookies/storage
agent-browser state load auth.json        # 加载（跳过登录）
```

### 截图和PDF

```bash
agent-browser screenshot page.png
agent-browser screenshot --full page.png
agent-browser pdf page.pdf
```

---

## 工作流程

```bash
# 1. 导航并快照
agent-browser open https://example.com
agent-browser snapshot -i --json

# 2. 从JSON解析refs，然后交互
agent-browser click @e2
agent-browser fill @e3 "text"

# 3. 页面变化后重新快照
agent-browser snapshot -i --json
```

---

## 快照输出格式

```json
{
  "success": true,
  "data": {
    "snapshot": "...",
    "refs": {
      "e1": {"role": "heading", "name": "Example Domain"},
      "e2": {"role": "button", "name": "Submit"},
      "e3": {"role": "textbox", "name": "Email"}
    }
  }
}
```

---

## 使用场景

### 场景一：搜索并提取

```bash
agent-browser open https://www.google.com
agent-browser snapshot -i --json
# AI识别搜索框 @e1
agent-browser fill @e1 "AI agents"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot -i --json
# AI识别结果refs
agent-browser get text @e3 --json
agent-browser get attr @e4 "href" --json
```

### 场景二：多会话测试

```bash
# Admin会话
agent-browser --session admin open app.com
agent-browser --session admin state load admin-auth.json

# User会话（并行）
agent-browser --session user open app.com
agent-browser --session user state load user-auth.json
```

### 场景三：绕过登录

```bash
# 首次登录后保存状态
agent-browser open https://app.com/login
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# 下次直接加载状态
agent-browser open https://app.com
agent-browser state load auth.json
```

---

## 最佳实践

| 实践 | 说明 |
|------|------|
| **总是使用 -i 标志** | 聚焦交互元素 |
| **总是使用 --json** | 便于解析 |
| **等待稳定** | `wait --load networkidle` |
| **保存认证状态** | 用 `state save/load` 跳过登录 |
| **使用会话** | 隔离不同浏览器上下文 |
| **调试用 --headed** | 看到浏览器操作 |

---

## 网络控制

```bash
agent-browser network route "**/ads/*" --abort           # 阻止
agent-browser network route "**/api/*" --body '{"x":1}'  # Mock
agent-browser network requests --filter api              # 查看
```

---

## Cookies和Storage

```bash
agent-browser cookies                     # 获取所有
agent-browser cookies set name value
agent-browser storage local key           # 获取localStorage
agent-browser storage local set key val
```

---

## 标签页和框架

```bash
agent-browser tab new https://example.com
agent-browser tab 2                       # 切换标签
agent-browser frame @e5                   # 切换iframe
agent-browser frame main                  # 返回主框架
```

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 深度研究 | 网页数据采集 |
| 网页净化 | 复杂页面提取 |
| API Gateway | 结合浏览器和API |
| SEO写作 | 竞品网站分析 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/agent-browser/` |
| SKILL.md | `/Users/bjd/intelligence/agent-browser/SKILL.md` |

---

## 链接

- **GitHub:** https://github.com/vercel-labs/agent-browser
- **作者:** Yossi Elkrief (@MaTriXy)

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:05*
*技能来源: 老庄发送*
*提供者: Vercel Labs*
*维护者: 姜小牙*