"""
俄罗斯方块 - Python + Pygame 版
面向对象设计，支持旋转、消行、等级加速、预览、最高分记录
"""

import pygame
import random
import json
import os

# ─── 常量 ───────────────────────────────────────────────
BLOCK_SIZE   = 30
GRID_WIDTH   = 10
GRID_HEIGHT  = 20
SCREEN_WIDTH  = BLOCK_SIZE * GRID_WIDTH  + 200   # 右侧留白给信息面板
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
FPS          = 60

# 颜色
COLORS = {
    'bg':        (20, 20, 30),
    'grid_line': (40, 40, 60),
    'text':      (255, 255, 255),
    'panel':     (30, 30, 50),
    'I': (0, 240, 240),
    'O': (240, 240, 0),
    'T': (160, 0, 240),
    'S': (0, 240, 0),
    'Z': (240, 0, 0),
    'J': (0, 0, 240),
    'L': (255, 165, 0),
}

# ─── 方块定义 ───────────────────────────────────────────
# 每个形状的4个旋转状态（用坐标偏移表示）
SHAPES = {
    'I': [[[0,1],[1,1],[2,1],[3,1]], [[2,0],[2,1],[2,2],[2,3]],
          [[0,2],[1,2],[2,2],[3,2]], [[1,0],[1,1],[1,2],[1,3]]],
    'O': [[[1,0],[2,0],[1,1],[2,1]], [[1,0],[2,0],[1,1],[2,1]],
          [[1,0],[2,0],[1,1],[2,1]], [[1,0],[2,0],[1,1],[2,1]]],
    'T': [[[1,0],[0,1],[1,1],[2,1]], [[1,0],[1,1],[2,1],[1,2]],
          [[0,1],[1,1],[2,1],[1,2]], [[1,0],[0,1],[1,1],[1,2]]],
    'S': [[[1,0],[2,0],[0,1],[1,1]], [[1,0],[1,1],[2,1],[2,2]],
          [[1,1],[2,1],[0,2],[1,2]], [[0,0],[0,1],[1,1],[1,2]]],
    'Z': [[[0,0],[1,0],[1,1],[2,1]], [[2,0],[1,1],[2,1],[1,2]],
          [[0,1],[1,1],[1,2],[2,2]], [[1,0],[0,1],[1,1],[0,2]]],
    'J': [[[0,0],[0,1],[1,1],[2,1]], [[0,0],[1,0],[0,1],[0,2]],
          [[0,1],[1,1],[2,1],[2,2]], [[1,0],[1,1],[0,2],[1,2]]],
    'L': [[[2,0],[0,1],[1,1],[2,1]], [[0,0],[0,1],[0,2],[1,2]],
          [[0,1],[1,1],[2,1],[0,2]], [[0,0],[1,0],[1,1],[1,2]]],
}

# 分数表
SCORE_TABLE = {1: 100, 2: 300, 3: 700, 4: 1500}
# 初始下落间隔（毫秒），每升一级减少
INIT_DROP_INTERVAL = 800
DROP_INTERVAL_DEC  = 50
MIN_DROP_INTERVAL  = 100

SCORE_FILE = os.path.join(os.path.dirname(__file__), 'tetris_highscore.json')

# ─── 辅助函数 ───────────────────────────────────────────
def load_highscore():
    try:
        with open(SCORE_FILE, 'r') as f:
            return json.load(f).get('highscore', 0)
    except Exception:
        return 0

def save_highscore(score):
    try:
        with open(SCORE_FILE, 'w') as f:
            json.dump({'highscore': score}, f)
    except Exception:
        pass

# ─── Tetromino 类 ───────────────────────────────────────
class Tetromino:
    def __init__(self, shape_name=None):
        self.shape_name = shape_name or random.choice(list(SHAPES.keys()))
        self.rotation  = 0
        self.color     = self.shape_name
        self._sync_blocks()

    def _sync_blocks(self):
        self.blocks = [list(b) for b in SHAPES[self.shape_name][self.rotation]]

    def rotate(self):
        prev = self.rotation
        self.rotation = (self.rotation + 1) % 4
        self._sync_blocks()
        return self.blocks

    def unrotate(self):
        self.rotation = (self.rotation - 1) % 4
        self._sync_blocks()

    @property
    def x(self):
        return self.blocks[0][0] if self.blocks else 0

    @property
    def y(self):
        return self.blocks[0][1] if self.blocks else 0

