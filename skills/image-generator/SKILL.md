---
name: image-generator
description: 通用图片生成技能，支持阿里云百炼(通义万象)和MiniMax。使用方法：python skills/image-generator/generate_image.py --prompt "描述" --filename "output.png" [--provider bailian|minimax] [--resolution 1K|2K|4K]
---

# 通用图片生成技能

支持阿里云百炼（通义万象）和 MiniMax 的图片生成工具。

## 用法

```bash
python /Users/bjd/Desktop/ZhugeDengpao-Team/skills/image-generator/generate_image.py \
  --prompt "你的图片描述" \
  --filename "output.png" \
  [--provider bailian|minimax] \
  [--resolution 1K|2K|4K]
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| --prompt | ✅ | 图片描述（中英文均可） |
| --filename | ✅ | 输出文件名 |
| --provider | ❌ | API提供商：bailian（默认）或 minimax |
| --resolution | ❌ | 分辨率：1K（默认）/ 2K / 4K |
| --output-dir | ❌ | 输出目录（默认当前目录） |

## 示例

```bash
# 使用百炼生成（默认）
python skills/image-generator/generate_image.py \
  --prompt "一只穿龙虾衣服的加菲猫，治愈风格，宫崎骏画风" \
  --filename "xiaohua.png" \
  --resolution 2K

# 使用MiniMax生成
python skills/image-generator/generate_image.py \
  --prompt "产品展示图，极简白色背景" \
  --filename "product.png" \
  --provider minimax \
  --resolution 2K
```

## API Key 配置

在 `.env` 文件中配置：

```
DASHSCOPE_API_KEY=sk-xxx      # 阿里云百炼
MINIMAX_API_KEY=sk-xxx        # MiniMax
```

## 分辨率说明

| 分辨率 | 百炼尺寸 | MiniMax尺寸 | 适用场景 |
|--------|---------|-------------|---------|
| 1K | 1024x1024 | 1024x1024 | 快速预览 |
| 2K | 1440x1440 | 1536x1536 | 正式使用 |
| 4K | 2048x2048 | 2048x2048 | 高清输出 |

## 注意事项

1. 百炼使用异步任务，生成时间约30-60秒
2. MiniMax 直接返回结果，速度更快
3. 百炼已配置API Key，可直接使用
4. MiniMax 需要额外配置 API Key