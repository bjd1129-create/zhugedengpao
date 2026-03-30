"""
扫雷游戏 - Minesweeper
使用 Python + Pygame 实现的经典扫雷游戏
"""

import pygame
import sys
import random
from enum import Enum
from typing import List, Set, Tuple, Optional

# ============ 配置常量 ============
class Config:
    # 窗口设置
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    
    # 游戏板设置
    ROWS = 16
    COLS = 30
    CELL_SIZE = 25
    CELL_GAP = 1
    
    # 颜色
    BG_COLOR = (200, 200, 200)
    CELL_UNREVEALED = (150, 150, 150)
    CELL_REVEALED = (220, 220, 220)
    CELL_MINE = (255, 0, 0)
    CELL_FLAG = (255, 150, 0)
    CELL_WRONG_FLAG = (255, 100, 100)
    TEXT_COLOR = (0, 0, 0)
    FLAG_COLOR = (255, 100, 0)
    MINE_COLOR = (0, 0, 0)
    
    # 数字颜色 (1-8)
    NUMBER_COLORS = [
        None,
        (0, 0, 255),      # 1 - 蓝色
        (0, 128, 0),       # 2 - 绿色
        (255, 0, 0),       # 3 - 红色
        (0, 0, 128),       # 4 - 深蓝
        (128, 0, 0),       # 5 - 深红
        (0, 128, 128),     # 6 - 青色
        (0, 0, 0),         # 7 - 黑色
        (128, 128, 128),   # 8 - 灰色
    ]
    
    # 游戏设置
    MINE_COUNT = 99
    MIN_ROWS = 9
    MIN_COLS = 9
    MIN_CELL_SIZE = 20
    MAX_CELL_SIZE = 40
    
    # 标题栏高度
    HEADER_HEIGHT = 50


# ============ 游戏状态枚举 ============
class GameState(Enum):
    READY = 0      # 准备开始
    PLAYING = 1   # 游戏中
    WON = 2       # 胜利
    LOST = 3      # 失败


# ============ 单元格类 ============
class Cell:
    """游戏板上的单个单元格"""
    
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
    
    def __repr__(self):
        state = "M" if self.is_mine else str(self.neighbor_mines)
        if self.is_flagged:
            state = "F"
        if not self.is_revealed:
            state = "?"
        return f"Cell({self.row},{self.col}):{state}"
    
    def get_rect(self) -> pygame.Rect:
        """获取单元格在屏幕上的矩形区域"""
        x = self.col * (Config.CELL_SIZE + Config.CELL_GAP)
        y = Config.HEADER_HEIGHT + self.row * (Config.CELL_SIZE + Config.CELL_GAP)
        return pygame.Rect(x, y, Config.CELL_SIZE, Config.CELL_SIZE)
    
    def draw(self, surface: pygame.Surface):
        """绘制单元格"""
        rect = self.get_rect()
        
        if self.is_revealed:
            # 已翻开的单元格
            if self.is_mine:
                # 地雷
                pygame.draw.rect(surface, Config.CELL_MINE, rect)
                self._draw_mine(surface, rect)
            else:
                # 空白或数字
                pygame.draw.rect(surface, Config.CELL_REVEALED, rect)
                if self.neighbor_mines > 0:
                    self._draw_number(surface, rect, self.neighbor_mines)
        else:
            # 未翻开的单元格
            if self.is_flagged:
                pygame.draw.rect(surface, Config.CELL_UNREVEALED, rect)
                self._draw_flag(surface, rect)
            else:
                pygame.draw.rect(surface, Config.CELL_UNREVEALED, rect)
                self._draw_tile(surface, rect)
        
        # 边框
        pygame.draw.rect(surface, (100, 100, 100), rect, 1)
    
    def _draw_mine(self, surface: pygame.Surface, rect: pygame.Rect):
        """绘制地雷图标"""
        center = rect.center
        radius = Config.CELL_SIZE // 3
        pygame.draw.circle(surface, Config.MINE_COLOR, center, radius)
        # 绘制十字
        pygame.draw.line(surface, Config.MINE_COLOR, 
                        (center[0] - radius, center[1]),
                        (center[0] + radius, center[1]), 2)
        pygame.draw.line(surface, Config.MINE_COLOR,
                        (center[0], center[1] - radius),
                        (center[0], center[1] + radius), 2)
    
    def _draw_flag(self, surface: pygame.Surface, rect: pygame.Rect):
        """绘制旗帜"""
        center = rect.center
        # 旗杆
        pygame.draw.line(surface, Config.FLAG_COLOR,
                        (center[0], rect.top + 3),
                        (center[0], rect.bottom - 3), 2)
        # 旗帜
        flag_points = [
            (center[0], rect.top + 3),
            (center[0] + 8, rect.top + 6),
            (center[0], rect.top + 9)
        ]
        pygame.draw.polygon(surface, Config.FLAG_COLOR, flag_points)
    
    def _draw_number(self, surface: pygame.Surface, rect: pygame.Rect, number: int):
        """绘制数字"""
        font = pygame.font.Font(None, Config.CELL_SIZE - 4)
        text = font.render(str(number), True, Config.NUMBER_COLORS[number])
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
    
    def _draw_tile(self, surface: pygame.Surface, rect: pygame.Rect):
        """绘制未翻开格子的3D效果"""
        # 浅色边框（左上）
        pygame.draw.line(surface, (255, 255, 255), rect.topleft, rect.midtop, 2)
        pygame.draw.line(surface, (255, 255, 255), rect.topleft, rect.midleft, 2)
        # 深色边框（右下）
        pygame.draw.line(surface, (80, 80, 80), rect.bottomleft, rect.midbottom, 2)
        pygame.draw.line(surface, (80, 80, 80), rect.bottomright, rect.midright, 2)


