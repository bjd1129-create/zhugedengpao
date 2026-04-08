# 操盘页面交接文档

## 交接时间
2026-04-08 11:49

## 交接方
- **交出**: 工程师 (Engineer)
- **接收**: 交易员 (Trader) 📈

---

## 一、页面文件位置

### 源文件
```
agents/engineer/website/pages/trading.html
```

### 部署平台
| 平台 | 域名 | 项目 |
|------|------|------|
| **Vercel** | https://xiaohuahua.vercel.app | zhugedengpaos-projects/xiaohua |
| **Cloudflare Pages** | https://dengpao.pages.dev | dengpao |

---

## 二、页面结构

### 4 个模拟盘（按顺序）
1. 📈 **美股模拟盘** - 老虎证券 - $1,000,000 初始
2. 📊 **期货模拟盘** - 老虎证券 - $500,000 初始
3. 🎯 **Polymarket 模拟盘** - Polymarket - $100,000 初始
4. ₿ **加密货币网格** - Binance - $10,000 初始

### 数据对象格式
```javascript
const simulations = {
  us: {
    name: "美股模拟盘",
    provider: "老虎证券",
    icon: "📈",
    initialCapital: 1000000,
    currentValue: 1023450,
    cash: 234500,
    currency: "USD",
    status: "running",
    positions: [
      { symbol: "AAPL", shares: 100, avgPrice: 175.50, currentPrice: 182.30, return: 6.15 }
    ],
    trades: [
      { time: "2026-04-08 10:30", type: "buy", symbol: "AAPL", shares: 100, price: 175.50, total: 17550 }
    ]
  },
  futures: { ... },
  polymarket: { ... },
  crypto: { ... }
};
```

---

## 三、部署命令

### Vercel 部署
```bash
cd agents/engineer/website
npx vercel --prod --yes --scope zhugedengpaos-projects

# 设置域名别名
npx vercel alias <deployment-url> xiaohuahua.vercel.app
```

### Cloudflare Pages 部署
```bash
cd agents/engineer/website
npx wrangler pages deploy pages --project-name=dengpao --commit-dirty=true
```

---

## 四、数据更新流程

### 1. 更新本地数据文件
交易员已有数据源：
- `data/trading/portfolio.json` - 主持仓数据
- `data/trading/price_aggregate.json` - 价格聚合（每 30 秒更新）
- `data/trading/tiger_us_paper.json` - 老虎证券美股模拟盘

### 2. 更新 trading.html 中的模拟数据
编辑 `agents/engineer/website/pages/trading.html` 中的 `simulations` 对象，更新：
- `currentValue` - 当前价值
- `cash` - 可用现金
- `positions` - 持仓列表
- `trades` - 交易记录

### 3. 部署到两个平台
```bash
# Vercel
npx vercel --prod --yes --scope zhugedengpaos-projects

# Cloudflare Pages
npx wrangler pages deploy pages --project-name=dengpao
```

---

## 五、Vercel 配置信息

### 项目信息
- **Project ID**: `prj_A3gLsQO5NjmnhIdmz8fk6AnYU6XD`
- **Organization**: `team_3TfZbZ1uGX7WWLVlew6yrU26`
- **Scope**: `zhugedengpaos-projects`
- **域名**: `xiaohuahua.vercel.app`
- **部署目录**: `pages/`（静态 HTML）

### vercel.json 配置
```json
{
  "framework": null,
  "buildCommand": "echo static",
  "outputDirectory": "pages"
}
```

---

## 六、Cloudflare Pages 配置

- **项目名**: `dengpao`
- **域名**: `dengpao.pages.dev`
- **部署目录**: `pages/`

---

## 七、交易员职责

### 日常更新
- [ ] 每 5 分钟更新价格数据（已有 cron 自动运行）
- [ ] 每日更新持仓数据到 `trading.html`
- [ ] 记录新交易历史
- [ ] 部署更新到 Vercel 和 CF Pages

### 定期维护
- [ ] 检查 API 连通性（老虎证券、Binance、Polymarket）
- [ ] 验证数据准确性
- [ ] 清理过期数据
- [ ] 备份重要数据（`portfolio.json` 等）

### 注意事项
1. **两个平台都要部署** - 确保数据同步
2. **CDN 缓存** - 部署后可能需要 2-5 分钟生效
3. **测试链接** - 部署后检查两个域名都能访问
4. **数据一致性** - 确保 Vercel 和 CF Pages 数据一致

---

## 八、相关文件清单

| 文件 | 用途 | 位置 |
|------|------|------|
| `trading.html` | 操盘页面 | `agents/engineer/website/pages/` |
| `trading_simulator.py` | 交易模拟器 | `agents/trader/` |
| `tiger_us_fetch.sh` | 老虎数据抓取 | `agents/trader/` |
| `portfolio.json` | 持仓数据 | `data/trading/` |
| `price_aggregate.json` | 价格聚合 | `data/trading/` |
| `tiger_us_paper.json` | 老虎模拟盘 | `data/trading/` |

---

## 九、常见问题

### Q: 部署后页面没更新？
A: 清除浏览器缓存（Cmd+Shift+R），等 2-5 分钟 CDN 刷新

### Q: Vercel 部署失败？
A: 检查 `vercel.json` 配置，确保 `outputDirectory: "pages"`

### Q: 数据不同步？
A: 两个平台都要部署，分别执行 Vercel 和 CF 部署命令

---

**交接完成时间**: 2026-04-08 11:49
**交易员确认**: 待确认

🦞 工程师 交
