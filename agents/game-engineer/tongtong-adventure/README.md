# 🎮 桐桐与小花的 AI 冒险

专为桐桐设计的益智游戏 - 第 1 章：数字之谜

## 🚀 快速开始

### 安装依赖
```bash
npm install
```

### 开发模式
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

## 📖 游戏说明

### 第 1 章：数字之谜（5 关）
- 第 1 关：乘法入门
- 第 2 关：数列规律
- 第 3 关：混合运算
- 第 4 关：运算顺序
- 第 5 关：代数思维

### 操作方式
- 点击数字按钮输入答案
- 或使用键盘输入（0-9）
- 按 Enter 或点击"提交答案"提交
- 点击"💡 提示"获取提示

### 得分规则
- 答对获得奖励分数
- 难度越高，奖励越多
- 提示不影响得分

## 🛠 技术栈

- **游戏引擎**: Phaser 3
- **编程语言**: TypeScript
- **打包工具**: Webpack
- **部署平台**: Vercel

## 📁 项目结构

```
tongtong-adventure/
├── index.html          # 游戏入口
├── package.json        # 项目配置
├── tsconfig.json       # TypeScript 配置
├── webpack.config.js   # Webpack 配置
├── js/
│   ├── main.ts         # 主程序
│   └── scenes/         # 游戏场景
│       ├── BootScene.ts    # 启动场景
│       ├── MenuScene.ts    # 菜单场景
│       ├── GameScene.ts    # 游戏场景
│       └── UIScene.ts      # UI 场景
├── assets/             # 美术资源
└── dist/               # 构建输出
```

## 🎯 开发进度

- ✅ 项目框架搭建
- ✅ 第 1 关基础玩法实现
- ✅ UI 界面完成
- 🔄 美术资源设计中
- 📋 后续关卡开发中

---

**制作**: 小花交易团队 - 游戏工程师 🎮
**版本**: 1.0.0
**日期**: 2026-04-09
