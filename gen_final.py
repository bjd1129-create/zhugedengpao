#!/usr/bin/env python3
"""Garfield lobster images - rate-limit aware, resume-capable"""
import os, base64, requests, time, json, sys

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

os.makedirs("images", exist_ok=True)

def get_last_idx():
    nums = []
    for f in os.listdir("images"):
        if f.startswith("garfield_lobster_") and f.endswith(".png"):
            try:
                nums.append(int(f.split("_")[2]))
            except:
                pass
    return max(nums) if nums else 0

def gen(idx, scene_id, variant_idx, prompt):
    # Check if already exists
    fname = f"images/garfield_lobster_{idx:03d}_{scene_id}_v{variant_idx+1}.png"
    if os.path.exists(fname):
        print(f"[{idx}/120] Already exists, skipping")
        return True
    
    for attempt in range(3):
        # Rate limit delay: 45s between requests to avoid RPM limit
        time.sleep(45)
        
        try:
            r = requests.post(
                "https://api.minimaxi.com/v1/image_generation",
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={"model": "image-01", "prompt": prompt, "aspect_ratio": "1:1", "response_format": "base64"},
                timeout=180
            )
            
            if r.status_code != 200:
                print(f"[{idx}] HTTP {r.status_code}: {r.text[:100]}")
                time.sleep(15)
                continue
            
            resp = r.json()
            
            # Check for rate limit in response body
            base_resp = resp.get("base_resp", {})
            if base_resp.get("status_code") == 1002:
                msg = base_resp.get("status_msg", "rate limit")
                print(f"[{idx}] Rate limited: {msg}. Waiting 60s...")
                time.sleep(60)
                continue
            
            # Check data field
            img_data = resp.get("data")
            if img_data is None:
                print(f"[{idx}] Response data is null. Waiting 60s...")
                time.sleep(60)
                continue
            
            img_list = img_data.get("image_base64") or img_data.get("b64_json")
            if not img_list:
                print(f"[{idx}] No image in data. Waiting 20s...")
                time.sleep(20)
                continue
            
            b64 = img_list[0] if isinstance(img_list, list) else img_list
            with open(fname, "wb") as f:
                f.write(base64.b64decode(b64))
            print(f"[{idx}/120] ✓ {fname} ({os.path.getsize(fname)//1024}KB)")
            return True
            
        except Exception as e:
            print(f"[{idx}] Exception: {e}")
            time.sleep(20)
    
    print(f"[{idx}/120] FAILED after 3 attempts")
    return False

def main():
    start_idx = get_last_idx() + 1
    total = len([f for f in os.listdir("images") if f.startswith("garfield_lobster_") and f.endswith(".png")])
    print(f"Starting: image {start_idx}/120 ({total} already exist)")
    
    for offset in range(120 - start_idx + 1):
        idx = start_idx + offset
        scene_idx = (idx - 1) // 12
        var_idx = (idx - 1) % 12
        
        if scene_idx >= len(SCENES):
            print("All done!")
            break
        
        scene_id, scene_desc = SCENES[scene_idx]
        prompt = f"{scene_desc}, {STYLE_VARIANTS[var_idx]}"
        
        print(f"\n--- Image {idx}/120 (scene={scene_id}, variant={var_idx+1}) ---")
        gen(idx, scene_id, var_idx, prompt)
    
    final = len([f for f in os.listdir("images") if f.startswith("garfield_lobster_") and f.endswith(".png")])
    print(f"\n=== FINISHED: {final}/120 images in images/ ===")

if __name__ == "__main__":
    main()