# -*- coding: utf-8 -*-
"""
AutoClaw v1.1 - 自动化脚本工具箱 (macOS / OpenClaw 适配版)
功能：健康检查 + 自动备份 + 进程守护

冲突规避设计：
  - 纯 Python 标准库，不依赖 node / npm / openclaw 进程
  - 只做「只读检查 + 文件复制」，不写入 OpenClaw 核心数据目录
  - 备份目标写入独立目录，不污染 ~/.openclaw/ 结构
  - 日志独立存放，不与 OpenClaw logs 混用
"""

import os
import sys
import shutil
import json
from datetime import datetime
from pathlib import Path

# ────────────────────────────────────────────
# 默认路径（macOS 适配，原始代码写的是 Windows 路径）
# ────────────────────────────────────────────
DEFAULT_WORKSPACE   = str(Path.home() / ".openclaw" / "workspace")
DEFAULT_BACKUP_ROOT = str(Path.home() / ".openclaw" / "skills_backup_autoclaw")
DEFAULT_LOG_DIR     = str(Path.home() / ".openclaw" / "skills_backup_autoclaw" / "logs")


class AutoClaw:
    def __init__(self, workspace_path=None, backup_root=None, log_dir=None):
        self.workspace  = workspace_path or DEFAULT_WORKSPACE
        self.backup_dir = backup_root    or DEFAULT_BACKUP_ROOT
        self.log_file   = os.path.join(log_dir or DEFAULT_LOG_DIR, "autoclaw.log")

        # 只创建 autoclaw 自己专属的目录，绝不碰 ~/.openclaw/ 根目录
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        self.config = {
            "max_backups":    10,   # 最多保留 10 个备份
            "check_interval": 30,   # 检查间隔（分钟，供外部 cron 参考）
            "auto_restart":   False, # 默认关闭自动重启，避免与 OpenClaw 进程管理冲突
        }

        # 监控的进程列表（仅检查脚本文件是否存在，不做进程操作）
        # ⚠️  不包含 openclaw 本身 —— 它有自己的守护机制，不应被外部干预
        self.monitored_processes = [
            # 如需监控其他脚本，在此添加，格式示例：
            # {
            #     "name": "My Bot",
            #     "script": "relative/path/to/bot.js",
            # }
        ]

    # ────────────────────────────────────────────
    # 日志
    # ────────────────────────────────────────────
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        print(entry)

    # ────────────────────────────────────────────
    # 健康检查（只读，不修改任何文件）
    # ────────────────────────────────────────────
    def health_check(self):
        self.log("=" * 50)
        self.log("AutoClaw 健康检查")
        self.log("=" * 50)

        # 检查 workspace 下的通用核心文件
        checks = {
            "MEMORY.md":           self._check_file("MEMORY.md"),
            "SOUL.md":             self._check_file("SOUL.md"),
            "skills/ 目录":        self._check_dir("skills"),
        }

        ok = sum(1 for v in checks.values() if v)
        total = len(checks)
        self.log(f"检查结果：{ok}/{total} 正常")
        self.log("[OK] 健康检查完成" if ok == total else "[WARN] 部分文件/目录缺失")
        return ok == total

    def _check_file(self, rel):
        path = os.path.join(self.workspace, rel)
        ok = os.path.isfile(path)
        self.log(f"  {'[OK]' if ok else '[MISSING]'} {rel}")
        return ok

    def _check_dir(self, rel):
        path = os.path.join(self.workspace, rel)
        ok = os.path.isdir(path)
        self.log(f"  {'[OK]' if ok else '[MISSING]'} {rel}/")
        return ok

    # ────────────────────────────────────────────
    # 自动备份
    # 备份目标：~/.openclaw/skills_backup_autoclaw/backup_YYYYMMDD_HHMMSS/
    # 绝不写入 ~/.openclaw/ 核心目录
    # ────────────────────────────────────────────
    def auto_backup(self):
        self.log("\n" + "=" * 50)
        self.log("AutoClaw 自动备份")
        self.log("=" * 50)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{ts}")

        files_to_backup = [
            "MEMORY.md",
            "SOUL.md",
            "IDENTITY.md",
            "USER.md",
        ]

        backed_up = 0
        for f in files_to_backup:
            src = os.path.join(self.workspace, f)
            if os.path.exists(src):
                dest_dir = os.path.join(backup_path, os.path.dirname(f))
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(src, os.path.join(backup_path, f))
                backed_up += 1
                self.log(f"  [OK] {f}")
            else:
                self.log(f"  [SKIP] {f} 不存在")

        self._cleanup_old_backups()
        self.log(f"\n[OK] 备份完成：{backed_up} 个文件 → {backup_path}")
        return backup_path

    def _cleanup_old_backups(self):
        try:
            backups = sorted([
                os.path.join(self.backup_dir, d)
                for d in os.listdir(self.backup_dir)
                if d.startswith("backup_") and os.path.isdir(os.path.join(self.backup_dir, d))
            ])
            while len(backups) > self.config["max_backups"]:
                oldest = backups.pop(0)
                shutil.rmtree(oldest)
                self.log(f"[CLEANUP] 删除旧备份：{oldest}")
        except Exception as e:
            self.log(f"[ERROR] 清理备份失败：{e}")

    # ────────────────────────────────────────────
    # 进程检查（只检查脚本文件存在性，不发送信号、不重启）
    # ────────────────────────────────────────────
    def check_processes(self):
        if not self.monitored_processes:
            self.log("[INFO] 无需监控的进程（OpenClaw 由自身守护，无需此处干预）")
            return
        self.log("\n" + "=" * 50)
        self.log("进程文件检查")
        self.log("=" * 50)
        for proc in self.monitored_processes:
            script_path = os.path.join(self.workspace, proc["script"])
            exists = os.path.exists(script_path)
            self.log(f"  {'[OK]' if exists else '[MISSING]'} {proc['name']} → {proc['script']}")
        self.log("[OK] 进程文件检查完成")

    # ────────────────────────────────────────────
    # 主入口
    # ────────────────────────────────────────────
    def run(self):
        self.log("\n" + "=" * 50)
        self.log("AutoClaw v1.1 启动")
        self.log("=" * 50)
        try:
            health_ok = self.health_check()
            self.auto_backup()
            self.check_processes()
            self.log("\n" + "=" * 50)
            self.log("AutoClaw 运行完成")
            self.log("=" * 50)
            return health_ok
        except Exception as e:
            self.log(f"[ERROR] 运行失败：{e}")
            return False


# ────────────────────────────────────────────
# 命令行入口
# 用法：python autoclaw.py [workspace_path]
# ────────────────────────────────────────────
if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_WORKSPACE
    AutoClaw(workspace_path=workspace).run()
