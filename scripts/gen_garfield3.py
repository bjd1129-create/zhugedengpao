#!/usr/bin/env python3
"""Garfield lobster images - with proper rate limiting"""
import os, base64, requests, time, json, sys

sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

API_KEY = "${MINIMAX_API_KEY}"

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

def gen(prompt, idx, scene_id, variant_idx):
    # Wait before each request to avoid rate limit (15 seconds = max 4 RPM)
    time.sleep(15)
    
    for attempt in range(3):
        try:
            print(f"  Calling API (attempt {attempt+1})...", flush=True)
            r = requests.post(
                "https://api.minimaxi.com/v1/image_generation",
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={"model": "image-01", "prompt": prompt, "aspect_ratio": "1:1", "response_format": "base64"},
                timeout=180
            )
            print(f"  HTTP {r.status_code}", flush=True)
            
            if r.status_code == 200:
                data = r.json()
                # Check for rate limit in response
                base_resp = data.get("base_resp", {})
                if base_resp.get("status_code") == 1002:
                    print(f"  Rate limited, waiting 30s...", flush=True)
                    time.sleep(30)
                    continue
                    
                img_data = data.get("data")
                if img_data:
                    img_list = img_data.get("image_base64") or img_data.get("b64_json")
                    if img_list:
                        b64 = img_list[0] if isinstance(img_list, list) else img_list
                        fname = f"images/garfield_lobster_{idx:03d}_{scene_id}_v{variant_idx+1}.png"
                        with open(fname, "wb") as f:
                            f.write(base64.b64decode(b64))
                        print(f"[{idx}/120] OK: {fname}", flush=True)
                        return True
                print(f"  Unexpected response: {str(data)[:200]}", flush=True)
            else:
                print(f"  Error: {r.text[:150]}", flush=True)
                
            time.sleep(10)
        except Exception as e:
            print(f"  Exception: {e}", flush=True)
            time.sleep(10)
    return False

def main():
    existing = []
    for f in os.listdir("images"):
        if f.startswith("garfield_lobster_") and f.endswith(".png"):
            try:
                num = int(f.split("_")[2])
                existing.append(num)
            except:
                pass
    start_idx = max(existing) + 1 if existing else 1
    print(f"Found {len(existing)} images, starting from {start_idx}", flush=True)

    for idx_offset in range(120 - start_idx + 1):
        idx = start_idx + idx_offset
        scene_idx = (idx - 1) // 12
        var_idx = (idx - 1) % 12

        if scene_idx >= len(SCENES):
            print(f"All 120 done!", flush=True)
            break

        scene_id, scene_desc = SCENES[scene_idx]
        variant = STYLE_VARIANTS[var_idx]
        prompt = f"{scene_desc}, {variant}"

        print(f"\n=== Image {idx}/120 ===", flush=True)
        ok = gen(prompt, idx, scene_id, var_idx)
        if not ok:
            print(f"FAILED {idx}, continuing...", flush=True)

    print(f"\n=== ALL DONE ===", flush=True)

if __name__ == "__main__":
    main()