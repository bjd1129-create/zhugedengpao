#!/usr/bin/env python3
"""
配色师任务：生成120张龙虾加菲猫官网配图
场景×12风格 = 120张
"""
import sys
import os
import json
import time
import requests
from datetime import datetime

# API配置
API_KEY = "sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"
API_URL = "https://api.minimaxi.com/v1/image_generation"

# 输出目录
OUTPUT_DIR = "/Users/bjd/Desktop/ZhugeDengpao-Team/images/ai-generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 12种场景
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

# 12种风格
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

# 生成120个prompt
prompts = []
for scene_id, scene_desc in SCENES:
    for style_id, style_desc in STYLES:
        prompt = f"{scene_desc}, {style_desc}"
        prompts.append((scene_id, style_id, prompt))

print(f"总共需要生成 {len(prompts)} 张图片")
print(f"场景数: {len(SCENES)}, 风格数: {len(STYLES)}")
print()

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 生成记录
success_count = 0
fail_count = 0
results = []
start_time = datetime.now()

def generate_image(idx, prompt, filename):
    """生成单张图片"""
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "response_format": "url"
    }
    
    for attempt in range(3):
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=90)
            data = resp.json()
            
            if resp.status_code == 429 or (data.get("base_resp", {}).get("status_code") in [2056, 10003]):
                wait_time = 30 * (attempt + 1)
                print(f"  ⚠️  限流，等待 {wait_time}s...")
                time.sleep(wait_time)
                continue
                
            if data.get("base_resp", {}).get("status_code") != 0:
                return {"success": False, "error": data.get("base_resp", {}).get("status_msg", "unknown"), "url": None}
            
            image_urls = data.get("data", {}).get("image_urls", [])
            if not image_urls:
                return {"success": False, "error": "no image URL", "url": None}
            
            image_url = image_urls[0]
            
            # 下载图片
            img_resp = requests.get(image_url, timeout=60)
            img_resp.raise_for_status()
            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, "wb") as f:
                f.write(img_resp.content)
            
            return {"success": True, "error": None, "url": image_url, "local_path": output_path}
            
        except Exception as e:
            if attempt < 2:
                time.sleep(5)
                continue
            return {"success": False, "error": str(e), "url": None}
    
    return {"success": False, "error": "max retries exceeded", "url": None}

# 开始生成
print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

for i, (scene_id, style_id, prompt) in enumerate(prompts, 1):
    filename = f"lobster_cat_{i:03d}.png"
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    # 检查是否已存在
    if os.path.exists(output_path):
        print(f"[{i:03d}/120] ⏭️  已存在，跳过: {filename}")
        success_count += 1
        results.append({
            "idx": i, "scene": scene_id, "style": style_id,
            "filename": filename, "status": "skipped (exists)", "prompt": prompt
        })
        continue
    
    print(f"[{i:03d}/120] 🔄 生成中: {filename}")
    print(f"         场景: {scene_id} | 风格: {style_id}")
    
    result = generate_image(i, prompt, filename)
    
    if result["success"]:
        print(f"         ✅ 成功! ({success_count + 1}/{i}张)")
        success_count += 1
        status = "success"
    else:
        print(f"         ❌ 失败: {result['error']}")
        fail_count += 1
        status = f"failed: {result['error']}"
    
    results.append({
        "idx": i, "scene": scene_id, "style": style_id,
        "filename": filename, "status": status, "prompt": prompt
    })
    
    # 每10张记录进度
    if i % 10 == 0:
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n📊 进度报告 [{i}/120]")
        print(f"   成功: {success_count} | 失败: {fail_count} | 耗时: {elapsed:.0f}s")
        print("=" * 60)
    
    # 5秒间隔避免RPM限制
    if i < 120:
        time.sleep(5)

end_time = datetime.now()
total_time = (end_time - start_time).total_seconds()

print("\n" + "=" * 60)
print("🎉 生成完成!")
print(f"   成功: {success_count}/120")
print(f"   失败: {fail_count}/120")
print(f"   总耗时: {total_time:.0f}秒 ({total_time/60:.1f}分钟)")
print("=" * 60)

# 保存详细记录
log_file = "/Users/bjd/Desktop/ZhugeDengpao-Team/content/配色师-120图生成记录.md"
with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"# 配色师任务记录 — {end_time.strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## 生成统计\n")
    f.write(f"- 目标：120张\n")
    f.write(f"- 成功：{success_count}张\n")
    f.write(f"- 失败：{fail_count}张\n")
    f.write(f"- 总耗时：{total_time:.0f}秒\n\n")
    f.write("## 具体生成列表\n\n")
    for r in results:
        emoji = "✅" if "success" in r["status"] else ("⏭️" if "skip" in r["status"] else "❌")
        f.write(f"{emoji} #{r['idx']:03d} | {r['scene']} + {r['style']} | {r['filename']} | {r['status']}\n")
        f.write(f"   Prompt: {r['prompt']}\n\n")

print(f"\n📄 详细记录已保存: {log_file}")
