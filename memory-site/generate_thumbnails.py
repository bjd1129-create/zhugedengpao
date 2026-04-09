#!/usr/bin/env python3
"""生成缩略图脚本"""

import json
import os
from PIL import Image
from pathlib import Path

SCRIPT_DIR = Path("/Users/bjd/Desktop/ZhugeDengpao-Team/memory-site")
PHOTOS_DIR = SCRIPT_DIR / "images"
THUMBNAILS_DIR = SCRIPT_DIR / "thumbnails"
PHOTOS_JSON = SCRIPT_DIR / "photos_by_folder_complete.json"
THUMBNAIL_SIZE = (400, 400)
QUALITY = 60

def generate_thumbnail(image_path: str, thumb_path: str) -> bool:
    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            original_width, original_height = img.size
            new_width = THUMBNAIL_SIZE[0]
            new_height = int(original_height * (new_width / original_width))
            thumb = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            thumb.save(thumb_path, 'JPEG', quality=QUALITY, optimize=True)
            return True
    except Exception as e:
        print(f"  错误: {image_path} - {e}")
        return False

def main():
    with open(PHOTOS_JSON, 'r', encoding='utf-8') as f:
        photos_data = json.load(f)
    
    THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
    
    total = 0
    success = 0
    failed = 0
    
    for year, photos in photos_data.items():
        if not photos:
            continue
        print(f"\n处理 {year} ({len(photos)} 张)...")
        
        for image_name in photos:
            thumb_name = Path(image_name).stem + '_thumb.jpg'
            thumb_path = THUMBNAILS_DIR / thumb_name
            
            if thumb_path.exists():
                success += 1
                continue
            
            total += 1
            image_path = PHOTOS_DIR / image_name
            if image_path.exists():
                if generate_thumbnail(str(image_path), str(thumb_path)):
                    print(f"  完成: {thumb_name}")
                    success += 1
                else:
                    failed += 1
            else:
                print(f"  跳过: {image_name} (找不到)")
                failed += 1
    
    print(f"\n统计: 总数={total}, 成功={success}, 失败={failed}")

if __name__ == '__main__':
    main()
