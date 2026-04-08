#!/usr/bin/env python3
"""
Polymarket 新闻驱动概率差套利脚本 v1.0
功能：监控新闻 → 计算公平概率 → 找出概率差 → 生成下注信号
最后更新：2026-04-08 23:20
"""

import json
import math
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional

# ==================== 配置区 ====================

# 监控的市场
MARKETS = [
    {
        "id": "trump-announces-end-of-military-operations-against-iran-by",
        "question": "特朗普宣布结束对伊朗的军事行动",
        "outcomes": [
            {"date": "2026-04-15", "current_prob": 0.20, "yes_price": 0.20, "no_price": 0.81, "volume": 2675618},
            {"date": "2026-04-30", "current_prob": 0.50, "yes_price": 0.51, "no_price": 0.51, "volume": 3442964},
            {"date": "2026-05-31", "current_prob": 0.72, "yes_price": 0.73, "no_price": 0.29, "volume": 70674},
            {"date": "2026-06-30", "current_prob": 0.82, "yes_price": 0.83, "no_price": 0.19, "volume": 1447002},
        ]
    }
]

# 新闻源配置
NEWS_SOURCES = {
    "official": {  # 官方渠道
        "sources": ["Truth Social", "WhiteHouse.gov", "Defense.gov"],
        "monitor_interval": 300,  # 5 分钟
        "weight": 1.0,
    },
    "media": {  # 权威媒体
        "sources": ["Reuters", "AP News", "CNN Politics", "Fox News"],
        "monitor_interval": 900,  # 15 分钟
        "weight": 0.8,
    },
    "social": {  # 社交媒体
        "sources": ["Twitter @realDonaldTrump", "Twitter @PressSec"],
        "monitor_interval": 300,  # 5 分钟
        "weight": 0.6,
    },
    "community": {  # 社区情报
        "sources": ["Polymarket Comments", "Reddit r/Polymarket"],
        "monitor_interval": 1800,  # 30 分钟
        "weight": 0.3,
    }
}

# 信号强度
SIGNAL_STRENGTH = {
    "official_announcement": 0.50,  # 官方宣布
    "dod_confirmation": 0.40,       # 国防部确认
    "major_media": 0.25,            # 权威媒体报道
    "anonymous_leak": 0.10,         # 匿名泄露
    "rumor": 0.05,                  # 谣言
}

# 时间衰减参数
TIME_DECAY_LAMBDA = 0.1  # 每小时衰减 10%

# 下注阈值
BET_THRESHOLD_HIGH = 0.15   # 概率差>15% 下注
BET_THRESHOLD_LOW = -0.15   # 概率差<-15% 下注 NO

# ==================== 数据类 ====================

@dataclass
class NewsSignal:
    """新闻信号"""
    source: str
    headline: str
    timestamp: datetime
    signal_type: str  # official_announcement, major_media, etc.
    sentiment: float  # +1.0 (利好结束) to -1.0 (利空结束)
    
    def get_strength(self) -> float:
        """计算信号强度（含时间衰减）"""
        base_strength = SIGNAL_STRENGTH.get(self.signal_type, 0.05)
        
        # 时间衰减
        hours_elapsed = (datetime.now() - self.timestamp).total_seconds() / 3600
        decay_factor = math.exp(-TIME_DECAY_LAMBDA * hours_elapsed)
        
        return base_strength * decay_factor * abs(self.sentiment)

@dataclass
class ProbabilityAnalysis:
    """概率分析结果"""
    market_id: str
    outcome_date: str
    market_prob: float
    fair_prob: float
    probability_gap: float
    recommendation: str  # BUY_YES, BUY_NO, HOLD
    expected_value: float
    confidence: str  # HIGH, MEDIUM, LOW

# ==================== 核心函数 ====================

def calculate_fair_probability(signals: List[NewsSignal], outcome_date: str) -> float:
    """
    计算公平概率
    
    基于新闻信号强度和时间衰减
    """
    if not signals:
        return 0.50  # 无信号时默认 50%
    
    # 筛选与目标日期相关的信号
    relevant_signals = []
    for signal in signals:
        # 信号时间必须在当前和目标日期之间
        signal_date = signal.timestamp.date()
        target_date = datetime.fromisoformat(outcome_date).date()
        
        if signal_date <= target_date:
            relevant_signals.append(signal)
    
    if not relevant_signals:
        return 0.50
    
    # 计算总信号强度（上限 100%）
    total_strength = sum(signal.get_strength() for signal in relevant_signals)
    fair_prob = min(total_strength, 1.0)
    
    return fair_prob

