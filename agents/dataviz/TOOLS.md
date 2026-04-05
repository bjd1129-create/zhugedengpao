# TOOLS.md - 数据官本地工具配置

## 核心工具

### Tiger OpenAPI 连接
- **连接模块**：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_connection.py`
- **数据更新脚本**：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_us_update.py`
- **账户**：21639635499102726（模拟盘 PAPER）
- **净值**：$1,000,000 | 现金：$1,000,000 | 购买力：$4,000,000

### 用法
```bash
# 更新老虎数据
python3 /Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_us_update.py
```
```python
import sys
sys.path.insert(0, '/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader')
from tiger_connection import get_assets, get_positions
```

### Git
- 工作目录：`/Users/bjd/Desktop/ZhugeDengpao-Team`
- 分支：main
- 部署：Cloudflare Pages（dengpao.pages.dev）

### 文件路径
- **老虎数据**：`/Users/bjd/Desktop/ZhugeDengpao-Team/website/data/trading/tiger_us_paper.json`
- **trading页面**：`/Users/bjd/Desktop/ZhugeDengpao-Team/website/pages/trading.html`
- **加密组合**：`/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json`

### Wrangler（Cloudflare部署）
```bash
npx wrangler pages deploy website --project-name=dengpao
```

### 数据新鲜度检查
- 最后更新时间 > 10分钟 → 标记为⚠️
- 最后更新时间 > 30分钟 → 标记为🔴
