# CrewAI 团队工作空间

**创建时间**: 2026-04-10
**状态**: ✅ 运行中
**桥接服务**: `http://127.0.0.1:8001` (CrewAI Bridge FastAPI)

---

## 一、空间定位

CrewAI 全自动执行团队的专属工作区。
- OpenClaw 大花团队 = **决策/协调层**（大脑）
- CrewAI 团队 = **自动化执行层**（手脚）

---

## 二、目录结构

```
agents/crewai/
├── crews/          # Crew 定义 (Python)
│   ├── __init__.py
│   └── core.py     # 4 个核心 Crew 工厂
├── config/         # Agent 定义 + LLM 配置
│   ├── __init__.py
│   ├── agents.py   # 6 个 Agent 角色定义
│   └── .env        # API Key 等敏感配置
├── results/        # 执行结果输出
├── memory/         # Agent 记忆沉淀
├── logs/           # Bridge 执行日志
├── dispatch.sh     # ⚡ 一键任务下发脚本
└── README.md       # 本文件
```

---

## 三、快速开始

### 方式一：dispatch.sh 脚本（推荐）

```bash
# 内容创作
./dispatch.sh content "AI如何帮普通人提升效率" "官网"

# 交易分析
./dispatch.sh trading BTC 5000

# 每日运营
./dispatch.sh daily_ops

# 深度调研
./dispatch.sh research "2026年DeFi市场趋势"

# 查看任务状态
./dispatch.sh status <task_id>

# 列出所有任务
./dispatch.sh list

# 检查服务健康
./dispatch.sh health
```

### 方式二：直接调用 API

```bash
# 提交任务
curl -X POST http://127.0.0.1:8001/api/tasks/start \
  -H "Content-Type: application/json" \
  -d '{"task_type": "content", "user_id": "laozhuang", "params": {"topic": "主题", "platform": "官网"}}'

# 查询进度
curl http://127.0.0.1:8001/api/tasks/<task_id>

# 健康检查
curl http://127.0.0.1:8001/api/health
```

---

## 四、可用 Crew 列表

| 任务类型 | 流程 | 参数 |
|---------|------|------|
| `content` | Scout调研 → Quill写作 → Observer审核 → Captain发布 | `topic`, `platform` |
| `trading` | Strategist分析 → Captain审批 → Observer复盘 | `symbol`, `amount`, `trade_type` |
| `daily_ops` | Scout情报 → Strategist分析 → Captain决策 → Observer审核 | `date` (可选) |
| `research` | Scout调研 → Strategist分析 → Observer评估 → Captain决策 | `research_topic` |

---

## 五、Agent 角色

| 角色 | 定位 | 职责 |
|------|------|------|
| **Captain** (CEO) | 最终决策者 | 拍板定案、风险控制 |
| **Strategist** (CFO) | 首席战略官 | 技术分析、基本面、仓位管理 |
| **Scout** (CMO) | 首席市场官 | 情报收集、市场调研 |
| **Quill** (内容总监) | 作家 | 内容创作、品牌文案 |
| **Engineer** (CTO) | 首席技术官 | 技术选型、架构设计 |
| **Observer** (COO) | 首席运营官 | 质量审核、流程复盘 |

---

## 六、技术栈

- **CrewAI**: `1.9.3`
- **Python**: `3.12` (独立 `.venv`)
- **LLM**: `qwen3.6-plus` (DashScope)
- **Bridge**: FastAPI + Uvicorn (线程池隔离，不阻塞 API)

---

## 七、已知问题

- CrewAI 多 Agent 链式调用较慢（每个 Agent 需等待 LLM 响应），单任务约 3-5 分钟
- 无搜索工具时 Agent 依赖自身知识库，建议调研类任务配合外部数据源

---

*最后更新: 2026-04-10 | 维护者: 大花团队*
