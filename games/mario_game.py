"""
超级玛丽 - Python + Pygame 实现
面向对象设计，包含：移动、跳跃、踩敌人、吃蘑菇、金币、旗子过关
"""

import pygame
import sys
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

# ==================== 初始化 ====================
pygame.init()
pygame.mixer.init()

# ==================== 常量 ====================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FPS = 60

# 颜色
SKY_BLUE = (107, 140, 255)
BRICK_BROWN = (181, 87, 30)
BRICK_DARK = (131, 57, 15)
GREEN = (0, 155, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
CREAM = (255, 243, 224)

# 方向
class Direction(Enum):
    LEFT = -1
    RIGHT = 1

# ==================== 音效（程序生成） ====================
class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            self.jump_sound = pygame.mixer.Sound(buffer=self._generate_beep(400, 0.1))
            self.coin_sound = pygame.mixer.Sound(buffer=self._generate_beep(800, 0.15))
            self.powerup_sound = pygame.mixer.Sound(buffer=self._generate_beep(600, 0.3))
            self.stomp_sound = pygame.mixer.Sound(buffer=self._generate_beep(200, 0.2))
            self.death_sound = pygame.mixer.Sound(buffer=self._generate_beep(150, 0.5))
            self.flag_sound = pygame.mixer.Sound(buffer=self._generate_beep(1000, 0.5))
        except:
            self.enabled = False

    def _generate_beep(self, freq: float, duration: float) -> bytes:
        import struct, math
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            val = int(32767 * math.sin(2 * math.pi * freq * t))
            buf += struct.pack('<h', val)
        return bytes(buf)

    def play(self, sound_name: str):
        if not self.enabled:
            return
        try:
            getattr(self, f"{sound_name}_sound").play()
        except:
            pass

sound_manager = SoundManager()

# ==================== 工具类 ====================
def load_sprite(path: str, size: tuple = None) -> pygame.Surface:
    """加载图片资源"""
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        return None

def create_rect(x: float, y: float, w: float, h: float) -> pygame.Rect:
    return pygame.Rect(int(x), int(y), int(w), int(h))

# ==================== 粒子效果 ====================
class Particle:
    def __init__(self, x: float, y: float, vx: float, vy: float, color: tuple, life: int = 30):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # 重力
        self.life -= 1

    def draw(self, surface: pygame.Surface, camera_x: int):
        alpha = int(255 * (self.life / self.max_life))
        size = max(2, int(6 * (self.life / self.max_life)))
        rect = create_rect(self.x - camera_x, self.y, size, size)
        pygame.draw.rect(surface, self.color, rect)


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []

    def emit(self, x: float, y: float, count: int = 5, color: tuple = WHITE, speed: float = 3):
        for _ in range(count):
            vx = random.uniform(-speed, speed)
            vy = random.uniform(-speed * 2, -1)
            self.particles.append(Particle(x, y, vx, vy, color, random.randint(20, 40)))

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, surface: pygame.Surface, camera_x: int):
        for p in self.particles:
            p.draw(surface, camera_x)


# ==================== 实体基类 ====================
class Entity(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: float, height: float):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
        self.rect = create_rect(x, y, width, height)
        self.on_ground = False
        self.alive = True

    def update_rect(self):
        self.rect = create_rect(self.x, self.y, self.width, self.height)

    def get_center(self) -> tuple:
        return (self.x + self.width / 2, self.y + self.height / 2)


