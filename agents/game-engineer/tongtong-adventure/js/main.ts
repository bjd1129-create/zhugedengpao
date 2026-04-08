import Phaser from 'phaser';
import { BootScene } from './scenes/BootScene';
import { MenuScene } from './scenes/MenuScene';
import { GameScene } from './scenes/GameScene';
import { UIScene } from './scenes/UIScene';

// 游戏配置
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 1024,
  height: 768,
  parent: 'game-container',
  backgroundColor: '#667eea',
  scene: [
    BootScene,
    MenuScene,
    GameScene,
    UIScene
  ],
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 0 },
      debug: false
    }
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  render: {
    pixelArt: true,
    antialias: false
  }
};

// 隐藏 loading 提示
const hideLoading = () => {
  const loading = document.getElementById('loading');
  if (loading) {
    loading.style.display = 'none';
  }
};

// 创建游戏实例
const game = new Phaser.Game(config);

// 游戏启动后隐藏 loading
game.events.once('ready', () => {
  hideLoading();
  console.log('🎮 桐桐与小花的 AI 冒险 启动成功!');
});

// 导出游戏实例（用于调试）
export { game };
