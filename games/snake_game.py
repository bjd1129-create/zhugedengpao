"""
贪吃蛇游戏 - Python + Pygame
面向对象设计 | 得分系统 | 加速模式 | 障碍物
"""

import math
import os
import random
import sys

import pygame

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────
CELL_SIZE   = 20
GRID_WIDTH  = 30
GRID_HEIGHT = 20
SCREEN_W    = GRID_WIDTH  * CELL_SIZE
SCREEN_H    = GRID_HEIGHT * CELL_SIZE
FPS_NORMAL  = 10
FPS_FAST    = 18
FPS_BOOST   = 25

# 颜色
C_BLACK       = (0, 0, 0)
C_WHITE       = (255, 255, 255)
C_DARK        = (30, 30, 30)
C_SNAKE_HEAD  = (50, 180, 50)
C_SNAKE_BODY  = (80, 200, 80)
C_SNAKE_DARK  = (40, 140, 40)
C_FOOD        = (255, 80, 80)
C_FOOD_GLOW   = (255, 120, 120)
C_OBSTACLE    = (100, 100, 100)
C_OBSTACLE_H  = (120, 120, 120)
C_UI_BG       = (20, 20, 30)
C_UI_ACCENT   = (80, 200, 120)
C_GOLD        = (255, 215, 0)
C_RED         = (220, 50, 50)
C_BLUE        = (80, 160, 255)
C_GREEN       = (80, 200, 80)
C_YELLOW      = (255, 240, 100)

pygame.init()
FONT_PATH = pygame.font.match_font("menlo") or pygame.font.get_default_font()
BIG_FONT  = pygame.font.Font(FONT_PATH, 48)
MID_FONT  = pygame.font.Font(FONT_PATH, 28)
SML_FONT  = pygame.font.Font(FONT_PATH, 18)


# ─────────────────────────────────────────────
# 方向
# ─────────────────────────────────────────────
class Dir:
    UP    = (0, -1)
    DOWN  = (0,  1)
    LEFT  = (-1, 0)
    RIGHT = ( 1, 0)

    @staticmethod
    def opposite(d):
        return {Dir.UP: Dir.DOWN, Dir.DOWN: Dir.UP,
                Dir.LEFT: Dir.RIGHT, Dir.RIGHT: Dir.LEFT}[d]

    @staticmethod
    def from_key(k):
        return {pygame.K_UP: Dir.UP, pygame.K_DOWN: Dir.DOWN,
                pygame.K_LEFT: Dir.LEFT, pygame.K_RIGHT: Dir.RIGHT}.get(k)


# ─────────────────────────────────────────────
# 粒子特效
# ─────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, vx, vy, life=20):
        self.x, self.y   = x, y
        self.vx, self.vy = vx, vy
        self.color       = color
        self.life        = life
        self.max_life    = life
        self.size        = random.randint(2, 5)

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vx *= 0.92
        self.vy *= 0.92
        self.life -= 1

    def draw(self, surf):
        alpha = int(255 * self.life / self.max_life)
        s = max(1, int(self.size * self.life / self.max_life))
        col = (*self.color[:3], alpha) if len(self.color) == 4 else (*self.color, alpha)
        buf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        pygame.draw.circle(buf, col, (s, s), s)
        surf.blit(buf, (int(self.x) - s, int(self.y) - s))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=8):
        for _ in range(count):
            angle = random.uniform(0, 6.283)
            speed = random.uniform(1.5, 4.0)
            self.particles.append(Particle(
                x, y, color,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                random.randint(15, 30)
            ))

    def update(self):
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)


