#!/usr/bin/env python3
"""老虎证券模拟账户(PAPER)测试"""
import sys
sys.path.insert(0, '/Users/bjd/.venv/tiger/lib/python3.14/site-packages')

from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.trade.trade_client import TradeClient
from tigeropen.common.consts import Language, SecurityType, Currency

tiger_id = '20158404'
paper_account = '21639635499102726'
license_code = 'TBNZ'

# PKCS#8私钥（base64格式，无PEM标记）
private_key_base64 = 'MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBAI0M43gf0b1Se1A2MlU2rT4okoJ6/Ed1q+YXWYRFWnODW9u/JJ9TtflwTTEz6ckS6f3L8jJ1Mbfr6Jx1kdAGiAuiJDawz1h67qBPMJfqSEJxkkHFoWJA35WTtUGNw2t/sFTUVIMNWc3CeCCm3U+9TUogce8Fm9w0PuJ9kQyBwOrFAgMBAAECgYEAgp3J04abwpcsDEZz68dbPLFzoxLipgYI7mT3B2716PxexyrFbiml3VyqjwLE3uf9+YGwQhuWs/vpB2I0ahByT/t4d6XAh6cgSf26CnR+MtsrQ3PJISUDCQVPFXzu6TY3n5x05rJgYeM6KPBGmamuL+O6hC2/AJzJCXtrDf0gM2ECQQDDzvoTbxLBhPGfEMw+rKaKLVngRj0ckYtR2AanSeNVzkwsi/OH/cn3JseQ5irYSk6rfqJ12JOMJPad6h9YIJ8pAkEAuGjBBzgVZtZIy/BmGO7gFfRW/tGrTDeKNzvaraDS9e6UXN2VaI2F5g19GWR+VRyWtYRfa4+tL7OtybCQN6jOPQJBAJ4LFFvVPh1GkcNiyogX0IAc5LsZ1j+V1g6kP5KNF9ntHhyihVkRZg9/lHqG3LQhHehb2QMnYMgwGYISM2RtSCkCQQClgBYk5XeHqK8CoMjwfYoNChH9dazXpUzdT1Ft3FUYtLrgMVmC0Oin09k/LcqXliXH2HpOrU6P7iD9TwHPgic9AkEAwb7UEYg8mxIBO1XHS4CGtcQzTCb6VVrYYFKr57OBLe1CnS2dhHEQFS9pwiKI1yoxfre4wZx09hxGwOr6fNGn+g=='

config = TigerOpenClientConfig(sandbox_debug=False, enable_dynamic_domain=True)
config.private_key = private_key_base64
config.tiger_id = tiger_id
config.account = paper_account
config.license = license_code
config.language = Language.zh_CN

client = TradeClient(config)

print("=== 模拟账户(PAPER)连接测试 ===")
print(f"Account: {paper_account}")
print()

# 获取账户资产
assets = client.get_assets(paper_account)
print("=== 账户资产 ===")
summary = assets.summary
print(f"账户ID: {assets.account}")
print(f"现金: \${summary.cash}")
print(f"净 liquidation: \${summary.net_liquidation}")
print(f"购买力: \${summary.buying_power}")
print(f"持仓市值: \${summary.gross_position_value}")
print(f"已实现PnL: \${summary.realized_pnl}")
print(f"未实现PnL: \${summary.unrealized_pnl}")
print()

# 获取持仓
positions = client.get_positions(paper_account)
print(f"=== 持仓 ({len(positions)}项) ===")
for p in positions:
    print(f"  {p.symbol} {p.quantity}股 @ \${p.market_price} 市值\${p.market_value} 浮盈\${p.unrealized_pnl}")
print()

# 查询行情（苹果股票）
from tigeropen.quote.quote_client import QuoteClient
quote_client = QuoteClient(config)
symbols = ['AAPL', 'TSLA', 'BTC']
print("=== 行情快照 ===")
for sym in symbols:
    try:
        contracts = quote_client.get_contracts(sym, SecurityType.STK, Currency.USD)
        if contracts:
            ticker = quote_client.get_market_data(contracts[0].symbol, fields=['last', 'open', 'high', 'low', 'volume'])
            print(f"  {sym}: \${ticker.last if hasattr(ticker,'last') else 'N/A'}")
    except Exception as e:
        print(f"  {sym}: 查询失败 - {e}")
