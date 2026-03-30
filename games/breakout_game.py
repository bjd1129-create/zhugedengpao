"""
打砖块游戏 - Breakout Game
Python + Pygame 面向对象实现
"""

import pygame
import random
import math
import sys

# ===== 常量 =====
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
GOLD = (255, 215, 0)
BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK, GOLD]

# ===== 工具类 =====

class Text:
    """文本渲染工具"""
    def __init__(self, font_size=24, color=WHITE, bold=False):
        try:
            self.font = pygame.font.SysFont("Arial", font_size, bold=bold)
        except:
            self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.surface = None
        self.rect = None

    def render(self, text):
        self.surface = self.font.render(str(text), True, self.color)
        self.rect = self.surface.get_rect()
        return self.surface, self.rect


# ===== 游戏对象 =====

class Paddle:
    """挡板"""
    def __init__(self):
        self.width = 120
        self.height = 16
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 40
        self.speed = 8
        self.color = LIGHT_BLUE
        self.original_width = self.width

    def move(self, dx):
        self.x += dx * self.speed
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))

    def draw(self, screen):
        # 主体
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=4)
        # 高光
        pygame.draw.rect(screen, WHITE, (self.x + 2, self.y + 2, self.width - 4, 4), border_radius=2)
        # 边缘
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y, self.width, self.height), 2, border_radius=4)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def expand(self, amount=30):
        """扩展挡板"""
        self.width = min(self.width + amount, SCREEN_WIDTH // 2)
        self.x = min(self.x, SCREEN_WIDTH - self.width)

    def shrink(self, amount=30):
        """缩小挡板"""
        self.width = max(self.width - amount, 40)

    def reset(self):
        self.width = self.original_width
        self.x = SCREEN_WIDTH // 2 - self.width // 2


class Ball:
    """球"""
    def __init__(self, x=None, y=None, dx=None, dy=None):
        self.radius = 10
        self.x = x or SCREEN_WIDTH // 2
        self.y = y or SCREEN_HEIGHT - 60
        self.dx = dx or random.choice([-4, 4])
        self.dy = dy or -5
        self.base_speed = 6
        self.speed = self.base_speed
        self.color = WHITE
        self.trail = []  # 拖尾效果

    def move(self):
        # 保存轨迹
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)

        self.x += self.dx
        self.y += self.dy

        # 边界碰撞
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.dx = -self.dx
            self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        if self.y - self.radius <= 0:
            self.dy = -self.dy
            self.y = self.radius

    def draw(self, screen):
        # 拖尾
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail) * 0.3)
            trail_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (*self.color, alpha), (self.radius, self.radius), self.radius - i)
            screen.blit(trail_surface, (tx - self.radius, ty - self.radius))

        # 主体
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # 高光
        pygame.draw.circle(screen, WHITE, (int(self.x) - 2, int(self.y) - 2), self.radius // 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 60
        self.dx = random.choice([-4, 4])
        self.dy = -5
        self.trail = []

    def speed_up(self):
        self.speed = min(self.speed + 0.5, 12)
        # 保持方向，增加速度
        angle = math.atan2(self.dy, self.dx)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def slow_down(self):
        self.speed = max(self.speed - 0.5, 3)
        angle = math.atan2(self.dy, self.dx)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed


class Brick:
    """砖块"""
    def __init__(self, x, y, width, height, color, hits=1, brick_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.original_color = color
        self.hits = hits
        self.max_hits = hits
        self.brick_type = brick_type  # normal, hard, explosive, multi
        self.active = True
        self.flash_timer = 0

    def draw(self, screen):
        if not self.active:
            return

        # 闪烁效果
        if self.flash_timer > 0:
            color = WHITE
            self.flash_timer -= 1
        else:
            color = self.color

        # 根据耐久度调整亮度
        if self.max_hits > 1:
            brightness = self.hits / self.max_hits
            r = min(255, int(color[0] * brightness + 50))
            g = min(255, int(color[1] * brightness + 50))
            b = min(255, int(color[2] * brightness + 50))
            color = (r, g, b)

        # 主体
        pygame.draw.rect(screen, color, self.rect, border_radius=3)
        # 高光
        pygame.draw.rect(screen, WHITE, (self.rect.x + 2, self.rect.y + 2, self.rect.w - 4, 4), border_radius=2)
        # 边缘
        pygame.draw.rect(screen, DARK_GRAY, (self.rect.x, self.rect.y, self.rect.w, self.rect.h), 2, border_radius=3)

        # 耐久度指示
        if self.max_hits > 1:
            text = Text(14, WHITE)
            surf, r = text.render(str(self.hits))
            r.center = self.rect.center
            screen.blit(surf, r)

        # 类型指示
        if self.brick_type == "explosive":
            pygame.draw.circle(screen, ORANGE, self.rect.center, 5)
        elif self.brick_type == "multi":
            pygame.draw.circle(screen, CYAN, self.rect.center, 5)

    def hit(self):
        self.hits -= 1
        self.flash_timer = 3
        if self.hits <= 0:
            self.active = False
            return True  # 被摧毁
        return False

    def get_center(self):
        return self.rect.center


class PowerUp:
    """道具"""
    TYPES = {
        "expand": {"color": GREEN, "symbol": "E", "name": "扩展挡板"},
        "shrink": {"color": RED, "symbol": "S", "name": "缩小挡板"},
        "multi": {"color": CYAN, "symbol": "M", "name": "三球模式"},
        "speed": {"color": ORANGE, "symbol": "F", "name": "加速球"},
        "slow": {"color": BLUE, "symbol": "L", "name": "减速球"},
        "life": {"color": PINK, "symbol": "+", "name": "增加生命"},
        "sticky": {"color": PURPLE, "symbol": "K", "name": "粘性挡板"},
    }

    def __init__(self, x, y, ptype=None):
        if ptype is None:
            ptype = random.choice(list(self.TYPES.keys()))
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.speed = 3
        self.type = ptype
        self.color = self.TYPES[ptype]["color"]
        self.symbol = self.TYPES[ptype]["symbol"]
        self.active = True
        self.lifetime = 300  # 10秒

    def move(self):
        self.y += self.speed
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
        # 闪烁即将消失
        if self.lifetime < 60 and self.lifetime % 10 < 5:
            return
        rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=5)
        text = Text(16, WHITE, bold=True)
        surf, r = text.render(self.symbol)
        r.center = rect.center
        screen.blit(surf, r)

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)


