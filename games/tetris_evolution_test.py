#!/usr/bin/env python3
"""
俄罗斯方块 - 进化基准测试版
小花出品 · 2026-03-30
"""

import pygame
import random
import sys
from enum import Enum

# =============================================================================
# 常量定义
# =============================================================================

BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 颜色
COLOR_BG = (20, 20, 30)
COLOR_GRID = (40, 40, 55)
COLOR_WHITE = (220, 220, 235)
COLOR_GHOST = (80, 80, 100)
COLOR_PANEL_BG = (28, 28, 42)

# 方块颜色 (每种形状对应一个颜色)
COLORS = [
    (0, 220, 220),    # I 青色
    (220, 220, 0),    # O 黄色
    (160, 0, 220),    # T 紫色
    (0, 0, 220),      # J 蓝色
    (220, 120, 0),    # L 橙色
    (0, 220, 0),      # S 绿色
    (220, 0, 0),      # Z 红色
]

# 计分表
SCORE_TABLE = {
    1: 100,
    2: 300,
    3: 600,
    4: 1000,
}

# =============================================================================
# 方块形状定义 (每个形状4个旋转状态)
# =============================================================================

SHAPES = [
    # I
    [[1, 1, 1, 1]],
    # O
    [[1, 1], [1, 1]],
    # T
    [[0, 1, 0], [1, 1, 1]],
    # J
    [[1, 0, 0], [1, 1, 1]],
    # L
    [[0, 0, 1], [1, 1, 1]],
    # S
    [[0, 1, 1], [1, 1, 0]],
    # Z
    [[1, 1, 0], [0, 1, 1]],
]

# 每种形状的初始位置 (保证生成时在可见区域上方)
SPAWN_POSITIONS = [
    (-1, 3),  # I 从上方
    (0, 4),   # O
    (0, 4),   # T
    (0, 4),   # J
    (0, 4),   # L
    (0, 4),   # S
    (0, 4),   # Z
]

# =============================================================================
# 游戏状态枚举
# =============================================================================

class GameState(Enum):
    START = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4


# =============================================================================
# Tetromino 类 - 方块逻辑
# =============================================================================

