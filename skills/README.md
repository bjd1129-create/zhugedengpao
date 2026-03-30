# OpenClaw Skills 仓库

这是 OpenClaw 分布式技能同步仓库。

## 结构

- `skills/`: 所有 OpenClaw 技能目录
- `config.yaml`: OpenClaw 统一配置文件

## 同步机制

每台机器每分钟自动拉取最新版本，确保所有节点技能同步。

## 添加新技能

1. 在 `~/.openclaw/skills/` 下创建或修改技能
2. 提交并推送到中央仓库：
   ```bash
   cd ~/.openclaw/skills
   git add .
   git commit -m "Add new skill"
   git push origin main
   ```

3. 其他节点会在 60 秒内自动拉取更新
