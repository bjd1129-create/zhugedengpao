# TASKS.md - 代码侠

**最后更新：2026-04-06 22:22 | 小花 🦞**
**重要：所有官网部署相关信息已对齐**

---

## 🔴 P0（立即执行）

**风控执行机**
- 目标：风控官发🟡→系统自动锁仓，🟢→解锁
- 状态：进行中

---

## 🟡 P1（等P0完成后）

**八卦页面重建**
- 娱乐定位，现有官网风格

---

## 🆕 官网部署维护（信息已对齐）

### 平台信息

| 平台 | 地址 | 状态 |
|------|------|------|
| **Vercel** | xiaohuahua.vercel.app | 主力，自动部署 |
| **CF Pages** | dengpao.pages.dev | 备用，手动 |

### GitHub仓库
- 仓库：github.com/bjd1129-create/zhugedengpao
- 主分支：main
- Vercel已关联，push自动触发部署

### Vercel Token（永久）
```
dHo95OkFlAlClRFXOXcGZtT9
```

### 部署命令
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team/website
vercel --token dHo95OkFlAlClRFXOXcGZtT9
```

### 页面目录
```
website/pages/        # 36个HTML页面
website/docs/        # 文档
```

### 核心页面
- index.html - 首页
- trading.html - 交易页面（读取 data/trading/tiger_us_paper.json）
- tongtong-letters.html - 桐桐的信（新增）

### 数据文件
- `data/trading/tiger_us_paper.json` - 老虎证券模拟账户数据
- `data/trading/portfolio.json` - 加密货币组合数据
- `data/trading/polymarket_portfolio.json` - Polymarket组合

### 飞书Bot
- App ID: cli_a949489c9ca15bd7

---

## 🆕 老虎证券API（已修复）

**私钥（PKCS#1格式）**
```
MIICXAIBAAKBgQCby+x38wRMjNZgdEKRsfqGPLD+TUrRFu4l5FQsmdZ5ZiZWXvXpdlR6MmnKk473jNvBnwUN8qDqujHrn0DOjfmrHCd46Pi+wsVkbf3xbKPXh9RabddOXfMMwTF0nh5P9wk9oG0GG1Prxz2cNHuMBBPE+6Whp/01jLgfcoZb7PImUwIDAQABAoGAVmv+VmNl5RjS6lpTewJhWAlenRI/CFFR9Y786mjDwj/Z0FuIyeKr5cUFTiwgSE3IsVUGtr/6Z3q1qmCC0JGNBnH5qttIZwLLxUl/RX31IiYwjUC8rY/AhPa5Uwp4nNYi3qKsMIYV1Efg2Rm1B68iZhL/GtEnSo0PMIdK8GSMqAECQQDT4pzMU35t69+qdZn1GGU2FQqe0MuYZk+eRPW2QRpnwaCWZiv60b6Fdjioh/UZbJ/gNetyxbcVDqti1sORN/hTAkEAvDvP7DsZoo7nBF7CcDd+IFKTPyHmzi65kIHek/SmQJ/JR4ZNKTWzFSdVnSzNSvFbkr7V4WAkSW1Gx1du5j9aAQJBALzQZwvJp5OKqxD6pUx9Bcww6frmc1eGbJLMPu2/jClDqbf8qlpjyFSkKg88wJR8cOfbBMqNF/5CyUVVvobNCpMCQDKbkiddLGM8MHhIUdaB1PMzwEr0/mzouxNTF1iIKjqtuxvzy8MMoP1K+gWsCfXgNlKZ5D8X7imfq6vkofhdiAECQBUpHPtTE6D2xpPYVlaL1KykPIb1GgAu228v1w+eqgi6zuSgTymZXvn2pIQ/mvzTgXOqU/CpkwhdDTLmDQMpgI0=
```

**Tiger ID**: 20158404
**账户**: 21639635499102726（模拟）
**License**: TBNZ
**环境**: PROD

**代理设置**（调用API时需要）：
```bash
export HTTPS_PROXY="http://127.0.0.1:7897"
export http_proxy="http://127.0.0.1:7897"
```

**测试命令**：
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
HTTPS_PROXY=http://127.0.0.1:7897 http_proxy=http://127.0.0.1:7897 /Users/bjd/.venv/tiger/bin/python3 agents/trader/tiger_api.py
```

---

最后更新：2026-04-06 22:22 | 小花 🦞
