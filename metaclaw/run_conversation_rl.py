#!/usr/bin/env python3
"""
MetaClaw 进化训练脚本
基于老庄提供的养虾计划
"""

import os
import sys
from pathlib import Path

# 添加虚拟环境路径
venv_path = Path.home() / ".venv" / "metaclaw" / "lib" / "python3.14" / "site-packages"
sys.path.insert(0, str(venv_path))

from tinker import Tinker
from tinker.cookbook import MetaClawConfig

# ========== 配置区域 ==========

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
KIMI_API_KEY = os.getenv("KIMI_API_KEY", "")

# MetaClaw 配置
config = MetaClawConfig(
    # 技能注入 - 自动检索并匹配最佳技能指令
    use_skills=True,
    
    # 技能进化 - 开启自我创造（烧钱模式）
    enable_skill_evolution=True,
    
    # 使用高智力模型
    model="gpt-4o",  # 或 "kimi-2.5" / "claude-3.5"
    
    # 全量上下文（关闭QMD检索）
    full_context=True,
    
    # 禁用上下文压缩
    context_compression=False,
    
    # 高频心跳间隔（秒）
    heartbeat_interval=300,  # 5分钟
)

# ========== 训练循环 ==========

def run_training():
    """运行训练循环"""
    print("🚀 MetaClaw 进化训练开始")
    print(f"📊 配置: use_skills={config.use_skills}, enable_evolution={config.enable_skill_evolution}")
    print(f"📊 模型: {config.model}")
    print(f"📊 全量上下文: {config.full_context}")
    print(f"📊 心跳间隔: {config.heartbeat_interval}秒")
    print()
    
    # 初始化 Tinker
    tinker = Tinker(config=config)
    
    # 连接 OpenClaw
    print("🔗 连接 OpenClaw 网关...")
    tinker.connect()
    
    # 开始训练循环
    print("💫 开始训练！每一次对话都是一次梯度更新...")
    print("按 Ctrl+C 停止训练")
    print()
    
    try:
        tinker.train_loop()
    except KeyboardInterrupt:
        print("\n🛑 训练停止")
    finally:
        tinker.close()

if __name__ == "__main__":
    # 检查 API Key
    if not OPENAI_API_KEY and not KIMI_API_KEY:
        print("⚠️ 请设置环境变量 OPENAI_API_KEY 或 KIMI_API_KEY")
        print("   export OPENAI_API_KEY='你的密钥'")
        sys.exit(1)
    
    run_training()
