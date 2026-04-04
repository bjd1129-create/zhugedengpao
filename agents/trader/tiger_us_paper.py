#!/usr/bin/env python3
"""
Tiger US Stock Paper Portfolio Fetcher v1.1
获取老虎证券模拟账户 + Yahoo Finance行情
"""
import sys, os, json, subprocess, re
from datetime import datetime

# 老虎证券配置
sys.path.insert(0, '/Users/bjd/.venv/tiger/lib/python3.14/site-packages')
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.trade.trade_client import TradeClient
from tigeropen.common.consts import Language

TIGER_ID = '20158404'
PAPER_ACCOUNT = '21639635499102726'
LICENSE_CODE = 'TBNZ'
PRIVATE_KEY = 'MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBAI0M43gf0b1Se1A2MlU2rT4okoJ6/Ed1q+YXWYRFWnODW9u/JJ9TtflwTTEz6ckS6f3L8jJ1Mbfr6Jx1kdAGiAuiJDawz1h67qBPMJfqSEJxkkHFoWJA35WTtUGNw2t/sFTUVIMNWc3CeCCm3U+9TUogce8Fm9w0PuJ9kQyBwOrFAgMBAAECgYEAgp3J04abwpcsDEZz68dbPLFzoxLipgYI7mT3B2716PxexyrFbiml3VyqjwLE3uf9+YGwQhuWs/vpB2I0ahByT/t4d6XAh6cgSf26CnR+MtsrQ3PJISUDCQVPFXzu6TY3n5x05rJgYeM6KPBGmamuL+O6hC2/AJzJCXtrDf0gM2ECQQDDzvoTbxLBhPGfEMw+rKaKLVngRj0ckYtR2AanSeNVzkwsi/OH/cn3JseQ5irYSk6rfqJ12JOMJPad6h9YIJ8pAkEAuGjBBzgVZtZIy/BmGO7gFfRW/tGrTDeKNzvaraDS9e6UXN2VaI2F5g19GWR+VRyWtYRfa4+tL7OtybCQN6jOPQJBAJ4LFFvVPh1GkcNiyogX0IAc5LsZ1j+V1g6kP5KNF9ntHhyihVkRZg9/lHqG3LQhHehb2QMnYMgwGYISM2RtSCkCQQClgBYk5XeHqK8CoMjwfYoNChH9dazXpUzdT1Ft3FUYtLrgMVmC0Oin09k/LcqXliXH2HpOrU6P7iD9TwHPgic9AkEAwb7UEYg8mxIBO1XHS4CGtcQzTCb6VVrYYFKr57OBLe1CnS2dhHEQFS9pwiKI1yoxfre4wZx09hxGwOr6fNGn+g=='

OUTPUT_PATH = os.path.expanduser('~/Desktop/ZhugeDengpao-Team/data/trading/tiger_us_paper.json')

# 策略配置
STRATEGY = {
    'name': '价值定投策略v1.0',
    'version': '1.0',
    'description': '月定投指数ETF + 季度再平衡 + 股息复利',
    'initial_cash': 1_000_000,
    'allocation': {
        'SPY':  {'target': 0.40, 'name': '标普500ETF', 'mode': '定投'},
        'QQQ':  {'target': 0.30, 'name': '纳斯达克100ETF', 'mode': '定投'},
        'VTI':  {'target': 0.20, 'name': '全市场ETF', 'mode': '定投'},
        'BND':  {'target': 0.10, 'name': '债券ETF', 'mode': '定投'},
    },
    'monthly_invest': 10000,
    'rebalance_threshold': 0.05,
}

WATCHED_SYMBOLS = ['SPY', 'QQQ', 'VTI', 'BND', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'JPM', 'V', 'JNJ']


def fetch_quotes(symbols):
    """批量获取行情（curl直接连接，不走代理）"""
    result = {}
    # 构建无代理环境
    no_proxy_env = {k: v for k, v in os.environ.items() if 'proxy' not in k.lower()}
    no_proxy_env['SSL_CERT_FILE'] = '/Users/bjd/.venv/tiger/lib/python3.14/site-packages/certifi/cacert.pem'

    for sym in symbols:
        try:
            cmd = [
                'curl', '-s', '--max-time', '8', '-A',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d'
            ]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10, env=no_proxy_env)
            data = json.loads(r.stdout)
            meta = data['chart']['result'][0]['meta']
            last = meta.get('regularMarketPrice', 0) or 0
            prev = meta.get('chartPreviousClose', 0) or 0
            change = round(last - prev, 2) if prev else 0
            change_pct = round((change / prev * 100), 2) if prev else 0
            result[sym] = {
                'last': last,
                'open': meta.get('regularMarketOpen', 0) or 0,
                'high': meta.get('regularMarketDayHigh', 0) or 0,
                'low': meta.get('regularMarketDayLow', 0) or 0,
                'prev_close': prev,
                'volume': meta.get('regularMarketVolume', 0) or 0,
                'change': change,
                'change_pct': change_pct,
            }
            print(f"  ✅ {sym}: ${last:.2f} ({change_pct:+.2f}%)")
        except Exception as e:
            print(f"  ⚠️ {sym}: 获取失败 ({e})")
            result[sym] = None
    return result


