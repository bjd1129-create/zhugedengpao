#!/usr/bin/env python3
import os
import base64
import requests
import time
import json

API_URL = "https://api.minimaxi.com/v1/image_generation"
API_KEY = "sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"

SCENES = [
    ("01_office", "A fat orange Garfield cat wearing a cute red lobster costume, sitting at a modern office desk, typing on a computer, cheerful expression, cartoon style, warm lighting"),
    ("02_coding", "A fat orange Garfield cat wearing a cute red lobster costume, sitting in front of multiple monitors with code displayed, surrounded by energy drinks and snacks, cartoon style, late night coding atmosphere"),
    ("03_meeting", "A fat orange Garfield cat wearing a cute red lobster costume, sitting at a conference table in a modern meeting room, presenting to other cartoon animals, professional cartoon style"),
    ("04_studying", "A fat orange Garfield cat wearing a cute red lobster costume, reading a thick book at a cozy desk with glasses on, warm cozy atmosphere, cartoon style"),
    ("05_coffee", "A fat orange Garfield cat wearing a cute red lobster costume, relaxing in a cozy cafe with a big cup of coffee and a slice of lasagna, steam rising from the coffee, cartoon style, warm cafe atmosphere"),
    ("06_presentation", "A fat orange Garfield cat wearing a cute red lobster costume, standing on a stage giving a speech, holding a microphone, audience of cartoon animals below, spotlight lighting, cartoon style"),
    ("07_cooking", "A fat orange Garfield cat wearing a cute red lobster costume, standing in a kitchen wearing an apron, cooking lasagna, kitchen counter full of ingredients, cartoon style"),
    ("08_travel", "A fat orange Garfield cat wearing a cute red lobster costume, sitting happily at the window of an airplane, looking out at clouds and blue sky, wearing a travel neck pillow, cartoon style"),
    ("09_exercise", "A fat orange Garfield cat wearing a cute red lobster costume, doing exercise in a gym, lifting light weights with a happy expression, cartoon style, energetic atmosphere"),
    ("10_sleeping", "A fat orange Garfield cat wearing a cute red lobster costume, sleeping soundly on a cozy bed with many pillows and a warm blanket, dreaming of fish and lasagna, cartoon style, moonlight from window"),
]

# 每个场景12个变体，风格/视角/氛围不同
STYLE_VARIANTS = [
    "digital art, vibrant colors, detailed, high quality",
    "anime style, soft colors, kawaii expression",
    "pixel art style, retro gaming aesthetic",
    "3D render, Pixar-like quality, glossy textures",
    "watercolor illustration style, soft brush strokes",
    "comic book style, bold outlines, halftone dots",
    "chibi style, super deformed cute version",
    "art nouveau style, elegant decorative frame",
    "cyberpunk style, neon lights and futuristic background",
    "vintage cartoon style from the 1950s, black and white with selective color",
    "hand-drawn sketch style, pencil on paper texture",
    "pop art style, bright bold colors, Andy Warhol inspired",
]

def generate_image(prompt, idx):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "response_format": "base64"
    }
    
    print(f"  Generating image {idx+1}/120...")
    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    
    if response.status_code != 200:
        print(f"  ERROR {response.status_code}: {response.text[:200]}")
        return None
    
    data = response.json()
    if "data" not in data:
        print(f"  ERROR: no data in response: {str(data)[:300]}")
        return None
    
    img_list = data["data"].get("image_base64") or data["data"].get("b64_json")
    if not img_list:
        print(f"  ERROR: no image data: {str(data)[:300]}")
        return None
    
    # 支持两种格式: {"data": {"image_base64": [...]}} 或 {"data": [{"b64_json": ...}]}
    if isinstance(img_list, list) and len(img_list) > 0:
        return img_list[0]
    elif isinstance(img_list, str):
        return img_list
    else:
        print(f"  ERROR: unexpected image data format: {str(data)[:300]}")
        return None

def save_image(b64_data, filename):
    img_data = base64.b64decode(b64_data)
    with open(filename, "wb") as f:
        f.write(img_data)
    print(f"  Saved: {filename}")

def main():
    os.makedirs("images", exist_ok=True)
    
    total = 0
    for scene_id, scene_desc in SCENES:
        for variant_idx, variant_style in enumerate(STYLE_VARIANTS):
            total += 1
            prompt = f"{scene_desc}, {variant_style}"
            filename = f"images/garfield_lobster_{total:03d}_{scene_id}_v{variant_idx+1}.png"
            
            print(f"\n[{total}/120] Scene: {scene_id}, variant {variant_idx+1}/12")
            
            b64 = generate_image(prompt, total - 1)
            if b64:
                save_image(b64, filename)
            
            # Rate limiting - small delay between requests
            time.sleep(1)
    
    print(f"\n✅ All 120 images generated!")

if __name__ == "__main__":
    main()
