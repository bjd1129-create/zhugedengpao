# SKILL.md - 数据官

## 核心技能：数据展示与页面开发

### 更新交易页面
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
git add trading.html
git commit -m "dataviz: 更新 $(date +%H:%M)"
git push origin main
```

### 触发Cloudflare部署
```bash
cd /Users/bjd/Desktop/ZhugeDengpao-Team
printf 'y\n' | npx wrangler pages deploy . --project-name=dengpao
```

### 检查页面状态
访问：https://dengpao.pages.dev/trading

### 读取 portfolio.json
```bash
python3 -c "
import json
p=json.load(open('data/trading/portfolio.json'))
print(f'更新: {p[\"lastUpdated\"]}')
print(f'总值: \${p[\"account\"][\"totalValue\"]:,.2f}')
for h in p['holdings']:
    print(f'{h[\"symbol\"]}: \${h[\"value\"]:,.2f}')
"
```

## 页面改进方向

### 当前已实现
- ✅ 实时价格（CoinGecko，15秒刷新）
- ✅ 账户总值联动（实时价格重算）
- ✅ 持仓分布环形图
- ✅ 网格状态可视化
- ✅ 多币种支持（BTC/ETH/AVAX/ADA）

### 可改进方向
- 添加收益曲线图（Canvas）
- 添加交易历史详情弹窗
- 添加持仓分布饼图
- 移动端适配优化
- 添加"最后更新时间"动画

## GitHub Push 规则
- trading.html → 直接 push
- portfolio.json → 一般不单独 push（交易员会同步）
- 其他页面改动 → 确认后 push