def get_tiger_config():
    config = TigerOpenClientConfig(sandbox_debug=False, enable_dynamic_domain=True)
    config.private_key = PRIVATE_KEY
    config.tiger_id = TIGER_ID
    config.account = PAPER_ACCOUNT
    config.license = LICENSE_CODE
    config.language = Language.zh_CN
    return config


def fetch_tiger_account(client):
    assets = client.get_assets(PAPER_ACCOUNT)
    a = assets[0]
    seg = a.segments.get('S') or a.segments.get('C')
    s = seg if seg else a.summary
    return {
        'account': a.account,
        'cash': getattr(s, 'cash', 0) or 0,
        'net_liquidation': getattr(s, 'net_liquidation', 0) or 0,
        'buying_power': getattr(s, 'buying_power', 0) or 0,
        'gross_position_value': getattr(s, 'gross_position_value', 0) or 0,
        'realized_pnl': getattr(s, 'realized_pnl', 0) or 0,
        'unrealized_pnl': getattr(s, 'unrealized_pnl', 0) or 0,
    }


def fetch_tiger_positions(client):
    positions = client.get_positions(PAPER_ACCOUNT)
    result = []
    for p in positions:
        result.append({
            'symbol': p.symbol,
            'quantity': float(p.quantity or 0),
            'market_price': float(p.market_price or 0),
            'market_value': float(p.market_value or 0),
            'unrealized_pnl': float(p.unrealized_pnl or 0),
            'average_cost': float(getattr(p, 'average_cost', 0) or 0),
        })
    return result


def compute_allocation(account, positions, quotes):
    """计算当前配置 vs 目标配置"""
    alloc = STRATEGY['allocation']
    holdings = {p['symbol']: p for p in positions}
    result = []

    for sym, cfg in alloc.items():
        q = quotes.get(sym, {})
        last = q.get('last', 0) if q else 0
        pos = holdings.get(sym, {})
        qty = pos.get('quantity', 0) if pos else 0
        value = qty * last
        target_pct = cfg['target']
        target_value = account['net_liquidation'] * target_pct

        result.append({
            'symbol': sym,
            'name': cfg['name'],
            'mode': cfg['mode'],
            'target_pct': target_pct,
            'target_value': round(target_value, 2),
            'current_value': round(value, 2),
            'current_qty': qty,
            'current_price': last,
            'diff': round(value - target_value, 2),
            'action': '买入' if value < target_value * 0.95 else ('卖出' if value > target_value * 1.05 else '持有'),
        })

    # 其他持仓（不在核心配置里）
    core_syms = set(alloc.keys())
    for p in positions:
        if p['symbol'] not in core_syms:
            q = quotes.get(p['symbol'], {})
            result.append({
                'symbol': p['symbol'],
                'name': p['symbol'],
                'mode': '持仓',
                'target_pct': 0,
                'target_value': 0,
                'current_value': round(p['market_value'], 2),
                'current_qty': p['quantity'],
                'current_price': p['market_price'],
                'diff': 0,
                'action': '观察',
            })

    return result


def main():
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"\n[🕐 {ts}] ═══ 老虎证券美股模拟账户 ═══")

    # 1. 老虎账户（需要SSL证书）
    tiger_env = os.environ.copy()
    tiger_env['SSL_CERT_FILE'] = '/Users/bjd/.venv/tiger/lib/python3.14/site-packages/certifi/cacert.pem'
    # 清除代理避免影响Tiger API
    for k in ['HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy']:
        tiger_env.pop(k, None)

    try:
        config = get_tiger_config()
        trade_client = TradeClient(config)
        account = fetch_tiger_account(trade_client)
        positions = fetch_tiger_positions(trade_client)
        print(f"  账户: {account['account']}")
        print(f"  现金: ${account['cash']:,.2f}")
        print(f"  净值: ${account['net_liquidation']:,.2f}")
        print(f"  持仓市值: ${account['gross_position_value']:,.2f}")
    except Exception as e:
        print(f"  ❌ 老虎账户获取失败: {e}")
        account = {'account': PAPER_ACCOUNT, 'cash': 0, 'net_liquidation': 0, 'buying_power': 0, 'gross_position_value': 0, 'realized_pnl': 0, 'unrealized_pnl': 0}
        positions = []

    # 2. Yahoo行情（使用curl，不走代理）
    print(f"\n  📊 行情:")
    quotes = fetch_quotes(WATCHED_SYMBOLS)

    # 3. 配置分析
    allocation = compute_allocation(account, positions, quotes)

    # 4. 输出
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    data = {
        'timestamp': now,
        'strategy': STRATEGY,
        'account': account,
        'positions': positions,
        'quotes': quotes,
        'allocation': allocation,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n  ✅ 已保存到 {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
