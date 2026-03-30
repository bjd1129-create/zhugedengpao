# AdClaw广告素材搜索技能

> **技能获取时间:** 2026-03-18 20:07
> **技能来源:** 老庄发送
> **提供者:** 妙智声科技
> **用途:** 竞品广告创意素材搜索

---

## 技能描述

广告素材搜索助手，帮助用户通过AdClaw搜索竞品广告创意素材，支持关键词、素材类型、地区、时间等多维度筛选。

---

## 触发关键词

```
"找素材"、"搜广告"、"广告视频"、"创意素材"
"竞品广告"、"ad creative"、"search ads"
```

---

## API配置

### 获取API Key

1. 访问 https://admapix.miaozhisheng.tech 注册
2. 获取API Key
3. 配置环境变量

```bash
openclaw config set skills.entries.adclaw.apiKey "你的API_KEY"
```

---

## API调用

### 端点

```
POST https://ad.h5.miaozhisheng.tech/api/data/search
```

### 请求示例

```bash
curl -s -X POST "https://ad.h5.miaozhisheng.tech/api/data/search" \
  -H "X-API-Key: $ADCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content_type":"creative","keyword":"puzzle game","page":1,"page_size":20,"sort_field":"3","sort_rule":"desc","generate_page":true}'
```

---

## 请求参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| keyword | string | "" | 搜索关键词 |
| creative_team | string[] | 全部 | 素材类型代码 |
| country_ids | string[] | 全球 | 国家代码 |
| start_date | string | 30天前 | 开始日期 YYYY-MM-DD |
| end_date | string | 今天 | 结束日期 |
| sort_field | string | "3" | 排序字段 |
| sort_rule | string | "desc" | 排序方向 |
| page | int | 1 | 页码 |
| page_size | int | 20 | 每页数量（最大60） |
| content_type | string | "creative" | 固定值 |
| generate_page | bool | true | 生成H5结果页 |

---

## 参数映射

### 素材类型

| 用户说的 | 代码 |
|----------|------|
| 视频 | ["010"] |
| 图片 | ["020"] |
| 试玩 | ["030"] |

### 地区

| 用户说的 | 国家代码 |
|----------|----------|
| 东南亚 | TH, VN, ID, MY, PH, SG |
| 美国 | US |
| 日韩 | JP, KR |
| 欧洲 | GB, DE, FR, IT, ES |

### 排序

| 用户说的 | sort_field | sort_rule |
|----------|------------|-----------|
| 最新 | "3" | "desc" |
| 最热/曝光最多 | "15" | "desc" |
| 最相关 | "11" | "desc" |
| 投放最久 | "4" | "desc" |

---

## 交互流程

### Step 1: 解析参数

从自然语言提取参数

### Step 2: 参数确认

```
📋 搜索参数确认：
🔑 关键词: puzzle game
🎬 素材类型: 视频 (010)
🌏 投放地区: 东南亚
📅 时间范围: 最近30天
📊 排序: 首次发现时间 ↓
📄 每页: 20条
```

### Step 3: 询问缺失参数

如果没有关键词，引导用户提供

### Step 4: 检查API Key

检查 `$ADCLAW_API_KEY` 是否配置

### Step 5: 执行搜索

构建curl命令调用API

### Step 6: 发送结果

```
🎯 搜到 XXX 条「keyword」的广告素材
👉 https://ad.h5.miaozhisheng.tech{page_url}
```

### Step 7: 后续交互

- "下一页" - 翻页
- "只看视频" - 筛选
- "换个关键词" - 重新搜索

---

## 使用场景

### 场景一：搜索竞品广告

```
用户：帮我搜Temu的广告素材

AI：📋 搜索参数确认：
🔑 关键词: Temu
🎬 素材类型: 全部
🌏 投放地区: 全球
📅 时间范围: 最近30天

确认搜索？
```

### 场景二：筛选视频素材

```
用户：搜puzzle game的视频广告，只要东南亚

AI：📋 搜索参数确认：
🔑 关键词: puzzle game
🎬 素材类型: 视频 (010)
🌏 投放地区: 东南亚 → TH, VN, ID, MY, PH, SG
📅 时间范围: 最近30天

🎯 搜到 156 条「puzzle game」的广告素材
👉 https://ad.h5.miaozhisheng.tech/p/xxx
```

---

## 输出原则

1. **参数确认优先** - 搜索前必须确认
2. **使用Markdown链接** - `[文本](url)`
3. **曝光量人性化** - 超过1万显示"x.x万"
4. **使用中文输出**
5. **简洁直接** - 不寒暄，直接给数据
6. **保持上下文** - 翻页记住之前参数

---

## 与其他技能协作

| 技能 | 协作场景 |
|------|----------|
| 竞品研究 | 分析竞品广告策略 |
| SEO写作 | 广告文案分析 |
| Agent Browser | 自动化素材采集 |

---

## 文件位置

| 文件 | 路径 |
|------|------|
| 技能包 | `/Users/bjd/intelligence/adclaw/` |
| SKILL.md | `/Users/bjd/intelligence/adclaw/SKILL.md` |
| 参数映射 | `/Users/bjd/intelligence/adclaw/references/param-mappings.md` |

---

## 链接

- **官网:** https://admapix.miaozhisheng.tech
- **结果展示:** https://ad.h5.miaozhisheng.tech

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本，技能包导入 |

---

*技能创建: 2026-03-18 20:07*
*技能来源: 老庄发送*
*提供者: 妙智声科技*
*维护者: 姜小牙*