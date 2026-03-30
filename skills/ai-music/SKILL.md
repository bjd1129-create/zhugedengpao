# AI音乐生成技能

> **技能获取时间:** 2026-03-18 19:57
> **技能来源:** 老庄指示
> **适用场景:** AI音乐创作、背景音乐制作、音频内容生成

---

## 技能描述

通过AI生成高质量音乐，支持指定风格、节奏、乐器、情绪等参数，自动生成音频文件并进行质量验证。

---

## 安装方式

```bash
# 安装音乐生成技能
npx clawhub@latest install music-generator

# 查看详细文档
clawhub docs music-generator
```

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    AI音乐生成流程                            │
└─────────────────────────────────────────────────────────────┘

1. 创建Composition Plan
   ├── 风格选择
   ├── 节奏设置
   ├── 乐器配置
   └── 情绪定义

2. AI生成音频
   ├── 根据计划生成
   └── 高质量音频输出

3. 质量验证
   ├── 自动检测质量
   ├── 失败自动重试
   └── 输出最终文件
```

---

## Composition Plan（作曲计划）

### JSON格式模板

```json
{
  "name": "轻松愉快的背景音乐",
  "style": "pop",
  "bpm": 120,
  "duration": 60,
  "instruments": ["piano", "guitar", "drums"],
  "mood": "happy",
  "key": "C",
  "time_signature": "4/4",
  "tempo": "moderate",
  "intensity": "medium"
}
```

### 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `style` | 音乐风格 | pop, rock, jazz, classical, electronic, hip-hop, ambient |
| `bpm` | 节拍速度 | 60-200 |
| `duration` | 时长（秒） | 10-300 |
| `instruments` | 乐器列表 | piano, guitar, drums, violin, synth, bass |
| `mood` | 情绪 | happy, sad, calm, energetic, dramatic, romantic |
| `key` | 调式 | C, D, E, F, G, A, B |
| `tempo` | 速度 | slow, moderate, fast |
| `intensity` | 强度 | low, medium, high |

---

## 使用场景

### 场景一：背景音乐生成

```json
{
  "name": "产品展示背景音乐",
  "style": "ambient",
  "bpm": 80,
  "duration": 120,
  "instruments": ["piano", "synth"],
  "mood": "calm",
  "key": "C",
  "intensity": "low"
}
```

### 场景二：视频配乐

```json
{
  "name": "短视频配乐",
  "style": "pop",
  "bpm": 128,
  "duration": 30,
  "instruments": ["guitar", "drums", "synth"],
  "mood": "energetic",
  "key": "G",
  "intensity": "high"
}
```

### 场景三：冥想音乐

```json
{
  "name": "冥想放松音乐",
  "style": "ambient",
  "bpm": 60,
  "duration": 300,
  "instruments": ["piano"],
  "mood": "calm",
  "key": "D",
  "intensity": "low"
}
```

---

## 音乐风格指南

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| **pop** | 流行、易接受 | 社交媒体、广告 |
| **rock** | 激烈、有力量 | 运动视频、宣传片 |
| **jazz** | 优雅、放松 | 高端场合、咖啡厅 |
| **classical** | 正式、庄重 | 纪录片、教育 |
| **electronic** | 现代、科技感 | 科技产品、游戏 |
| **hip-hop** | 节奏感强 | 运动、街舞 |
| **ambient** | 氛围、舒缓 | 冥想、背景音乐 |

---

## 情绪映射

| 情绪 | BPM建议 | 乐器建议 |
|------|---------|----------|
| **happy** | 120-140 | guitar, drums, synth |
| **sad** | 60-80 | piano, violin |
| **calm** | 60-90 | piano, synth |
| **energetic** | 130-160 | drums, synth, bass |
| **dramatic** | 80-110 | orchestra, piano |
| **romantic** | 70-100 | piano, violin, guitar |

---

## 质量验证机制

### 自动验证

```bash
# 生成后自动验证
music-generator generate --plan plan.json --verify

# 验证失败自动重试
music-generator generate --plan plan.json --retry 3
```

### 验证标准

| 指标 | 标准 |
|------|------|
| 音频质量 | 320kbps |
| 格式 | MP3 / WAV |
| 降噪 | 自动降噪 |
| 平衡 | 左右声道平衡 |

---

## 输出格式

| 格式 | 说明 |
|------|------|
| **MP3** | 标准格式，兼容性好 |
| **WAV** | 无损格式，专业制作 |
| **FLAC** | 无损压缩，高保真 |

---

## 注意事项

| 注意项 | 说明 |
|--------|------|
| **版权** | 生成的音乐可用于商业用途 |
| **时长限制** | 建议30-300秒 |
| **质量验证** | 失败自动重试，最多3次 |
| **存储空间** | 音频文件较大，注意存储 |

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| AI视频制作 | 视频配乐 |
| SEO写作 | 音乐描述文案 |
| 飞书文档 | 音乐项目文档 |
| Twitter运营 | 发布音乐作品 |

---

## 详细文档

https://github.com/openclaw/skills/tree/main/skills/wells1137/music-generator/SKILL.md

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，记录技能获取 |

---

*技能创建: 2026-03-18 19:57*
*技能来源: 老庄指示*
*维护者: 姜小牙*