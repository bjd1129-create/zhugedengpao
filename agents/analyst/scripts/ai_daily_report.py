#!/usr/bin/env python3
"""
AI 深度日报自动生成脚本
功能：抓取 5 个固定信息源的最新内容，生成 Markdown 报告并发送到飞书
运行时间：每天 08:00
输出位置：agents/analyst/reports/ai-daily-YYYY-MM-DD.md
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import feedparser
from bs4 import BeautifulSoup

# 配置
WORKSPACE_ROOT = Path("/Users/bjd/Desktop/ZhugeDengpao-Team")
REPORTS_DIR = WORKSPACE_ROOT / "agents/analyst" / "reports"
TEMPLATE_FILE = WORKSPACE_ROOT / "agents/analyst" / "report_template.md"

# 5 个固定信息源配置
SOURCES = {
    "anthropic": {
        "name": "Anthropic 官方博客",
        "rss_url": "https://www.anthropic.com/rss",
        "web_url": "https://www.anthropic.com/news"
    },
    "openclaw": {
        "name": "OpenClaw GitHub",
        "api_url": "https://api.github.com/repos/openclaw-labs/openclaw/events",
        "web_url": "https://github.com/openclaw-labs/openclaw"
    },
    "hackernews": {
        "name": "Hacker News AI 板块",
        "api_url": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "web_url": "https://news.ycombinator.com/front?day=2024-01-01"
    },
    "simon": {
        "name": "Simon Willison 博客",
        "rss_url": "https://simonwillison.net/atom/everything/",
        "web_url": "https://simonwillison.net/"
    },
    "arxiv": {
        "name": "ArXiv AI 论文",
        "rss_url": "http://export.arxiv.org/rss/cs.AI",
        "web_url": "https://arxiv.org/list/cs.AI/recent"
    }
}

def fetch_anthropic_news():
    """获取 Anthropic 博客最新文章"""
    try:
        feed = feedparser.parse(SOURCES["anthropic"]["rss_url"])
        if feed.entries:
            latest = feed.entries[0]
            return {
                "title": latest.title,
                "link": latest.link,
                "summary": latest.get("summary", "")[:500],
                "published": latest.get("published", "")
            }
    except Exception as e:
        print(f"Error fetching Anthropic: {e}")
    return None

def fetch_openclaw_updates():
    """获取 OpenClaw GitHub 最近活动"""
    try:
        response = requests.get(SOURCES["openclaw"]["api_url"], timeout=10)
        if response.status_code == 200:
            events = response.json()[:5]  # 最近 5 个事件
            summaries = []
            for event in events:
                event_type = event["type"]
                actor = event["actor"]["login"]
                summaries.append(f"- {event_type} by @{actor}")
            return {
                "updates": "\n".join(summaries),
                "link": SOURCES["openclaw"]["web_url"]
            }
    except Exception as e:
        print(f"Error fetching OpenClaw: {e}")
    return None

def fetch_hackernews_ai():
    """获取 Hacker News AI 相关热门话题"""
    try:
        response = requests.get(SOURCES["hackernews"]["api_url"], timeout=10)
        if response.status_code == 200:
            story_ids = response.json()[:10]  # Top 10
            stories = []
            for story_id in story_ids[:5]:  # 只取前 5 个
                story_response = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=5
                )
                if story_response.status_code == 200:
                    story = story_response.json()
                    if story and "ai" in story.get("title", "").lower() or "llm" in story.get("title", "").lower():
                        stories.append({
                            "title": story["title"],
                            "url": story["url"],
                            "score": story.get("score", 0)
                        })
            return {
                "stories": stories,
                "link": SOURCES["hackernews"]["web_url"]
            }
    except Exception as e:
        print(f"Error fetching HackerNews: {e}")
    return None

def fetch_simon_blog():
    """获取 Simon Willison 博客最新文章"""
    try:
        feed = feedparser.parse(SOURCES["simon"]["rss_url"])
        if feed.entries:
            latest = feed.entries[0]
            return {
                "title": latest.title,
                "link": latest.link,
                "summary": latest.get("summary", "")[:500],
                "published": latest.get("published", "")
            }
    except Exception as e:
        print(f"Error fetching Simon Willison: {e}")
    return None

def fetch_arxiv_papers():
    """获取 ArXiv 最新 AI 论文"""
    try:
        feed = feedparser.parse(SOURCES["arxiv"]["rss_url"])
        if feed.entries:
            papers = []
            for entry in feed.entries[:3]:  # 最新 3 篇
                papers.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", "")[:300]
                })
            return {
                "papers": papers,
                "link": SOURCES["arxiv"]["web_url"]
            }
    except Exception as e:
        print(f"Error fetching ArXiv: {e}")
    return None

def generate_report_content(data):
    """根据抓取的数据生成报告内容"""
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 读取模板
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()
    
    # 填充数据
    content = template.format(
        date=today,
        anthropic_url=data.get("anthropic", {}).get("link", ""),
        openclaw_url=data.get("openclaw", {}).get("link", ""),
        hn_url=data.get("hackernews", {}).get("link", ""),
        simon_url=data.get("simon", {}).get("link", ""),
        other_url=data.get("arxiv", {}).get("link", ""),
        other_name="ArXiv",
        timestamp=timestamp
    )
    
    # 填充各来源的摘要和洞察（简化版本，实际可接入 AI 生成）
    content = content.replace(
        "（200-300 字，概括主要内容、技术突破、产品更新等）",
        data.get("anthropic", {}).get("summary", "今日暂无更新")[:300]
    )
    
    return content

def save_report(content):
    """保存报告到文件"""
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"ai-daily-{today}.md"
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return report_path

def send_to_feishu(report_path):
    """发送报告到飞书（需要配置飞书 Webhook）"""
    # TODO: 配置飞书 Webhook URL
    webhook_url = os.getenv("FEISHU_WEBHOOK_URL")
    
    if not webhook_url:
        print("未配置飞书 Webhook，跳过发送")
        return
    
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": f"📊 AI 深度日报已生成\n\n{report_path}\n\n请查看完整报告。"
            }
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            print("报告已成功发送到飞书")
        else:
            print(f"发送失败：{response.text}")
    except Exception as e:
        print(f"Error sending to Feishu: {e}")

def main():
    """主函数"""
    print(f"开始生成 AI 深度日报 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 抓取各来源数据
    data = {}
    
    print("抓取 Anthropic...")
    data["anthropic"] = fetch_anthropic_news()
    
    print("抓取 OpenClaw GitHub...")
    data["openclaw"] = fetch_openclaw_updates()
    
    print("抓取 Hacker News...")
    data["hackernews"] = fetch_hackernews_ai()
    
    print("抓取 Simon Willison...")
    data["simon"] = fetch_simon_blog()
    
    print("抓取 ArXiv...")
    data["arxiv"] = fetch_arxiv_papers()
    
    # 生成报告
    print("生成报告...")
    content = generate_report_content(data)
    
    # 保存报告
    report_path = save_report(content)
    print(f"报告已保存：{report_path}")
    
    # 发送到飞书
    send_to_feishu(report_path)
    
    print("日报生成完成！")

if __name__ == "__main__":
    main()
