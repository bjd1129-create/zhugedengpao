#!/usr/bin/env python3
"""
=================================================================
🐍 贪吃蛇AI对战系统 - 红蓝军对抗 Round 1
红方：提出贪吃蛇GUI+AI自动游玩完整方案
蓝方：严格审查所有漏洞
=================================================================
"""

import tkinter as tk
import random
import threading
import time
from collections import deque
import sys
import os

# ============ 红方代码 v1.0 ============
# 完整贪吃蛇GUI + A*寻路AI

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
CANVAS_WIDTH = CELL_SIZE * GRID_WIDTH
CANVAS_HEIGHT = CELL_SIZE * GRID_HEIGHT

class SnakeGame:
    """贪吃蛇游戏主类"""
    
    def __init__(self, master, ai_enabled=True):
        self.master = master
        self.master.title("🐍 贪吃蛇AI - 红方v1.0")
        self.ai_enabled = ai_enabled
        
        # 游戏状态
        self.score = 0
        self.game_over = False
        self.paused = False
        
        # 蛇身体 [head, body..., tail]
        self.snake = deque([(GRID_WIDTH//2, GRID_HEIGHT//2)])
        self.direction = (1, 0)  # 向右
        self.next_direction = (1, 0)
        
        # 食物
        self.food = self._spawn_food()
        
        # 创建画布
        self.canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='#1a1a2e')
        self.canvas.pack()
        
        # 控制面板
        control_frame = tk.Frame(master, bg='#16213e')
        control_frame.pack(fill=tk.X)
        
        tk.Label(control_frame, text=f"得分: {self.score}", 
                fg='#e94560', bg='#16213e', font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(control_frame, text="AI模式: 运行中", 
                fg='#0f3460', bg='#16213e', font=('Arial', 12))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        tk.Button(control_frame, text="重新开始", command=self.reset_game,
                bg='#e94560', fg='white', relief=tk.FLAT).pack(side=tk.RIGHT, padx=10)
        
        # 绑定方向键
        self.master.bind('<Left>', lambda e: self._set_direction((-1, 0)))
        self.master.bind('<Right>', lambda e: self._set_direction((1, 0)))
        self.master.bind('<Up>', lambda e: self._set_direction((0, -1)))
        self.master.bind('<Down>', lambda e: self._set_direction((0, 1)))
        self.master.bind('<space>', lambda e: self._toggle_pause())
        
        # 启动游戏
        self._draw()
        if self.ai_enabled:
            self.ai_thread = threading.Thread(target=self._ai_loop, daemon=True)
            self.ai_thread.start()
        self._game_loop()
    
    def _spawn_food(self):
        """生成食物"""
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in self.snake:
                return pos
    
    def _set_direction(self, new_dir):
        """设置方向（防止180度掉头）"""
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.next_direction = new_dir
    
    def _toggle_pause(self):
        """暂停/继续"""
        self.paused = not self.paused
    
    def _game_loop(self):
        """主游戏循环"""
        if self.game_over:
            return
        
        if not self.paused:
            self.direction = self.next_direction
            self._move_snake()
            self._check_collision()
            self._draw()
        
        # 速度：分数越高越快
        speed = max(50, 200 - self.score * 2)
        self.master.after(speed, self._game_loop)
    
    def _ai_loop(self):
        """AI控制循环"""
        while not self.game_over:
            if not self.paused:
                direction = self._get_ai_direction()
                if direction:
                    self.next_direction = direction
            time.sleep(0.05)  # AI决策频率
    
    def _get_ai_direction(self):
        """A*寻路AI"""
        head = self.snake[0]
        target = self.food
        
        # 计算到食物的最短路径
        path = self._astar(head, target)
        if path and len(path) > 1:
            next_pos = path[1]
            dx = next_pos[0] - head[0]
            dy = next_pos[1] - head[1]
            return (dx, dy)
        
        # 如果无法直达，四方向试探
        for d in [(1,0), (-1,0), (0,1), (0,-1)]:
            if d == (-self.direction[0], -self.direction[1]):
                continue
            new_head = (head[0] + d[0], head[1] + d[1])
            if self._is_safe(new_head):
                return d
        
        return None
    
    def _astar(self, start, goal):
        """A*寻路算法"""
        def heuristic(a, b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])
        
        open_set = {start}
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        
        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            
            if current == goal:
                # 重建路径
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1][1:]
            
            open_set.remove(current)
            
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                neighbor = (current[0]+dx, current[1]+dy)
                
                # 检查是否有效
                if not (0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT):
                    continue
                if neighbor in self.snake:
                    continue
                
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    open_set.add(neighbor)
        
        return []
    
    def _is_safe(self, pos):
        """检查位置是否安全"""
        if not (0 <= pos[0] < GRID_WIDTH and 0 <= pos[1] < GRID_HEIGHT):
            return False
        return pos not in self.snake
    
    def _move_snake(self):
        """移动蛇"""
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        self.snake.appendleft(new_head)
        
        if new_head == self.food:
            self.score += 10
            self.food = self._spawn_food()
        else:
            self.snake.pop()
    
    def _check_collision(self):
        """检查碰撞"""
        head = self.snake[0]
        
        # 撞墙
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
            self._game_over()
            return
        
        # 撞自己
        if head in list(self.snake)[1:]:
            self._game_over()
            return
    
    def _game_over(self):
        """游戏结束"""
        self.game_over = True
        self.canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, 
                text=f"游戏结束!\n得分: {self.score}\n按重新开始继续", 
                fill='#e94560', font=('Arial', 20, 'bold'), justify=tk.CENTER)
    
    def _draw(self):
        """绘制游戏"""
        self.canvas.delete('all')
        
        # 绘制网格（淡色）
        for x in range(0, CANVAS_WIDTH, CELL_SIZE):
            self.canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill='#2a2a4a', width=1)
        for y in range(0, CANVAS_HEIGHT, CELL_SIZE):
            self.canvas.create_line(0, y, CANVAS_WIDTH, y, fill='#2a2a4a', width=1)
        
        # 绘制食物
        fx, fy = self.food
        self.canvas.create_oval(fx*CELL_SIZE+2, fy*CELL_SIZE+2,
                (fx+1)*CELL_SIZE-2, (fy+1)*CELL_SIZE-2,
                fill='#e94560', outline='#ff6b6b')
        
        # 绘制蛇
        for i, (x, y) in enumerate(self.snake):
            if i == 0:  # 头
                self.canvas.create_rectangle(x*CELL_SIZE+1, y*CELL_SIZE+1,
                        (x+1)*CELL_SIZE-1, (y+1)*CELL_SIZE-1,
                        fill='#4ecca3', outline='#45b393', width=2)
                # 眼睛
                eye_offset = CELL_SIZE//4
                if self.direction == (1, 0):
                    self.canvas.create_oval(x*CELL_SIZE+CELL_SIZE*2//3, y*CELL_SIZE+eye_offset,
                            x*CELL_SIZE+CELL_SIZE*3//4, y*CELL_SIZE+eye_offset*2,
                            fill='black')
                    self.canvas.create_oval(x*CELL_SIZE+CELL_SIZE*2//3, y*CELL_SIZE+CELL_SIZE-eye_offset*2,
                            x*CELL_SIZE+CELL_SIZE*3//4, y*CELL_SIZE+CELL_SIZE-eye_offset,
                            fill='black')
            else:  # 身体
                color = f'#{90-i*3:02x}{180-i*5:02x}{120-i*3:02x}'
                self.canvas.create_rectangle(x*CELL_SIZE+2, y*CELL_SIZE+2,
                        (x+1)*CELL_SIZE-2, (y+1)*CELL_SIZE-2,
                        fill='#4ecca3', outline='#3db892')
        
        # 更新分数显示
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and '得分' in child.cget('text'):
                        child.config(text=f"得分: {self.score}")
    
    def reset_game(self):
        """重置游戏"""
        self.snake = deque([(GRID_WIDTH//2, GRID_HEIGHT//2)])
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.food = self._spawn_food()
        self._draw()
        if self.ai_enabled:
            self.ai_thread = threading.Thread(target=self._ai_loop, daemon=True)
            self.ai_thread.start()
        self._game_loop()


if __name__ == '__main__':
    print("=" * 60)
    print("🐍 贪吃蛇AI - 红方v1.0 | Python GUI + A*寻路")
    print("=" * 60)
    print("操作: 方向键移动 | 空格暂停 | 重新开始按钮重置")
    print("AI模式: A*寻路自动找食物")
    print("=" * 60)
    
    root = tk.Tk()
    root.configure(bg='#16213e')
    game = SnakeGame(root, ai_enabled=True)
    root.mainloop()
