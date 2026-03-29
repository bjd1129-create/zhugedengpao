---
title: OpenClaw 双版本连发：v2026.3.22 + v2026.3.23 合并更新指南
source: jimo.studio
url: https://jimo.studio/blog/openclaw-dual-version-release-combined-update-guide-v2026322-and-v2026323/
score: 9.0
tags: [OpenClaw, 版本更新, 安全修复, Memory系统]
date: 2026-03-29
summary: OpenClaw两周连发v2026.3.22和v2026.3.23，累计10+项安全修复、Memory重大架构升级、50+Bug修复，建议尽快升级。
---

## 核心更新

**Memory 系统重大架构升级**：QMD后端搜索模式改为CPU-only召回，结果限制提前处理降低内存，索引优化避免读取完整markdown文件。

**安全加固**：Memory-LanceDB防护prompt-injection攻击，Media限制本地媒体读取仅限workspace/和sandboxes/，Exec工具增强approvals机制防止safeBins绕过，配对令牌升级为256-bit base64url。

**渠道功能**：Telegram渠道需要数字发送者ID白名单授权，Browser工具强化文件上传下载防护，认证与配对安全全面加强。

**安全默认值变更**：autoCapture默认禁用防止意外捕获PII，Prompt注入防护跳过可疑载荷，Watcher限制监控markdown文件。
