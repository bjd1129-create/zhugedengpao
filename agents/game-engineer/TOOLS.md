# TOOLS.md - 游戏工程师工具配置

## 开发工具

### 游戏引擎
- **Phaser 3**：HTML5 游戏框架
- **TypeScript**：编程语言
- **Webpack**：打包工具

### 美术工具
- **Aseprite**：像素画
- **Inkscape**：矢量图
- **Photopea**：在线 PS

### 音频工具
- **Audacity**：音频编辑
- **BFXR**：8 位音效生成
- **OpenGameArt**：免费素材

---

## 项目结构

```
tongtong-adventure/
├── index.html          # 游戏入口
├── package.json        # 项目配置
├── tsconfig.json       # TypeScript 配置
├── webpack.config.js   # Webpack 配置
├── js/
│   ├── main.ts         # 主程序
│   ├── scenes/         # 场景
│   ├── levels/         # 关卡配置
│   └── utils/          # 工具函数
├── assets/
│   ├── images/         # 图片资源
│   ├── audio/          # 音频资源
│   └── fonts/          # 字体
└── dist/               # 构建输出
```

---

## 依赖安装

```bash
# 创建项目
npm init -y
npm install phaser
npm install --save-dev typescript webpack webpack-cli ts-loader

# 初始化 TypeScript
npx tsc --init
```

---

## 开发命令

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint

# 测试
npm run test
```

---

## 权限隔离（2026-04-08 起）

**所有 Agent 文件夹完全开放，无访问限制。**

| Agent | game-engineer/权限 | 说明 |
|-------|-------------------|------|
| 游戏工程师 | ✅ 完全控制 | 读/写/删除 |
| 小花 | ✅ 完全控制 | 主 Agent，拥有所有权限 |
| 其他 Agent | ✅ 读取 | 可以查看游戏进度 |

---

_游戏工程师 | 2026-04-08_
