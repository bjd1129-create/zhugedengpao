# 老庄与小花 - 设计资产索引
**版本：** v1.0
**更新时间：** 2026-03-31 10:00
**负责人：** 配色师

---

## 一、品牌吉祥物（Garfield Lobster）

仓库路径：`/Users/bjd/Desktop/ZhugeDengpao-Team/images/`

### 1.1 统计
| 类型 | 数量 | 说明 |
|------|------|------|
| garfield_lobster_*.png | **43张** | 龙虾加菲猫系列（实际清点） |
| mascot-hero-001.png | 1张 | 首张自主生成，用于首页Hero |
| lobster.svg | 1张 | 龙虾图标矢量 |
| zhuge-bulbo.png | 1张 | - |

**注意：** 之前报告误写为"13张"，实际为43张，已更正。

### 1.2 场景分类

| 场景代码 | 场景名 | 文件名模式 | 数量 |
|---------|--------|-----------|------|
| 01 | office（办公室） | garfield_lobster_00X_01_office_vX.png | ~10张 |
| 02 | coding（编码中） | garfield_lobster_01X_02_coding_vX.png | ~10张 |
| 03 | meeting（会议中） | garfield_lobster_02X_03_meeting_vX.png | ~10张 |
| 04 | studying（学习中） | garfield_lobster_03X_04_studying_vX.png | ~10张 |

### 1.3 核心资产（推荐使用）

| 优先级 | 文件名 | 用途 | 适用场景 |
|--------|--------|------|----------|
| ★★★★★ | mascot-hero-001.png | Hero大图 | 首页主视觉 |
| ★★★★☆ | garfield_lobster_001_01_office_v1.png | 办公室开场 | 办公室页面 |
| ★★★★☆ | garfield_lobster_021_02_coding_v9.png | 编码画面 | 工作场景 |
| ★★★★☆ | garfield_lobster_033_03_meeting_v9.png | 会议场景 | 团队介绍 |

---

## 二、品牌头像

| 文件名 | 用途 | 备注 |
|--------|------|------|
| xiaohua_new.jpg | 小花头像 | 官网使用 |
| xiaohua_test.jpg | 测试用 | 勿用于正式场景 |
| xiaohua_minimax.jpg | AI生成版 | 备用 |
| xiaohua.jpg | 早期版本 | 备用 |
| xiaohua_banner.jpg | Banner版 | 横幅使用 |

---

## 二.2 小花新形象（脑洞精灵）

**版本：** v2.0 | **日期：** 2026-03-31 | **相似度：** <50%（已达标）

### 主形象
| 文件名 | 用途 | 备注 |
|--------|------|------|
| xiaohua-comic-char.png | 漫画主角/官网各页面 | ✅ 核心资产，优先使用 |

### 漫画草稿（第一话《如果我有工资》）
| 文件名 | 用途 | 状态 |
|--------|------|------|
| comic-ep1-p1.png | 四格第1格 | ✅ 草稿完成 |
| comic-ep1-p2.png | 四格第2格 | ✅ 草稿完成 |
| comic-ep1-p3.png | 四格第3格 | ✅ 草稿完成 |
| comic-ep1-p4.png | 四格第4格 | ✅ 草稿完成 |

### 漫画草稿（第五话衍生）
| 文件名 | 用途 | 状态 |
|--------|------|------|
| comic5-ep1-p1.png | 五格第1格 | ✅ 草稿完成 |
| comic5-ep1-p2.png | 五格第2格 | ✅ 草稿完成 |
| comic5-ep1-p3.png | 五格第3格 | ✅ 草稿完成 |
| comic5-ep1-p4.png | 五格第4格 | ✅ 草稿完成 |
| comic5-ep1-p5.png | 五格第5格 | ✅ 草稿完成 |

### 其他生成图片
| 文件名 | 用途 | 备注 |
|--------|------|------|
| mascot-greeting.png | 招呼图 | v13承诺已兑现 |
| hero-homepage.png | 首页Hero大图 | 自主生成 |
| banner-opengraph.png | 社交分享图 | 自主生成 |

---

## 三、日记封面系列

仓库路径：`/Users/bjd/Desktop/ZhugeDengpao-Team/images/diary-covers/`

| 文件名 | 天数 | 用途 |
|--------|------|------|
| diary-cover-01-day-0.png | Day 0 | 起点 |
| diary-cover-02-day-1.png | Day 1 |  |
| ... | ... | 持续到Day 23 |
| diary-cover-23-day-23.png | Day 23 | 最新 |

共23张封面图，覆盖项目全周期。

---

## 四、设计规范文件

| 文件名 | 用途 |
|--------|------|
| color-palette-2026-03-30.css | 品牌配色CSS变量 |
| mascot-enhancement.css | 吉祥物增强样式 |

---

## 五、图片使用指南

### 5.1 首页Hero区
- **推荐：** mascot-hero-001.png
- **备选：** garfield_lobster_001_01_office_v1.png

### 5.2 内页吉祥物
- 浮动吉祥物：lobster.svg 或任意 garfield_lobster 系列
- 场景图：根据页面主题选择对应场景代码

### 5.3 图片命名规范
```
{主题}_{序号}_{场景}_{版本}.png
例：garfield_lobster_001_01_office_v1.png
```

---

**下次更新：** 官网实际使用脑洞精灵形象后同步截图到此索引

**更新记录：**
- v1.0（2026-03-31 10:00）：初版
- v1.1（2026-03-31 17:00）：补充脑洞精灵资产入库（xiaohua-comic-char.png、漫画草稿系列、其他生成图片）
