# TASKS.md - 代码侠

**最后更新：2026-04-07 07:55 | 小花 🦞**
**官网部署已交接给代码侠**

---

## 🔴 P0

**给桐桐写信**
- 小花要求每个agent给桐桐写一封信
- 格式：标题「给桐桐的信（来自XXX）」+ 温馨内容 + 落款
- 完成后发给我（sessions_send），我来汇总

**story.html 锚点**
- 目标：在 story.html 每个故事区块添加 `id="story-N"`（N=1-28）
- 原因：story-wall.html 跳转依赖此锚点
- 状态：待认领

~~风控执行机~~ ❌ **已废弃**（风控官已禁用，信号源消失）

---

## 🟡 P1

~~八卦页面重建~~ — 等小花分配新任务

~~风控执行机~~ ❌ **已废弃**（风控官已禁用，信号源消失）

---

## 🆕 官网部署规范（代码侠负责）

### 默认部署流程：push自动部署
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
git add .
git commit -m "简短描述"
git push origin main
# Vercel自动检测push，自动部署到 xiaohuahua.vercel.app
```

### 需要手动vercel deploy的情况
data/目录的文件更新（Vercel不监听data/）：
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team/website
vercel --token dHo95OkFlAlClRFXOXcGZtT9
```

### 平台信息

| 平台 | 地址 | 状态 |
|------|------|------|
| **Vercel** | xiaohuahua.vercel.app | 主力，push自动 |
| **CF Pages** | dengpao.pages.dev | 备用 |

### GitHub仓库
- github.com/bjd1129-create/zhugedengpao
- 主分支：main（所有开发必须在main）
- **重要：不要在其他分支开发，必须在main**

### Vercel Token（永久）
```
dHo95OkFlAlClRFXOXcGZtT9
```

---

## 📁 目录结构

```
website/pages/   # 36个HTML页面
website/docs/    # 文档
data/trading/   # 交易数据（不自动同步，需手动vercel deploy）
```

---

## 🔑 老虎证券API

**私钥（PKCS#1格式）**
```
MIICXAIBAAKBgQCby+x38wRMjNZgdEKRsfqGPLD+TUrRFu4l5FQsmdZ5ZiZWXvXpdlR6MmnKk473jNvBnwUN8qDqujHrn0DOjfmrHCd46Pi+wsVkbf3xbKPXh9RabddOXfMMwTF0nh5P9wk9oG0GG1Prxz2cNHuMBBPE+6Whp/01jLgfcoZb7PImUwIDAQABAoGAVmv+VmNl5RjS6lpTewJhWAlenRI/CFFR9Y786mjDwj/Z0FuIyeKr5cUFTiwgSE3IsVUGtr/6Z3q1qmCC0JGNBnH5qttIZwLLxUl/RX31IiYwjUC8rY/AhPa5Uwp4nNYi3qKsMIYV1Efg2Rm1B68iZhL/GtEnSo0PMIdK8GSMqAECQQDT4pzMU35t69+qdZn1GGU2FQqe0MuYZk+eRPW2QRpnwaCWZiv60b6Fdjioh/UZbJ/gNetyxbcVDqti1sORN/hTAkEAvDvP7DsZoo7nBF7CcDd+IFKTPyHmzi65kIHek/SmQJ/JR4ZNKTWzFSdVnSzNSvFbkr7V4WAkSW1Gx1du5j9aAQJBALzQZwvJp5OKqxD6pUx9Bcww6frmc1eGbJLMPu2/jClDqbf8qlpjyFSkKg88wJR8cOfbBMqNF/5CyUVVvobNCpMCQDKbkiddLGM8MHhIUdaB1PMzwEr0/mzouxNTF1iIKjqtuxvzy8MMoP1K+gWsCfXgNlKZ5D8X7imfq6vkofhdiAECQBUpHPtTE6D2xpPYVlaL1KykPIb1GgAu228v1w+eqgi6zuSgTymZXvn2pIQ/mvzTgXOqU/CpkwhdDTLmDQMpgI0=
```

**Tiger ID**: 20158404
**账户**: 21639635499102726（模拟）
**环境**: PROD

**测试命令**：
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
HTTPS_PROXY=http://127.0.0.1:7897 http_proxy=http://127.0.0.1:7897 /Users/bjd/.venv/tiger/bin/python3 agents/trader/tiger_api.py
```

---

最后更新：2026-04-07 07:55 | 小花 🦞
