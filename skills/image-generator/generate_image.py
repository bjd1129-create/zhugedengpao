#!/usr/bin/env python3
"""
通用图片生成脚本 - 支持阿里云百炼/MiniMax
用法:
  python generate_image.py --prompt "描述" --filename "output.png" [--provider bailian|minimax] [--resolution 1K|2K]
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("错误: 请安装 requests 库: pip install requests")
    sys.exit(1)

# API 配置
BAILIAN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
MINIMAX_API_URL = "https://api.minimax.chat/v1/imagegenerations"

def get_api_key(provider):
    """获取 API Key"""
    if provider == "bailian":
        key = os.environ.get("DASHSCOPE_API_KEY", "")
        if not key:
            # 尝试从 .env 文件读取
            env_path = Path(__file__).parent.parent.parent / ".env"
            if env_path.exists():
                for line in env_path.read_text().splitlines():
                    if line.startswith("DASHSCOPE_API_KEY="):
                        key = line.split("=", 1)[1].strip()
                        break
        return key
    elif provider == "minimax":
        key = os.environ.get("MINIMAX_API_KEY", "")
        if not key:
            env_path = Path(__file__).parent.parent.parent / ".env"
            if env_path.exists():
                for line in env_path.read_text().splitlines():
                    if line.startswith("MINIMAX_API_KEY="):
                        key = line.split("=", 1)[1].strip()
                        break
        return key
    return ""

def generate_bailian(prompt, resolution="1K"):
    """使用阿里云百炼生成图片"""
    api_key = get_api_key("bailian")
    if not api_key:
        return None, "错误: 未配置 DASHSCOPE_API_KEY"
    
    # 分辨率映射
    size_map = {
        "1K": "1024*1024",
        "2K": "1440*1440",
        "4K": "2048*2048"
    }
    size = size_map.get(resolution, "1024*1024")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"
    }
    
    payload = {
        "model": "wanx-v1",
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "size": size,
            "n": 1
        }
    }
    
    try:
        response = requests.post(BAILIAN_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            # 异步任务，需要轮询
            task_id = result.get("output", {}).get("task_id")
            if task_id:
                return poll_bailian_task(task_id, api_key)
            return None, "错误: 未获取到任务ID"
        else:
            return None, f"API错误: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"请求失败: {str(e)}"

def poll_bailian_task(task_id, api_key, max_wait=120):
    """轮询百炼异步任务"""
    import time
    
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    for _ in range(max_wait // 3):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                result = resp.json()
                status = result.get("output", {}).get("task_status")
                
                if status == "SUCCEEDED":
                    # 获取图片URL
                    results = result.get("output", {}).get("results", [])
                    if results:
                        img_url = results[0].get("url")
                        if img_url:
                            img_resp = requests.get(img_url, timeout=60)
                            if img_resp.status_code == 200:
                                return img_resp.content, None
                    return None, "错误: 未获取到图片URL"
                elif status == "FAILED":
                    return None, f"任务失败: {result}"
                elif status in ["PENDING", "RUNNING"]:
                    time.sleep(3)
                    continue
        except Exception as e:
            time.sleep(3)
            continue
    
    return None, "错误: 任务超时"

def generate_minimax(prompt, resolution="1K"):
    """使用 MiniMax 生成图片"""
    api_key = get_api_key("minimax")
    if not api_key:
        return None, "错误: 未配置 MINIMAX_API_KEY"
    
    # 分辨率映射
    size_map = {
        "1K": "1024x1024",
        "2K": "1536x1536",
        "4K": "2048x2048"
    }
    size = size_map.get(resolution, "1024x1024")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "size": size,
        "n": 1
    }
    
    try:
        response = requests.post(MINIMAX_API_URL, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            # MiniMax 返回 base64 或 URL
            data = result.get("data", [])
            if data:
                img_data = data[0]
                # 检查是 base64 还是 URL
                if "b64_json" in img_data:
                    return base64.b64decode(img_data["b64_json"]), None
                elif "url" in img_data:
                    img_resp = requests.get(img_data["url"], timeout=60)
                    if img_resp.status_code == 200:
                        return img_resp.content, None
            return None, "错误: 未获取到图片数据"
        else:
            return None, f"API错误: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"请求失败: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="通用图片生成脚本")
    parser.add_argument("--prompt", required=True, help="图片描述")
    parser.add_argument("--filename", required=True, help="输出文件名")
    parser.add_argument("--provider", default="bailian", choices=["bailian", "minimax"], help="API提供商")
    parser.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"], help="分辨率")
    parser.add_argument("--output-dir", default=".", help="输出目录")
    
    args = parser.parse_args()
    
    print(f"🦞 正在生成图片...")
    print(f"   提供商: {args.provider}")
    print(f"   描述: {args.prompt}")
    print(f"   分辨率: {args.resolution}")
    
    # 生成图片
    if args.provider == "bailian":
        img_data, error = generate_bailian(args.prompt, args.resolution)
    else:
        img_data, error = generate_minimax(args.prompt, args.resolution)
    
    if error:
        print(f"❌ {error}")
        sys.exit(1)
    
    # 保存图片
    output_path = Path(args.output_dir) / args.filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(img_data)
    
    print(f"✅ 图片已保存: {output_path.absolute()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())