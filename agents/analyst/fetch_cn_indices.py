#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国股指期货数据抓取脚本
数据源：AkShare（新浪财经）
品种：IH(上证 50)、IF(沪深 300)、IC(中证 500)、IM(中证 1000)
"""

import json
import akshare as ak
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# 中国股指期货配置
CN_INDICES_CONFIG = {
    "IH": {"desc": "上证 50 股指期货", "exchange": "CFFEX"},
    "IF": {"desc": "沪深 300 股指期货", "exchange": "CFFEX"},
    "IC": {"desc": "中证 500 股指期货", "exchange": "CFFEX"},
    "IM": {"desc": "中证 1000 股指期货", "exchange": "CFFEX"},
}

def fetch_cn_indices_akshare():
    """使用 AkShare 抓取中国股指期货实时数据"""
    print("\n=== 中国股指期货 ===")
    
    data = {}
    
    try:
        # 获取所有股指期货行情
        df = ak.futures_display_main_sina()
        
        if df is not None and len(df) > 0:
            # 筛选中金所期货
            cn_indices_df = df[df['exchange'].str.contains('中金所', na=False)]
            
            for product, info in CN_INDICES_CONFIG.items():
                print(f"  抓取 {product} ({info['desc']})...", end=" ")
                
                # 筛选对应品种
                product_df = cn_indices_df[cn_indices_df['symbol'].str.startswith(product, na=False)]
                
                if len(product_df) > 0:
                    latest = product_df.iloc[0]
                    
                    price = float(latest.get('close', latest.get('price', 0)))
                    change_pct = float(latest.get('pct_chg', latest.get('change_pct', 0)))
                    volume = int(latest.get('volume', latest.get('vol', 0)))
                    contract = latest.get('symbol', f"{product}2505")
                    
                    data[product] = {
                        "price": round(price, 2),
                        "change_pct": round(change_pct, 2),
                        "volume": volume,
                        "contract": contract,
                        "desc": info["desc"],
                        "source": "CFFEX (AkShare)"
                    }
                    
                    print(f"¥{price:.1f} ({change_pct:+.2f}%) 成交量：{volume:,}")
                else:
                    print("✗ 无数据")
        else:
            print("✗ 无法获取期货数据")
            
    except Exception as e:
        print(f"✗ 错误：{e}")
        # 使用模拟数据作为备用
        mock_prices = {
            "IH": {"price": 2850.0, "change_pct": 1.2, "volume": 15000},
            "IF": {"price": 3950.0, "change_pct": 0.8, "volume": 25000},
            "IC": {"price": 6250.0, "change_pct": 0.5, "volume": 20000},
            "IM": {"price": 5850.0, "change_pct": 0.3, "volume": 12000},
        }
        for product, info in CN_INDICES_CONFIG.items():
            if product not in data:
                p = mock_prices[product]
                data[product] = {
                    "price": p["price"],
                    "change_pct": p["change_pct"],
                    "volume": p["volume"],
                    "contract": f"{product}2505",
                    "desc": info["desc"],
                    "source": "CFFEX (模拟备用)"
                }
                print(f"  {product}: ¥{p['price']:.1f} ({p['change_pct']:+.1f}%) [备用]")
    
    return data

def main():
    print(f"[{datetime.now().astimezone().isoformat()}] 开始抓取中国股指期货数据 (AkShare)...")
    
    # 抓取中国股指期货
    cn_data = fetch_cn_indices_akshare()
    
    # 保存
    output_file = DATA_DIR / "cn_indices_prices.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cn_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ 数据已保存：{output_file}")
    print(f"[{datetime.now().astimezone().isoformat()}] 完成！")

if __name__ == "__main__":
    main()