# ============ 游戏板类 ============
class Board:
    """游戏板管理"""
    
    def __init__(self, rows: int, cols: int, mine_count: int):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.cells: List[List[Cell]] = []
        self.mines_placed = False
        self.flag_count = 0
        self.revealed_count = 0
        self._init_cells()
    
    def _init_cells(self):
        """初始化所有单元格"""
        self.cells = []
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                row_cells.append(Cell(row, col))
            self.cells.append(row_cells)
    
    def _in_bounds(self, row: int, col: int) -> bool:
        """检查坐标是否在边界内"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def _get_neighbors(self, row: int, col: int) -> List[Cell]:
        """获取指定单元格的邻居"""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self._in_bounds(nr, nc):
                    neighbors.append(self.cells[nr][nc])
        return neighbors
    
    def place_mines(self, exclude_row: int, exclude_col: int):
        """随机布雷，排除第一次点击的位置及其邻居"""
        # 获取需要排除的区域
        exclude_set = set()
        exclude_set.add((exclude_row, exclude_col))
        for cell in self._get_neighbors(exclude_row, exclude_col):
            exclude_set.add((cell.row, cell.col))
        
        # 可放置的位置
        available = []
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in exclude_set:
                    available.append((row, col))
        
        # 随机布雷
        mines_to_place = min(self.mine_count, len(available))
        mine_positions = random.sample(available, mines_to_place)
        
        for row, col in mine_positions:
            self.cells[row][col].is_mine = True
        
        # 计算每个格子的邻居雷数
        self._calculate_neighbors()
        self.mines_placed = True
    
    def _calculate_neighbors(self):
        """计算每个单元格的邻居雷数"""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if not cell.is_mine:
                    neighbors = self._get_neighbors(row, col)
                    cell.neighbor_mines = sum(1 for n in neighbors if n.is_mine)
    
    def reveal(self, row: int, col: int) -> bool:
        """翻开格子，返回是否触雷"""
        if not self._in_bounds(row, col):
            return False
        
        cell = self.cells[row][col]
        if cell.is_revealed or cell.is_flagged:
            return False
        
        cell.is_revealed = True
        self.revealed_count += 1
        
        if cell.is_mine:
            return True
        
        # 如果周围没有雷，自动翻开邻居
        if cell.neighbor_mines == 0:
            for neighbor in self._get_neighbors(row, col):
                if not neighbor.is_revealed and not neighbor.is_flagged:
                    self.reveal(neighbor.row, neighbor.col)
        
        return False
    
    def toggle_flag(self, row: int, col: int) -> bool:
        """切换旗帜，返回是否成功"""
        if not self._in_bounds(row, col):
            return False
        
        cell = self.cells[row][col]
        if cell.is_revealed:
            return False
        
        cell.is_flagged = not cell.is_flagged
        self.flag_count += 1 if cell.is_flagged else -1
        return True
    
    def check_win(self) -> bool:
        """检查是否获胜"""
        total_cells = self.rows * self.cols
        non_mine_cells = total_cells - self.mine_count
        return self.revealed_count == non_mine_cells
    
    def get_all_mines(self) -> List[Tuple[int, int]]:
        """获取所有地雷位置"""
        mines = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_mine:
                    mines.append((row, col))
        return mines
    
    def reveal_all_mines(self):
        """显示所有地雷"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_mine:
                    self.cells[row][col].is_revealed = True
    
    def reveal_wrong_flags(self):
        """显示所有错误旗帜"""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if cell.is_flagged and not cell.is_mine:
                    cell.is_revealed = True  # 标记为显示错误
    
    def draw(self, surface: pygame.Surface):
        """绘制整个游戏板"""
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].draw(surface)


