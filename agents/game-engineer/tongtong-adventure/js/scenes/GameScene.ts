import Phaser from 'phaser';

interface LevelData {
  level: number;
  type: string;
  question: string;
  answer: number | string;
  hints: string[];
  difficulty: number;
  reward: number;
}

interface GameSceneData {
  level: number;
}

export class GameScene extends Phaser.Scene {
  private levelData: LevelData | null = null;
  private currentLevel: number = 1;
  private inputText: Phaser.GameObjects.Text | null = null;
  private feedbackText: Phaser.GameObjects.Text | null = null;
  private hintIndex: number = 0;
  private score: number = 0;
  private currentAnswer: string = '';

  constructor() {
    super({ key: 'GameScene' });
  }

  init(data: GameSceneData) {
    this.currentLevel = data.level || 1;
    this.hintIndex = 0;
    this.currentAnswer = '';
    this.loadLevelData();
  }

  private loadLevelData() {
    const levels: LevelData[] = [
      {
        level: 1,
        type: 'math',
        question: '我有 3 个头，每个头有 4 只眼睛，我有多少只眼睛？',
        answer: 12,
        hints: ['用乘法', '3 乘以 4'],
        difficulty: 1,
        reward: 10
      },
      {
        level: 2,
        type: 'math',
        question: '2, 4, 6, 8, 下一个数字是？',
        answer: 10,
        hints: ['每次加 2', '偶数数列'],
        difficulty: 1,
        reward: 10
      },
      {
        level: 3,
        type: 'math',
        question: '15 ÷ 3 + 7 = ?',
        answer: 12,
        hints: ['先除后加', '15÷3=5'],
        difficulty: 2,
        reward: 15
      },
      {
        level: 4,
        type: 'math',
        question: '100 - 25 × 3 = ?',
        answer: 25,
        hints: ['先乘后减', '25×3=75'],
        difficulty: 2,
        reward: 15
      },
      {
        level: 5,
        type: 'math',
        question: '一个数加上它自己等于 20，这个数是？',
        answer: 10,
        hints: ['x + x = 20', '2x = 20'],
        difficulty: 2,
        reward: 20
      }
    ];

    this.levelData = levels[this.currentLevel - 1] || null;
  }

  create() {
    const { width, height } = this.scale;

    if (!this.levelData) {
      this.showChapterComplete();
      return;
    }

    // 背景
    this.add.rectangle(0, 0, width, height, 0x667eea)
      .setOrigin(0)
      .setDepth(-1);

    // 关卡信息
    this.add.text(30, 30, `第 ${this.currentLevel} 关`, {
      font: 'bold 32px Arial',
      color: '#ffffff'
    });

    this.add.text(width - 30, 30, `⭐ 分数：${this.score}`, {
      font: 'bold 32px Arial',
      color: '#ffcc00'
    }).setOrigin(1, 0);

    // 问题框
    const questionBox = this.add.rectangle(width / 2, 200, 900, 200, 0xffffff)
      .setDepth(0);
    
    this.add.text(width / 2, 200, this.levelData.question, {
      font: 'bold 36px Arial',
      color: '#333333',
      wordWrap: { width: 860 }
    }).setOrigin(0.5);

    // 输入提示
    this.add.text(width / 2, 350, '请输入你的答案：', {
      font: '24px Arial',
      color: '#ffffff'
    }).setOrigin(0.5);

    // 输入框背景
    const inputBg = this.add.rectangle(width / 2, 410, 400, 60, 0xffffff);
    
    // 输入文本
    this.inputText = this.add.text(width / 2, 410, '', {
      font: 'bold 32px Arial',
      color: '#333333'
    }).setOrigin(0.5);

    // 提交按钮
    const submitButton = this.add.rectangle(width / 2 - 150, 500, 200, 60, 0x4CAF50)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => submitButton.setFillStyle(0x66BB6A))
      .on('pointerout', () => submitButton.setFillStyle(0x4CAF50))
      .on('pointerdown', () => this.checkAnswer());

    this.add.text(width / 2 - 150, 500, '提交答案', {
      font: 'bold 24px Arial',
      color: '#ffffff'
    }).setOrigin(0.5);

