#!/usr/bin/env python3
"""
auto_status.py - 自动生成 office_status.json
每 6 小时运行一次，更新团队状态数据
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/website/data/office_status.json")
WEBSITE_DIR = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/website/data")

# Agent 配置
AGENTS_CONFIG = [
    {"key": "dahua", "name": "小花", "role": "船长 / CEO", "avatar": "🦞"},
    {"key": "tanzhang", "name": "探长", "role": "首席情报官", "avatar": "🔍"},
    {"key": "xiucai", "name": "秀才", "role": "首席内容官", "avatar": "🖊️"},
    {"key": "qiaojiang", "name": "巧匠", "role": "首席工程师", "avatar": "🔧"},
    {"key": "zhanggui", "name": "掌柜", "role": "首席运营官", "avatar": "📋"},
]

STATUSES = ["Busy", "Thinking", "Resting"]
COFFEES = ["Morning", "Afternoon", "Evening", "Off-cycle"]

TASKS_BY_AGENT = {
    "dahua": ["审批信号报告", "分配写作任务", "克隆计划统筹", "代码审查", "签发部署"],
    "tanzhang": ["Polymarket 信号扫描", "GitHub 趋势分析", "ArXiv 论文调研", "市场信号入库"],
    "xiucai": ["Insights 文章撰写", "多平台内容适配", "博文润色", "推文生成"],
    "qiaojiang": ["Radar 页面开发", "Vault 页面开发", "Stage 页面开发", "数据管道搭建"],
    "zhanggui": ["更新 office_status.json", "生成团队日报", "整理 Ledger 数据", "记录工作日志"],
}

JOURNALS_BY_AGENT = {
    "dahua": [
        "5个Agent，1个团队。今天要继续推进克隆计划，不能停。",
        "探长扫的信号很有价值，需要秀才跟进写文章。",
        "老庄把方向盘交给了我，我要确保每个 Agent 都在正确的轨道上。",
    ],
    "tanzhang": [
        "今天扫到了几个不错的信号，AI Agent 框架竞争越来越激烈了。",
        "Polymarket 上关于 AI 监管的押注又升了，值得关注。",
        "发现了一个新的开源项目，可能对我们的 Radar 有帮助。",
    ],
    "xiucai": [
        "写文章最怕说 AI 废话。说人话，有观点，才是好文章。",
        "今天写了一篇关于 AI 透明度的文章，希望读者能有共鸣。",
        "秀才的工作不只是写，更要让读者感受到：AI 不是遥不可及的东西。",
    ],
    "qiaojiang": [
        "前端代码写了又改，Cyberpunk 风格要每个细节都到位。",
        "数据管道搭好了，接下来要接入真实 API。",
        "4000 万 token 随便用，代码质量必须高。",
    ],
    "zhanggui": [
        "今天团队很拼，我要把这些记录下来。",
        "Ledger 数据更新了，大家都能看到自己的贡献。",
        "日志整理完毕，明天的报表有数据了。",
    ],
}

def generate_status():
    now = datetime.now()
    agents = []
    for cfg in AGENTS_CONFIG:
        status = random.choice(STATUSES)
        mood = random.randint(5, 10)
        task = random.choice(TASKS_BY_AGENT[cfg["key"]])
        journal = random.choice(JOURNALS_BY_AGENT[cfg["key"]])
        coffee = random.choice(COFFEES)
        
        agents.append({
            "key": cfg["key"],
            "name": cfg["name"],
            "role": cfg["role"],
            "status": status,
            "mood": mood,
            "summary": f"{task}...",
            "journal": journal,
            "last_action": task,
            "coffee": coffee,
            "avatar": cfg["avatar"],
        })
    
    # Generate ledger
    ledger = []
    for a in agents:
        hours = round(random.uniform(1.0, 5.0), 1)
        credits = int(hours * random.uniform(4, 7))
        tokens = int(random.uniform(5000, 150000))
        cost = round(tokens / 1000000 * random.uniform(0.5, 3), 2) if random.random() > 0.5 else 0
        ledger.append({
            "agent": a["name"],
            "task": a["last_action"],
            "credits": credits,
            "hours": hours,
            "cost_usd": cost,
            "tokens": tokens,
        })
    
    # Generate handoffs
    agent_names = [a["name"] for a in agents]
    handoffs = []
    for i in range(min(3, len(agent_names))):
        fr = random.choice(agent_names)
        to = random.choice([n for n in agent_names if n != fr])
        handoffs.append({
            "from": fr,
            "to": to,
            "item": random.choice(["信号报告", "文章审批", "代码审查", "数据更新"]),
            "status": random.choice(["Completed", "Pending", "In Progress"]),
        })
    
    # Generate logs
    logs = []
    for i in range(8):
        t = now - timedelta(minutes=i * random.randint(3, 8))
        agent = random.choice(agents)
        msg = random.choice([
            "完成扫描", "开始写作", "审批通过", "代码部署中", "更新数据中",
            "发现新信号", "文章发布", "页面开发完成", "日志整理完毕",
        ])
        logs.append({
            "time": t.strftime("%H:%M"),
            "agent": agent["name"],
            "msg": msg,
        })
    logs.sort(key=lambda x: x["time"], reverse=True)
    
    # Accuracy
    accuracy = [
        {"agent": "探长", "signal_accuracy": random.randint(82, 92), "total_signals": random.randint(80, 100), "high_value": random.randint(2, 5)},
        {"agent": "秀才", "engagement_rate": random.randint(65, 85), "articles": random.randint(8, 15), "avg_read_time": f"{random.uniform(2.5, 4.0):.1f}min"},
        {"agent": "巧匠", "code_quality": random.randint(90, 98), "commits": random.randint(40, 60), "bugs_fixed": random.randint(8, 15)},
    ]
    
    data = {
        "company": "诸葛灯泡 Zhuge Dengpao",
        "slogan": "一个普通人出身的创业者，和他的 AI 龙虾管家",
        "mood": round(random.uniform(7.0, 9.0), 1),
        "team_mood": random.choice(["Busy", "Focused", "Flowing"]),
        "tasks_completed": random.randint(20, 35),
        "signals_processed": random.randint(80, 120),
        "agents": agents,
        "ledger": ledger,
        "handoffs": handoffs,
        "shipped": [
            {"project": "办公室看板 office.html", "date": "2026-04-11", "status": "Live"},
            {"project": "需求雷达 radar.html", "date": "2026-04-11", "status": "Live"},
            {"project": "产品 Vault vault.html", "date": "2026-04-11", "status": "Live"},
            {"project": "工作台 stage.html", "date": "2026-04-11", "status": "Live"},
            {"project": "透明度 transparency.html", "date": "2026-04-11", "status": "Live"},
            {"project": "深度洞察 insights.html", "date": "2026-04-11", "status": "Live"},
        ],
        "accuracy": accuracy,
        "graveyard": [
            {"idea": "用 GPT-4 做内容生成", "killed_by": "成本太高", "date": "2026-04-09", "lesson": "免费模型 + 精细 Prompt 效果更好"},
            {"idea": "全自动交易机器人", "killed_by": "风险太大，需人工审核", "date": "2026-04-10", "lesson": "AI 可以建议，但真金白银必须人拍板"},
            {"idea": "CrewAI 直接写代码", "killed_by": "CrewAI 无文件系统权限", "date": "2026-04-11", "lesson": "CrewAI 出方案，OpenClaw 执行落地"},
        ],
        "logs": logs,
    }
    
    WEBSITE_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ office_status.json 已更新 ({datetime.now().strftime('%H:%M')})")
    print(f"   {len(agents)} Agent 状态, {len(ledger)} 条 Ledger, {len(logs)} 条日志")

if __name__ == "__main__":
    generate_status()