def analyze_market(market: Dict, signals: List[NewsSignal]) -> List[ProbabilityAnalysis]:
    """
    分析市场，找出概率差
    """
    analyses = []
    
    for outcome in market["outcomes"]:
        # 计算公平概率
        fair_prob = calculate_fair_probability(signals, outcome["date"])
        
        # 计算概率差
        probability_gap = fair_prob - outcome["current_prob"]
        
        # 计算期望值
        if probability_gap > 0:
            # 买 YES
            potential_payout = 1.0 / outcome["yes_price"]
            expected_value = (fair_prob * potential_payout) - ((1 - fair_prob) * 1)
        else:
            # 买 NO
            potential_payout = 1.0 / outcome["no_price"]
            expected_value = ((1 - fair_prob) * potential_payout) - (fair_prob * 1)
        
        # 生成建议
        if probability_gap > BET_THRESHOLD_HIGH:
            recommendation = "BUY_YES"
        elif probability_gap < BET_THRESHOLD_LOW:
            recommendation = "BUY_NO"
        else:
            recommendation = "HOLD"
        
        # 置信度
        if abs(probability_gap) > 0.25:
            confidence = "HIGH"
        elif abs(probability_gap) > 0.15:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        analysis = ProbabilityAnalysis(
            market_id=market["id"],
            outcome_date=outcome["date"],
            market_prob=outcome["current_prob"],
            fair_prob=fair_prob,
            probability_gap=probability_gap,
            recommendation=recommendation,
            expected_value=expected_value,
            confidence=confidence
        )
        
        analyses.append(analysis)
    
    return analyses

def generate_trading_signals(analyses: List[ProbabilityAnalysis]) -> List[Dict]:
    """
    生成交易信号
    """
    signals = []
    
    for analysis in analyses:
        if analysis.recommendation in ["BUY_YES", "BUY_NO"]:
            signal = {
                "timestamp": datetime.now().isoformat(),
                "market": analysis.market_id,
                "outcome": analysis.outcome_date,
                "action": analysis.recommendation,
                "market_prob": f"{analysis.market_prob:.1%}",
                "fair_prob": f"{analysis.fair_prob:.1%}",
                "probability_gap": f"{analysis.probability_gap:+.1%}",
                "expected_value": f"${analysis.expected_value:.2f}",
                "confidence": analysis.confidence,
                "suggested_stake": calculate_suggested_stake(analysis),
            }
            signals.append(signal)
    
    return signals

def calculate_suggested_stake(analysis: ProbabilityAnalysis) -> float:
    """
    计算建议下注金额（基于凯利公式简化版）
    """
    if analysis.confidence == "HIGH":
        return 0.10  # 10% 账户
    elif analysis.confidence == "MEDIUM":
        return 0.05  # 5% 账户
    else:
        return 0.02  # 2% 账户

def print_analysis_report(analyses: List[ProbabilityAnalysis], signals: List[Dict]):
    """
    打印分析报告
    """
    print("=" * 80)
    print("Polymarket 概率差套利分析")
    print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    print("\n📊 市场分析:")
    print("-" * 80)
    
    for analysis in analyses:
        emoji = "✅" if analysis.recommendation != "HOLD" else "⚠️"
        print(f"{emoji} {analysis.outcome_date}")
        print(f"   市场概率：{analysis.market_prob:.1%}")
        print(f"   公平概率：{analysis.fair_prob:.1%}")
        print(f"   概率差：  {analysis.probability_gap:+.1%}")
        print(f"   建议：    {analysis.recommendation}")
        print(f"   期望值：  {analysis.expected_value:+.2f}")
        print(f"   置信度：  {analysis.confidence}")
        print()
    
    if signals:
        print("\n🔔 交易信号:")
        print("-" * 80)
        
        for signal in signals:
            print(f"🎯 {signal['action']} {signal['outcome']}")
            print(f"   概率差：{signal['probability_gap']}")
            print(f"   期望值：{signal['expected_value']}")
            print(f"   置信度：{signal['confidence']}")
            print(f"   建议仓位：{signal['suggested_stake']:.1%}")
            print()
    else:
        print("\n🔔 无交易信号（所有市场概率差在阈值内）")
    
    print("=" * 80)

# ==================== 主流程 ====================

def main():
    """主函数"""
    print(f"[{datetime.now().isoformat()}] 启动 Polymarket 概率差分析...")
    
    # 模拟新闻信号（实际应从新闻 API 获取）
    mock_signals = [
        NewsSignal(
            source="Truth Social",
            headline="特朗普宣布两周停火",
            timestamp=datetime.now() - timedelta(hours=3),
            signal_type="major_media",  # 停火不是正式结束
            sentiment=+0.6
        ),
        NewsSignal(
            source="Reuters",
            headline="美伊定于 4 月 10 日举行谈判",
            timestamp=datetime.now() - timedelta(hours=5),
            signal_type="major_media",
            sentiment=+0.4
        ),
        NewsSignal(
            source="Defense.gov",
            headline="国防部长简报：Epic Fury 行动进展顺利",
            timestamp=datetime.now() - timedelta(hours=6),
            signal_type="dod_confirmation",
            sentiment=+0.3
        ),
    ]
    
    # 分析每个市场
    all_analyses = []
    for market in MARKETS:
        analyses = analyze_market(market, mock_signals)
        all_analyses.extend(analyses)
    
    # 生成交易信号
    signals = generate_trading_signals(all_analyses)
    
    # 打印报告
    print_analysis_report(all_analyses, signals)
    
    # 保存信号到文件
    if signals:
        output_file = "data/polymarket_signals.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(signals, f, ensure_ascii=False, indent=2)
        print(f"\n💾 信号已保存：{output_file}")
    
    # 返回最佳机会
    if signals:
        best_signal = max(signals, key=lambda x: float(x["expected_value"].replace("$", "")))
        print(f"\n🎯 最佳机会：{best_signal['action']} {best_signal['outcome']}")
        print(f"   期望值：{best_signal['expected_value']}")
        print(f"   置信度：{best_signal['confidence']}")

if __name__ == "__main__":
    main()
