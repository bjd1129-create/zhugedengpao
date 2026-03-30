#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Skill - 检查 MemOS 从节点更新

主脑 (朱小璋) 使用此技能定期检查从节点状态
"""

import sys
import os
sys.path.append('/Users/bjd/intelligence/swarm')

from memos_distributed_bus import MemOSListener

def check_memos():
    """
    检查 MemOS 从节点更新
    
    使用示例 (在 OpenClaw 中):
    > 检查从节点有什么新动态
    > 看看刘伯温完成任务了吗
    > 有哪些 Agent 需要分配新任务
    """
    
    listener = MemOSListener()
    report = listener.get_team_status_report()
    
    return report

def check_agent_status(agent_name: str = None):
    """
    检查特定 Agent 状态
    
    Args:
        agent_name: Agent 名称 (如：刘伯温)
    
    Returns:
        str: 状态报告
    """
    
    listener = MemOSListener()
    updates = listener.check_new_updates(hours=24, agent_filter=agent_name)
    
    if not updates:
        return f"暂无 {agent_name} 的更新"
    
    report = []
    report.append(f"📋 {agent_name} 的最近动态:\n")
    
    for update in updates:
        report.append(f"• {update['content'][:100]}...")
    
    return "\n".join(report)

def get_pending_tasks():
    """
    获取待审核任务
    
    Returns:
        str: 待审核任务列表
    """
    
    listener = MemOSListener()
    updates = listener.check_new_updates(hours=24)
    
    pending = [
        u for u in updates
        if '✅' in u['content'] and 'status:pending_review' in u['content']
    ]
    
    if not pending:
        return "暂无待审核任务"
    
    report = []
    report.append("📋 待审核任务:\n")
    
    for task in pending:
        report.append(f"• {task['content'][:100]}...")
    
    return "\n".join(report)

# 主函数 (命令行测试)
if __name__ == "__main__":
    print("🧠 OpenClaw Skill - check_memos")
    print("="*60)
    
    # 测试检查更新
    print("\n📊 团队状态报告:\n")
    report = check_memos()
    print(report)
    
    # 测试检查特定 Agent
    print("\n\n📋 刘伯温状态:\n")
    status = check_agent_status("刘伯温")
    print(status)
    
    # 测试获取待审核任务
    print("\n\n📋 待审核任务:\n")
    pending = get_pending_tasks()
    print(pending)