# ─────────────────────────────────────────────
# 蛇
# ─────────────────────────────────────────────
class Snake:
    def __init__(self, x, y):
        self.reset(x, y)

    def reset(self, x, y):
        self.segments = [pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)]
        self.dir       = Dir.RIGHT
        self.next_dir  = Dir.RIGHT
        self.growing   = 0
        self.alive     = True
        self.length    = 1

    @property
    def head(self):
        return self.segments[0]

    def set_dir(self, d):
        if d != Dir.opposite(self.dir):
            self.next_dir = d

    def move(self):
        self.dir = self.next_dir
        head = self.head
        new_head = pygame.Rect(
            head.x + self.dir[0] * CELL_SIZE,
            head.y + self.dir[1] * CELL_SIZE,
            CELL_SIZE, CELL_SIZE
        )
        if self.growing > 0:
            self.segments.insert(0, new_head)
            self.growing -= 1
        else:
            self.segments.insert(0, new_head)
            self.segments.pop()

    def grow(self, n=1):
        self.growing += n
        self.length  += n

    def check_collision_self(self):
        return self.head.collidelist(self.segments[1:]) != -1

    def check_collision_wall(self):
        return (self.head.left < 0 or self.head.right  > SCREEN_W or
                self.head.top  < 0 or self.head.bottom > SCREEN_H)

    def draw(self, surf, tick):
        # 绘制身体
        for i, seg in enumerate(reversed(self.segments)):
            is_head = (i == len(self.segments) - 1)
            pulse = abs(math.sin(tick * 0.15 + i * 0.3)) * 0.15 + 0.85
            color = C_SNAKE_HEAD if is_head else C_SNAKE_BODY

            if not is_head:
                # 渐暗尾部
                factor = 1 - i / len(self.segments) * 0.4
                color = tuple(int(c * factor * pulse) for c in C_SNAKE_BODY)

            rect = seg.inflate(-2, -2)
            pygame.draw.rect(surf, color, rect, border_radius=4)

            # 高光
            hi = rect.inflate(-6, -6)
            hi_color = tuple(min(255, c + 40) for c in color)
            pygame.draw.rect(surf, hi_color, hi, border_radius=3)


# ─────────────────────────────────────────────
# 食物
# ─────────────────────────────────────────────
class FoodType:
    NORMAL = 0
    SPEED   = 1   # 蓝：加速
    SCORE   = 2   # 金：双倍分数
    GROW    = 3   # 绿：长身体

class Food:
    NORMAL_COLOR = C_FOOD
    SPEED_COLOR  = C_BLUE
    SCORE_COLOR  = C_GOLD
    GROW_COLOR   = C_GREEN

    POINT_VALUES = {
        FoodType.NORMAL: 10,
        FoodType.SPEED:  5,
        FoodType.SCORE:  25,
        FoodType.GROW:   15,
    }

    def __init__(self, rect, ftype=FoodType.NORMAL):
        self.rect  = rect
        self.type  = ftype
        self.tick = 0

    @property
    def color(self):
        return {FoodType.NORMAL: self.NORMAL_COLOR,
                FoodType.SPEED:  self.SPEED_COLOR,
                FoodType.SCORE:  self.SCORE_COLOR,
                FoodType.GROW:   self.GROW_COLOR}[self.type]

    def draw(self, surf, tick):
        self.tick = tick
        r = self.rect
        cx, cy = r.centerx, r.centery

        # 发光效果
        pulse = abs(math.sin(tick * 0.1)) * 4 + 2
        glow_rect = r.inflate(int(pulse * 2), int(pulse * 2))
        glow_surf = pygame.Surface((glow_rect.w, glow_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*self.color, 60), glow_surf.get_rect(), border_radius=8)
        surf.blit(glow_surf, glow_rect.topleft)

        # 主体
        inner = r.inflate(-4, -4)
        pygame.draw.rect(surf, self.color, inner, border_radius=6)

        # 小图标
        label = {FoodType.NORMAL: "🍎", FoodType.SPEED: "⚡",
                 FoodType.SCORE: "⭐", FoodType.GROW: "🌱"}[self.type]
        lbl_surf = SML_FONT.render(label, True, C_WHITE)
        lbl_rect = lbl_surf.get_rect(center=(cx, cy))
        surf.blit(lbl_surf, lbl_rect)


# ─────────────────────────────────────────────
# 障碍物
# ─────────────────────────────────────────────
class Obstacle:
    def __init__(self, rect):
        self.rect = rect

    def draw(self, surf, tick):
        r = self.rect
        # 主体
        pygame.draw.rect(surf, C_OBSTACLE, r, border_radius=3)
        # 边框
        pygame.draw.rect(surf, C_OBSTACLE_H, r.inflate(-3, -3), 2, border_radius=3)
        # X 纹理
        cx, cy = r.center
        pygame.draw.line(surf, C_OBSTACLE_H, (r.left+4, r.top+4),
                         (r.right-4, r.bottom-4), 2)
        pygame.draw.line(surf, C_OBSTACLE_H, (r.right-4, r.top+4),
                         (r.left+4, r.bottom-4), 2)