# ==================== 马里奥 ====================
class Mario(Entity):
    SPEED = 4
    JUMP_FORCE = -12
    GRAVITY = 0.5
    MAX_FALL_SPEED = 15

    SIZE_SMALL = (32, 48)
    SIZE_BIG = (32, 64)

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 32, 48)
        self.big = False
        self.facing = Direction.RIGHT
        self.walk_frame = 0
        self.walk_timer = 0
        self.jump_frame = 0
        self.invincible = 0
        self.dead = False
        self.death_timer = 0
        self.reached_flag = False
        self.flag_slide_timer = 0
        self.crouching = False

    def make_big(self):
        if not self.big:
            self.big = True
            self.height = 64
            self.y -= 16
            self.update_rect()
            sound_manager.play("powerup")

    def make_small(self):
        if self.big:
            self.big = False
            self.height = 48
            self.y += 16
            self.update_rect()
            self.invincible = 60

    def jump(self):
        if self.on_ground and not self.dead and not self.reached_flag:
            self.vy = self.JUMP_FORCE
            self.on_ground = False
            sound_manager.play("jump")

    def update(self, keys, platforms: list):
        if self.dead:
            self.death_timer += 1
            if self.death_timer > 30:
                self.vy += 0.5
                self.y += self.vy
            return

        if self.reached_flag:
            self.flag_slide_timer += 1
            if self.flag_slide_timer > 30:
                self.vy = 4
                self.y += self.vy
                self.vx = 0
            return

        # 移动
        self.crouching = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.SPEED
            self.facing = Direction.LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.SPEED
            self.facing = Direction.RIGHT
        else:
            self.vx = 0

        # 跳跃动画帧
        if not self.on_ground:
            self.jump_frame = (self.jump_frame + 1) % 4
        else:
            self.jump_frame = 0

        # 行走动画
        if abs(self.vx) > 0 and self.on_ground:
            self.walk_timer += 1
            if self.walk_timer > 6:
                self.walk_timer = 0
                self.walk_frame = (self.walk_frame + 1) % 4
        else:
            self.walk_frame = 0
            self.walk_timer = 0

        # 加速/减速
        self.vx *= 0.85

        # 重力
        self.vy += self.GRAVITY
        if self.vy > self.MAX_FALL_SPEED:
            self.vy = self.MAX_FALL_SPEED

        # 碰撞检测
        self.on_ground = False
        self.x += self.vx
        self._collide_horizontal(platforms)
        self.y += self.vy
        self._collide_vertical(platforms)

        # 无敌时间
        if self.invincible > 0:
            self.invincible -= 1

        self.update_rect()

    def _collide_horizontal(self, platforms: list):
        for plat in platforms:
            if not plat.solid:
                continue
            if self.rect.colliderect(plat.rect):
                if self.vx > 0:
                    self.x = plat.rect.left - self.width
                elif self.vx < 0:
                    self.x = plat.rect.right
                self.vx = 0
                self.update_rect()

    def _collide_vertical(self, platforms: list):
        for plat in platforms:
            if not plat.solid:
                continue
            if self.rect.colliderect(plat.rect):
                if self.vy > 0:
                    self.y = plat.rect.top - self.height
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = plat.rect.bottom
                    self.vy = 0
                self.update_rect()

    def draw(self, surface: pygame.Surface, camera_x: int):
        if self.invincible > 0 and self.invincible % 8 < 4:
            return  # 闪烁效果

        x = int(self.x - camera_x)
        y = int(self.y)

        # 简单绘制（不使用图片资源）
        if self.big:
            self._draw_big_mario(surface, x, y)
        else:
            self._draw_small_mario(surface, x, y)

    def _draw_small_mario(self, surface: pygame.Surface, x: int, y: int):
        # 帽子
        pygame.draw.rect(surface, RED, (x + 4, y, 24, 10))
        # 脸
        pygame.draw.rect(surface, CREAM, (x + 4, y + 10, 24, 14))
        # 眼睛
        eye_x = x + 22 if self.facing == Direction.RIGHT else x + 6
        pygame.draw.rect(surface, BLACK, (eye_x, y + 12, 4, 4))
        # 身体
        pygame.draw.rect(surface, RED, (x + 4, y + 24, 24, 14))
        # 背带
        pygame.draw.rect(surface, BROWN, (x + 8, y + 24, 6, 14))
        pygame.draw.rect(surface, BROWN, (x + 18, y + 24, 6, 14))
        # 腿
        leg_color = BROWN if self.jump_frame == 0 else (120, 70, 30)
        pygame.draw.rect(surface, leg_color, (x + 4, y + 38, 10, 10))
        pygame.draw.rect(surface, leg_color, (x + 18, y + 38, 10, 10))

    def _draw_big_mario(self, surface: pygame.Surface, x: int, y: int):
        # 帽子
        pygame.draw.rect(surface, RED, (x + 4, y, 24, 10))
        # 脸
        pygame.draw.rect(surface, CREAM, (x + 4, y + 10, 24, 18))
        # 眼睛
        eye_x = x + 22 if self.facing == Direction.RIGHT else x + 6
        pygame.draw.rect(surface, BLACK, (eye_x, y + 14, 4, 4))
        # 鼻子
        pygame.draw.rect(surface, CREAM, (x + 24, y + 18, 6, 4))
        # 身体
        pygame.draw.rect(surface, RED, (x + 4, y + 28, 24, 20))
        # M标志
        pygame.draw.rect(surface, RED, (x + 12, y + 32, 8, 8))
        pygame.draw.rect(surface, BROWN, (x + 12, y + 32, 8, 2))
        # 背带
        pygame.draw.rect(surface, BROWN, (x + 8, y + 28, 6, 20))
        pygame.draw.rect(surface, BROWN, (x + 18, y + 28, 6, 20))
        # 裤子
        pygame.draw.rect(surface, BROWN, (x + 4, y + 48, 10, 8))
        pygame.draw.rect(surface, BROWN, (x + 18, y + 48, 10, 8))
        # 腿/脚
        foot_color = (120, 70, 30)
        if not self.on_ground:
            foot_color = (100, 60, 20)
        pygame.draw.rect(surface, foot_color, (x + 2, y + 56, 12, 8))
        pygame.draw.rect(surface, foot_color, (x + 18, y + 56, 12, 8))


