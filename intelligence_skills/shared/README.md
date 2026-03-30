# 华夏智能共享技能库

**所有 Agent 共用一个技能库！**

## 📂 技能库位置

**主存储:** `/Users/bjd/intelligence/skills/shared/`

**同步目标:**
- MBP: `~/intelligence/skills/shared/`
- AZW: `~/intelligence/skills/shared/`
- i3: `~/intelligence/skills/shared/`
- 大明智能团队：`~/intelligence/skills/shared/`

## 🔄 同步机制

**同步频率:** 实时同步 (文件变更时)

**同步方式:** rsync + inotify

**同步脚本:** `/Users/bjd/intelligence/skills/sync-skills.sh`

## 📚 技能分类

### 1. 通用技能 (所有 Agent 共享)

- `communication.md` - 沟通技能
- `coordination.md` - 协调技能
- `analysis.md` - 分析技能
- `planning.md` - 规划技能

### 2. 角色技能 (按角色共享)

- `ceo/` - CEO/领袖技能
- `cto/` - CTO/技术技能
- `developer/` - 开发技能
- `designer/` - 设计技能

### 3. 项目技能 (按项目共享)

- `official-website/` - 官网开发技能
- `pixel-office/` - 像素办公室技能
- `memos/` - Memos 集成技能

## 🚀 使用方式

### 在 OpenClaw 配置中引用

```yaml
skills:
  - path: /Users/bjd/intelligence/skills/shared/communication.md
  - path: /Users/bjd/intelligence/skills/shared/coordination.md
```

### 动态加载技能

```python
from skills_loader import load_skill

# 加载共享技能
skill = load_skill('/Users/bjd/intelligence/skills/shared/communication.md')
```

## 📊 技能库统计

| 分类 | 技能数 | 状态 |
|------|--------|------|
| 通用技能 | 4 | ✅ 已创建 |
| 角色技能 | 0 | ⏳ 待创建 |
| 项目技能 | 0 | ⏳ 待创建 |

## 🔄 更新流程

1. **创建/修改技能** → 保存到共享技能库
2. **自动同步** → rsync 同步到所有 Agent
3. **热加载** → Agent 自动加载新技能
4. **版本控制** → Git 记录变更历史

---

*华夏智能 HUAXIA.AI | 团队进化官：张良*
