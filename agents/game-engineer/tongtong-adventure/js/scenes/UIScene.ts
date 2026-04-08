import Phaser from 'phaser';

export class UIScene extends Phaser.Scene {
  private scoreText: Phaser.GameObjects.Text | null = null;
  private score: number = 0;

  constructor() {
    super({ key: 'UIScene' });
  }

  create() {
    const { width } = this.scale;

    // 分数显示（右上角）
    this.add.text(width - 30, 30, '⭐ 分数:', {
      font: 'bold 24px Arial',
      color: '#ffcc00',
      stroke: '#333333',
      strokeThickness: 4
    }).setOrigin(1, 0);

    this.scoreText = this.add.text(width - 30, 65, '0', {
      font: 'bold 32px Arial',
      color: '#ffffff',
      stroke: '#333333',
      strokeThickness: 4
    }).setOrigin(1, 0);

    // 监听游戏场景的分数更新
    const gameScene = this.scene.get('GameScene');
    if (gameScene) {
      gameScene.events.on('scoreUpdate', (newScore: number) => {
        this.updateScore(newScore);
      });
    }
  }

  private updateScore(newScore: number) {
    if (!this.scoreText) return;

    // 分数变化动画
    const oldScore = this.score;
    this.score = newScore;

    if (newScore > oldScore) {
      // 分数增加时的动画
      this.tweens.add({
        targets: this.scoreText,
        scaleX: 1.3,
        scaleY: 1.3,
        duration: 150,
        yoyo: true,
        ease: 'Power2'
      });

      // 显示分数增加提示
      const diff = newScore - oldScore;
      const floatText = this.add.text(
        this.scale.width - 100,
        100,
        `+${diff}`,
        {
          font: 'bold 28px Arial',
          color: '#4CAF50',
          stroke: '#ffffff',
          strokeThickness: 3
        }
      ).setOrigin(0.5);

      this.tweens.add({
        targets: floatText,
        y: 50,
        alpha: 0,
        duration: 1000,
        onComplete: () => floatText.destroy()
      });
    }
  }
}