# ─────────────────────────────────────────────
# 地图（管理食物和障碍物）
# ─────────────────────────────────────────────
class GameMap:
    def __init__(self):
        self.foods     = []
        self.obstacles = []
        self._obstacle_rects = []

    def generate_obstacles(self, level):
        """根据等级生成障碍物"""
        self.obstacles.clear()
        self._obstacle_rects.clear()
        count = min(3 + level * 2, 15)
        for _ in range(count):
            for _ in range(50):  # 最多尝试50次
                x = random.randint(0, GRID_WIDTH  - 1) * CELL_SIZE
                y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                if not any(r.colliderect(rect) for r in self._obstacle_rects):
                    self.obstacles.append(Obstacle(rect))
                    self._obstacle_rects.append(rect)
                    break

    def spawn_food(self, snake_segs, extra_exclude=None):
        """在空位生成食物"""
        exclude = set(snake_segs) | set(self._obstacle_rects)
        if extra_exclude:
            exclude |= set(extra_exclude)

        # 随机决定类型
        r = random.random()
        if r < 0.60:
            ftype = FoodType.NORMAL
        elif r < 0.75:
            ftype = FoodType.SPEED
        elif r < 0.88:
            ftype = FoodType.SCORE
        else:
            ftype = FoodType.GROW

        for _ in range(200):
            x = random.randint(0, GRID_WIDTH  - 1) * CELL_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if not any(r.colliderect(rect) for r in exclude):
                self.foods.append(Food(rect, ftype))
                return

    def check_snake_collision(self, snake_head):
        return snake_head.collidelist(self._obstacle_rects) != -1

    def draw(self, surf, tick):
        for obs in self.obstacles:
            obs.draw(surf, tick)
        for food in self.foods:
            food.draw(surf, tick)

    def reset(self):
        self.foods.clear()
        self.obstacles.clear()
        self._obstacle_rects.clear()


# ─────────────────────────────────────────────
# 游戏状态机
# ─────────────────────────────────────────────
class GameState:
    MENU    = "menu"
    PLAYING = "playing"
    PAUSED  = "paused"
    GAMEOVER= "gameover"


