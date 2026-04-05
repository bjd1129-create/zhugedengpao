# TOOLS.md - 交易员本地工具配置

## 核心工具

### Tiger OpenAPI 连接（必须用这个！）
- **连接模块**：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_connection.py`
- **数据更新脚本**：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_us_update.py`
- **测试脚本**：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_test.py`
- **Python路径**：`/Users/bjd/.venv/tiger/bin/python`
- **账户**：21639635499102726（模拟盘 PAPER）
- **净值**：$1,000,000 | **现金**：$1,000,000 | **购买力**：$4,000,000

### 用法示例
```python
import sys
sys.path.insert(0, '/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader')
from tiger_connection import get_assets, get_positions, get_orders

# 获取资产
assets = get_assets()
# 获取持仓
positions = get_positions()
# 获取订单
orders = get_orders()
```

### 数据文件
- **老虎数据**：`/Users/bjd/Desktop/ZhugeDengpao-Team/website/data/trading/tiger_us_paper.json`
- **加密组合**：`/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json`

### 脚本路径
- 网格模拟器：`/Users/bjd/Desktop/ZhugeDengpao-Team/trading_simulator.py`
- 老虎抓取：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_us_fetch.sh`

### Git
- 工作目录：`/Users/bjd/Desktop/ZhugeDengpao-Team`
- 分支：main

## 代理配置

Binance API 需要代理，老虎证券 API 不需要代理。
```bash
PROXY='{"https":"http://127.0.0.1:7897"}'
```
