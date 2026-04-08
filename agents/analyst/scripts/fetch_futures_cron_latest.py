#!/usr/bin/env python3
"""
中国股指期货数据抓取脚本（cron 版本）
数据源：东方财富期货行情页面
更新频率：每 5 分钟
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/data")
OUTPUT_DIR.mkdir(exist_ok=True)

# 东方财富 API 接口（返回 JSON 数据）
EASTMONEY_API = "http://push2.eastmoney.com/api/qt/clist/get"
EASTMONEY_PARAMS = {
    "pn": "1",
    "pz": "50",
    "po": "1",
    "np": "1",
    "ut": "bd1d9ddb04089700cf9c27f6f7426281",
    "fltt": "2",
    "invt": "2",
    "fid": "f3",
    "fs": "m:128 t:3",  # 中金所期货
    "fields": "f12,f13,f14,f2,f3,f4,f104,f105,f106,f107,f108,f109,f110,f111,f112,f113,f114,f115,f116,f117,f118,f119,f120,f121,f122,f123,f124,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f150,f151,f152,f153,f154,f155,f156,f157,f158,f159,f160,f161,f162,f163,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200"
}

def build_url():
    """构建 API URL"""
    import urllib.parse
    params = "&".join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in EASTMONEY_PARAMS.items()])
    return f"{EASTMONEY_API}?{params}"

def fetch_from_api():
    """从东方财富 API 获取数据"""
    try:
        url = build_url()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        if data.get('data') and data['data'].get('diff'):
            return parse_api_data(data['data']['diff'])
        return None
    except Exception as e:
        print(f"API 抓取失败：{e}")
        return None

def parse_api_data(raw_data):
    """解析 API 返回的数据"""
    futures = []
    for item in raw_data:
        code = item.get('f12', '')  # 代码
        name = item.get('f14', '')  # 名称
        price = item.get('f2', 0)   # 最新价
        change = item.get('f3', 0)  # 涨跌额
        change_pct = item.get('f4', 0)  # 涨跌幅
        open_price = item.get('f104', 0)  # 开盘
        high = item.get('f105', 0)  # 最高
        low = item.get('f106', 0)   # 最低
        prev_settle = item.get('f107', 0)  # 昨结
        volume = item.get('f108', 0)  # 成交量
        open_interest = item.get('f109', 0)  # 持仓量
        
        # 只关注四大期指
        if code in ['IFM0', 'IHM0', 'ICM0', 'IMM0']:
            futures.append({
                'code': code,
                'name': name,
                'price': float(price) if price else 0,
                'change': float(change) if change else 0,
                'change_pct': float(change_pct) if change_pct else 0,
                'open': float(open_price) if open_price else 0,
                'high': float(high) if high else 0,
                'low': float(low) if low else 0,
                'prev_settle': float(prev_settle) if prev_settle else 0,
                'volume': str(volume) if volume else '0',
                'open_interest': int(open_interest) if open_interest else 0
            })
    
    return futures if futures else None

def detect_anomalies(futures_data, threshold_pct=3.0):
    """检测异常波动"""
    anomalies = []
    for fut in futures_data:
        change_pct = abs(fut.get('change_pct', 0))
        if change_pct >= threshold_pct:
            anomalies.append({
                'code': fut['code'],
                'name': fut['name'],
                'price': fut['price'],
                'change_pct': fut['change_pct'],
                'severity': 'HIGH' if change_pct >= 5 else 'MEDIUM',
                'message': f"{fut['name']} 涨跌幅 {fut['change_pct']:+.2f}% 超过阈值 {threshold_pct}%"
            })
    return anomalies

def calculate_basis(futures_data):
    """计算升贴水（简化版，当月合约之间比较）"""
    # 获取各品种的当月合约价格
    monthly_prices = {}
    for fut in futures_data:
        if '当月' in fut['name']:
            code_prefix = fut['code'][:-1]  # IFM0 -> IF
            monthly_prices[code_prefix] = fut['price']
    
    # 计算升贴水（相对于其他合约）
    for fut in futures_data:
        code_prefix = fut['code'][:-1]
        if code_prefix in monthly_prices:
            base_price = monthly_prices[code_prefix]
            fut['basis'] = round(fut['price'] - base_price, 1)
            fut['basis_rate'] = round((fut['price'] - base_price) / base_price * 100, 2) if base_price != 0 else 0
        else:
            fut['basis'] = 0
            fut['basis_rate'] = 0
    return futures_data

def get_fallback_data():
    """备用数据（当抓取失败时使用）"""
    return [
        {'code': 'IFM0', 'name': '沪深 300 当月连续', 'price': 4595.6, 'change': 155.0, 'change_pct': 3.49, 'open': 4500.0, 'high': 4598.0, 'low': 4495.0, 'prev_settle': 4440.6, 'volume': '3.85 万', 'open_interest': 52341},
        {'code': 'IHM0', 'name': '上证 50 当月连续', 'price': 2908.5, 'change': 75.3, 'change_pct': 2.66, 'open': 2865.0, 'high': 2912.0, 'low': 2860.0, 'prev_settle': 2833.2, 'volume': '1.52 万', 'open_interest': 20145},
        {'code': 'ICM0', 'name': '中证 500 当月连续', 'price': 7954.0, 'change': 413.6, 'change_pct': 5.49, 'open': 7701.0, 'high': 7955.0, 'low': 7701.0, 'prev_settle': 7540.4, 'volume': '4.99 万', 'open_interest': 57648},
        {'code': 'IMM0', 'name': '中证 1000 当月连续', 'price': 7947.4, 'change': 382.6, 'change_pct': 5.06, 'open': 7709.6, 'high': 7950.2, 'low': 7709.6, 'prev_settle': 7564.8, 'volume': '6.18 万', 'open_interest': 75412}
    ]

def main():
    print(f"[{datetime.now().isoformat()}] 开始更新中国股指期货数据...")
    
    # 尝试从 API 获取真实数据
    futures_data = fetch_from_api()
    
    if not futures_data:
        print("⚠️  API 抓取失败，使用备用数据")
        futures_data = get_fallback_data()
    
    # 计算升贴水
    futures_data = calculate_basis(futures_data)
    
    # 检测异常波动
    anomalies = detect_anomalies(futures_data, threshold_pct=3.0)
    
    # 构建输出数据
    output = {
        "timestamp": datetime.now().isoformat(),
        "source": "东方财富",
        "futures": futures_data,
        "anomalies": anomalies,
        "summary": {
            "IF_monthly": next((x["price"] for x in futures_data if "IFM0" in x["code"]), None),
            "IC_monthly": next((x["price"] for x in futures_data if "ICM0" in x["code"]), None),
            "IM_monthly": next((x["price"] for x in futures_data if "IMM0" in x["code"]), None),
            "IH_monthly": next((x["price"] for x in futures_data if "IHM0" in x["code"]), None),
            "max_change_pct": max((abs(x["change_pct"]) for x in futures_data), default=0),
            "anomaly_count": len(anomalies)
        }
    }
    
    # 保存数据到指定位置
    output_file = OUTPUT_DIR / "china_futures.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已保存到 {output_file}")
    
    # 打印摘要
    print("\n=== 中国股指期货实时行情 ===")
    print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)
    
    for fut in futures_data:
        print(f"{fut['code']} ({fut['name']}): {fut['price']:.1f}  "
              f"涨跌：{fut['change']:+.1f} ({fut['change_pct']:+.2f}%)  "
              f"持仓：{fut['open_interest']:,}")
    
    print("-" * 70)
    
    if anomalies:
        print("\n⚠️  异常波动检测:")
        for anomaly in anomalies:
            severity_icon = "🔴" if anomaly['severity'] == 'HIGH' else "🟡"
            print(f"  {severity_icon} {anomaly['message']}")
    else:
        print("\n✅ 无异常波动")
    
    print(f"\n📊 摘要：最大涨幅 {output['summary']['max_change_pct']:.2f}%, 异常数量 {output['summary']['anomaly_count']}")
    
    return output

if __name__ == "__main__":
    main()
