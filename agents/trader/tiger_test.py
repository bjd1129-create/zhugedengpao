#!/usr/bin/env python3
"""Tiger OpenAPI 连接测试"""
import base64, subprocess, time, json, requests, datetime
from urllib.parse import parse_qsl

# ====== 配置 ======
TIGER_ID = "20158404"
ACCOUNT_ID = "21639635499102726"
LICENSE = "TBNZ"

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

BASE_URL = "https://openapi.tigerfintech.com/gateway"

PEM_FILE = '/tmp/tkey.pem'
pem_text = "-----BEGIN RSA PRIVATE KEY-----\n"
pem_text += "\n".join([PRIVATE_KEY_B64[i:i+64] for i in range(0, len(PRIVATE_KEY_B64), 64)])
pem_text += "\n-----END RSA PRIVATE KEY-----"
with open(PEM_FILE, 'w') as f:
    f.write(pem_text)

def sign(data: str) -> str:
    r = subprocess.run(['openssl', 'dgst', '-sha1', '-sign', PEM_FILE],
        input=data.encode('utf-8'), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"签名失败: {r.stderr.decode()}")
    return base64.b64encode(r.stdout).decode('utf-8')

def api_call(method: str, biz: dict = None) -> requests.Response:
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
        BASE_URL,
        headers=headers,
        params=dict(parse_qsl(sign_content + "&sign=" + signature)),
        data=json.dumps(body, ensure_ascii=False),
        timeout=15
    )
    return resp

def test(method: str, biz: dict = None):
    print(f"\n{'='*50}")
    print(f"Method: {method}")
    resp = api_call(method, biz)
    print(f"状态码: {resp.status_code}")
    try:
        data = resp.json()
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
        return data
    except:
        print(resp.text[:500])
        return None

if __name__ == "__main__":
    print(f"Tiger ID: {TIGER_ID}")
    print(f"账户: {ACCOUNT_ID}")
    print(f"Base URL: {BASE_URL}")
    
    # 1. 获取账户列表
    test("accounts", {"account": ACCOUNT_ID})
    
    # 2. 获取账户信息
    test("account.info", {"account": ACCOUNT_ID})
    
    # 3. 获取持仓
    test("positions", {"account": ACCOUNT_ID})
    
    # 4. 获取资产
    test("assets", {"account": ACCOUNT_ID})
