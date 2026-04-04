#!/usr/bin/env python3
"""查询Tiger账户列表和授权情况"""
import sys
sys.path.insert(0, '/Users/bjd/.venv/tiger/lib/python3.14/site-packages')

from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.trade.trade_client import TradeClient
from tigeropen.common.consts import Language

tiger_id = '20158404'
account = '21208479777116329'  # 用户给的账户ID
license_code = 'TBNZ'
private_key_base64 = 'MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBAI0M43gf0b1Se1A2MlU2rT4okoJ6/Ed1q+YXWYRFWnODW9u/JJ9TtflwTTEz6ckS6f3L8jJ1Mbfr6Jx1kdAGiAuiJDawz1h67qBPMJfqSEJxkkHFoWJA35WTtUGNw2t/sFTUVIMNWc3CeCCm3U+9TUogce8Fm9w0PuJ9kQyBwOrFAgMBAAECgYEAgp3J04abwpcsDEZz68dbPLFzoxLipgYI7mT3B2716PxexyrFbiml3VyqjwLE3uf9+YGwQhuWs/vpB2I0ahByT/t4d6XAh6cgSf26CnR+MtsrQ3PJISUDCQVPFXzu6TY3n5x05rJgYeM6KPBGmamuL+O6hC2/AJzJCXtrDf0gM2ECQQDDzvoTbxLBhPGfEMw+rKaKLVngRj0ckYtR2AanSeNVzkwsi/OH/cn3JseQ5irYSk6rfqJ12JOMJPad6h9YIJ8pAkEAuGjBBzgVZtZIy/BmGO7gFfRW/tGrTDeKNzvaraDS9e6UXN2VaI2F5g19GWR+VRyWtYRfa4+tL7OtybCQN6jOPQJBAJ4LFFvVPh1GkcNiyogX0IAc5LsZ1j+V1g6kP5KNF9ntHhyihVkRZg9/lHqG3LQhHehb2QMnYMgwGYISM2RtSCkCQQClgBYk5XeHqK8CoMjwfYoNChH9dazXpUzdT1Ft3FUYtLrgMVmC0Oin09k/LcqXliXH2HpOrU6P7iD9TwHPgic9AkEAwb7UEYg8mxIBO1XHS4CGtcQzTCb6VVrYYFKr57OBLe1CnS2dhHEQFS9pwiKI1yoxfre4wZx09hxGwOr6fNGn+g=='

config = TigerOpenClientConfig(sandbox_debug=False, enable_dynamic_domain=True)
config.private_key = private_key_base64
config.tiger_id = tiger_id
config.account = account
config.license = license_code
config.language = Language.zh_CN

client = TradeClient(config)

# 获取账户列表
accounts = client.get_managed_accounts()
print(f"=== 账户列表 ({len(accounts)}个) ===")
for a in accounts:
    print(f"  account={a.account}")
    print(f"  account_type={a.account_type}")
    print(f"  capability={a.capability}")
    print(f"  status={a.status}")
    print()

# 用第一个真实账户测试
real_account = accounts[0].account
print(f"=== 使用账户 {real_account} 获取资产 ===")
config.account = real_account
client2 = TradeClient(config)
try:
    assets = client2.get_assets(real_account)
    print(assets)
except Exception as e:
    print(f"失败: {e}")

try:
    positions = client2.get_positions(real_account)
    print(f"\n=== 持仓 ({len(positions)}项) ===")
    for p in positions:
        print(f"  {p.symbol} {p.quantity}股 @ \${p.market_price} 市值\${p.market_value} 浮盈\${p.unrealized_pnl}")
except Exception as e:
    print(f"持仓失败: {e}")