class Tetromino:
    """单个方块对象，管理形状、位置、旋转"""

    def __init__(self, shape_idx=None):
        if shape_idx is None:
            shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape_idx = shape_idx
        self.color = COLORS[shape_idx]
        self.rotation = 0
        self.x, self.y = SPAWN_POSITIONS[shape_idx]
        self.shape = SHAPES[shape_idx]

    def clone(self):
        """返回一个深拷贝"""
        t = Tetromino(self.shape_idx)
        t.rotation = self.rotation
        t.x = self.x
        t.y = self.y
        t.shape = self.shape
        return t

    def get_matrix(self):
        """获取当前旋转状态的矩阵"""
        return self.shape

    def rotate(self, board):
        """顺时针旋转，返回是否成功"""
        old_shape = self.shape
        old_rot = self.rotation
        self.rotation = (self.rotation + 1) % 4

        # 计算新的旋转状态
        # 简单模拟：转置+反转
        matrix = [row[:] for row in self.shape]
        rows = len(matrix)
        cols = len(matrix[0])
        rotated = [[matrix[rows - 1 - r][c] for r in range(rows)] for c in range(cols)]
        self.shape = rotated

        if self.collides(board, self.x, self.y):
            # 尝试墙踢 (wall kick) - 向左或向右偏移一格
            for dx in [1, -1, 2, -2]:
                if not self.collides(board, self.x + dx, self.y):
                    self.x += dx
                    return True
            # 恢复
            self.shape = old_shape
            self.rotation = old_rot
            return False
        return True

    def collides(self, board, x, y, shape=None):
        """检测是否与board或边界碰撞"""
        if shape is None:
            shape = self.shape
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    nx = x + c
                    ny = y + r
                    if nx < 0 or nx >= GRID_WIDTH:
                        return True
                    if ny >= GRID_HEIGHT:
                        return True
                    if ny >= 0 and board[ny][nx] != 0:
                        return True
        return False

    def move(self, dx, dy, board):
        """移动方块，返回是否成功"""
        if not self.collides(board, self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            return True
        return False

    def hard_drop(self, board):
        """硬降落：直接落到底部"""
        dropped = 0
        while not self.collides(board, self.x, self.y + 1):
            self.y += 1
            dropped += 1
        return dropped

    def get_ghost_y(self, board):
        """获取幽灵方块的Y位置"""
        gy = self.y
        while not self.collides(board, self.x, gy + 1):
            gy += 1
        return gy


# =============================================================================
# Board 类 - 游戏板管理
# =============================================================================

class Board:
    """游戏棋盘，管理所有已固定的方块"""

    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def lock(self, tetromino):
        """将方块固定到棋盘"""
        for r, row in enumerate(tetromino.shape):
            for c, cell in enumerate(row):
                if cell:
                    y = tetromino.y + r
                    x = tetromino.x + c
                    if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                        self.grid[y][x] = tetromino.color

    def clear_lines(self):
        """清除已满的行，返回消除行数"""
        cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(cell != 0 for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)
                cleared += 1
            else:
                y -= 1
        return cleared

    def is_game_over(self):
        """检测是否游戏结束（顶行有方块）"""
        return any(cell != 0 for cell in self.grid[1])


# =============================================================================
# Renderer 类 - 渲染层
# =============================================================================

class Renderer:
    """pygame渲染器，负责所有绘制"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块 - 进化基准测试")
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        """绘制游戏区域网格"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)

    def draw_block(self, x, y, color, surface=None):
        """绘制单个方块"""
        if surface is None:
            surface = self.screen
        rect = pygame.Rect(x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2, BLOCK_SIZE - 2)
        pygame.draw.rect(surface, color, rect)
        # 高光
        highlight = tuple(min(255, c + 60) for c in color)
        pygame.draw.line(surface, highlight, rect.topleft, rect.topright, 2)
        pygame.draw.line(surface, highlight, rect.topleft, rect.bottomleft, 2)

    def draw_ghost(self, tetromino):
        """绘制幽灵方块（虚影）"""
        gy = tetromino.get_ghost_y(None)  # 传None跳过board碰撞检测
        # 用board重新计算
        ghost_x = tetromino.x
        ghost_y = tetromino.y
        while True:
            for r, row in enumerate(tetromino.shape):
                for c, cell in enumerate(row):
                    if cell:
                        ny = ghost_y + r + 1
                        nx = ghost_x + c
                        if ny >= GRID_HEIGHT or (ny >= 0 and self._board_grid[ny][nx] != 0):
                            break
                else:
                    continue
                break
            else:
                ghost_y += 1
                continue
            break

        for r, row in enumerate(tetromino.shape):
            for c, cell in enumerate(row):
                if cell:
                    gy_row = ghost_y + r
                    if 0 <= gy_row < GRID_HEIGHT:
                        rect = pygame.Rect(
                            (ghost_x + c) * BLOCK_SIZE + 1,
                            gy_row * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2, BLOCK_SIZE - 2
                        )
                        pygame.draw.rect(self.screen, COLOR_GHOST, rect, 2)

    def set_board_reference(self, board):
        """设置board引用用于幽灵方块计算"""
        self._board_grid = board.grid

    def draw_board(self, board):
        """绘制已固定的方块"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if board.grid[y][x] != 0:
                    self.draw_block(x, y, board.grid[y][x])

    def draw_tetromino(self, tetromino, ghost=False):
        """绘制当前下落的方块"""
        color = COLOR_GHOST if ghost else tetromino.color
        for r, row in enumerate(tetromino.shape):
            for c, cell in enumerate(row):
                if cell:
                    y = tetromino.y + r
                    x = tetromino.x + c
                    if y >= 0:
                        self.draw_block(x, y, color)

    def draw_panel(self, score, level, lines):
        """绘制右侧信息面板"""
        px = GRID_WIDTH * BLOCK_SIZE + 10
        self.screen.fill(COLOR_PANEL_BG,
                        (px, 0, SCREEN_WIDTH - px, SCREEN_HEIGHT))

        title = self.font_medium.render("小花 · 俄罗斯方块", True, COLOR_WHITE)
        self.screen.blit(title, (px + 5, 10))

        # 分隔线
        pygame.draw.line(self.screen, COLOR_GRID,
                        (px + 5, 38), (SCREEN_WIDTH - 10, 38), 1)

        labels = [
            ("得分", f"{score:,}"),
            ("消除行数", str(lines)),
            ("等级", str(level)),
        ]
        y_offset = 55
        for label, value in labels:
            lbl = self.font_small.render(label, True, (150, 150, 170))
            val = self.font_large.render(value, True, COLOR_WHITE)
            self.screen.blit(lbl, (px + 10, y_offset))
            self.screen.blit(val, (px + 10, y_offset + 18))
            y_offset += 75

        # 操作说明
        pygame.draw.line(self.screen, COLOR_GRID,
                        (px + 5, 290), (SCREEN_WIDTH - 10, 290), 1)
        help_texts = [
            "← → 移动",
            "↑ 旋转",
            "↓ 软降",
            "空格 硬降",
            "P 暂停",
            "R 重新开始",
        ]
        y = 300
        for text in help_texts:
            surf = self.font_small.render(text, True, (130, 130, 150))
            self.screen.blit(surf, (px + 10, y))
            y += 22

    def draw_start_screen(self):
        """绘制开始界面"""
        self.screen.fill(COLOR_BG)
        title = self.font_large.render("俄罗斯方块", True, COLOR_WHITE)
        subtitle = self.font_medium.render("进化基准测试版", True, (150, 150, 180))
        hint = self.font_small.render("按 ENTER 开始游戏", True, (100, 200, 255))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2,
                                  SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2,
                                 SCREEN_HEIGHT // 2 + 40))
        pygame.display.flip()

    def draw_game_over(self, score):
        """绘制游戏结束界面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        go_text = self.font_large.render("GAME OVER", True, (220, 60, 60))
        score_text = self.font_medium.render(f"最终得分: {score:,}", True, COLOR_WHITE)
        restart = self.font_small.render("按 R 重新开始", True, (100, 200, 255))
        self.screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2,
                                    SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                       SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2,
                                    SCREEN_HEIGHT // 2 + 50))

    def draw_paused(self):
        """绘制暂停界面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        text = self.font_large.render("PAUSED", True, COLOR_WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                                SCREEN_HEIGHT // 2 - 20))

    def flip(self):
        pygame.display.flip()

    def tick(self, fps):
        self.clock.tick(fps)


# =============================================================================
# Game 类 - 游戏主逻辑
# =============================================================================

class Game:
    """游戏主控制器"""

    def __init__(self):
        self.renderer = Renderer()
        self.state = GameState.START
        self.reset()

    def reset(self):
        """重置游戏"""
        self.board = Board()
        self.renderer.set_board_reference(self.board)
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.drop_timer = 0
        self.drop_interval = 0.5  # 秒
        self.state = GameState.PLAYING
        self.lines_to_next_level = 10

    def spawn_piece(self):
        """生成新方块"""
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        # 检查游戏结束
        if self.current_piece.collides(self.board.grid, self.current_piece.x,
                                         self.current_piece.y):
            self.state = GameState.GAME_OVER

    def handle_events(self):
        """处理输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == GameState.START:
                    if event.key == pygame.K_RETURN:
                        self.reset()
                    return

                if self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset()
                    return

                if self.state == GameState.PLAYING:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.move(-1, 0, self.board.grid)
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.move(1, 0, self.board.grid)
                    elif event.key == pygame.K_UP:
                        self.current_piece.rotate(self.board.grid)
                    elif event.key == pygame.K_DOWN:
                        if self.current_piece.move(0, 1, self.board.grid):
                            self.score += 1  # 软降加分
                    elif event.key == pygame.K_SPACE:
                        dropped = self.current_piece.hard_drop(self.board.grid)
                        self.score += dropped * 2  # 硬降加分
                        self.lock_piece()
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSED

                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING

    def lock_piece(self):
        """锁定当前方块到棋盘"""
        self.board.lock(self.current_piece)
        cleared = self.board.clear_lines()
        if cleared > 0:
            self.score += SCORE_TABLE.get(cleared, 0)
            self.lines_cleared += cleared
            # 升级
            if self.lines_cleared >= self.lines_to_next_level:
                self.level += 1
                self.lines_to_next_level += self.level * 10
                self.drop_interval = max(0.05, self.drop_interval * 0.85)
        self.spawn_piece()

    def update(self, dt):
        """游戏更新"""
        if self.state != GameState.PLAYING:
            return

        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0
            if not self.current_piece.move(0, 1, self.board.grid):
                self.lock_piece()

    def render(self):
        """渲染画面"""
        self.renderer.screen.fill(COLOR_BG)

        if self.state == GameState.START:
            self.renderer.draw_start_screen()
            self.renderer.flip()
            return

        # 绘制游戏区域
        self.renderer.draw_grid()
        self.renderer.set_board_reference(self.board)

        # 幽灵方块
        self.renderer.draw_ghost(self.current_piece)

        # 棋盘已固定方块
        self.renderer.draw_board(self.board)

        # 当前方块
        self.renderer.draw_tetromino(self.current_piece)

        # 右侧面板
        self.renderer.draw_panel(self.score, self.level, self.lines_cleared)

        if self.state == GameState.GAME_OVER:
            self.renderer.draw_game_over(self.score)
        elif self.state == GameState.PAUSED:
            self.renderer.draw_paused()

        self.renderer.flip()

    def run(self):
        """主循环"""
        while True:
            dt = self.renderer.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    game = Game()
    game.run()