BROWN = (139, 69, 19)


# ==================== 平台/砖块 ====================
class Brick(Entity):
    def __init__(self, x: float, y: float, brick_type: str = "brick"):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.brick_type = brick_type
        self.solid = True
        self.hit = False
        self.hit_timer = 0
        self.has_item = brick_type in ["?block", "?block_empty"]
        self.contains_coin = brick_type == "?block"
        self.contains_mushroom = brick_type == "?block_mushroom"
        self.dead = False

    def update(self):
        if self.hit:
            self.hit_timer += 1

    def draw(self, surface: pygame.Surface, camera_x: int):
        bx = int(self.x - camera_x)
        by = int(self.y)

        if self.brick_type == "brick":
            pygame.draw.rect(surface, BRICK_BROWN, (bx, by, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, BRICK_DARK, (bx + 2, by + 2, TILE_SIZE - 4, TILE_SIZE - 4))
            # 砖块纹理
            pygame.draw.line(surface, BRICK_BROWN, (bx, by + 10), (bx + TILE_SIZE, by + 10), 2)
            pygame.draw.line(surface, BRICK_BROWN, (bx, by + 20), (bx + TILE_SIZE, by + 20), 2)
            pygame.draw.line(surface, BRICK_BROWN, (bx, by + 30), (bx + TILE_SIZE, by + 30), 2)
            pygame.draw.line(surface, BRICK_DARK, (bx + 20, by), (bx + 20, by + 10), 2)
            pygame.draw.line(surface, BRICK_DARK, (bx + 10, by + 10), (bx + 10, by + 20), 2)
            pygame.draw.line(surface, BRICK_DARK, (bx + 30, by + 10), (bx + 30, by + 20), 2)
            pygame.draw.line(surface, BRICK_DARK, (bx + 20, by + 20), (bx + 20, by + 30), 2)
            pygame.draw.line(surface, BRICK_DARK, (bx + 10, by + 30), (bx + 10, by + 40), 2)
            pygame.draw.line(surface, BRICK_DARK, (bx + 30, by + 30), (bx + 30, by + 40), 2)
        elif self.brick_type == "?block" or self.brick_type == "?block_mushroom" or self.brick_type == "?block_empty":
            pygame.draw.rect(surface, ORANGE, (bx, by, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, YELLOW, (bx + 2, by + 2, TILE_SIZE - 4, TILE_SIZE - 4), 3)
            # 问号
            if self.brick_type == "?block":
                font = pygame.font.SysFont(None, 30, bold=True)
                text = font.render("?", True, YELLOW)
                surface.blit(text, (bx + 12, by + 5))
            elif self.brick_type == "?block_mushroom":
                font = pygame.font.SysFont(None, 30, bold=True)
                text = font.render("?", True, YELLOW)
                surface.blit(text, (bx + 12, by + 5))
        elif self.brick_type == "ground":
            pygame.draw.rect(surface, GREEN, (bx, by, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, DARK_GREEN, (bx, by, TILE_SIZE, 8))
            # 草丛纹理
            pygame.draw.rect(surface, (50, 180, 50), (bx + 4, by + 2, 8, 4))
            pygame.draw.rect(surface, (50, 180, 50), (bx + 18, by + 2, 8, 4))
            pygame.draw.rect(surface, (50, 180, 50), (bx + 32, by + 2, 4, 4))


# ==================== 敌人 ====================
class Goomba(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 32, 32)
        self.vx = -1.5
        self.vy = 0
        self.alive = True
        self.death_timer = 0
        self.squished = False
        self.walk_frame = 0
        self.walk_timer = 0

    def update(self, platforms: list):
        if self.squished:
            self.death_timer += 1
            return

        self.vy += 0.4
        if self.vy > 10:
            self.vy = 10

        self.x += self.vx
        self.walk_timer += 1
        if self.walk_timer > 10:
            self.walk_timer = 0
            self.walk_frame = (self.walk_frame + 1) % 2

        # 简单碰撞转向
        for plat in platforms:
            if plat.solid and self.rect.colliderect(plat.rect):
                if self.vx > 0 and self.x + self.width > plat.rect.left and self.x < plat.rect.left:
                    self.x = plat.rect.left - self.width
                    self.vx = -self.vx
                elif self.vx < 0 and self.x < plat.rect.right and self.x + self.width > plat.rect.right:
                    self.x = plat.rect.right
                    self.vx = -self.vx

        # 掉落检测
        for plat in platforms:
            if plat.solid and self.vy > 0:
                # 脚部碰撞
                foot_rect = create_rect(self.x + 2, self.y + self.height - 4, self.width - 4, 8)
                if foot_rect.colliderect(plat.rect):
                    self.y = plat.rect.top - self.height
                    self.vy = 0

        self.update_rect()

    def stomp(self):
        self.squished = True
        self.vy = -6
        self.vx = 0
        sound_manager.play("stomp")

    def draw(self, surface: pygame.Surface, camera_x: int):
        gx = int(self.x - camera_x)
        gy = int(self.y)

        if self.squished:
            # 被踩扁
            pygame.draw.ellipse(surface, BROWN, (gx, gy + 20, 32, 12))
            return

        # 身体
        pygame.draw.ellipse(surface, BROWN, (gx + 2, gy + 4, 28, 24))
        # 眼睛（愤怒的白色）
        pygame.draw.ellipse(surface, WHITE, (gx + 4, gy + 8, 10, 10))
        pygame.draw.ellipse(surface, WHITE, (gx + 18, gy + 8, 10, 10))
        pygame.draw.ellipse(surface, BLACK, (gx + 6, gy + 10, 6, 6))
        pygame.draw.ellipse(surface, BLACK, (gx + 20, gy + 10, 6, 6))
        # 脚
        fy = gy + 26 + (4 if self.walk_frame == 0 else 0)
        pygame.draw.ellipse(surface, BLACK, (gx + 2, fy, 10, 6))
        pygame.draw.ellipse(surface, BLACK, (gx + 20, fy, 10, 6))


class Koopa(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 32, 48)
        self.vx = -1.5
        self.vy = 0
        self.alive = True
        self.shell = False
        self.shell_timer = 0
        self.active = True

    def update(self, platforms: list):
        if self.shell:
            self.shell_timer += 1
            return

        self.vy += 0.4
        if self.vy > 10:
            self.vy = 10

        if self.active:
            self.x += self.vx

        # 掉落检测
        for plat in platforms:
            if plat.solid and self.vy > 0:
                foot_rect = create_rect(self.x + 2, self.y + self.height - 4, self.width - 4, 8)
                if foot_rect.colliderect(plat.rect):
                    self.y = plat.rect.top - self.height
                    self.vy = 0

        self.update_rect()

    def turn_to_shell(self):
        self.shell = True
        self.height = 32
        self.y += 16
        self.vx = 0
        self.update_rect()
        sound_manager.play("stomp")

    def draw(self, surface: pygame.Surface, camera_x: int):
        kx = int(self.x - camera_x)
        ky = int(self.y)

        if self.shell:
            # 龟壳
            pygame.draw.ellipse(surface, GREEN, (kx, ky, 32, 28))
            pygame.draw.ellipse(surface, YELLOW, (kx + 4, ky + 4, 24, 20))
            return

        # 壳
        pygame.draw.ellipse(surface, GREEN, (kx + 2, ky + 16, 28, 28))
        pygame.draw.ellipse(surface, YELLOW, (kx + 6, ky + 20, 20, 20))
        # 头
        pygame.draw.ellipse(surface, YELLOW, (kx + 2, ky, 20, 20))
        # 眼睛
        ex = kx + 12 if self.vx > 0 else kx + 2
        pygame.draw.ellipse(surface, WHITE, (ex, ky + 4, 8, 8))
        pygame.draw.ellipse(surface, BLACK, (ex + 2, ky + 6, 4, 4))
        # 脚
        pygame.draw.ellipse(surface, YELLOW, (kx + 2, ky + 40, 10, 8))
        pygame.draw.ellipse(surface, YELLOW, (kx + 20, ky + 40, 10, 8))


# ==================== 物品 ====================
class Coin(Entity):
    def __init__(self, x: float, y: float, from_block: bool = False):
        super().__init__(x, y, 24, 32)
        self.from_block = from_block
        self.vy = -8 if from_block else 0
        self.vx = 0
        self.collected = False
        self.rotation = 0
        self.active = True

    def update(self):
        if self.from_block and not self.collected:
            self.vy += 0.3
            self.y += self.vy
            if self.vy > 0:
                self.collected = True
        self.rotation += 10

    def draw(self, surface: pygame.Surface, camera_x: int):
        if self.collected and self.from_block:
            return
        cx = int(self.x - camera_x)
        cy = int(self.y)

        # 旋转的金币效果
        scale = abs(math.cos(math.radians(self.rotation)))
        w = int(24 * scale)
        if w < 2:
            return
        pygame.draw.ellipse(surface, YELLOW, (cx + 12 - w // 2, cy, w, 28))
        pygame.draw.ellipse(surface, ORANGE, (cx + 12 - w // 2, cy, w, 28), 2)


import math


class Mushroom(Entity):
    def __init__(self, x: float, y: float, mushroom_type: str = "super"):
        super().__init__(x, y, 32, 32)
        self.mushroom_type = mushroom_type
        self.vx = 2 if mushroom_type == "super" else 2
        self.vy = 0
        self.emerged = False
        self.emerge_timer = 0
        self.active = True
        self.spawn_y = y

    def update(self, platforms: list):
        if not self.emerged:
            self.emerge_timer += 1
            self.y -= 1
            if self.emerge_timer > 32:
                self.emerged = True
            return

        self.vy += 0.4
        if self.vy > 10:
            self.vy = 10

        self.x += self.vx

        # 碰撞检测
        for plat in platforms:
            if plat.solid and self.rect.colliderect(plat.rect):
                if self.vx > 0 and self.x + self.width > plat.rect.left and self.x < plat.rect.left:
                    self.x = plat.rect.left - self.width
                    self.vx = -self.vx
                elif self.vx < 0 and self.x < plat.rect.right and self.x + self.width > plat.rect.right:
                    self.x = plat.rect.right
                    self.vx = -self.vx
                if self.vy > 0:
                    foot_rect = create_rect(self.x + 2, self.y + self.height - 4, self.width - 4, 8)
                    if foot_rect.colliderect(plat.rect):
                        self.y = plat.rect.top - self.height
                        self.vy = 0

        self.update_rect()

    def draw(self, surface: pygame.Surface, camera_x: int):
        mx = int(self.x - camera_x)
        my = int(self.y)

        # 蘑菇帽
        pygame.draw.ellipse(surface, RED, (mx, my, 32, 20))
        pygame.draw.ellipse(surface, WHITE, (mx + 4, my + 4, 8, 8))
        pygame.draw.ellipse(surface, WHITE, (mx + 18, my + 4, 8, 8))
        # 茎
        pygame.draw.rect(surface, CREAM, (mx + 8, my + 18, 16, 14))
        # 眼睛
        pygame.draw.ellipse(surface, WHITE, (mx + 4, my + 18, 10, 10))
        pygame.draw.ellipse(surface, WHITE, (mx + 18, my + 18, 10, 10))
        pygame.draw.ellipse(surface, BLACK, (mx + 6, my + 20, 5, 5))
        pygame.draw.ellipse(surface, BLACK, (mx + 20, my + 20, 5, 5))


# ==================== 旗子 ====================
class Flag:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 320

    def draw(self, surface: pygame.Surface, camera_x: int):
        fx = int(self.x - camera_x)

        # 旗杆
        pygame.draw.rect(surface, GRAY, (fx + 10, self.y, 8, self.height))
        # 顶部球
        pygame.draw.circle(surface, GREEN, (fx + 14, self.y), 8)
        # 旗帜
        pygame.draw.polygon(surface, GREEN, [
            (fx + 18, self.y + 10),
            (fx + 55, self.y + 30),
            (fx + 18, self.y + 50)
        ])
        # 旗帜纹理
        pygame.draw.line(surface, DARK_GREEN, (fx + 22, self.y + 20), (fx + 50, self.y + 28), 2)
        pygame.draw.line(surface, DARK_GREEN, (fx + 22, self.y + 30), (fx + 50, self.y + 38), 2)


# ==================== 游戏场景/关卡 ====================
class Level:
    def __init__(self, level_num: int = 1):
        self.level_num = level_num
        self.platforms: List[Brick] = []
        self.enemies: List[Entity] = []
        self.items: List[Entity] = []
        self.coins: List[Coin] = []
        self.flag: Optional[Flag] = None
        self.particles = ParticleSystem()
        self.coin_count = 0
        self.build()

    def build(self):
        """构建关卡"""
        w = SCREEN_WIDTH
        h = SCREEN_HEIGHT

        # 地面 - 多个区块
        ground_rows = 3
        ground_y = h - TILE_SIZE * ground_rows

        for gx in range(0, 3200, TILE_SIZE):
            for gy in range(ground_y, h, TILE_SIZE):
                b = Brick(gx, gy, "ground")
                self.platforms.append(b)

        # 左上角平台
        for bx in range(120, 280, TILE_SIZE):
            self.platforms.append(Brick(bx, 360, "brick"))

        # 问号砖块
        q_positions = [(280, 320), (400, 320), (480, 240), (680, 320)]
        for qx, qy in q_positions:
            self.platforms.append(Brick(qx, qy, "?block"))

        # 问号砖块（蘑菇）
        self.platforms.append(Brick(360, 320, "?block_mushroom"))

        # 中间高台
        for bx in range(760, 1040, TILE_SIZE):
            self.platforms.append(Brick(bx, 400, "brick"))

        # 悬浮砖块
        for bx in [1120, 1160, 1200]:
            self.platforms.append(Brick(bx, 320, "brick"))

        # 更多问号
        self.platforms.append(Brick(1280, 280, "?block"))
        self.platforms.append(Brick(1320, 280, "?block"))

        # 大管道
        self._build_pipe(520, 440, 80, 120)
        self._build_pipe(900, 400, 80, 160)

        # 敌人
        for ex in [350, 500, 800, 1000, 1300, 1500, 1700, 1900, 2100]:
            self.enemies.append(Goomba(ex, ground_y - 32))

        # 乌龟
        for tx in [1100, 1600, 2000]:
            self.enemies.append(Koopa(tx, ground_y - 48))

        # 分散的金币
        for cx in [200, 440, 640, 820, 1060, 1250, 1400, 1550, 1750, 1950]:
            coin = Coin(cx, ground_y - 100, False)
            coin.vy = 0
            self.coins.append(coin)

        # 隐藏的金币（上方悬浮）
        hidden_coin_positions = [
            (300, 280), (460, 200), (700, 200),
            (1150, 280), (1180, 280), (1210, 280)
        ]
        for cx, cy in hidden_coin_positions:
            c = Coin(cx, cy, False)
            c.vy = 0
            self.coins.append(c)

        # 旗子 - 关卡终点
        self.flag = Flag(2400, ground_y - 320)

        # 更多平台和敌人（后半段）
        for bx in range(1500, 1700, TILE_SIZE):
            self.platforms.append(Brick(bx, 380, "brick"))

        for bx in range(1850, 2050, TILE_SIZE):
            self.platforms.append(Brick(bx, 340, "brick"))

        for bx in range(2200, 2400, TILE_SIZE):
            self.platforms.append(Brick(bx, 420, "brick"))

        # 补充敌人
        for ex in [2300, 2450]:
            self.enemies.append(Goomba(ex, ground_y - 32))

    def _build_pipe(self, x: int, y: int, width: int, height: int):
        """构建管道"""
        for py in range(y, y + height, TILE_SIZE):
            for px in range(x, x + width, TILE_SIZE):
                self.platforms.append(Brick(px, py, "pipe"))

    def update(self):
        for e in self.enemies:
            e.update(self.platforms)
        for item in self.items:
            item.update(self.platforms)
        for c in self.coins:
            c.update()
        self.particles.update()

    def draw(self, surface: pygame.Surface, camera_x: int):
        # 天空背景
        surface.fill(SKY_BLUE)

        # 云朵装饰
        self._draw_clouds(surface, camera_x)

        # 平台
        for plat in self.platforms:
            plat.draw(surface, camera_x)

        # 敌人
        for e in self.enemies:
            if e.alive or (hasattr(e, 'squished') and not getattr(e, 'squished', False)):
                e.draw(surface, camera_x)

        # 物品
        for item in self.items:
            if item.active:
                item.draw(surface, camera_x)

        # 金币
        for c in self.coins:
            c.draw(surface, camera_x)

        # 粒子
        self.particles.draw(surface, camera_x)

        # 旗子
        if self.flag:
            self.flag.draw(surface, camera_x)

    def _draw_clouds(self, surface: pygame.Surface, camera_x: int):
        import random
        random.seed(42)  # 固定随机
        for i in range(15):
            cx = i * 200 + 50 - (camera_x * 0.3) % 200
            cy = 60 + (i % 3) * 40
            self._draw_cloud(surface, int(cx), int(cy))

    def _draw_cloud(self, surface: pygame.Surface, x: int, y: int):
        pygame.draw.ellipse(surface, WHITE, (x, y, 60, 30))
        pygame.draw.ellipse(surface, WHITE, (x + 15, y - 10, 40, 25))
        pygame.draw.ellipse(surface, WHITE, (x + 30, y, 50, 25))


# ==================== HUD ====================
class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 28, bold=True)
        self.font_large = pygame.font.SysFont(None, 36, bold=True)

    def draw(self, surface: pygame.Surface, mario: Mario, coins: int, lives: int, level: int):
        # 背景条
        pygame.draw.rect(surface, BLACK, (0, 0, SCREEN_WIDTH, 44))
        pygame.draw.rect(surface, (30, 30, 60), (0, 0, SCREEN_WIDTH, 44))

        # 生命
        life_text = self.font.render(f"生命: {lives}", True, WHITE)
        surface.blit(life_text, (10, 10))

        # 分数
        score_text = self.font.render(f"分数: {coins * 100}", True, WHITE)
        surface.blit(score_text, (200, 10))

        # 金币数
        coin_text = self.font.render(f"金币: {coins}", True, YELLOW)
        surface.blit(coin_text, (400, 10))

        # 关卡
        level_text = self.font.render(f"关卡 {level}", True, GREEN)
        surface.blit(level_text, (600, 10))

        # 马里奥状态
        if mario.big:
            status = "超级玛丽"
        else:
            status = "小玛丽"
        status_text = self.font.render(status, True, RED)
        surface.blit(status_text, (700, 10))


# ==================== 游戏主类 ====================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("超级玛丽 - Super Mario")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"  # start, playing, gameover, win
        self.level_num = 1
        self.score = 0
        self.lives = 3
        self.camera_x = 0
        self.max_camera_x = 2400
        self.start_screen()
        self.hud = HUD()

    def start_screen(self):
        """开始画面"""
        self.screen.fill(SKY_BLUE)
        font_title = pygame.font.SysFont(None, 60, bold=True)
        font_sub = pygame.font.SysFont(None, 30)

        title = font_title.render("超级玛丽", True, RED)
        subtitle = font_sub.render("Super Mario Clone", True, WHITE)
        prompt = font_sub.render("按 SPACE 开始游戏", True, YELLOW)

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 180))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 240))
        self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 320))

        # 操作说明
        controls = [
            "← → 或 A D : 移动",
            "空格 或 W 或 ↑ : 跳跃",
            "↓ 或 S : 下蹲(大玛丽)",
        ]
        for i, c in enumerate(controls):
            t = font_sub.render(c, True, WHITE)
            self.screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 400 + i * 30))

        pygame.display.flip()

        # 等待开始
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def reset_level(self):
        """重置关卡"""
        self.level = Level(self.level_num)
        self.mario = Mario(100, SCREEN_HEIGHT - TILE_SIZE * 4 - 48)
        self.camera_x = 0

    def start_game(self):
        """开始游戏"""
        self.reset_level()
        self.state = "playing"
        self.game_loop()

    def game_loop(self):
        """主循环"""
        while self.running:
            self.clock.tick(FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        return
                    if self.state == "playing":
                        if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                            self.mario.jump()
                        if event.key == pygame.K_r:
                            # 重置当前关卡
                            self.reset_level()

            if self.state == "playing":
                keys = pygame.key.get_pressed()
                self.update(keys)
                self.draw()

        pygame.quit()

    def update(self, keys: pygame.key):
        """更新游戏状态"""
        if self.state != "playing":
            return

        # 更新马里奥
        self.mario.update(keys, self.level.platforms)

        # 更新关卡
        self.level.update()

        # 相机跟随
        target_cam = int(self.mario.x - SCREEN_WIDTH // 3)
        self.camera_x += (target_cam - self.camera_x) * 0.1
        if self.camera_x < 0:
            self.camera_x = 0
        if self.camera_x > self.max_camera_x - SCREEN_WIDTH:
            self.camera_x = self.max_camera_x - SCREEN_WIDTH

        # 马里奥碰撞检测
        self._check_collisions()

        # 检测过关
        if self.mario.x > self.max_camera_x:
            self.state = "win"
            self.show_win_screen()

        # 检测死亡
        if self.mario.y > SCREEN_HEIGHT + 100:
            self._mario_die()

    def _check_collisions(self):
        mario = self.mario
        level = self.level

        # 碰撞敌人的逻辑
        for enemy in level.enemies[:]:
            if not enemy.alive:
                continue
            if hasattr(enemy, 'squished') and enemy.squished:
                if enemy.death_timer > 30:
                    level.enemies.remove(enemy)
                continue

            if mario.rect.colliderect(enemy.rect):
                # 判断是否从上方踩
                mario_bottom = mario.y + mario.height
                enemy_top = enemy.y + 8
                if mario.vy > 0 and mario_bottom < enemy_top + 20:
                    # 踩死敌人
                    if isinstance(enemy, Goomba):
                        enemy.stomp()
                        self.score += 100
                        level.particles.emit(enemy.x + 16, enemy.y, 8, BROWN)
                    elif isinstance(enemy, Koopa) and not enemy.shell:
                        enemy.turn_to_shell()
                        self.score += 100
                        level.particles.emit(enemy.x + 16, enemy.y, 8, GREEN)
                    elif isinstance(enemy, Koopa) and enemy.shell:
                        # 踢龟壳
                        enemy.vx = mario.facing.value * 8
                        enemy.active = True
                        self.score += 400
                else:
                    # 碰到敌人
                    if mario.invincible <= 0:
                        if mario.big:
                            mario.make_small()
                            sound_manager.play("powerup")
                        else:
                            self._mario_die()

        # 碰撞物品（金币、蘑菇）
        for item in level.items[:]:
            if not item.active:
                continue
            if mario.rect.colliderect(item.rect):
                if isinstance(item, Coin):
                    item.collected = True
                    level.coin_count += 1
                    self.score += 200
                    sound_manager.play("coin")
                    level.particles.emit(item.x + 12, item.y + 16, 5, YELLOW)
                elif isinstance(item, Mushroom):
                    item.active = False
                    mario.make_big()
                    self.score += 1000
                    level.particles.emit(item.x + 16, item.y + 16, 10, RED)
                level.items.remove(item)

        # 碰撞问号砖块
        for brick in level.platforms:
            if brick.brick_type.startswith("?block"):
                if mario.rect.colliderect(brick.rect):
                    # 从下方碰撞
                    if mario.vy < 0 and mario.y + mario.height > brick.y and mario.y < brick.y:
                        mario.vy = 0
                        mario.y = brick.rect.bottom
                        brick.hit = True

                        if brick.contains_coin:
                            # 弹出金币
                            coin = Coin(brick.x + 8, brick.y - 32, True)
                            level.coins.append(coin)
                            level.coin_count += 1
                            self.score += 200
                            sound_manager.play("coin")
                            brick.contains_coin = False
                            brick.brick_type = "?block_empty"
                        elif brick.contains_mushroom:
                            # 弹出蘑菇
                            mushroom = Mushroom(brick.x + 4, brick.y - 32)
                            level.items.append(mushroom)
                            sound_manager.play("powerup")
                            brick.contains_mushroom = False
                            brick.brick_type = "?block_empty"

        # 收集漂浮金币
        for coin in level.coins[:]:
            if not coin.from_block and not coin.collected:
                if mario.rect.colliderect(coin.rect):
                    coin.collected = True
                    level.coin_count += 1
                    self.score += 100
                    sound_manager.play("coin")
                    level.particles.emit(coin.x + 12, coin.y + 16, 5, YELLOW)
                    level.coins.remove(coin)

        # 检测旗子碰撞（过关）
        if level.flag:
            flag = level.flag
            mario_rect = create_rect(mario.x, mario.y, mario.width, mario.height)
            flag_rect = create_rect(flag.x, flag.y, flag.width, flag.height)
            if mario_rect.colliderect(flag_rect):
                if not mario.reached_flag:
                    mario.reached_flag = True
                    sound_manager.play("flag")

    def _mario_die(self):
        self.mario.dead = True
        self.mario.vy = -12
        sound_manager.play("death")
        self.lives -= 1

        pygame.time.delay(2000)
        if self.lives <= 0:
            self.state = "gameover"
            self.show_gameover_screen()
        else:
            self.reset_level()

    def draw(self):
        """渲染"""
        self.screen.fill(SKY_BLUE)

        # 绘制关卡
        self.level.draw(self.screen, int(self.camera_x))

        # 绘制马里奥
        self.mario.draw(self.screen, int(self.camera_x))

        # 绘制HUD
        self.hud.draw(self.screen, self.mario, self.level.coin_count, self.lives, self.level_num)

        pygame.display.flip()

    def show_gameover_screen(self):
        """游戏结束画面"""
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(None, 50, bold=True)
        font_small = pygame.font.SysFont(None, 30)

        go_text = font.render("GAME OVER", True, RED)
        score_text = font_small.render(f"最终得分: {self.score}", True, WHITE)
        restart = font_small.render("按 R 重新开始", True, YELLOW)

        self.screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, 200))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 270))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 330))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.lives = 3
                        self.score = 0
                        self.level_num = 1
                        waiting = False
                        self.start_game()

    def show_win_screen(self):
        """过关画面"""
        self.screen.fill(SKY_BLUE)
        font = pygame.font.SysFont(None, 50, bold=True)
        font_small = pygame.font.SysFont(None, 30)

        win_text = font.render("过关！", True, GREEN)
        score_text = font_small.render(f"得分: {self.score}  金币: {self.level.coin_count}", True, WHITE)
        prompt = font_small.render("按 SPACE 进入下一关", True, YELLOW)

        self.screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 200))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 270))
        self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 330))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.level_num += 1
                        self.score += self.level.coin_count * 200
                        waiting = False
                        self.reset_level()
                        self.state = "playing"


# ==================== 主程序 ====================
if __name__ == "__main__":
    game = Game()
    game.start_game()