    // 提示按钮
    const hintButton = this.add.rectangle(width / 2 + 150, 500, 200, 60, 0xFF9800)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => hintButton.setFillStyle(0xFFB74D))
      .on('pointerout', () => hintButton.setFillStyle(0xFF9800))
      .on('pointerdown', () => this.showHint());

    this.add.text(width / 2 + 150, 500, '💡 提示', {
      font: 'bold 24px Arial',
      color: '#ffffff'
    }).setOrigin(0.5);

    // 反馈文本
    this.feedbackText = this.add.text(width / 2, 580, '', {
      font: 'bold 28px Arial',
      color: '#ffffff'
    }).setOrigin(0.5);

    // 返回按钮
    const backButton = this.add.rectangle(80, height - 40, 140, 50, 0xf44336)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => backButton.setFillStyle(0xef5350))
      .on('pointerout', () => backButton.setFillStyle(0xf44336))
      .on('pointerdown', () => this.backToMenu());

    this.add.text(80, height - 40, '← 返回', {
      font: 'bold 20px Arial',
      color: '#ffffff'
    }).setOrigin(0.5);

    // 键盘输入支持
    this.input.keyboard?.on('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Backspace') {
        if (this.inputText) {
          this.inputText.setText(this.inputText.text.slice(0, -1));
        }
      } else if (event.key === 'Enter') {
        this.checkAnswer();
      } else if (event.key.length === 1 && event.key.match(/[0-9]/)) {
        if (this.inputText) {
          this.inputText.setText(this.inputText.text + event.key);
        }
      }
    });

    // 首次进入显示引导
    if (this.currentLevel === 1) {
      this.showTutorial();
    }
  }

  private showTutorial() {
    const { width, height } = this.scale;
    
    const overlay = this.add.rectangle(0, 0, width, height, 0x000000, 0.7)
      .setOrigin(0)
      .setDepth(100);
    
    const tutorialText = this.add.text(width / 2, height / 2 - 50, 
      '🎮 欢迎来到桐桐的冒险！\n\n' +
      '1️⃣ 看上面的问题\n' +
      '2️⃣ 用键盘输入答案（数字 0-9）\n' +
      '3️⃣ 按 Enter 或点"提交答案"\n\n' +
      '加油，桐桐！💪', {
        font: 'bold 28px Arial',
        color: '#ffffff',
        align: 'center',
        lineSpacing: 15
      }).setOrigin(0.5).setDepth(101);
    
    const startButton = this.add.rectangle(width / 2, height / 2 + 100, 250, 60, 0x4CAF50)
      .setInteractive({ useHandCursor: true })
      .setDepth(101)
      .on('pointerdown', () => {
        overlay.destroy();
        tutorialText.destroy();
        startButton.destroy();
      });
    
    this.add.text(width / 2, height / 2 + 100, '开始游戏', {
      font: 'bold 28px Arial',
      color: '#ffffff'
    }).setOrigin(0.5).setDepth(101);
  }

  private checkAnswer() {
    if (!this.levelData) return;

    const playerAnswer = parseInt(this.inputText?.text.trim() || '');
    const correctAnswer = this.levelData.answer as number;

    if (isNaN(playerAnswer)) {
      this.feedbackText?.setText('🤔 先输入答案哦~');
      this.feedbackText?.setColor('#FF9800');
      return;
    }

    if (playerAnswer === correctAnswer) {
      this.score += this.levelData.reward;
      this.feedbackText?.setText('🎉 太棒了！答对了！');
      this.feedbackText?.setColor('#4CAF50');
      this.celebrate();
      this.time.delayedCall(1500, () => {
        this.nextLevel();
      });
    } else {
      this.feedbackText?.setText('💪 再试一次，你可以的！');
      this.feedbackText?.setColor('#f44336');
      if (this.inputText) {
        this.inputText.setText('');
      }
      this.tweens.add({
        targets: this.inputText,
        x: this.inputText!.x + 10,
        duration: 50,
        yoyo: true,
        repeat: 3
      });
    }

    this.events.emit('scoreUpdate', this.score);
  }

  private showHint() {
    if (!this.levelData || this.hintIndex >= this.levelData.hints.length) {
      this.feedbackText?.setText('💡 相信自己，你可以做出来的！');
      this.feedbackText?.setColor('#FF9800');
      return;
    }

    const hint = this.levelData.hints[this.hintIndex];
    this.feedbackText?.setText(`💡 提示：${hint}`);
    this.feedbackText?.setColor('#2196F3');
    this.hintIndex++;
  }

  private celebrate() {
    const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff];
    
    for (let i = 0; i < 50; i++) {
      const x = this.scale.width / 2;
      const y = this.scale.height / 2;
      const particle = this.add.circle(x, y, 5, Phaser.Math.RND.pick(colors));
      
      this.tweens.add({
        targets: particle,
        x: x + Phaser.Math.Between(-300, 300),
        y: y + Phaser.Math.Between(-300, 300),
        alpha: 0,
        duration: Phaser.Math.Between(800, 1500),
        onComplete: () => particle.destroy()
      });
    }
  }

  private nextLevel() {
    const nextLevel = this.currentLevel + 1;
    
    if (nextLevel > 5) {
      this.showChapterComplete();
    } else {
      this.scene.restart({ level: nextLevel });
    }
  }

  private showChapterComplete() {
    const { width, height } = this.scale;
    
    this.add.rectangle(0, 0, width, height, 0x000000, 0.8)
      .setOrigin(0)
      .setDepth(100);

    this.add.text(width / 2, height / 2 - 50, '🎊 第 1 章完成！🎊', {
      font: 'bold 48px Arial',
      color: '#ffcc00'
    }).setOrigin(0.5);

    this.add.text(width / 2, height / 2 + 30, `最终得分：${this.score}`, {
      font: 'bold 36px Arial',
      color: '#ffffff'
    }).setOrigin(0.5);

    this.add.text(width / 2, height / 2 + 100, '太棒了，桐桐！继续挑战下一章吧！', {
      font: '24px Arial',
      color: '#4CAF50'
    }).setOrigin(0.5);

    const menuButton = this.add.rectangle(width / 2, height / 2 + 180, 300, 70, 0x2196F3)
      .setInteractive({ useHandCursor: true })
      .setDepth(101)
      .on('pointerdown', () => {
        this.scene.stop('UIScene');
        this.scene.start('MenuScene');
      });

    this.add.text(width / 2, height / 2 + 180, '返回菜单', {
      font: 'bold 28px Arial',
      color: '#ffffff'
    }).setOrigin(0.5).setDepth(101);
  }

  private backToMenu() {
    this.scene.stop('UIScene');
    this.scene.start('MenuScene');
  }
}