# ─────────────────────────────────────────────
# 主游戏类
# ─────────────────────────────────────────────
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H + 60))
        pygame.display.set_caption("🐍 贪吃蛇 | Snake Game")
        self.clock  = pygame.time.Clock()

        self.state      = GameState.MENU
        self.snake      = Snake(GRID_WIDTH // 2 * CELL_SIZE,
                                 GRID_HEIGHT // 2 * CELL_SIZE)
        self.game_map   = GameMap()
        self.particles  = ParticleSystem()

        self.score      = 0
        self.high_score = self._load_high_score()
        self.level      = 1
        self.fps        = FPS_NORMAL
        self.speed_mode = False
        self.speed_timer= 0
        self.score_x2   = False
        self.score_x2_t  = 0
        self.tick       = 0
        self.food_eaten = 0

    # ── 存档 ──
    def _load_high_score(self):
        path = os.path.join(os.path.dirname(__file__), "snake_highscore.txt")
        try:
            return int(open(path).read().strip())
        except:
            return 0

    def _save_high_score(self):
        path = os.path.join(os.path.dirname(__file__), "snake_highscore.txt")
        open(path, "w").write(str(self.high_score))

    # ── 初始化 / 重置 ──
    def _start_game(self):
        self.snake.reset(GRID_WIDTH // 2 * CELL_SIZE,
                         GRID_HEIGHT // 2 * CELL_SIZE)
        self.game_map.reset()
        self.game_map.generate_obstacles(self.level)
        self.game_map.spawn_food(self.snake.segments)
        self.particles = ParticleSystem()
        self.score      = 0
        self.level      = 1
        self.fps        = FPS_NORMAL
        self.speed_mode = False
        self.speed_timer= 0
        self.score_x2   = False
        self.score_x2_t = 0
        self.food_eaten = 0
        self.state      = GameState.PLAYING

    # ── 输入 ──
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                # 全局
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state in (GameState.MENU, GameState.GAMEOVER):
                        pygame.quit(); sys.exit()
                    return

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.state in (GameState.MENU, GameState.GAMEOVER):
                        self._start_game()
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    return

                if self.state == GameState.PLAYING:
                    d = Dir.from_key(event.key)
                    if d:
                        self.snake.set_dir(d)

    # ── 更新 ──
    def _update(self):
        if self.state != GameState.PLAYING:
            return

        self.tick += 1

        # 速度计时器
        if self.speed_mode:
            self.speed_timer -= 1
            if self.speed_timer <= 0:
                self.speed_mode = False
                self.fps = FPS_NORMAL

        if self.score_x2:
            self.score_x2_t -= 1
            if self.score_x2_t <= 0:
                self.score_x2 = False

        # 移动蛇
        self.snake.move()
        head = self.snake.head

        # 撞墙
        if self.snake.check_collision_wall():
            self._die(); return

        # 撞自己
        if self.snake.check_collision_self():
            self._die(); return

        # 撞障碍物
        if self.game_map.check_snake_collision(head):
            self._die(); return

        # 检查吃食物
        eaten = None
        for i, food in enumerate(self.game_map.foods):
            if head.colliderect(food.rect):
                eaten = (i, food)
                break

        if eaten:
            i, food = eaten
            self.game_map.foods.pop(i)

            # 粒子
            cx, cy = food.rect.centerx, food.rect.centery
            self.particles.emit(cx, cy, food.color, 12)

            pts = food.POINT_VALUES[food.type] * (2 if self.score_x2 else 1)
            self.score += pts
            self.food_eaten += 1

            # 效果
            if food.type == FoodType.SPEED:
                self.speed_mode  = True
                self.speed_timer = FPS_NORMAL * 5
                self.fps = FPS_FAST
            elif food.type == FoodType.SCORE:
                self.score_x2  = True
                self.score_x2_t = FPS_NORMAL * 8
            elif food.type == FoodType.GROW:
                self.snake.grow(3)

            # 生成新食物
            self.game_map.spawn_food(self.snake.segments)

            # 每5个食物升级
            if self.food_eaten % 5 == 0:
                self._level_up()

        self.particles.update()

    def _level_up(self):
        self.level += 1
        self.fps = min(FPS_BOOST, FPS_NORMAL + (self.level - 1) * 2)
        self.game_map.generate_obstacles(self.level)
        # 生成额外食物
        self.game_map.spawn_food(self.snake.segments)

    def _die(self):
        self.snake.alive = False
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()
        self.state = GameState.GAMEOVER

    # ── 绘制 ──
    def _draw_bg(self, surf):
        surf.fill(C_DARK)
        # 网格
        for x in range(0, SCREEN_W + 1, CELL_SIZE):
            pygame.draw.line(surf, (40, 40, 40), (x, 0), (x, SCREEN_H))
        for y in range(0, SCREEN_H + 1, CELL_SIZE):
            pygame.draw.line(surf, (40, 40, 40), (0, y), (SCREEN_W, y))

    def _draw_ui_bar(self, surf):
        bar_y = SCREEN_H
        pygame.draw.rect(surf, C_UI_BG, (0, bar_y, SCREEN_W, 60))

        # 分数
        label = SML_FONT.render("SCORE", True, (150, 150, 150))
        surf.blit(label, (15, bar_y + 5))
        score_col = C_GOLD if self.score_x2 else C_UI_ACCENT
        sc = MID_FONT.render(str(self.score), True, score_col)
        surf.blit(sc, (15, bar_y + 22))

        # 倍分提示
        if self.score_x2:
            x2 = MID_FONT.render("×2!", True, C_GOLD)
            surf.blit(x2, (100, bar_y + 22))

        # 速度提示
        if self.speed_mode:
            spd = MID_FONT.render("⚡", True, C_BLUE)
            surf.blit(spd, (160, bar_y + 22))

        # 最高分
        hi = SML_FONT.render(f"BEST: {self.high_score}", True, (120, 120, 120))
        surf.blit(hi, (15, bar_y + 46))

        # 关卡
        lv = MID_FONT.render(f"LV.{self.level}", True, C_WHITE)
        lv_rect = lv.get_rect(centerx=SCREEN_W // 2, centery=bar_y + 35)
        surf.blit(lv, lv_rect)

        # 操作提示
        hint = SML_FONT.render("ESC=暂停  方向键移动", True, (100, 100, 100))
        hint_rect = hint.get_rect(right=SCREEN_W - 15, centery=bar_y + 35)
        surf.blit(hint, hint_rect)

    def _draw_center_msg(self, surf, title, title_color, lines, sub=None):
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surf.blit(overlay, (0, 0))

        # 标题
        t_surf = BIG_FONT.render(title, True, title_color)
        t_rect = t_surf.get_rect(centerx=SCREEN_W // 2, centery=SCREEN_H // 2 - 60)
        surf.blit(t_surf, t_rect)

        # 副标题
        if sub:
            s_surf = MID_FONT.render(sub, True, C_WHITE)
            s_rect = s_surf.get_rect(centerx=SCREEN_W // 2, centery=SCREEN_H // 2 - 15)
            surf.blit(s_surf, s_rect)

        # 说明行
        y = SCREEN_H // 2 + 20
        for line in lines:
            l_surf = SML_FONT.render(line, True, (180, 180, 180))
            l_rect = l_surf.get_rect(centerx=SCREEN_W // 2, y=y)
            surf.blit(l_surf, l_rect)
            y += 24

    def _draw_menu(self, surf):
        self._draw_bg(surf)
        self._draw_ui_bar(surf)

        # 标题
        t = BIG_FONT.render("🐍 贪吃蛇", True, C_UI_ACCENT)
        t_rect = t.get_rect(centerx=SCREEN_W // 2, centery=SCREEN_H // 2 - 80)
        surf.blit(t, t_rect)

        sub = MID_FONT.render("SNAKE GAME", True, (150, 150, 150))
        sub_rect = sub.get_rect(centerx=SCREEN_W // 2, centery=SCREEN_H // 2 - 35)
        surf.blit(sub, sub_rect)

        # 最高分
        hi = MID_FONT.render(f"最高分: {self.high_score}", True, C_GOLD)
        hi_rect = hi.get_rect(centerx=SCREEN_W // 2, centery=SCREEN_H // 2 + 5)
        surf.blit(hi, hi_rect)

        # 开始提示（闪烁）
        alpha = int((math.sin(self.tick * 0.08) + 1) * 0.5 * 255)
        prompt = BIG_FONT.render("按 ENTER 开始", True, C_WHITE)
        prompt.set_alpha(alpha)
        p_rect = prompt.get_rect(centerx=SCREEN_W // 2, centery=SCREEN_H // 2 + 60)
        surf.blit(prompt, p_rect)

        # 操作说明
        hints = [
            "方向键 / WASD 控制方向",
            "ESC 暂停  |  ENTER 开始",
            "⭐=双倍分  ⚡=加速  🌱=长身体",
        ]
        y = SCREEN_H // 2 + 120
        for h in hints:
            hs = SML_FONT.render(h, True, (120, 120, 120))
            hr = hs.get_rect(centerx=SCREEN_W // 2, y=y)
            surf.blit(hs, hr)
            y += 22

    def _draw_gameover(self, surf):
        # 绘制游戏画面（模糊效果用暗色代替）
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 120))
        surf.blit(dim, (0, 0))

        lines = [f"得分: {self.score}", f"关卡: {self.level}"]
        if self.score >= self.high_score:
            lines.append("🎉 新纪录！")
        self._draw_center_msg(self.screen, "💀 GAME OVER", C_RED,
                                lines, "按 ENTER 重新开始")

    def _draw_paused(self, surf):
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 120))
        surf.blit(dim, (0, 0))
        self._draw_center_msg(surf, "⏸  暂停", C_WHITE,
                                [], "按 ESC 或 ENTER 继续")

    # ── 主循环 ──
    def run(self):
        while True:
            self._handle_events()

            if self.state == GameState.MENU:
                self.tick += 1
                self._draw_menu(self.screen)
            else:
                self._update()
                self._draw_bg(self.screen)
                self.game_map.draw(self.screen, self.tick)
                self.snake.draw(self.screen, self.tick)
                self.particles.draw(self.screen)
                self._draw_ui_bar(self.screen)

                if self.state == GameState.PAUSED:
                    self._draw_paused(self.screen)
                elif self.state == GameState.GAMEOVER:
                    self._draw_gameover(self.screen)

            pygame.display.flip()
            effective_fps = self.fps if self.state == GameState.PLAYING else 15
            self.clock.tick(effective_fps)


# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
