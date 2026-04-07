#!/bin/bash
# 获取老虎证券美股数据 + Yahoo Finance行情
# 兼容两种网络环境

OUT_FILE="/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/tiger_us_paper.json"
VENV_PY="/Users/bjd/.venv/tiger/bin/python"
CERT_FILE="/Users/bjd/.venv/tiger/lib/python3.14/site-packages/certifi/cacert.pem"

# 清理代理环境获取Tiger数据
echo "[$(date +%H:%M:%S)] 获取老虎证券数据..."
TIGER_DATA=$(SSH_ASKPASS=1 SSL_CERT_FILE="$CERT_FILE" \
  env -i HOME="$HOME" \
       USER="$USER" \
       PATH="$PATH" \
       SSL_CERT_FILE="$CERT_FILE" \
       TERM="$TERM" \
       LANG="$LANG" \
       "$VENV_PY" -c "
import sys, os, json
sys.path.insert(0, '/Users/bjd/.venv/tiger/lib/python3.14/site-packages')
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.trade.trade_client import TradeClient
from tigeropen.common.consts import Language

PRIVATE_KEY = 'MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBAI0M43gf0b1Se1A2MlU2rT4okoJ6/Ed1q+YXWYRFWnODW9u/JJ9TtflwTTEz6ckS6f3L8jJ1Mbfr6Jx1kdAGiAuiJDawz1h67qBPMJfqSEJxkkHFoWJA35WTtUGNw2t/sFTUVIMNWc3CeCCm3U+9TUogce8Fm9w0PuJ9kQyBwOrFAgMBAAECgYEAgp3J04abwpcsDEZz68dbPLFzoxLipgYI7mT3B2716PxexyrFbiml3VyqjwLE3uf9+YGwQhuWs/vpB2I0ahByT/t4d6XAh6cgSf26CnR+MtsrQ3PJISUDCQVPFXzu6TY3n5x05rJgYeM6KPBGmamuL+O6hC2/AJzJCXtrDf0gM2ECQQDDzvoTbxLBhPGfEMw+rKaKLVngRj0ckYtR2AanSeNVzkwsi/OH/cn3JseQ5irYSk6rfqJ12JOMJPad6h9YIJ8pAkEAuGjBBzgVZtZIy/BmGO7gFfRW/tGrTDeKNzvaraDS9e6UXN2VaI2F5g19GWR+VRyWtYRfa4+tL7OtybCQN6jOPQJBAJ4LFFvVPh1GkcNiyogX0IAc5LsZ1j+V1g6kP5KNF9ntHhyihVkRZg9/lHqG3LQhHehb2QMnYMgwGYISM2RtSCkCQQClgBYk5XeHqK8CoMjwfYoNChH9dazXpUzdT1Ft3FUYtLrgMVmC0Oin09k/LcqXliXH2HpOrU6P7iD9TwHPgic9AkEAwb7UEYg8mxIBO1XHS4CGtcQzTCb6VVrYYFKr57OBLe1CnS2dhHEQFS9pwiKI1yoxfre4wZx09hxGwOr6fNGn+g=='
config = TigerOpenClientConfig(sandbox_debug=False, enable_dynamic_domain=True)
config.private_key = PRIVATE_KEY
config.tiger_id = '20158404'
config.account = '21639635499102726'
config.license = 'TBNZ'
config.language = Language.zh_CN

client = TradeClient(config)
assets = client.get_assets('21639635499102726')
a = assets[0]
seg = a.segments.get('S') or a.segments.get('C') or a.summary
print(json.dumps({
    'account': a.account,
    'cash': float(getattr(seg, 'cash', 0) or 0),
    'net_liquidation': float(getattr(seg, 'net_liquidation', 0) or 0),
    'buying_power': float(getattr(seg, 'buying_power', 0) or 0),
    'gross_position_value': float(getattr(seg, 'gross_position_value', 0) or 0),
    'realized_pnl': float(getattr(seg, 'realized_pnl', 0) or 0),
    'unrealized_pnl': float(getattr(seg, 'unrealized_pnl', 0) or 0),
}))
" 2>&1)

echo "Tiger data: ${TIGER_DATA:0:100}..."

# 获取Yahoo Finance行情（通过代理）
echo "[$(date +%H:%M:%S)] 获取Yahoo Finance行情..."
YQ=""
for SYM in SPY QQQ VTI BND AAPL MSFT GOOGL AMZN NVDA META TSLA JPM V JNJ; do
  PRICE=$(curl -s --max-time 5 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
    "https://query1.finance.yahoo.com/v8/finance/chart/$SYM?interval=1d&range=1d" 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin); m=d['chart']['result'][0]['meta']; print(f'{m[\"regularMarketPrice\"]},{m.get(\"chartPreviousClose\",0)}')" 2>/dev/null)
  if [ -n "$PRICE" ]; then
    LAST=$(echo $PRICE | cut -d, -f1)
    PREV=$(echo $PRICE | cut -d, -f2)
    CHG=$(python3 -c "print(round($LAST-$PREV,2))")
    CHG_PCT=$(python3 -c "print(round(($LAST-$PREV)/$PREV*100,2))" 2>/dev/null || echo "0")
    echo "  ✅ $SYM: \$$LAST ($CHG_PCT%)"
    YQ="$YQ\"$SYM\": {\"last\":$LAST,\"prev_close\":$PREV,\"change\":$CHG,\"change_pct\":$CHG_PCT},"
  else
    echo "  ⚠️ $SYM: 获取失败"
    YQ="$YQ\"$SYM\": null,"
  fi
done

YQ="{${YQ%,}}"

# 组装最终JSON
NOW=$(date +"%Y-%m-%dT%H:%M:%S+08:00")
cat > "$OUT_FILE" << EOF
{
  "timestamp": "$NOW",
  "strategy": {
    "name": "价值定投策略v1.0",
    "version": "1.0",
    "description": "月定投指数ETF + 季度再平衡 + 股息复利",
    "initial_cash": 1000000,
    "allocation": {
      "SPY":  {"target": 0.40, "name": "标普500ETF", "mode": "定投"},
      "QQQ":  {"target": 0.30, "name": "纳斯达克100ETF", "mode": "定投"},
      "VTI":  {"target": 0.20, "name": "全市场ETF", "mode": "定投"},
      "BND":  {"target": 0.10, "name": "债券ETF", "mode": "定投"}
    },
    "monthly_invest": 10000,
    "rebalance_threshold": 0.05
  },
  "account": $TIGER_DATA,
  "positions": [],
  "quotes": $YQ,
  "allocation": []
}
EOF

echo "[$(date +%H:%M:%S)] ✅ 数据已保存到 $OUT_FILE"

# 同步到website目录（供trading.html前端读取）
WEBSITE_DATA="/Users/bjd/Desktop/ZhugeDengpao-Team/website/data/trading"
cp "$OUT_FILE" "$WEBSITE_DATA/tiger_us_paper.json"
cp "/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/portfolio.json" "$WEBSITE_DATA/portfolio.json" 2>/dev/null
cp "/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/polymarket_data.json" "$WEBSITE_DATA/polymarket_data.json" 2>/dev/null
cp "/Users/bjd/Desktop/ZhugeDengpao-Team/data/trading/polymarket_portfolio.json" "$WEBSITE_DATA/polymarket_portfolio.json" 2>/dev/null
echo "[$(date +%H:%M:%S)] ✅ 已同步到website/data/trading/"
