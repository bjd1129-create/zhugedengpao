#!/usr/bin/env python3
"""
配色师：继续生成龙虾加菲猫120图（第22-120张）
"""
import sys, os, json, time, requests
from datetime import datetime

API_KEY = "sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"
API_URL = "https://api.minimaxi.com/v1/image_generation"
OUTPUT_DIR = "/Users/bjd/Desktop/ZhugeDengpao-Team/images/ai-generated"
LOG_FILE = "/Users/bjd/Desktop/ZhugeDengpao-Team/content/配色师-120图生成记录.md"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCENES = [
    ("scene01", "穿红色龙虾衣服的橙色加菲猫在办公室工作，现代化办公室背景"),
    ("scene02", "穿红色龙虾衣服的橙色加菲猫写代码，现代科技风格"),
    ("scene03", "穿红色龙虾衣服的橙色加菲猫开会，会议室场景"),
    ("scene04", "穿红色龙虾衣服的橙色加菲猫学习，书房场景"),
    ("scene05", "穿红色龙虾衣服的橙色加菲猫喝咖啡，咖啡厅场景"),
    ("scene06", "穿红色龙虾衣服的橙色加菲猫演讲，演讲台场景"),
    ("scene07", "穿红色龙虾衣服的橙色加菲猫做饭，现代厨房背景"),
    ("scene08", "穿红色龙虾衣服的橙色加菲猫旅行，户外风景"),
    ("scene09", "穿红色龙虾衣服的橙色加菲猫运动，健身房场景"),
    ("scene10", "穿红色龙虾衣服的橙色加菲猫睡觉，温馨卧室"),
]

STYLES = [
    ("digital_art", "digital art, high quality, detailed illustration"),
    ("anime", "anime style, Japanese animation, cel shaded"),
    ("pixel_art", "pixel art style, 8-bit, retro game"),
    ("3d_render", "3D render, Pixar style, cinema quality, volumetric lighting"),
    ("watercolor", "watercolor painting, soft colors, artistic brush strokes"),
    ("comic", "comic book style, bold lines, vibrant colors"),
    ("chibi", "chibi cartoon style, cute, big eyes, kawaii"),
    ("cyberpunk", "cyberpunk neon style, neon lights, futuristic city"),
    ("vintage", "vintage illustration, old fashion, classic style"),
    ("sketch", "pencil sketch style, hand drawn, grayscale"),
    ("pop_art", "pop art Andy Warhol style, bold colors, halftone dots"),
    ("art_nouveau", "Art Nouveau style, elegant curves, decorative"),
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

start_idx = 22  # 从第22张开始
success = 0
fail = 0

def log(msg):
    print(msg, flush=True)
    with open(LOG_FILE.replace(".md", ".log"), "a") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")

for scene_id, scene_desc in SCENES:
    for style_id, style_desc in STYLES:
        pass  # skip scenes 1-2 already done

# Build all 120 items
all_items = []
for scene_id, scene_desc in SCENES:
    for style_id, style_desc in STYLES:
        all_items.append((scene_id, style_id, scene_desc, style_desc))

log(f"开始生成剩余图片 (从第22张起)")
total = 120

for idx_base in range(10):  # scenes 0-9
    for style_idx in range(12):  # styles 0-11
        img_num = idx_base * 12 + style_idx + 1  # 1-120
        
        if img_num < start_idx:
            continue
        
        filename = f"lobster_cat_{img_num:03d}.png"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(output_path):
            log(f"[{img_num:03d}/{total}] 跳过(已存在): {filename}")
            continue
        
        scene_id, scene_desc = SCENES[idx_base]
        style_id, style_desc = STYLES[style_idx]
        prompt = f"{scene_desc}, {style_desc}"
        
        payload = {
            "model": "image-01",
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "response_format": "url"
        }
        
        for attempt in range(3):
            try:
                resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
                data = resp.json()
                
                status_code = data.get("base_resp", {}).get("status_code", 0)
                if status_code in [2056, 10003] or resp.status_code == 429:
                    wait = 30 * (attempt + 1)
                    log(f"[{img_num}] ⚠️ 限流(status={status_code})，等待{wait}s...")
                    time.sleep(wait)
                    continue
                
                if status_code != 0:
                    log(f"[{img_num}] ❌ API错误: {data.get('base_resp',{}).get('status_msg')}")
                    time.sleep(2)
                    break
                
                image_urls = data.get("data", {}).get("image_urls", [])
                if not image_urls:
                    log(f"[{img_num}] ❌ 无图片URL")
                    time.sleep(2)
                    break
                
                image_url = image_urls[0]
                img_resp = requests.get(image_url, timeout=60)
                img_resp.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(img_resp.content)
                
                success += 1
                log(f"[{img_num:03d}/{total}] ✅ 成功: {filename} ({success}张)")
                break
                
            except Exception as e:
                if attempt < 2:
                    time.sleep(5)
                    continue
                fail += 1
                log(f"[{img_num}] ❌ 失败({attempt+1}次): {e}")
        
        # Rate limit: 5s between images
        time.sleep(5)

log(f"\n🎉 完成! 成功:{success} 失败:{fail}")