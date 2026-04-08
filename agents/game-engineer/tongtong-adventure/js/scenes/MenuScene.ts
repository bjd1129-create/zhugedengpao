import Phaser from 'phaser';

export class MenuScene extends Phaser.Scene {
  constructor() {
    super({ key: 'MenuScene' });
  }

  create() {
    const { width, height } = this.scale;

    // 游戏标题
    this.add.text(width / 2, 150, '🎮 桐桐与小花的 AI 冒险', {
      font: 'bold 48px Arial',
      color: '#ffffff',
      stroke: '#333333',
      strokeThickness: 6
    }).setOrigin(0.5);

    // 副标题
    this.add.text(width / 2, 210, '专为桐桐设计的益智游戏', {
      font: '24px Arial',
      color: '#ffcc00'
    }).setOrigin(0.5);

    // 开始游戏按钮
    const startButton = this.add.rectangle(width / 2, 350, 300, 80, 0x4CAF50)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => startButton.setFillStyle(0x66BB6A))
      .on('pointerout', () => startButton.setFillStyle(0x4CAF50))
      .on('pointerdown', () => this.startGame());

    this.add.text(width / 2, 350, '▶ 开始游戏', {
      font: 'bold 32px Arial',
      color: '#ffffff'
    }).setOrigin(0.5);

    // 关卡选择按钮
    const levelButton = this.add.rectangle(width / 2, 460, 300, 80, 0x2196F3)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => levelButton.setFillStyle(0x42A5F5))
      .on('pointerout', () => levelButton.setFillStyle(0x2196F3))
      .on('pointerdown', () => this.showLevelSelect());

    this.add.text(width / 2, 460, '📋 关卡选择', {
      font: 'bold 32px Arial',
      color: '#ffffff'
    }).setOrigin(0.5);

    // 版本信息
    this.add.text(width / 2, height - 50, 'Version 1.0.0 | 小花交易团队制作', {
      font: '16px Arial',
      color: '#cccccc'
    }).setOrigin(0.5);

    // 装饰元素
    this.createDecorations();
  }

  createDecorations() {
    // 添加一些装饰性的星星
    for (let i = 0; i < 20; i++) {
      const x = Phaser.Math.Between(50, 974);
      const y = Phaser.Math.Between(50, 718);
      const size = Phaser.Math.Between(5, 15);
      const star = this.add.text(x, y, '⭐', {
        font: `${size}px Arial`
      }).setAlpha(0.6);
      
      // 简单的闪烁动画
      this.tweens.add({
        targets: star,
        alpha: 0.3,
        duration: 1000,
        yoyo: true,
        repeat: -1,
        delay: Phaser.Math.Between(0, 1000)
      });
    }
  }

  startGame() {
    // 启动 UI 场景
    this.scene.launch('UIScene');
    // 启动游戏场景，从第 1 关开始
    this.scene.start('GameScene', { level: 1 });
  }

  showLevelSelect() {
    // TODO: 实现关卡选择界面
    this.add.text(this.scale.width / 2, 600, '关卡选择功能开发中...', {
      font: '20px Arial',
      color: '#ffcc00'
    }).setOrigin(0.5);
  }
}
