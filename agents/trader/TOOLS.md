# TOOLS.md - 交易员本地工具配置

## 核心工具

### Python 环境
- **路径**：`/Users/bjd/.venv/tiger/bin/python`
- **Tiger API**：`/Users/bjd/.venv/tiger/lib/python3.14/site-packages/tigeropen/`
- **SSL证书**：`/Users/bjd/.venv/tiger/lib/python3.14/site-packages/certifi/cacert.pem`

### 数据文件
- portfolio.json：`/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json`
- 美股数据：`/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/tiger_us_paper.json`

### 脚本路径
- 网格模拟器：`/Users/bjd/Desktop/ZhugeDengpao-Team/trading_simulator.py`
- 老虎抓取：`/Users/bjd/Desktop/ZhugeDengpao-Team/agents/trader/tiger_us_fetch.sh`

### Git
- 工作目录：`/Users/bjd/Desktop/ZhugeDengpao-Team`
- 分支：main

## 代理配置

某些API需要代理：
```bash
PROXY='{"https":"http://127.0.0.1:7897"}'
```

Binance API 需要代理。
老虎证券 API 不需要代理。
