# TOOLS.md - 风控官本地工具配置

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
from tiger_connection import get_assets, get_positions
```

### Python 环境
- **路径**：`/Users/bjd/.venv/tiger/bin/python`

### 数据文件
- **老虎数据**：`/Users/bjd/Desktop/ZhugeDengpao-Team/website/data/trading/tiger_us_paper.json`
- **加密组合**：`/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json`

### 风控参数（速查）
- 止损线：$9,500
- 止盈线：$10,500
- 警告线：$10,000
- 单笔上限：$300
- 单日最大亏损：$500（5%）

### 汇报目标
- 小花：sessions_send(sessionKey: agent:main:main)
- 交易员：sessions_send(sessionKey: agent:main:main)
