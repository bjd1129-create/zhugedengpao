#!/usr/bin/env python3
"""
fetch_real_data.py - 抓取真实市场数据，更新 Radar 信号
数据源: Polymarket API, GitHub API, ArXiv API
"""

import json
import urllib.request
import ssl
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/website/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def safe_request(url, headers=None):
    """安全 HTTP 请求"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # 默认真实浏览器 UA
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    if headers:
        default_headers.update(headers)
    
    req = urllib.request.Request(url, headers=default_headers)
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"  ⚠️ 请求失败 {url}: {e}")
        return None

def fetch_polymarket_signals():
    """抓取 Polymarket 热门市场（多端点降级）"""
    print("📊 抓取 Polymarket 热门市场...")
    
    # 尝试多个端点
    endpoints = [
        "https://polymarket.com/api/markets?closed=false&limit=15&order=volume&ascending=false",
        "https://clob.polymarket.com/markets?closed=false&limit=15&order_by=volume",
    ]
    
    for url in endpoints:
        data = safe_request(url)
        if data and (isinstance(data, list) and len(data) > 0 or "data" in data):
            markets = data if isinstance(data, list) else data.get("data", [])
            signals = []
            for m in markets[:10]:
                try:
                    question = m.get("question") or m.get("title") or "Unknown"
                    volume = m.get("volume", m.get("volume24hr", 0))
                    prices = m.get("prices", []) or m.get("outcomePrices", [])
                    price_str = prices[0] if prices else "0"
                    vol = float(volume) if volume else 0
                    price = float(price_str) if price_str and price_str != "N/A" else 0
                    signals.append({
                        "id": m.get("id", m.get("condition_id", "")),
                        "title": question[:80],
                        "desc": f"交易量: ${vol:,.0f} | 是概率: {price*100:.1f}%",
                        "source": "Polymarket",
                        "time": "刚刚",
                        "priority": "high" if vol > 100000 else "medium",
                        "tags": ["Polymarket", "预测市场", "实时"],
                        "action": f"→ 查看市场: {m.get('slug', m.get('id', ''))}",
                        "volume": vol,
                    })
                except (ValueError, KeyError, TypeError) as e:
                    print(f"  ⚠️ 解析市场数据失败: {e}")
                    continue
            if signals:
                print(f"  ✅ 获取 {len(signals)} 个 Polymarket 信号")
                return signals
    
    print("  ⚠️ Polymarket 全部端点失败，尝试 HN 替代...")
    return fetch_hn_signals()

def fetch_hn_signals():
    """Hacker News 热门作为 Polymarket 的备用数据源"""
    print("  📰 抓取 Hacker News 热门作为替代...")
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    data = safe_request(url)
    if not data:
        return []
    
    signals = []
    for item_id in data[:10]:
        item = safe_request(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
        if item and item.get("title"):
            signals.append({
                "id": str(item_id),
                "title": item["title"][:80],
                "desc": f" {item.get('score', 0)} 分 | 💬 {item.get('descendants', 0)} 评论 | {item.get('url', 'No URL')[:60]}",
                "source": "HackerNews",
                "time": "刚刚",
                "priority": "high" if item.get("score", 0) > 200 else "medium",
                "tags": ["HackerNews", "科技", "趋势"],
                "action": f"→ 查看: {item.get('url', '')}",
                "volume": item.get("score", 0),
            })
    print(f"  ✅ 获取 {len(signals)} 个 HN 信号")
    return signals

def fetch_github_trending():
    """抓取 GitHub 热门项目（通过公共 API）"""
    print("🐙 抓取 GitHub 热门项目...")
    
    url = "https://api.github.com/search/repositories?q=created:>2026-04-01+stars:>100&sort=stars&order=desc&per_page=10"
    headers = {"Accept": "application/vnd.github.v3+json"}
    data = safe_request(url, headers)
    
    if not data or "items" not in data:
        return []
    
    signals = []
    for repo in data["items"][:8]:
        desc = repo.get('description') or 'No description'
        signals.append({
            "id": repo.get("id", ""),
            "title": repo.get("full_name", ""),
            "desc": f"⭐ {repo.get('stargazers_count', 0)} | 🍴 {repo.get('forks_count', 0)} | {desc[:100]}",
            "source": "GitHub",
            "time": "今天",
            "priority": "high" if repo.get('stargazers_count', 0) > 500 else "medium",
            "tags": ["GitHub", repo.get("language", "Unknown"), "开源"],
            "action": f"→ 查看: {repo.get('html_url', '')}",
            "volume": repo.get('stargazers_count', 0),
        })
    
    print(f"  ✅ 获取 {len(signals)} 个 GitHub 信号")
    return signals

def fetch_x_signals():
    """加载由诸葛灯泡浏览器抓取的 X/Twitter 信号"""
    print("🐦 加载 X 信号 (via Browser/GetDayTrends)...")
    x_file = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/agents/engineer/website/data/x_signals.json")
    if x_file.exists():
        try:
            data = json.loads(x_file.read_text())
            print(f"  ✅ 获取 {len(data)} 个 X 信号")
            return data
        except json.JSONDecodeError:
            print("  ⚠️ X 数据文件解析失败")
            return []
    print("  ℹ️ 暂无 X 数据 (需运行 Browser 任务)")
    return []

def update_radar_data():
    """更新雷达数据"""
    print("\n📡 更新需求雷达数据...")
    
    all_signals = []
    
    # 抓取真实数据
    pm_signals = fetch_polymarket_signals()
    gh_signals = fetch_github_trending()
    x_signals = fetch_x_signals()  # 新增 X 信号源
    
    all_signals.extend(pm_signals)
    all_signals.extend(gh_signals)
    all_signals.extend(x_signals)
    
    if not all_signals:
        print("  ⚠️ 无新信号，保留现有数据")
        return
    
    # 保存
    output_file = OUTPUT_DIR / "radar_signals.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "total_signals": len(all_signals),
            "signals": all_signals,
        }, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ 保存 {len(all_signals)} 个信号到 radar_signals.json")

if __name__ == "__main__":
    update_radar_data()
    print("\n✅ 数据更新完成")
