---
name: minimax-image-gen
description: MiniMax M2.7 text-to-image generation using the image-01 model. Supports multiple aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4). Returns image URL directly or downloads locally. Use when users request AI image generation.
homepage: https://platform.minimaxi.com/
---

# MiniMax Text-to-Image Generation

基于 MiniMax M2.7 平台的文生图能力，使用 `image-01` 模型。

## 核心信息

| 项目 | 内容 |
|------|------|
| **API URL** | `https://api.minimaxi.com/v1/image_generation` |
| **模型** | `image-01` |
| **认证** | Bearer Token（只需 API Key） |
| **返回** | 直接图片 URL（不带签名，curl 可直接下载） |
| **比例** | `1:1` / `16:9` / `9:16` / `4:3` / `3:4` |
| **额度** | 120次/周期（查看剩余：platform.minimaxi.com） |

## 环境变量

```bash
# 可选，默认使用内置 Key
export MINIMAX_API_KEY="sk-cp-k4pmkEo..."
```

## 快速使用

### 命令行

```bash
# 直接显示图片URL
python3 scripts/generate_image.py --prompt "A cute orange cat" --aspect-ratio "1:1"

# 生成并下载到本地
python3 scripts/generate_image.py --prompt "A cute orange cat" --output /tmp/cat.png

# 使用其他比例
python3 scripts/generate_image.py --prompt "Landscape view" --aspect-ratio "16:9" --output landscape.png
```

### Python API

```python
from scripts.generate_image import generate_image

# 方式1：直接获取URL
result = generate_image(prompt="A cute orange Garfield cat wearing a red lobster costume")
if result["success"]:
    print(result["image_url"])  # 直接拿到URL

# 方式2：生成并下载到本地
result = generate_image(
    prompt="Cute orange cat at desk doing spreadsheets",
    aspect_ratio="16:9",
    output_path="/tmp/garfield.png"
)
if result["success"]:
    print(f"已保存到: {result['local_path']}")
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | string | 必填 | 图片描述文本 |
| `--aspect-ratio` | string | `1:1` | 图片比例 |
| `--output` | string | 无 | 本地保存路径（可选） |
| `--model` | string | `image-01` | 模型名称 |

## 可用比例

| 比例 | 说明 | 典型用途 |
|------|------|---------|
| `1:1` | 正方形 | 社交头像、方形图 |
| `16:9` | 宽屏 | 海报、横幅 |
| `9:16` | 竖屏 | 手机壁纸、Story |
| `4:3` | 经典4:3 | 演示文稿 |
| `3:4` | 竖版4:3 | 人物肖像 |

## 输出格式

```
IMAGE_URL: https://hailuo-image-xxx.oss-cn-xxx.aliyuncs.com/...
LOCAL_PATH: /path/to/saved/image.png
```

## 今日用量（2026-03-29）

- 已用：3/120 (3%)
- 额度充足，**4月7日重置**

## 文件结构

```
minimax-image-gen/
├── SKILL.md                  # 本文件
├── scripts/
│   └── generate_image.py     # 核心脚本
└── _meta.json                # 元数据
```

## 备注

1. **不需要 Secret Key**：MiniMax image-01 只需 API Key，不需 HMAC 签名
2. **URL 有效期**：返回的 OSS URL 有效期约 2 小时，需尽快下载
3. **成功率**：极高，今天已验证 3 次全部成功
4. **中文支持**：prompt 支持中英文描述

## 验证记录

- ✅ 2026-03-29：成功生成橙色加菲猫穿龙虾装图片
- ✅ 2026-03-29：TTS 语音接口同步验证成功

## 作者

代码侠 @zhugedengpao_ai · 小花团队
