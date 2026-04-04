#!/usr/bin/env python3
"""老虎证券API连接测试 - 只读查询账户信息"""
import sys
sys.path.insert(0, '/Users/bjd/.venv/tiger/lib/python3.14/site-packages')

from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.tiger_open_client import TigerOpenClient
from tigeropen.trade.trade_client import TradeClient
from tigeropen.common.consts import Language

# 老虎账户配置
tiger_id = '20158404'
account = '21208479777116329'
license_code = 'TBNZ'
sandbox = False

# 用户的PKCS#8私钥（base64格式，无PEM标记）
private_key_base64 = 'MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBAI0M43gf0b1Se1A2MlU2rT4okoJ6/Ed1q+YXWYRFWnODW9u/JJ9TtflwTTEz6ckS6f3L8jJ1Mbfr6Jx1kdAGiAuiJDawz1h67qBPMJfqSEJxkkHFoWJA35WTtUGNw2t/sFTUVIMNWc3CeCCm3U+9TUogce8Fm9w0PuJ9kQyBwOrFAgMBAAECgYEAgp3J04abwpcsDEZz68dbPLFzoxLipgYI7mT3B2716PxexyrFbiml3VyqjwLE3uf9+YGwQhuWs/vpB2I0ahByT/t4d6XAh6cgSf26CnR+MtsrQ3PJISUDCQVPFXzu6TY3n5x05rJgYeM6KPBGmamuL+O6hC2/AJzJCXtrDf0gM2ECQQDDzvoTbxLBhPGfEMw+rKaKLVngRj0ckYtR2AanSeNVzkwsi/OH/cn3JseQ5irYSk6rfqJ12JOMJPad6h9YIJ8pAkEAuGjBBzgVZtZIy/BmGO7gFfRW/tGrTDeKNzvaraDS9e6UXN2VaI2F5g19GWR+VRyWtYRfa4+tL7OtybCQN6jOPQJBAJ4LFFvVPh1GkcNiyogX0IAc5LsZ1j+V1g6kP5KNF9ntHhyihVkRZg9/lHqG3LQhHehb2QMnYMgwGYISM2RtSCkCQQClgBYk5XeHqK8CoMjwfYoNChH9dazXpUzdT1Ft3FUYtLrgMVmC0Oin09k/LcqXliXH2HpOrU6P7iD9TwHPgic9AkEAwb7UEYg8mxIBO1XHS4CGtcQzTCb6VVrYYFKr57OBLe1CnS2dhHEQFS9pwiKI1yoxfre4wZx09hxGwOr6fNGn+g=='

# 创建配置
config = TigerOpenClientConfig(
    sandbox_debug=sandbox,
    enable_dynamic_domain=True
)
config.private_key = private_key_base64
config.tiger_id = tiger_id
config.account = account
config.license = license_code
config.language = Language.zh_CN

# 创建交易客户端
client = TradeClient(config)

print("=== 连接测试 ===")
print(f"Tiger ID: {tiger_id}")
print(f"Account: {account}")
print(f"License: {license_code}")
print(f"环境: {'Sandbox' if sandbox else 'PROD'}")
print()

# 获取账户列表
accounts = client.get_managed_accounts()
print(f"=== 账户列表 ({len(accounts)}个) ===")
for a in accounts:
    print(f"  {a}")
print()

# 获取账户资产
try:
    assets = client.get_assets(account)
    print("=== 账户资产 ===")
    print(assets)
except Exception as e:
    print(f"get_assets 失败: {e}")

# 获取持仓
try:
    positions = client.get_positions(account)
    print(f"\n=== 持仓 ({len(positions)}项) ===")
    total_value = 0
    for p in positions:
        mv = float(p.market_value) if p.market_value else 0
        total_value += mv
        print(f"  {p.symbol} {p.quantity}股 @ \${p.market_price} 市值\${mv:.2f} 浮盈\${float(p.unrealized_pnl or 0):.2f}")
    print(f"持仓总市值: \${total_value:.2f}")
except Exception as e:
    print(f"get_positions 失败: {e}")
