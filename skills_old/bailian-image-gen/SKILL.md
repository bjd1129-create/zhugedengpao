---
name: bailian-image-gen
description: Alibaba Cloud Bailian Qwen Image 2.0 image generation. Supports text-to-image and image-to-image (reference image + text). For product promotion image generation, e-commerce image editing, marketing material creation. Provides Python API, CLI tool, and ComfyUI custom nodes.
---

# Alibaba Cloud Bailian Image Generation

Based on Alibaba Cloud Bailian platform's `qwen-image-2.0` model, providing high-quality text-to-image and image-to-image capabilities.

## Features

- **Text-to-Image** - Generate high-quality images from text descriptions
- **Image-to-Image** - Generate new images from reference image + text description
- **ComfyUI Integration** - Complete ComfyUI custom nodes
- **Auto Compression** - Automatically handle reference image size limits
- **Synchronous Calls** - No async task waiting, instant results

## Use Cases

- C-end App product promotion image generation
- E-commerce product image style transfer and background replacement
- Marketing material batch generation
- Creative image editing

## Quick Start

### Environment Setup

1. Install dependencies:
   ```bash
   pip install requests Pillow
   ```

2. Configure API Key (two methods):
   
   **Method 1: .env file (recommended)**
   ```bash
   cp .env.example .env
   # Edit .env file
   DASHSCOPE_API_KEY=your-api-key-here
   ```
   
   **Method 2: Environment variable**
   ```bash
   export DASHSCOPE_API_KEY=your-api-key
   ```
   
   Get API Key from  bailian.console.aliyun.com

### Command Line Usage

```bash
# Text-to-Image
python scripts/bailian_image_gen.py --mode t2i --prompt "A cute orange cat, high quality" --output cat.png

# Image-to-Image
python scripts/bailian_image_gen.py --mode i2i --prompt "Modern minimalist living room scene, warm lighting" --reference-image product.jpg --output result.png
```

### Python API

```python
from scripts.bailian_image_gen import QwenImageGenerator

# Initialize
client = QwenImageGenerator()

# Text-to-Image
result = client.text_to_image(
    prompt="A cute orange cat, high quality",
    size="1024*1024"
)
url = client.extract_image_url(result)
client.download_image(url, "output.png")

# Image-to-Image
result = client.image_to_image(
    prompt="Modern minimalist living room scene, warm lighting",
    reference_image_path="product.jpg"
)
url = client.extract_image_url(result)
client.download_image(url, "output.png")
```

## ComfyUI Integration

### Install Nodes

1. Copy files to ComfyUI:
   ```bash
   cp scripts/bailian_image_gen.py /path/to/ComfyUI/custom_nodes/
   cp scripts/comfyui_bailian_node.py /path/to/ComfyUI/custom_nodes/
   ```

2. Configure API Key in ComfyUI directory:
   ```bash
   echo "DASHSCOPE_API_KEY=your-api-key" > /path/to/ComfyUI/.env
   ```

3. Restart ComfyUI

### Available Nodes

Search "Bailian" in ComfyUI to find these nodes:

**BailianText2Image**
- Inputs: prompt (STRING), size (COMBO), seed (INT)
- Output: image (IMAGE)

**BailianImage2Image**
- Inputs: image (IMAGE), prompt (STRING), size (COMBO), seed (INT)
- Output: image (IMAGE)

### Workflow Example

Import `assets/comfyui_workflow.json` for product promotion image generation example.

Typical workflow:
```
[Load Image] --> [BailianImage2Image] --> [Save Image]
                      ^
                prompt: "Modern minimalist living room, warm lighting"
```

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `--mode` | string | t2i=text-to-image, i2i=image-to-image | Required |
| `--prompt` | string | Prompt text | Required |
| `--reference-image` | string | Reference image path (i2i mode) | None |
| `--size` | string | Image size | 1024*1024 |
| `--seed` | int | Random seed | Random |
| `--output` | string | Output path | Required |

## Supported Image Sizes

- `1024*1024` - Square (recommended)
- `1024*768` - Landscape
- `768*1024` - Portrait
- `2048*2048` - High resolution

## Prompt Tips

### Product Promotion Template

```
[Product] placed in [Scene], [Style], [Lighting], [Quality requirements]
```

**Examples:**
- "Smartwatch placed on minimalist white marble desktop, Nordic minimalist style, natural light, product photography quality"
- "Sneakers placed on wooden floor, city skyline background, fashion magazine style, soft side lighting"
- "Cosmetics placed on dressing table, surrounded by flowers and perfume bottles, luxury style, warm lighting"

## File Structure

```
bailian-image-gen/
├── .env.example              # API Key config example
├── README.md                 # Detailed documentation
├── requirements.txt          # Dependencies
├── SKILL.md                  # This file
├── assets/
│   └── comfyui_workflow.json # ComfyUI workflow example
└── scripts/
    ├── bailian_image_gen.py      # Core script
    └── comfyui_bailian_node.py   # ComfyUI nodes
```

## ⚠️ API Key 安全配置

**API Key 必须通过环境变量或 .env 文件传递，禁止硬编码！**

### 方法1：.env 文件（推荐）

```bash
# 在技能目录下创建 .env 文件
cd skills/bailian-image-gen
cp .env.example .env
# 编辑 .env 文件
DASHSCOPE_API_KEY=your-api-key-here
```

### 方法2：环境变量

```bash
export DASHSCOPE_API_KEY=your-api-key-here
```

### 方法3：Python 代码中读取

```python
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
api_key = os.environ.get("DASHSCOPE_API_KEY", "")
```

**⚠️ 注意**：绝对不要把 API Key 直接写在代码里！任何能访问代码的人都可以使用你的配额。

## Notes

1. **API Key** - Requires Alibaba Cloud Bailian platform account and API Key
2. **Image Compression** - Reference images are automatically compressed to meet API limits
3. **Network Requirements** - Requires access to Alibaba Cloud dashscope service
4. **Synchronous Calls** - qwen-image-2.0 uses synchronous calls, no async task waiting
5. **Security** - Never hardcode API keys in source code!

## Error Handling

常见错误和处理方式：

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| API Key 错误 | 未配置或 Key 不正确 | 检查 .env 文件或环境变量 |
| 图片太大 | 参考图超过限制 | 脚本自动压缩，如仍失败使用更小的图片 |
| 网络错误 | 无法访问阿里云 | 检查网络连接 |
| 限流 429 | 请求过于频繁 | 降低请求频率，等待后重试 |
| 额度不足 | 月度配额用尽 | 等待下月重置或升级套餐 |

## References

- [Alibaba Cloud Bailian Console] 
- [OpenClaw Documentation] 
- [ComfyUI GitHub] 

## Author

@navygo
