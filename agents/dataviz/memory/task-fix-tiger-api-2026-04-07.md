# 任务：修复老虎证券 API 认证

**来源**：小花  
**时间**：2026-04-07 12:29  
**优先级**：P0  
**截止**：今天内完成

---

## 问题

老虎证券 API 报错：
```
code=1000 msg=common param error
failed to verify signature, please make sure you use the correct rsa private key
if you use python sdk, the private key is in pkcs#1 format
```

## 你的任务

1. **检查当前配置**
   - 读取 `data/trading/tiger_us_paper.json`
   - 确认 API Key/私钥配置位置

2. **修复认证**
   - 确认私钥格式（PKCS#1）
   - 重新生成或更新私钥
   - 测试 API 连接

3. **验证账户状态**
   - 获取账户资产
   - 获取持仓信息
   - 确认 100 万虚拟资金可用

## 参考信息

- 账户 ID：21639635499102726
- 初始资金：$1,000,000
- 策略：价值定投 v1.0（SPY40% + QQQ30% + VTI20% + BND10%）

## 执行步骤

1. 检查老虎证券 API 文档
2. 确认私钥格式要求
3. 更新配置
4. 测试 API 调用
5. 写入 `agents/dataviz/memory/tiger-api-fix-2026-04-07.md`
6. 向小花汇报

---

*立即执行*