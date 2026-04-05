# TOOLS.md - 策略师本地工具配置

## 核心工具

### Tiger OpenAPI 连接
- **连接模块**：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_connection.py`
- **数据更新脚本**：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_us_update.py`
- **账户**：21639635499102726（模拟盘 PAPER）
- **净值**：$1,000,000 | 现金：$1,000,000 | 购买力：$4,000,000

### 用法示例
```python
import sys
sys.path.insert(0, '/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader')
from tiger_connection import get_assets, get_positions, get_orders
```

### Python 环境
- **路径**：`/Users/bjd/.venv/tiger/bin/python`
- **代理**：`{"https":"http://127.0.0.1:7897"}`

### 数据文件
- **老虎数据**：`/Users/bjd/Desktop/ZhugeDengpao-Team/website/data/trading/tiger_us_paper.json`
- **加密组合**：`/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json`
- **价格聚合**：`/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/price_aggregate.json`

### API
- Binance REST：`https://api.binance.com/api/v3/`
- K线间隔：1m/5m/15m/1h/4h/1d

### 工作目录
`/Users/bjd/Desktop/ZhugeDengpao-Team`
