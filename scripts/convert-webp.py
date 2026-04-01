#!/usr/bin/env python3
"""Convert xiaohua images to WebP format."""
from PIL import Image
import os

files = ['xiaohua.jpg', 'xiaohua_banner.jpg']
output_dir = '/Users/bjd/Desktop/ZhugeDengpao-Team/images'

for f in files:
    src = os.path.join(output_dir, f)
    webp = os.path.join(output_dir, f.replace('.jpg', '.webp'))
    
    if not os.path.exists(src):
        print(f"SKIP: {src} not found")
        continue
    
    orig_size = os.path.getsize(src)
    img = Image.open(src)
    
    # Remove alpha channel if present (WebP lossless doesn't support RGBA well with some viewers)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background
    
    img.save(webp, 'WEBP', quality=80)
    new_size = os.path.getsize(webp)
    saved = orig_size - new_size
    pct = saved / orig_size * 100
    print(f"{f}: {orig_size//1024}KB → {new_size//1024}KB WebP (saved {saved//1024}KB, {pct:.1f}%)")
