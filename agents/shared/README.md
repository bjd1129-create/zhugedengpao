# 共享目录 - 完全开放访问

**最后更新**：2026-04-08 21:27

---

## 权限说明

**所有 Agent 可以完全访问此目录**

| Agent | 读取 | 写入 | 删除 |
|-------|------|------|------|
| 小花 | ✅ | ✅ | ✅ |
| 交易员 | ✅ | ✅ | ✅ |
| 工程师 | ✅ | ✅ | ✅ |
| 协调官 | ✅ | ✅ | ✅ |
| 数据分析师 | ✅ | ✅ | ✅ |

---

## 目录结构

```
agents/shared/
├── messages/     # 消息队列（Agent 间通信）
├── data/         # 共享数据（交易数据、市场数据等）
├── docs/         # 共享文档（联合报告、协作指南等）
└── README.md     # 本文件
```

---

## 使用规范

### 消息队列（messages/）

**发送消息**：
```bash
echo '{"from":"交易员","to":"工程师","content":"请更新交易页面"}' > messages/engineer.json
```

**接收消息**：
```bash
if [ -f "messages/本 agent.json" ]; then
  cat messages/本 agent.json
  rm messages/本 agent.json
fi
```

### 共享数据（data/）

**写入数据**：
```bash
cat > data/trades_today.json << 'DATA'
{"trades": [...]}
DATA
```

**读取数据**：
```bash
cat data/trades_today.json
```

### 共享文档（docs/）

**创建联合文档**：
```bash
cat > docs/联合复盘-2026-04-09.md << 'DOC'
# 联合复盘

## 交易员
...

## 数据分析师
...
DOC
```

---

## 文件命名规范

| 类型 | 命名格式 | 示例 |
|------|---------|------|
| 消息 | `目标 agent.json` | `trader.json` |
| 数据 | `内容_日期.json` | `trades_2026-04-09.json` |
| 文档 | `主题 - 日期.md` | `联合复盘 -2026-04-09.md` |

---

## 清理规则

- 消息文件：读取后删除
- 数据文件：保留 30 天
- 文档文件：永久保留

---

_小花团队 | 2026-04-08_
