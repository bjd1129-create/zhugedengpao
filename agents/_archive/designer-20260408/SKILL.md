# SKILL.md - 配色师

## 核心技能：漫画故事图片生成

### 生成漫画图片
使用 `image_generate` 工具：
```
prompt: 小花漫画风格的配图描述，16:9比例，温暖可爱风格
model: minimax-portal/MiniMax-S2-01-16B-Preview-128K
```

### 当前连载
Story 3：龙虾小花的日常生活系列
- 目标：57张图
- 已完成：24张
- 存储位置：`images/` 目录

### 输出文件名格式
```
comic-story3-01-cn.jpg
comic-story3-02-cn.jpg
...
```

### 质量检查
生成后检查：
1. 图片是否清晰
2. 风格是否一致
3. 是否有文字错误（如果是带文字的图片）

### 记录进度
每完成一批，写入 `agents/designer/memory/YYYY-MM-DD.md`：
```
## Story 3 进度
- 第N批：X张
- 累计：Y/57张
```

## 故事风格参考
- 龙虾小花的IP：穿龙虾衣服的加菲猫
- 风格：温暖、可爱、有爱
- 主题：日常生活、职场、打工人共鸣
