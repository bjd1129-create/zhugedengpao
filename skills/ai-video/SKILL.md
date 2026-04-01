# AI视频制作技能

> **技能获取时间:** 2026-03-18 19:56
> **技能来源:** 老庄指示
> **适用场景:** AI视频生成、内容创作、多媒体制作

---

## 技能描述

通过Evolink API调用多个AI视频生成模型，支持文生视频、图生视频、首尾帧视频、自动配音等功能。

---

## 安装方式

```bash
# 安装Evolink视频技能
npx clawhub@latest install evolink-video

# 查看详细文档
clawhub docs evolink-video
```

---

## 支持的模型（37个）

### 主流模型

| 模型 | 提供商 | 特点 |
|------|--------|------|
| **Sora** | OpenAI | 高质量、长视频 |
| **Kling** | 快手 | 高质量、中文优化 |
| **Veo 3** | Google | 专业级、细节丰富 |
| **Seedance** | 字节跳动 | 舞蹈、动作流畅 |
| **Hailuo** | 海螺 | 快速生成 |
| **WAN** | 阿里 | 商业级 |
| **Grok** | xAI | 创意风格 |

---

## 核心功能

### 1. 文生视频（text-to-video）

```bash
# 文字描述生成视频
evolink generate --prompt "一只可爱的小猫在草地上奔跑" --model kling --duration 5
```

**参数：**
| 参数 | 说明 |
|------|------|
| `--prompt` | 视频描述文本 |
| `--model` | 使用的模型 |
| `--duration` | 视频时长（秒） |
| `--resolution` | 分辨率（720p/1080p/4K） |

---

### 2. 图生视频（image-to-video）

```bash
# 图片生成视频
evolink generate --image input.jpg --prompt "让图片中的人物开始跳舞" --model seedance
```

**参数：**
| 参数 | 说明 |
|------|------|
| `--image` | 输入图片路径 |
| `--prompt` | 动作描述 |
| `--model` | 使用的模型 |

---

### 3. 首尾帧视频

```bash
# 首尾帧生成中间过渡视频
evolink generate --first-frame start.jpg --last-frame end.jpg --duration 3
```

**用途：**
- 创意转场
- 平滑过渡
- 动画制作

---

### 4. 自动配音

```bash
# 视频自动配音
evolink voiceover --video output.mp4 --text "这是视频配音文本" --voice "zh-CN-female"
```

**支持的声音：**
| 语言 | 声音选项 |
|------|----------|
| 中文 | male, female, child |
| 英文 | male, female |
| 日文 | male, female |

---

## API配置

### 获取API Key

1. 访问 https://evolink.ai
2. 注册账号
3. 获取API Key

### 配置环境变量

```bash
# 设置环境变量
export EVOLINK_API_KEY="your-api-key-here"

# 或添加到配置文件
echo 'EVOLINK_API_KEY="your-api-key-here"' >> ~/.env
```

---

## 使用场景

### 场景一：社交媒体视频

```bash
# 生成短视频
evolink generate \
  --prompt "一只金毛犬在海边奔跑，阳光明媚" \
  --model kling \
  --duration 10 \
  --resolution 1080p \
  --output social_video.mp4
```

### 场景二：产品演示视频

```bash
# 图生视频：产品展示
evolink generate \
  --image product.png \
  --prompt "产品360度旋转展示" \
  --model veo3 \
  --output product_demo.mp4
```

### 场景三：创意转场

```bash
# 首尾帧转场
evolink generate \
  --first-frame scene1.jpg \
  --last-frame scene2.jpg \
  --duration 2 \
  --output transition.mp4
```

### 场景四：配音视频

```bash
# 添加配音
evolink voiceover \
  --video my_video.mp4 \
  --text "欢迎观看本期视频，今天我们将介绍..." \
  --voice zh-CN-female \
  --output final_video.mp4
```

---

## 模型选择指南

| 需求 | 推荐模型 | 说明 |
|------|----------|------|
| **高质量长视频** | Sora | 最佳画质 |
| **中文内容** | Kling | 中文优化 |
| **专业制作** | Veo 3 | 细节丰富 |
| **舞蹈动作** | Seedance | 动作流畅 |
| **快速生成** | Hailuo | 速度快 |
| **创意风格** | Grok | 独特风格 |

---

## 视频规格

| 规格 | 说明 |
|------|------|
| **分辨率** | 720p / 1080p / 4K |
| **时长** | 3-60秒 |
| **帧率** | 24 / 30 / 60 fps |
| **格式** | MP4 / MOV |

---

## 费用说明

| 模型 | 价格 | 说明 |
|------|------|------|
| Kling | $0.05/秒 | 性价比高 |
| Sora | $0.20/秒 | 高质量 |
| Veo 3 | $0.15/秒 | 专业级 |

---

## 注意事项

| 注意项 | 说明 |
|--------|------|
| **API Key安全** | 不要泄露API Key |
| **内容审核** | 部分内容可能被拒绝 |
| **生成时间** | 高质量视频需要等待 |
| **版权问题** | 注意使用权限 |

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| SEO写作 | 视频脚本创作 |
| PDF生成 | 视频方案文档 |
| 飞书文档 | 视频项目文档 |
| Twitter运营 | 发布视频内容 |

---

## 详细文档

https://github.com/openclaw/skills/tree/main/skills/evolinkai/evolink-video/SKILL.md

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，记录技能获取 |

---

*技能创建: 2026-03-18 19:56*
*技能来源: 老庄指示*
*维护者: 姜小牙*