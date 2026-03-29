import base64
import requests
import os
import sys

url = "https://api.minimaxi.com/v1/image_generation"

# 从环境变量获取 key
api_key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_API_KEY")

if not api_key:
    print("Error: MINIMAX_API_KEY not found in environment")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "image-01",
    "prompt": "一只穿着红色龙虾衣服的橙色加菲猫，非常可爱，温暖风格，高质量插画",
    "aspect_ratio": "1:1",
    "response_format": "base64"
}

print("Generating image...")
response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()

images = response.json()["data"]["image_base64"]
output_path = "/Users/bjd/Desktop/ZhugeDengpao-Team/images/xiaohua_test.png"

for i, img_data in enumerate(images):
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(img_data))
    print(f"Saved to {output_path}")
