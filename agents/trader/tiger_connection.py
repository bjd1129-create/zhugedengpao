"""
Tiger OpenAPI 连接模块
用法:
  from tiger_connection import TigerAPI
  api = TigerAPI()
  api.get_accounts()
  api.get_assets()
  api.get_positions()
"""
import base64
import subprocess
import datetime
import json
import requests
from urllib.parse import parse_qsl
from typing import Optional

TIGER_ID = "20158404"
ACCOUNT_ID = "21639635499102726"
LICENSE = "TBNZ"
BASE_URL = "https://openapi.tigerfintech.com/gateway"

PRIVATE_KEY_B64 = (
    "MIICXAIBAAKBgQCby+x38wRMjNZgdEKRsfqGPLD+TUrRFu4l5FQsmdZ5ZiZWXvXpdlR6M"
    "mnKk473jNvBnwUN8qDqujHrn0DOjfmrHCd46Pi+wsVkbf3xbKPXh9RabddOXfMMwTF0n"
    "h5P9wk9oG0GG1Prxz2cNHuMBBPE+6Whp/01jLgfcoZb7PImUwIDAQABAoGAVmv+VmNl"
    "5RjS6lpTewJhWAlenRI/CFFR9Y786mjDwj/Z0FuIyeKr5cUFTiwgSE3IsVUGtr/6Z3q1"
    "qmCC0JGNBnH5qttIZwLLxUl/RX31IiYwjUC8rY/AhPa5Uwp4nNYi3qKsMIYV1Efg2Rm1"
    "B68iZhL/GtEnSo0PMIdK8GSMqAECQQDT4pzMU35t69+qdZn1GGU2FQqe0MuYZk+eRPW2Q"
    "RpnwaCWZiv60b6Fdjioh/UZbJ/gNetyxbcVDqti1sORN/hTAkEAvDvP7DsZoo7nBF7Cc"
    "Dd+IFKTPyHmzi65kIHek/SmQJ/JR4ZNKTWzFSdVnSzNSvFbkr7V4WAkSW1Gx1du5j9a"
    "AQJBALzQZwvJp5OKqxD6pUx9Bcww6frmc1eGbJLMPu2/jClDqbf8qlpjyFSkKg88wJR8"
    "cOfbBMqNF/5CyUVVvobNCpMCQDKbkiddLGM8MHhIUdaB1PMzwEr0/mzouxNTF1iIKjqt"
    "uxvzy8MMoP1K+gWsCfXgNlKZ5D8X7imfq6vkofhdiAECQBUpHPtTE6D2xpPYVlaL1Kyk"
    "PIb1GgAu228v1w+eqgi6zuSgTymZXvn2pIQ/mvzTgXOqU/CpkwhdDTLmDQMpgI0="
)

PEM_FILE = '/tmp/tkey.pem'

def _init_pem():
    pem_text = "-----BEGIN RSA PRIVATE KEY-----\n"
    pem_text += "\n".join([PRIVATE_KEY_B64[i:i+64] for i in range(0, len(PRIVATE_KEY_B64), 64)])
    pem_text += "\n-----END RSA PRIVATE KEY-----"
    with open(PEM_FILE, 'w') as f:
        f.write(pem_text)

_init_pem()

def sign(data: str) -> str:
    r = subprocess.run(
        ['openssl', 'dgst', '-sha256', '-sign', PEM_FILE],
        input=data.encode('utf-8'), capture_output=True
    )
    if r.returncode != 0:
        raise RuntimeError(f"签名失败: {r.stderr.decode()}")
    return base64.b64encode(r.stdout).decode('utf-8')

def _call(method: str, biz: Optional[dict] = None) -> dict:
    """通用API调用"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    biz_str = json.dumps(biz or {}, ensure_ascii=False, separators=(',', ':'))
    params = {
        "biz_content": biz_str,
        "charset": "UTF-8",
        "method": method,
        "sign_type": "RSA",
        "timestamp": timestamp,
        "tiger_id": TIGER_ID,
        "version": "3.0",
    }
    pairs = [f"{k}={v}" for k, v in sorted(params.items())]
    sign_content = "&".join(pairs)
    signature = sign(sign_content)
    body = dict(params)
    body["sign"] = signature
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    resp = requests.post(
        BASE_URL, headers=headers,
        params=dict(parse_qsl(sign_content + "&sign=" + signature)),
        data=json.dumps(body, ensure_ascii=False), timeout=15
    )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Tiger API error {data.get('code')}: {data.get('message')}")
    return data

def get_accounts() -> dict:
    """获取账户列表"""
    return _call("accounts", {"account": ACCOUNT_ID})

def get_assets() -> dict:
    """获取账户资产"""
    return _call("assets", {"account": ACCOUNT_ID})

def get_positions() -> dict:
    """获取持仓"""
    return _call("positions", {"account": ACCOUNT_ID})

def get_orders(limit: int = 50) -> dict:
    """获取订单"""
    return _call("orders", {"account": ACCOUNT_ID, "limit": limit})

if __name__ == "__main__":
    print("=== Tiger API 测试 ===")
    print(f"账户: {ACCOUNT_ID}")
    
    print("\n--- 账户 ---")
    data = get_accounts()
    items = json.loads(data["data"])["items"]
    for acc in items:
        print(f"  {acc['account']} | {acc['accountType']} | {acc['capability']} | {acc['status']}")
    
    print("\n--- 资产 ---")
    data = get_assets()
    items = json.loads(data["data"])["items"]
    for a in items:
        print(f"  现金: ${a['cashValue']:,.2f} | 净值: ${a['netLiquidation']:,.2f} | 购买力: ${a['buyingPower']:,.2f}")
    
    print("\n--- 持仓 ---")
    data = get_positions()
    items = json.loads(data["data"])["items"]
    print(f"  {'空' if not items else items}")
