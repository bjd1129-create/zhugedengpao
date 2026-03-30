#!/usr/bin/env python3
"""
MiniMax Image Generation - Text-to-Image
Model: image-01
API: https://api.minimaxi.com/v1/image_generation
"""

import os
import sys
import json
import requests
import argparse
import shutil


# Default API configuration
DEFAULT_BASE_URL = "https://api.minimaxi.com"
DEFAULT_MODEL = "image-01"
DEFAULT_API_KEY = "sk-cp-k4pmkEoPQSNnBA0DeWEdXXFFiAaM-1F5kVLlaGawg1bYZTszcrOw7vY62ESuCsTq1FHRh1cnupzo2wGpHR1PAJSRonu776s0MhXu7Wsau8BbYwt3LS3Fh2o"


def load_api_key():
    """Load API key from environment or use default"""
    return os.environ.get("MINIMAX_API_KEY") or DEFAULT_API_KEY


def generate_image(prompt: str, api_key: str = None, base_url: str = DEFAULT_BASE_URL,
                   model: str = DEFAULT_MODEL, aspect_ratio: str = "1:1",
                   output_path: str = None) -> dict:
    """
    Generate image from text prompt using MiniMax API.

    Returns:
        dict with keys: success (bool), image_url (str), local_path (str), error (str)
    """
    api_key = api_key or load_api_key()
    url = f"{base_url}/v1/image_generation"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "url"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        if data.get("base_resp", {}).get("status_code") != 0:
            return {"success": False, "error": data.get("base_resp", {}).get("status_msg", "Unknown error")}

        image_urls = data.get("data", {}).get("image_urls", [])
        if not image_urls:
            return {"success": False, "error": "No image URL in response"}

        image_url = image_urls[0]
        result = {"success": True, "image_url": image_url, "local_path": None}

        # Download image if output path provided
        if output_path:
            try:
                # URL is unsigned, direct download works
                img_response = requests.get(image_url, timeout=60)
                img_response.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                result["local_path"] = output_path
                print(f"[OK] Image saved: {output_path}")
            except Exception as e:
                result["local_path"] = None
                result["download_error"] = str(e)

        return result

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {e}"}
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid JSON response"}


def main():
    parser = argparse.ArgumentParser(description="MiniMax Text-to-Image Generation")
    parser.add_argument("--prompt", "-p", required=True, help="Image prompt text")
    parser.add_argument("--api-key", help="MiniMax API Key (or set MINIMAX_API_KEY env)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name")
    parser.add_argument("--aspect-ratio", default="1:1",
                        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
                        help="Image aspect ratio")
    parser.add_argument("--output", "-o", help="Output file path (optional, returns URL if omitted)")

    args = parser.parse_args()

    result = generate_image(
        prompt=args.prompt,
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model,
        aspect_ratio=args.aspect_ratio,
        output_path=args.output
    )

    if result["success"]:
        print(f"IMAGE_URL: {result['image_url']}")
        if result.get("local_path"):
            print(f"LOCAL_PATH: {result['local_path']}")
        sys.exit(0)
    else:
        print(f"[ERROR] {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
