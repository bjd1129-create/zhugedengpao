#!/usr/bin/env python3
import json
from PIL import Image
from pathlib import Path

SCRIPT_DIR = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/memory-site")
PHOTOS_DIR = SCRIPT_DIR / "images"
THUMBNAILS_DIR = SCRIPT_DIR / "thumbnails"
PHOTOS_JSON = SCRIPT_DIR / "photos_by_folder_complete.json"
SIZE = (400, 400)
QUALITY = 60

with open(PHOTOS_JSON) as f:
    data = json.load(f)

count = 0
for year in ['2018年', '2019年']:
    for name in data.get(year, []):
        thumb_path = THUMBNAILS_DIR / (Path(name).stem + '_thumb.jpg')
        if thumb_path.exists():
            continue
        img_path = PHOTOS_DIR / name
        if img_path.exists():
            try:
                with Image.open(img_path) as img:
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    w, h = img.size
                    new_w = SIZE[0]
                    new_h = int(h * (new_w / w))
                    img.resize((new_w, new_h), Image.Resampling.LANCZOS).save(thumb_path, 'JPEG', quality=QUALITY, optimize=True)
                    print(f"完成: {name}")
                    count += 1
            except Exception as e:
                print(f"错误: {name} - {e}")
print(f"新增 {count} 张缩略图")
