# SKILL.md - 游戏工程师核心技能

## 游戏引擎

### Phaser 3 基础
```typescript
// 游戏配置
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  scene: [BootScene, MenuScene, GameScene, WinScene],
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 0 },
      debug: false
    }
  }
};

// 加载资源
preload() {
  this.load.image('tongtong', 'assets/characters/tongtong.png');
  this.load.image('xiaohua', 'assets/characters/xiaohua.png');
  this.load.audio('bgm', 'assets/audio/bgm/adventure.mp3');
}

// 创建场景
create() {
  this.add.image(400, 300, 'background');
  this.player = this.physics.add.sprite(100, 300, 'tongtong');
  this.cursors = this.input.keyboard.createCursorKeys();
}

// 更新逻辑
update() {
  if (this.cursors.left.isDown) {
    this.player.setVelocityX(-160);
  }
}
```

---

## 关卡实现

### 谜题模板
```typescript
interface Puzzle {
  id: number;
  type: 'math' | 'logic' | 'memory' | 'space' | 'programming';
  question: string;
  answer: any;
  hints: string[];
  difficulty: 1 | 2 | 3 | 4 | 5;
}

// 数学谜题示例
const mathPuzzle: Puzzle = {
  id: 1,
  type: 'math',
  question: '我有 3 个头，每个头有 4 只眼睛，我有多少只眼睛？',
  answer: 12,
  hints: ['用乘法', '3 乘以 4'],
  difficulty: 1
};
```

---

## 趣味设计

### 反馈设计
```typescript
// 成功反馈
function showSuccess() {
  // 粒子特效
  const particles = this.add.particles(0, 0, 'star', {
    speed: 100,
    scale: { start: 1, end: 0 },
    blendMode: 'ADD'
  });
  
  // 音效
  this.sound.play('success');
  
  // 动画
  this.tweens.add({
    targets: this.player,
    y: this.player.y - 50,
    duration: 200,
    yoyo: true
  });
}

// 收集反馈
function collectItem(item: string) {
  // 显示获得物品
  this.add.text(400, 300, `获得：${item}`, {
    fontSize: '32px',
    color: '#gold'
  });
  
  // 播放音效
  this.sound.play('collect');
}
```

### 隐藏彩蛋
```typescript
// 生日彩蛋
if (playerInput === '20170307') {
  showLetterFromFather(); // 显示老庄给桐桐的信
  playVoiceMessage();     // 播放老庄语音
}

// 隐藏关卡
if (codeFragments === 100) {
  unlockHiddenLevel(); // 解锁隐藏章节
}
```

---

## 存档系统

```typescript
interface SaveData {
  playerName: string;
  currentLevel: number;
  stars: number[];
  codeFragments: number;
  playTime: number;
  achievements: string[];
}

function saveGame(data: SaveData) {
  localStorage.setItem('tongtong_save', JSON.stringify(data));
}

function loadGame(): SaveData {
  const saved = localStorage.getItem('tongtong_save');
  return saved ? JSON.parse(saved) : createDefaultSave();
}
```

---

## 部署流程

```bash
# 1. 构建游戏
npm run build

# 2. 复制到官网目录
cp -r dist/* ../website/tongtong-adventure/

# 3. 提交部署
git add website/tongtong-adventure/
git commit -m "feat: 桐桐游戏上线"
git push

# 4. Vercel 自动部署
# 访问：dengpao.pages.dev/tongtong-adventure/
```

---

_游戏工程师 | 2026-04-08_