class Particle:
    """粒子效果"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(-6, -1)
        self.color = color
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.radius = random.randint(2, 5)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.2  # 重力
        self.life -= 1

    def draw(self, screen):
        alpha = int(255 * self.life / self.max_life)
        surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (self.radius, self.radius), self.radius)
        screen.blit(surf, (self.x - self.radius, self.y - self.radius))


# ===== 关卡 =====

class Level:
    """关卡生成器"""
    @staticmethod
    def generate(level_num):
        bricks = []
        rows = min(5 + level_num, 10)
        cols = 10
        brick_width = (SCREEN_WIDTH - 40) // cols
        brick_height = 25
        padding = 4

        # 砖块布局类型
        layouts = [
            # 标准排列
            lambda r, c: (r * (brick_height + padding) + 40,
                         c * brick_width + 20,
                         brick_width - padding, brick_height,
                         BRICK_COLORS[r % len(BRICK_COLORS)],
                         1, "normal"),
            # 钻石排列
            lambda r, c: ((r + abs(c - cols // 2)) * (brick_height + padding) + 40,
                         c * brick_width + 20,
                         brick_width - padding, brick_height,
                         BRICK_COLORS[(r + c) % len(BRICK_COLORS)],
                         1, "normal"),
            # 防御塔
            lambda r, c: ((cols // 2 - abs(c - cols // 2)) * (brick_height + padding) + 40,
                         c * brick_width + 20,
                         brick_width - padding, brick_height,
                         BRICK_COLORS[c % len(BRICK_COLORS)],
                         1, "normal"),
        ]

        layout = layouts[level_num % len(layouts)]

        for r in range(rows):
            for c in range(cols):
                y, x, w, h, color, hits, btype = layout(r, c)

                # 特殊砖块
                if level_num >= 2 and random.random() < 0.05:
                    btype = "hard"
                    hits = 2
                elif level_num >= 3 and random.random() < 0.03:
                    btype = "explosive"
                    hits = 1
                elif level_num >= 4 and random.random() < 0.05:
                    btype = "multi"
                    hits = 1

                bricks.append(Brick(x, y, w, h, color, hits, btype))

        return bricks


# ===== 游戏主类 =====

class BreakoutGame:
    """游戏主类"""
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("打砖块 - Breakout")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # 初始化游戏状态
        self.reset_game()
        self.high_score = 0

    def reset_game(self):
        """重置游戏"""
        self.paddle = Paddle()
        self.balls = [Ball()]
        self.bricks = []
        self.powerups = []
        self.particles = []
        self.level = 1
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.level_complete = False
        self.sticky = False
        self.balls_stuck = []  # 粘在挡板上的球
        self.level_complete_timer = 0
        self.game_over_timer = 0

        self.load_level(self.level)

    def load_level(self, level_num):
        """加载关卡"""
        self.bricks = Level.generate(level_num)
        self.powerups = []
        self.level_complete = False
        self.level_complete_timer = 0

        # 重置挡板和球
        self.paddle.reset()
        for ball in self.balls:
            ball.reset()

    def play_sound(self, sound_type):
        """播放音效（简单生成）"""
        try:
            import numpy as np
            sample_rate = 22050
            duration = 0.1 if sound_type != "explosion" else 0.2
            samples = int(sample_rate * duration)
            wave = np.zeros(samples)
            freq = 440 if sound_type == "hit" else 220 if sound_type == "powerup" else 110
            for i in range(samples):
                wave[i] = np.sin(2 * np.pi * freq * i / sample_rate) * (1 - i / samples)
            wave = (wave * 32767 * 0.3).astype(np.int16)
            stereo = np.column_stack((wave, wave))
            sound = pygame.mixer.Sound(buffer=stereo.tobytes())
            sound.set_volume(0.3)
            sound.play()
        except:
            pass

    def spawn_powerup(self, x, y):
        """生成道具"""
        if random.random() < 0.25:  # 25%概率
            ptype = random.choice(list(PowerUp.TYPES.keys()))
            self.powerups.append(PowerUp(x, y, ptype))

    def spawn_particles(self, x, y, color, count=10):
        """生成粒子"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def apply_powerup(self, ptype):
        """应用道具效果"""
        self.play_sound("powerup")

        if ptype == "expand":
            self.paddle.expand()
        elif ptype == "shrink":
            self.paddle.shrink()
        elif ptype == "multi":
            new_balls = []
            for ball in self.balls:
                if ball not in self.balls_stuck:
                    new_ball = Ball(ball.x, ball.y, ball.dx * 1.2, -abs(ball.dy))
                    new_balls.append(new_ball)
                    new_ball2 = Ball(ball.x, ball.y, ball.dx * -1.2, -abs(ball.dy))
                    new_balls.append(new_ball2)
            self.balls.extend(new_balls)
        elif ptype == "speed":
            for ball in self.balls:
                ball.speed_up()
        elif ptype == "slow":
            for ball in self.balls:
                ball.slow_down()
        elif ptype == "life":
            self.lives += 1
        elif ptype == "sticky":
            self.sticky = True

    def handle_input(self, event):
        """处理输入"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.paddle.move(-1)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.paddle.move(1)
            elif event.key == pygame.K_SPACE:
                if self.game_over:
                    self.reset_game()
                elif self.paused:
                    self.paused = False
                else:
                    # 释放粘住的球
                    for ball in self.balls_stuck:
                        ball.dy = -abs(ball.dy) if ball.dy >= 0 else ball.dy
                        ball.dx = random.choice([-4, 4]) * (ball.speed / ball.base_speed)
                    self.balls_stuck.clear()
            elif event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            elif event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_p:
                self.paused = not self.paused

    def update(self):
        """更新游戏逻辑"""
        if self.paused or self.game_over:
            if self.game_over and self.game_over_timer > 0:
                self.game_over_timer -= 1
            return

        # 粒子效果
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

        # 关卡完成检查
        if self.level_complete:
            self.level_complete_timer += 1
            if self.level_complete_timer >= 120:  # 2秒后进入下一关
                self.level += 1
                self.load_level(self.level)
            return

        # 更新道具
        self.powerups = [p for p in self.powerups if p.active]
        for powerup in self.powerups:
            powerup.move()
            # 挡板碰撞
            if powerup.get_rect().colliderect(self.paddle.get_rect()):
                self.apply_powerup(powerup.type)
                powerup.active = False

        # 更新挡板
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move(1)

        # 更新球
        balls_to_remove = []
        for ball in self.balls:
            if ball in self.balls_stuck:
                ball.x = self.paddle.x + self.paddle.width // 2
                ball.y = self.paddle.y - ball.radius - 2
                continue

            ball.move()

            # 挡板碰撞
            if ball.get_rect().colliderect(self.paddle.get_rect()) and ball.dy > 0:
                # 计算反弹角度
                hit_pos = (ball.x - self.paddle.x) / self.paddle.width
                angle = (hit_pos - 0.5) * math.pi * 0.7
                speed = ball.speed
                ball.dx = math.sin(angle) * speed
                ball.dy = -abs(math.cos(angle) * speed)
                ball.y = self.paddle.y - ball.radius

                self.play_sound("hit")

                # 粘性挡板
                if self.sticky:
                    self.balls_stuck.append(ball)
                    self.sticky = False

            # 砖块碰撞
            for brick in self.bricks:
                if not brick.active:
                    continue
                if ball.get_rect().colliderect(brick.rect):
                    # 简单反弹
                    if abs(ball.x - brick.rect.centerx) / brick.rect.width > abs(ball.y - brick.rect.centery) / brick.rect.height:
                        ball.dx = -ball.dx
                    else:
                        ball.dy = -ball.dy

                    destroyed = brick.hit()
                    self.score += 10 if not destroyed else 20

                    # 生成粒子
                    self.spawn_particles(brick.rect.centerx, brick.rect.centery, brick.color)

                    # 爆炸砖块
                    if brick.brick_type == "explosive" and destroyed:
                        for b in self.bricks:
                            if b.active and abs(b.rect.centerx - brick.rect.centerx) < 80 and abs(b.rect.centery - brick.rect.centery) < 80:
                                if b != brick:
                                    destroyed_exp = b.hit()
                                    self.score += 20 if destroyed_exp else 10
                                    self.spawn_particles(b.rect.centerx, b.rect.centery, b.color, 5)
                        self.spawn_particles(brick.rect.centerx, brick.rect.centery, ORANGE, 30)

                    # 生成道具
                    if destroyed:
                        self.spawn_powerup(brick.rect.centerx, brick.rect.centery)

                    self.play_sound("hit")
                    break

            # 出界
            if ball.y > SCREEN_HEIGHT + 50:
                balls_to_remove.append(ball)

        # 移除出界的球
        for ball in balls_to_remove:
            if ball in self.balls:
                self.balls.remove(ball)

        # 所有球都没了
        if len(self.balls) == 0:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
            else:
                # 重置球
                new_ball = Ball()
                self.balls = [new_ball]
                self.balls_stuck = [new_ball]
                self.paddle.reset()

        # 关卡完成
        if all(not b.active for b in self.bricks):
            self.level_complete = True
            self.score += self.level * 100

    def draw(self):
        """绘制"""
        self.screen.fill(BLACK)

        # 绘制背景网格
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, (20, 20, 30), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (20, 20, 30), (0, y), (SCREEN_WIDTH, y))

        # 绘制砖块
        for brick in self.bricks:
            brick.draw(self.screen)

        # 绘制粒子
        for p in self.particles:
            p.draw(self.screen)

        # 绘制道具
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # 绘制挡板
        self.paddle.draw(self.screen)

        # 绘制球
        for ball in self.balls:
            ball.draw(self.screen)

        # UI
        self.draw_ui()

        # 暂停
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            text = Text(48, WHITE, bold=True)
            surf, r = text.render("PAUSED")
            r.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(surf, r)
            text2 = Text(24, GRAY)
            surf2, r2 = text2.render("Press P to continue")
            r2.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            self.screen.blit(surf2, r2)

        # 游戏结束
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            text = Text(64, RED, bold=True)
            surf, r = text.render("GAME OVER")
            r.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
            self.screen.blit(surf, r)
            text2 = Text(32, WHITE)
            surf2, r2 = text2.render(f"Score: {self.score}  |  Level: {self.level}")
            r2.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            self.screen.blit(surf2, r2)
            text3 = Text(24, GRAY)
            surf3, r3 = text3.render("Press SPACE or R to restart")
            r3.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
            self.screen.blit(surf3, r3)

        # 关卡完成
        if self.level_complete:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            text = Text(48, GREEN, bold=True)
            surf, r = text.render(f"LEVEL {self.level} COMPLETE!")
            r.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
            self.screen.blit(surf, r)
            text2 = Text(24, WHITE)
            surf2, r2 = text2.render("Get ready for the next level...")
            r2.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
            self.screen.blit(surf2, r2)

        pygame.display.flip()

    def draw_ui(self):
        """绘制UI"""
        # 分数
        text = Text(24, WHITE)
        surf, r = text.render(f"Score: {self.score}")
        r.topleft = (10, 10)
        self.screen.blit(surf, r)

        # 关卡
        surf2, r2 = text.render(f"Level: {self.level}")
        r2.topleft = (10, 40)
        self.screen.blit(surf2, r2)

        # 生命
        heart_text = "❤ " * self.lives if self.lives <= 5 else f"❤ x{self.lives}"
        surf3, r3 = text.render(heart_text)
        r3.topright = (SCREEN_WIDTH - 10, 10)
        self.screen.blit(surf3, r3)

        # 最高分
        if self.high_score > 0:
            surf4, r4 = text.render(f"Best: {self.high_score}")
            r4.topright = (SCREEN_WIDTH - 10, 40)
            self.screen.blit(surf4, r4)

        # 控制提示
        hint = Text(16, GRAY)
        controls = "← → Move  |  SPACE Launch  |  P Pause  |  R Restart"
        surf_h, r_h = hint.render(controls)
        r_h.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 5)
        self.screen.blit(surf_h, r_h)

    def run(self):
        """主循环"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.handle_input(event)

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# ===== 入口 =====

if __name__ == "__main__":
    print("=" * 50)
    print("       打砖块游戏 - Breakout Game")
    print("=" * 50)
    print("\n控制说明:")
    print("  ← / A   : 左移挡板")
    print("  → / D   : 右移挡板")
    print("  SPACE   : 发射球 / 重新开始")
    print("  P       : 暂停/继续")
    print("  R       : 重新开始")
    print("  ESC     : 退出游戏")
    print("\n道具说明:")
    print("  E (绿)  : 扩展挡板")
    print("  S (红)  : 缩小挡板")
    print("  M (青)  : 三球模式")
    print("  F (橙)  : 加速球")
    print("  L (蓝)  : 减速球")
    print("  + (粉)  : 增加生命")
    print("  K (紫)  : 粘性挡板")
    print("\n开始游戏...")
    print("=" * 50)

    try:
        game = BreakoutGame()
        game.run()
    except Exception as e:
        print(f"游戏出错: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
