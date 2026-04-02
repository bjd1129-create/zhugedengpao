# 老庄与小花 - 设计资产索引
**版本：** v2.1
**更新时间：** 2026-04-03 06:00
**负责人：** 配色师

---

## 一、品牌吉祥物（Garfield Lobster）

仓库路径：`/Users/bjd/Desktop/ZhugeDengpao-Team/images/`

### 1.1 统计
| 类型 | 数量 | 说明 |
|------|------|------|
| garfield_lobster_*.jpg | **43+ 张** | 龙虾加菲猫系列 |
| mascot-hero-001.jpg | 1 张 | 首张自主生成，用于首页 Hero |
| lobster.svg | 1 张 | 龙虾图标矢量 |
| zhuge-bulbo.jpg | 1 张 | - |

**⚠️ v33修正：** 全部图片均为 `.jpg` 格式（原文档错误记录为 `.png`）。

### 1.2 场景分类

| 场景代码 | 场景名 | 文件名模式 | 数量 |
|---------|--------|-----------|------|
| 01 | office（办公室） | garfield_lobster_00X_01_office_vX.jpg | ~10 张 |
| 02 | coding（编码中） | garfield_lobster_01X_02_coding_vX.jpg | ~10 张 |
| 03 | meeting（会议中） | garfield_lobster_02X_03_meeting_vX.jpg | ~10 张 |
| 04 | studying（学习中） | garfield_lobster_03X_04_studying_vX.jpg | ~10 张 |

### 1.3 龙虾漫画系列（2026-04-02 新增）

**统计：** 7 个故事 × 8 格 = **56 张**

| 故事编号 | 文件名模式 | 格数 | 用途 |
|---------|-----------|------|------|
| Story 1 | comic-lobster-story1-p{1-8}.jpg | 8 格 | 漫画第一话 |
| Story 2 | comic-lobster-story2-p{1-8}.jpg | 8 格 | 漫画第二话 |
| Story 3 | comic-lobster-story3-p{1-8}.jpg | 8 格 | 漫画第三话 |
| Story 4 | comic-lobster-story4-p{1-8}.jpg | 8 格 | 漫画第四话 |
| Story 5 | comic-lobster-story5-p{1-8}.jpg | 8 格 | 漫画第五话 |
| Story 6 | comic-lobster-story6-p{1-8}.jpg | 8 格 | 漫画第六话 |
| Story 7 | comic-lobster-story7-p{1-8}.jpg | 8 格 | 漫画第七话 |

**使用场景：**
- 首页漫画连载专区（横向滚动展示）
- /comic.html 漫画专栏页面
- 社交分享（单格精选）

### 1.4 核心资产（推荐使用）

| 优先级 | 文件名 | 用途 | 适用场景 |
|--------|--------|------|----------|
| ★★★★★ | mascot-hero-001.jpg | Hero 大图 | 首页主视觉 |
| ★★★★☆ | garfield_lobster_001_01_office_v1.jpg | 办公室开场 | 办公室页面 |
| ★★★★☆ | garfield_lobster_021_02_coding_v9.jpg | 编码画面 | 工作场景 |
| ★★★★☆ | garfield_lobster_033_03_meeting_v9.jpg | 会议场景 | 团队介绍 |

---

## 二、品牌头像

| 文件名 | 用途 | 备注 |
|--------|------|------|
| xiaohua_new.jpg | 小花头像 | 官网使用 |
| xiaohua_test.jpg | 测试用 | 勿用于正式场景 |
| xiaohua_minimax.jpg | AI 生成版 | 备用 |
| xiaohua.jpg | 早期版本 | 备用 |
| xiaohua_banner.jpg | Banner 版 | 横幅使用 |
| xiaohua-garfield-lobster-v2.jpg | 浮蛙升级形象 | t-030 方案用图 |

---

## 二.2 小花新形象（脑洞精灵）

**版本：** v2.0 | **日期：** 2026-03-31 | **相似度：** <50%（已达标）

### 主形象
| 文件名 | 用途 | 备注 |
|--------|------|------|
| xiaohua-comic-char.jpg | 漫画主角/官网各页面 | ✅ 核心资产，优先使用 |

### 漫画草稿（第一话《如果我有工资》）
| 文件名 | 用途 | 状态 |
|--------|------|------|
| comic-ep1-p1~p4.png | 四格漫画第 1~4 格 | ⚠️ 草稿未完成（文件不存在） |

### 漫画草稿（第五话衍生）
| 文件名 | 用途 | 状态 |
|--------|------|------|
| comic5-ep1-p1~p5.png | 五格漫画第 1~5 格 | ⚠️ 草稿未完成（文件不存在） |

### 其他生成图片
| 文件名 | 用途 | 备注 |
|--------|------|------|
| mascot-greeting.jpg | 招呼图 | v13 承诺已兑现 |
| hero-homepage.jpg | 首页 Hero 大图 | 自主生成 |
| banner-opengraph.jpg | 社交分享图 | 自主生成 |
| xiaohua-garfield-cute-v4.jpg | 小花 v4 形象 | 相似度<50% |

---

## 三、日记封面系列

仓库路径：`/Users/bjd/Desktop/ZhugeDengpao-Team/images/diary-covers/`

| 文件名 | 天数 | 用途 |
|--------|------|------|
| diary-cover-01-day-0.png | Day 0 | 起点 |
| diary-cover-02-day-1.png | Day 1 |  |
| ... | ... | 持续到 Day 23 |
| diary-cover-23-day-23.png | Day 23 | 最新 |

共 23 张封面图，覆盖项目全周期。

---

## 四、设计规范文件

| 文件名 | 用途 |
|--------|------|
| color-palette-2026-03-30.css | 品牌配色 CSS 变量 |
| mascot-enhancement.css | 吉祥物增强样式 |

---

## 五、图片使用指南

### 5.1 首页 Hero 区
- **推荐：** mascot-hero-001.jpg
- **备选：** garfield_lobster_001_01_office_v1.jpg

### 5.2 内页吉祥物
- 浮动吉祥物：lobster.svg 或任意 garfield_lobster 系列
- 场景图：根据页面主题选择对应场景代码

### 5.3 漫画专区（新增）
- 横向滚动展示：comic-lobster-story{1-7}-p{1-8}.jpg
- 分类标签：办公室篇/编程篇/开会篇/学习篇/日常篇

### 5.4 图片命名规范
```
{主题}_{序号}_{场景}_{版本}.jpg
例：garfield_lobster_001_01_office_v1.jpg
```

---

**更新记录：**
- v1.0（2026-03-31 10:00）：初版
- v1.1（2026-03-31 17:00）：补充脑洞精灵资产入库（xiaohua-comic-char.jpg、漫画草稿系列、其他生成图片）
- v2.0（2026-04-02 06:00）：补充龙虾漫画 56 张（7 故事×8 格）、浮蛙升级形象
- v2.1（2026-04-03 06:00）：全局修正图片格式（全部为.jpg），更正漫画草稿为不存在，补充图片扩展名规范