# ─── Board 类 ────────────────────────────────────────────
class Board:
    def __init__(self):
        # 2D list，None 表示空，字符串表示颜色key
        self.grid = [[None] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def inside(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def occupied(self, x, y):
        if not self.inside(x, y):
            return True
        return self.grid[y][x] is not None

    def place(self, tetromino, ox, oy, color):
        for bx, by in tetromino.blocks:
            gx, gy = ox + bx, oy + by
            if self.inside(gx, gy):
                self.grid[gy][gx] = color

    def full_line_rows(self):
        rows = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(GRID_WIDTH)):
                rows.append(y)
        return rows

    def clear_lines(self, rows):
        rows.sort(reverse=True)
        for r in rows:
            del self.grid[r]
            self.grid.insert(0, [None] * GRID_WIDTH)

    def game_over(self):
        return any(self.grid[0][x] is not None for x in range(GRID_WIDTH))

# ─── TetrisGame 类 ──────────────────────────────────────
class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')
        self.clock  = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_norm  = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)

        self.highscore = load_highscore()
        self._reset()

    def _reset(self):
        self.board    = Board()
        self.score    = 0
        self.level    = 1
        self.lines    = 0
        self.current  = Tetromino()
        self.next     = Tetromino()
        self.game_over_flag = False
        self.paused   = False
        self.last_drop = pygame.time.get_ticks()
        self.drop_interval = INIT_DROP_INTERVAL

    def drop_interval_for(self, level):
        return max(MIN_DROP_INTERVAL, INIT_DROP_INTERVAL - (level - 1) * DROP_INTERVAL_DEC)

    # ── 碰撞检测 ──
    def _collide(self, tetromino, ox, oy):
        for bx, by in tetromino.blocks:
            if self.board.occupied(ox + bx, oy + by):
                return True
        return False

    # ── 移动 ──
    def move(self, dx):
        if self.game_over_flag or self.paused:
            return
        if not self._collide(self.current, self.current.x + dx, self.current.y):
            # 原地不动时同步x坐标
            for i, (bx, by) in enumerate(self.current.blocks):
                self.current.blocks[i][0] += dx

    def rotate(self):
        if self.game_over_flag or self.paused:
            return
        self.current.rotate()
        # 旋转后检测冲突，尝试墙踢
        if self._collide(self.current, self.current.x, self.current.y):
            for kick in [1, -1, 2, -2]:
                if not self._collide(self.current, self.current.x + kick, self.current.y):
                    for i in range(len(self.current.blocks)):
                        self.current.blocks[i][0] += kick
                    return
            self.current.unrotate()  # 无法旋转则还原

    def hard_drop(self):
        if self.game_over_flag or self.paused:
            return
        while not self._collide(self.current, self.current.x, self.current.y + 1):
            for i in range(len(self.current.blocks)):
                self.current.blocks[i][1] += 1
        self._lock()

    def _lock(self):
        self.board.place(self.current, self.current.x, self.current.y, self.current.color)
        rows = self.board.full_line_rows()
        if rows:
            self.board.clear_lines(rows)
            self.lines += len(rows)
            self.score  += SCORE_TABLE.get(len(rows), 0) * self.level
            self.level   = self.lines // 10 + 1
            self.drop_interval = self.drop_interval_for(self.level)
        if self.board.game_over():
            self.game_over_flag = True
            if self.score > self.highscore:
                self.highscore = self.score
                save_highscore(self.highscore)
        else:
            self.current = self.next
            self.next     = Tetromino()

    # ── 重力下落 ──
    def tick(self):
        if self.game_over_flag or self.paused:
            return
        now = pygame.time.get_ticks()
        if now - self.last_drop >= self.drop_interval:
            self.last_drop = now
            if not self._collide(self.current, self.current.x, self.current.y + 1):
                for i in range(len(self.current.blocks)):
                    self.current.blocks[i][1] += 1
            else:
                self._lock()

    # ── 渲染 ──────────────────────────────────────────────
    def _draw_block(self, surface, gx, gy, color_key, alpha=255):
        rect = pygame.Rect(gx * BLOCK_SIZE, gy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        color = COLORS.get(color_key, (200, 200, 200))
        pygame.draw.rect(surface, color, rect)
        # 高光边框
        highlight = tuple(min(255, c + 60) for c in color)
        pygame.draw.line(surface, highlight, rect.topleft, rect.topright, 2)
        pygame.draw.line(surface, highlight, rect.topleft, rect.bottomleft, 2)
        # 阴影
        shadow = tuple(max(0, c - 60) for c in color)
        pygame.draw.line(surface, shadow, rect.bottomleft, rect.bottomright, 2)
        pygame.draw.line(surface, shadow, rect.topright, rect.bottomright, 2)

    def _draw_board(self, surface):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board.grid[y][x]:
                    self._draw_block(surface, x, y, self.board.grid[y][x])

    def _draw_current(self, surface):
        for bx, by in self.current.blocks:
            self._draw_block(surface, bx, by, self.current.color)

    def _draw_preview(self, surface):
        px = GRID_WIDTH * BLOCK_SIZE + 20
        surface.blit(self.font_norm.render('NEXT', True, COLORS['text']), (px, 20))
        for bx, by in self.next.blocks:
            ox = px + bx * BLOCK_SIZE // 2
            oy = 60 + by * BLOCK_SIZE // 2
            bw = BLOCK_SIZE // 2
            color = COLORS.get(self.next.color, (200, 200, 200))
            rect = pygame.Rect(ox, oy, bw, bw)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (255,255,255), rect, 1)

    def _draw_panel(self, surface):
        px = GRID_WIDTH * BLOCK_SIZE + 10
        # 信息面板背景
        panel_rect = pygame.Rect(px, 0, SCREEN_WIDTH - px, SCREEN_HEIGHT)
        pygame.draw.rect(surface, COLORS['panel'], panel_rect)
        pygame.draw.line(surface, COLORS['grid_line'], panel_rect.topleft, panel_rect.bottomleft, 2)

        self._draw_preview(surface)

        y = 180
        items = [
            (f'SCORE: {self.score}', self.font_norm),
            (f'LEVEL: {self.level}',  self.font_norm),
            (f'LINES: {self.lines}',  self.font_norm),
            ('',                      self.font_small),
            (f'BEST: {self.highscore}', self.font_norm),
        ]
        for text, font in items:
            surface.blit(font.render(text, True, COLORS['text']), (px + 10, y))
            y += 35

        # 操作提示
        y = 380
        tips = ['↑ / Z : 旋转', '← → : 左右', '↓ : 加速', '空格: 硬降', 'P: 暂停', 'R: 重新开始']
        for tip in tips:
            surface.blit(self.font_small.render(tip, True, (150,150,180)), (px + 10, y))
            y += 25

    def _draw_grid(self, surface):
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(surface, COLORS['grid_line'],
                             (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(surface, COLORS['grid_line'],
                             (0, y * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))

    def _draw_game_over(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        msg1 = self.font_large.render('GAME OVER', True, (255, 80, 80))
        msg2 = self.font_norm.render(f'最终得分: {self.score}', True, COLORS['text'])
        msg3 = self.font_norm.render('按 R 重新开始', True, (150, 150, 150))
        surface.blit(msg1, (SCREEN_WIDTH // 2 - msg1.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        surface.blit(msg2, (SCREEN_WIDTH // 2 - msg2.get_width() // 2, SCREEN_HEIGHT // 2))
        surface.blit(msg3, (SCREEN_WIDTH // 2 - msg3.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def _draw_paused(self, surface):
        msg = self.font_large.render('PAUSED', True, (255, 255, 100))
        surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

    def render(self):
        self.screen.fill(COLORS['bg'])
        self._draw_grid(self.screen)
        self._draw_board(self.screen)
        if not self.game_over_flag:
            self._draw_current(self.screen)
        self._draw_panel(self.screen)
        if self.game_over_flag:
            self._draw_game_over(self.screen)
        elif self.paused:
            self._draw_paused(self.screen)
        pygame.display.flip()

    # ── 事件处理 ──
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._reset()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif not self.game_over_flag and not self.paused:
                    if event.key in (pygame.K_UP, pygame.K_z):
                        self.rotate()
                    elif event.key == pygame.K_LEFT:
                        self.move(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1)
                    elif event.key == pygame.K_DOWN:
                        self.move(0)   # 加速下落一格
                        # 手动下落一格
                        if not self._collide(self.current, self.current.x, self.current.y + 1):
                            for i in range(len(self.current.blocks)):
                                self.current.blocks[i][1] += 1
                        self.last_drop = pygame.time.get_ticks()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
        return True

    # ── 主循环 ──
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.tick()
            self.render()
        pygame.quit()

# ─── 入口 ────────────────────────────────────────────────
if __name__ == '__main__':
    TetrisGame().run()
