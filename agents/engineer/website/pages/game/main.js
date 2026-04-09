// 超级马里奥风格平台跳跃游戏
// 控制：← → 移动，↑/空格 跳跃，R 重来

class BootScene extends Phaser.Scene {
  constructor() { super('BootScene'); }

  create() {
    // 创建玩家纹理（绿色方块 - 桐桐）
    const pg = this.make.graphics({ x: 0, y: 0 });
    pg.fillStyle(0x00ff00);
    pg.fillRect(0, 0, 32, 32);
    pg.generateTexture('player', 32, 32);

    // 创建地面纹理（棕色）
    const gg = this.make.graphics({ x: 0, y: 0 });
    gg.fillStyle(0x8B4513);
    gg.fillRect(0, 0, 32, 32);
    gg.generateTexture('ground', 32, 32);

    // 创建平台纹理
    const pg2 = this.make.graphics({ x: 0, y: 0 });
    pg2.fillStyle(0x654321);
    pg2.fillRect(0, 0, 80, 16);
    pg2.generateTexture('platform', 80, 16);

    // 创建金币纹理
    const cg = this.make.graphics({ x: 0, y: 0 });
    cg.fillStyle(0xFFD700);
    cg.fillCircle(10, 10, 10);
    cg.generateTexture('coin', 20, 20);

    // 创建敌人纹理（红色怪物）
    const eg = this.make.graphics({ x: 0, y: 0 });
    eg.fillStyle(0xff0000);
    eg.fillRect(0, 0, 32, 32);
    eg.generateTexture('enemy', 32, 32);

    // 创建旗杆纹理
    const fg = this.make.graphics({ x: 0, y: 0 });
    fg.fillStyle(0x0000ff);
    fg.fillRect(0, 0, 8, 80);
    fg.fillStyle(0xff0000);
    fg.fillTriangle(8, 0, 8, 30, 40, 15);
    fg.generateTexture('flag', 40, 80);

    this.scene.start('PlayScene');
  }
}

class PlayScene extends Phaser.Scene {
  constructor() { super('PlayScene'); }

  create() {
    this.gameOver = false;
    this.score = 0;

    // 平台组
    this.platforms = this.physics.add.staticGroup();

    // 地面
    for (let i = 0; i < 25; i++) {
      this.platforms.create(i * 32, 584, 'ground');
    }

    // 墙壁
    this.platforms.create(-16, 300, 'ground');
    this.platforms.create(816, 300, 'ground');

    // 浮动平台
    this.platforms.create(200, 450, 'platform');
    this.platforms.create(400, 380, 'platform');
    this.platforms.create(600, 300, 'platform');
    this.platforms.create(300, 220, 'platform');
    this.platforms.create(100, 150, 'platform');

    // 玩家
    this.player = this.physics.add.sprite(50, 500, 'player');
    this.player.setBounce(0.1);
    this.player.setCollideWorldBounds(true);

    // 金币
    this.coins = this.physics.add.group();
    this.coins.create(220, 420, 'coin');
    this.coins.create(420, 350, 'coin');
    this.coins.create(620, 270, 'coin');
    this.coins.create(320, 190, 'coin');
    this.coins.create(120, 120, 'coin');

    // 敌人
    this.enemies = this.physics.add.group();
    const enemy = this.enemies.create(400, 550, 'enemy');
    enemy.setVelocityX(-100);
    enemy.setCollideWorldBounds(true);
    enemy.setBounce(1);

    // 终点
    const flag = this.physics.add.sprite(750, 540, 'flag');
    flag.setImmovable(true);

    // 碰撞
    this.physics.add.collider(this.player, this.platforms);
    this.physics.add.collider(this.coins, this.platforms);
    this.physics.add.collider(this.enemies, this.platforms);
    this.physics.add.collider(this.enemies, this.player, this.hitEnemy, null, this);
    this.physics.add.overlap(this.player, this.coins, this.collectCoin, null, this);
    this.physics.add.overlap(this.player, flag, this.reachGoal, null, this);

    // 控制
    this.cursors = this.input.keyboard.createCursorKeys();
    this.input.keyboard.on('keydown-R', () => {
      if (this.gameOver) this.scene.restart();
    });

    // UI
    this.scoreText = this.add.text(16, 16, '分数：0', {
      fontSize: '24px',
      color: '#fff',
      fontFamily: 'Arial',
      stroke: '#000',
      strokeThickness: 4
    });

    this.add.text(16, 560, '← → 移动 | ↑/空格 跳跃 | R 重来', {
      fontSize: '16px',
      color: '#fff',
      fontFamily: 'Arial',
      stroke: '#000',
      strokeThickness: 3
    });
  }

  update() {
    if (this.gameOver) return;

    if (this.cursors.left.isDown) {
      this.player.setVelocityX(-200);
    } else if (this.cursors.right.isDown) {
      this.player.setVelocityX(200);
    } else {
      this.player.setVelocityX(0);
    }

    if ((this.cursors.up.isDown || this.cursors.space.isDown) && this.player.body.touching.down) {
      this.player.setVelocityY(-400);
    }
  }

  collectCoin(player, coin) {
    coin.disableBody(true, true);
    this.score += 10;
    this.scoreText.setText('分数：' + this.score);
  }

  hitEnemy(player, enemy) {
    if (player.body.velocity.y > 0 && player.y < enemy.y) {
      enemy.disableBody(true, true);
      this.player.setVelocityY(-300);
      this.score += 20;
      this.scoreText.setText('分数：' + this.score);
    } else {
      this.gameOver = true;
      this.physics.pause();
      this.player.setTint(0xff0000);
      this.add.text(300, 300, '游戏结束！\n按 R 重新开始', {
        fontSize: '32px',
        color: '#ff0000',
        fontFamily: 'Arial',
        align: 'center',
        stroke: '#000',
        strokeThickness: 4
      });
    }
  }

  reachGoal(player, flag) {
    this.gameOver = true;
    this.physics.pause();
    this.player.setTint(0x00ff00);
    this.add.text(200, 300, '恭喜通关！\n分数：' + this.score + '\n按 R 再玩一次', {
      fontSize: '32px',
      color: '#00ff00',
      fontFamily: 'Arial',
      align: 'center',
      stroke: '#000',
      strokeThickness: 4
    });
  }
}

// 游戏配置
const config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  backgroundColor: '#667eea',
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 500, x: 0 },
      debug: false
    }
  },
  scene: ['BootScene', 'PlayScene']
};

// 启动游戏
new Phaser.Game(config);
