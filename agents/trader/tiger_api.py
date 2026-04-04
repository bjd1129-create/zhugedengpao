#!/usr/bin/env python3
"""
老虎证券Tiger API - 交易员Agent调用模块
PAPER账户（模拟盘）：21639635499102726
"""
import sys
import os
sys.path.insert(0, '/Users/bjd/.venv/tiger/lib/python3.14/site-packages')
os.environ['SSL_CERT_FILE'] = '/Users/bjd/.venv/tiger/lib/python3.14/site-packages/certifi/cacert.pem'

from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.trade.trade_client import TradeClient
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.common.consts import Language, SecurityType, Currency, OrderStatus
from tigeropen.common.util.order_utils import limit_order

# 配置
TIGER_ID = '20158404'
PAPER_ACCOUNT = '21639635499102726'
REAL_ACCOUNT = '7664186'
LICENSE = 'TBNZ'

# 私钥（base64，无PEM标记）
PRIVATE_KEY = 'MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBAI0M43gf0b1Se1A2MlU2rT4okoJ6/Ed1q+YXWYRFWnODW9u/JJ9TtflwTTEz6ckS6f3L8jJ1Mbfr6Jx1kdAGiAuiJDawz1h67qBPMJfqSEJxkkHFoWJA35WTtUGNw2t/sFTUVIMNWc3CeCCm3U+9TUogce8Fm9w0PuJ9kQyBwOrFAgMBAAECgYEAgp3J04abwpcsDEZz68dbPLFzoxLipgYI7mT3B2716PxexyrFbiml3VyqjwLE3uf9+YGwQhuWs/vpB2I0ahByT/t4d6XAh6cgSf26CnR+MtsrQ3PJISUDCQVPFXzu6TY3n5x05rJgYeM6KPBGmamuL+O6hC2/AJzJCXtrDf0gM2ECQQDDzvoTbxLBhPGfEMw+rKaKLVngRj0ckYtR2AanSeNVzkwsi/OH/cn3JseQ5irYSk6rfqJ12JOMJPad6h9YIJ8pAkEAuGjBBzgVZtZIy/BmGO7gFfRW/tGrTDeKNzvaraDS9e6UXN2VaI2F5g19GWR+VRyWtYRfa4+tL7OtybCQN6jOPQJBAJ4LFFvVPh1GkcNiyogX0IAc5LsZ1j+V1g6kP5KNF9ntHhyihVkRZg9/lHqG3LQhHehb2QMnYMgwGYISM2RtSCkCQQClgBYk5XeHqK8CoMjwfYoNChH9dazXpUzdT1Ft3FUYtLrgMVmC0Oin09k/LcqXliXH2HpOrU6P7iD9TwHPgic9AkEAwb7UEYg8mxIBO1XHS4CGtcQzTCb6VVrYYFKr57OBLe1CnS2dhHEQFS9pwiKI1yoxfre4wZx09hxGwOr6fNGn+g=='

_trade_client = None
_quote_client = None

def get_trade_client(use_paper=True):
    global _trade_client
    if _trade_client is None:
        config = TigerOpenClientConfig(sandbox_debug=False, enable_dynamic_domain=True)
        config.private_key = PRIVATE_KEY
        config.tiger_id = TIGER_ID
        config.account = PAPER_ACCOUNT if use_paper else REAL_ACCOUNT
        config.license = LICENSE
        config.language = Language.zh_CN
        _trade_client = TradeClient(config)
    return _trade_client

def get_quote_client():
    global _quote_client
    if _quote_client is None:
        config = TigerOpenClientConfig(sandbox_debug=False, enable_dynamic_domain=True)
        config.private_key = PRIVATE_KEY
        config.tiger_id = TIGER_ID
        config.account = PAPER_ACCOUNT
        config.license = LICENSE
        config.language = Language.zh_CN
        _quote_client = QuoteClient(config)
    return _quote_client

def get_account_info():
    """获取账户信息"""
    client = get_trade_client()
    assets = client.get_assets(PAPER_ACCOUNT)
    a = assets[0]
    return {
        'account': a.account,
        'cash': a.summary.cash,
        'net_liquidation': a.summary.net_liquidation,
        'buying_power': a.summary.buying_power,
        'realized_pnl': a.summary.realized_pnl,
        'unrealized_pnl': a.summary.unrealized_pnl,
    }

def get_positions():
    """获取持仓"""
    client = get_trade_client()
    positions = client.get_positions(PAPER_ACCOUNT)
    return [
        {
            'symbol': p.symbol,
            'quantity': p.quantity,
            'market_price': p.market_price,
            'market_value': p.market_value,
            'unrealized_pnl': p.unrealized_pnl,
        }
        for p in positions
    ]

def get_quote(symbol, sec_type=SecurityType.STK, currency=Currency.USD):
    """获取实时行情"""
    qc = get_quote_client()
    contracts = qc.get_contracts(symbol, sec_type, currency)
    if not contracts:
        return None
    data = qc.get_market_data(contracts[0].symbol, fields=['last', 'open', 'high', 'low', 'volume', 'change_ratio'])
    return data

def place_order(symbol, quantity, price, sec_type=SecurityType.STK, currency=Currency.USD, action='BUY'):
    """下单（限价单）"""
    client = get_trade_client()
    contract = client.get_contract(symbol, sec_type, currency)
    order = limit_order(contract, action, quantity, price)
    result = client.place_order(order)
    return result

def get_orders():
    """获取订单列表"""
    client = get_trade_client()
    return client.get_orders(account=PAPER_ACCOUNT)

if __name__ == '__main__':
    print("=== 老虎证券API测试 ===")
    info = get_account_info()
    print(f"账户: {info['account']}")
    print(f"现金: ${info['cash']:,.2f}")
    print(f"净值: ${info['net_liquidation']:,.2f}")
    print(f"购买力: ${info['buying_power']:,.2f}")
    print(f"持仓: {get_positions()}")
    
    print("\n=== 行情测试 ===")
    q = get_quote('AAPL')
    print(f"AAPL: {q}")
