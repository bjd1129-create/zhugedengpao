# 交易数据保护规则

## 铁律：portfolio.json 是核心数据

### 绝对禁止
- ❌ 禁止清空 portfolio.json
- ❌ 禁止删除 fills（交易记录）
- ❌ 禁止修改历史交易数据
- ❌ 禁止在不备份的情况下修改模拟器

### 操作规范
1. **改模拟器前**：先 `git add data/trading/portfolio.json && git commit -m "backup"`
2. **修改模拟器**：只改代码逻辑，不动数据文件
3. **数据坏了**：先 git commit 坏的版本，再修复（而不是删除）
4. **portfolio.json**：只追加新数据，历史数据永不删除

### 数据结构保护
- `fills[]`：所有历史交易，只增不减
- `equityCurve`：每日净值，追加不覆盖
- `holdings`：快照，不删历史记录