# ============ 游戏类 ============
class Minesweeper:
    """扫雷游戏主类"""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("扫雷 - Minesweeper")
        
        # 计算窗口大小
        board_width = Config.COLS * (Config.CELL_SIZE + Config.CELL_GAP) + Config.CELL_GAP
        board_height = Config.ROWS * (Config.CELL_SIZE + Config.CELL_GAP) + Config.CELL_GAP
        Config.WINDOW_WIDTH = board_width
        Config.WINDOW_HEIGHT = board_height + Config.HEADER_HEIGHT
        
        self.screen = pygame.display.set_mode(
            (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.board = Board(Config.ROWS, Config.COLS, Config.MINE_COUNT)
        self.state = GameState.READY
        self.start_time = 0
        self.elapsed_time = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.running = True
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                elif event.key == pygame.K_r:
                    self.reset_game()
                    return
                elif event.key == pygame.K_q:
                    self.running = False
                    return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < Config.HEADER_HEIGHT:
                    # 点击了标题栏，忽略
                    continue
                
                mouse_pos = event.pos
                col = mouse_pos[0] // (Config.CELL_SIZE + Config.CELL_GAP)
                row = (mouse_pos[1] - Config.HEADER_HEIGHT) // (Config.CELL_SIZE + Config.CELL_GAP)
                
                if not self.board._in_bounds(row, col):
                    continue
                
                cell = self.board.cells[row][col]
                
                if self.state == GameState.WON or self.state == GameState.LOST:
                    if event.button == 1:  # 左键重新开始
                        self.reset_game()
                    continue
                
                if cell.is_revealed:
                    # 如果是数字，尝试批量标记
                    if cell.neighbor_mines > 0:
                        self._chord_click(row, col)
                    continue
                
                if event.button == 1:  # 左键 - 翻开
                    self._left_click(row, col)
                elif event.button == 3:  # 右键 - 标记旗帜
                    self._right_click(row, col)
    
    def _left_click(self, row: int, col: int):
        """处理左键点击"""
        if self.state == GameState.READY:
            # 第一次点击，开始计时
            self.board.place_mines(row, col)
            self.state = GameState.PLAYING
            self.start_time = pygame.time.get_ticks()
        
        if self.board.cells[row][col].is_flagged:
            # 有旗帜的不能翻开
            return
        
        hit_mine = self.board.reveal(row, col)
        
        if hit_mine:
            self.state = GameState.LOST
            self.board.reveal_all_mines()
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        elif self.board.check_win():
            self.state = GameState.WON
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
    
    def _right_click(self, row: int, col: int):
        """处理右键点击"""
        if self.state == GameState.READY:
            # 第一次右键也可以开始
            self.state = GameState.PLAYING
            self.start_time = pygame.time.get_ticks()
        
        if self.state != GameState.PLAYING:
            return
        
        self.board.toggle_flag(row, col)
    
    def _chord_click(self, row: int, col: int):
        """中键/和弦点击 - 快速标记周围未标记的格子"""
        cell = self.board.cells[row][col]
        if not cell.is_revealed or cell.neighbor_mines == 0:
            return
        
        # 找出周围未翻开的格子
        neighbors = self.board._get_neighbors(row, col)
        flagged = sum(1 for n in neighbors if n.is_flagged)
        
        # 如果旗帜数等于数字，翻开所有未标记的邻居
        if flagged == cell.neighbor_mines:
            for neighbor in neighbors:
                if not neighbor.is_revealed and not neighbor.is_flagged:
                    if self.state == GameState.READY:
                        self.board.place_mines(neighbor.row, neighbor.col)
                        self.state = GameState.PLAYING
                        self.start_time = pygame.time.get_ticks()
                    
                    hit_mine = self.board.reveal(neighbor.row, neighbor.col)
                    if hit_mine:
                        self.state = GameState.LOST
                        self.board.reveal_all_mines()
                        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                        return
    
    def reset_game(self):
        """重置游戏"""
        self.board = Board(Config.ROWS, Config.COLS, Config.MINE_COUNT)
        self.state = GameState.READY
        self.start_time = 0
        self.elapsed_time = 0
    
    def draw_header(self):
        """绘制标题栏"""
        # 背景
        pygame.draw.rect(self.screen, (180, 180, 180), 
                        (0, 0, Config.WINDOW_WIDTH, Config.HEADER_HEIGHT))
        pygame.draw.line(self.screen, (100, 100, 100),
                        (0, Config.HEADER_HEIGHT - 1),
                        (Config.WINDOW_WIDTH, Config.HEADER_HEIGHT - 1), 2)
        
        # 地雷计数
        remaining = Config.MINE_COUNT - self.board.flag_count
        mine_text = self.font.render(f"💣 {remaining:03d}", True, (0, 0, 0))
        self.screen.blit(mine_text, (10, 10))
        
        # 计时器
        if self.state == GameState.PLAYING:
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        else:
            elapsed = self.elapsed_time
        time_text = self.font.render(f"⏱ {elapsed:03d}", True, (0, 0, 0))
        time_rect = time_text.get_rect(topright=(Config.WINDOW_WIDTH - 10, 10))
        self.screen.blit(time_text, time_rect)
        
        # 游戏状态提示
        if self.state == GameState.WON:
            status = "🎉 胜利!"
        elif self.state == GameState.LOST:
            status = "💥 失败!"
        else:
            status = "🚩 按R重新开始"
        
        status_text = self.small_font.render(status, True, (0, 0, 0))
        status_rect = status_text.get_rect(center=(Config.WINDOW_WIDTH // 2, Config.HEADER_HEIGHT // 2))
        self.screen.blit(status_text, status_rect)
    
    def draw_instructions(self):
        """绘制操作说明"""
        if self.state != GameState.READY:
            return
        
        font = pygame.font.Font(None, 20)
        text = "左键翻开 | 右键标记旗帜 | R重新开始 | ESC退出"
        instruction = font.render(text, True, (100, 100, 100))
        # 居中显示在标题栏
        rect = instruction.get_rect(center=(Config.WINDOW_WIDTH // 2, Config.HEADER_HEIGHT // 2 + 15))
        self.screen.blit(instruction, rect)
    
    def draw(self):
        """绘制画面"""
        self.screen.fill(Config.BG_COLOR)
        
        # 标题栏
        self.draw_header()
        if self.state == GameState.READY:
            self.draw_instructions()
        
        # 游戏板
        self.board.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """游戏主循环"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


# ============ 主程序入口 ============
if __name__ == "__main__":
    game = Minesweeper()
    game.run()
