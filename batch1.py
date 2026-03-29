#!/usr/bin/env python3
"""Batch 1: images 1-30"""
import os, base64, requests, time, json

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

def gen(prompt, idx, scene_id, variant_idx):
    try:
        r = requests.post(
            "https://api.minimaxi.com/v1/image_generation",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": "image-01", "prompt": prompt, "aspect_ratio": "1:1", "response_format": "base64"},
            timeout=120
        )
        if r.status_code != 200:
            print(f"  ERROR {r.status_code}: {r.text[:150]}")
            return False
        data = r.json()
        img_list = data.get("data", {}).get("image_base64") or data.get("data", {}).get("b64_json")
        if not img_list:
            print(f"  ERROR no img: {str(data)[:200]}")
            return False
        b64 = img_list[0] if isinstance(img_list, list) else img_list
        fname = f"images/garfield_lobster_{idx:03d}_{scene_id}_v{variant_idx+1}.png"
        with open(fname, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  [{idx}/120] OK: {fname}")
        return True
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return False

def main():
    idx = 1
    for si, (scene_id, scene_desc) in enumerate(SCENES):
        for vi, variant in enumerate(STYLE_VARIANTS):
            prompt = f"{scene_desc}, {variant}"
            ok = False
            for attempt in range(3):
                if gen(prompt, idx, scene_id, vi):
                    ok = True
                    break
                time.sleep(5)
            if not ok:
                print(f"  FAILED after 3 attempts: {idx}")
            idx += 1
            time.sleep(1)
            if idx > 30:
                return

if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)
    main()
    print("Batch 1 done (images 1-30)")