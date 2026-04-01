# Auto-Updater自动更新技能

> **技能获取时间:** 2026-03-18 20:08
> **技能来源:** 老庄发送
> **用途:** 自动更新Clawdbot和所有已安装技能

---

## 技能描述

自动更新Clawdbot核心和所有已安装技能，设置每日定时检查，更新完成后发送汇总报告。

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **Clawdbot更新** | 自动检测并更新Clawdbot核心 |
| **技能更新** | 通过ClawdHub更新所有已安装技能 |
| **定时执行** | 每日定时运行（默认4:00 AM） |
| **汇总报告** | 更新完成后发送变更摘要 |

---

## 快速设置

```bash
# 一句话设置
clawdbot cron add \
  --name "Daily Auto-Update" \
  --cron "0 4 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --wake now \
  --deliver \
  --message "Run daily auto-updates: check for Clawdbot updates and update all skills. Report what was updated."
```

---

## 更新流程

```
1. 检测安装类型
   ├── npm全局安装 → npm update -g clawdbot@latest
   ├── pnpm全局安装 → pnpm update -g clawdbot@latest
   ├── bun全局安装 → bun update -g clawdbot@latest
   └── 源码安装 → clawdbot update

2. 运行doctor
   └── clawdbot doctor --yes

3. 更新技能
   └── clawdhub update --all

4. 发送汇总
   └── 版本变更、更新列表、错误信息
```

---

## 检测安装类型

```bash
# npm全局
npm list -g clawdbot 2>/dev/null && echo "npm-global"

# 源码安装
[ -d ~/.clawdbot/.git ] && echo "source-install"

# pnpm
pnpm list -g clawdbot 2>/dev/null && echo "pnpm-global"

# bun
bun pm ls -g 2>/dev/null | grep clawdbot && echo "bun-global"
```

---

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| Time | 4:00 AM | 更新时间 |
| Timezone | 系统默认 | 时区设置 |
| Delivery | 主会话 | 报告发送位置 |

### 自定义示例

```bash
# 不同时间
--cron "0 6 * * *"  # 早上6点

# 不同时区
--tz "Asia/Shanghai"

# 每周更新
--cron "0 4 * * 0"  # 每周日凌晨4点
```

---

## 更新报告格式

### 完整更新

```
🔄 Daily Auto-Update Complete

**Clawdbot**
Updated: v2026.1.9 → v2026.1.10

**Skills Updated (3)**
1. prd: 2.0.3 → 2.0.4
2. browser: 1.2.0 → 1.2.1
3. nano-banana-pro: 3.1.0 → 3.1.2

**Skills Already Current (5)**
gemini, sag, things-mac, himalaya, peekaboo

✅ All updates completed successfully.
```

### 无更新

```
🔄 Daily Auto-Update Check

**Clawdbot**: v2026.1.10 (already latest)

**Skills**: All 8 installed skills are current.

Nothing to update today.
```

### 部分更新

```
🔄 Daily Auto-Update Complete (with issues)

**Clawdbot**: v2026.1.9 → v2026.1.10 ✅

**Skills Updated (1)**
1. prd: 2.0.3 → 2.0.4 ✅

**Skills Failed (1)**
1. ❌ nano-banana-pro: Network timeout
   Recommendation: Run `clawdhub update nano-banana-pro` manually

⚠️ Completed with 1 error.
```

---

## 手动命令

### 检查更新（不应用）

```bash
clawdhub update --all --dry-run
```

### 查看已安装技能

```bash
clawdhub list
```

### 查看Clawdbot版本

```bash
clawdbot --version
```

---

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| `EACCES` 权限错误 | 使用sudo或修复权限 |
| 网络超时 | 重试一次，然后报告 |
| Git冲突（源码安装） | 使用 `clawdbot update --force` |

---

## 禁用自动更新

```bash
# 移除定时任务
clawdbot cron remove "Daily Auto-Update"

# 或临时禁用
# 在配置中设置 cron.enabled = false
```

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 自我进化引擎 | 结合自动更新能力 |
| 安全审计 | 更新后安全检查 |
| 飞书文档 | 更新日志同步 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/auto-updater/` |
| SKILL.md | `/Users/bjd/intelligence/auto-updater/SKILL.md` |
| Agent指南 | `/Users/bjd/intelligence/auto-updater/references/agent-guide.md` |
| 示例报告 | `/Users/bjd/intelligence/auto-updater/references/summary-examples.md` |

---

## 链接

- **Clawdbot更新指南:** https://docs.clawd.bot/install/updating
- **ClawdHub CLI:** https://docs.clawd.bot/tools/clawdhub
- **Cron Jobs:** https://docs.clawd.bot/cron

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:08*
*技能来源: 老庄发送*
*维护者: 姜小牙*