"""
2048 Game - Python + Pygame
A complete, animated, object-oriented 2048 implementation.
"""

import pygame
import random
import json
import os
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
CELL_SIZE       = 120
CELL_GAP        = 12
GRID_PADDING    = 16
WINDOW_SIZE     = GRID_PADDING * 2 + 4 * CELL_SIZE + 3 * CELL_GAP
SCORE_H         = 80
WIN_H          = WINDOW_SIZE + SCORE_H

TILE_COLORS: Dict[int, Tuple[int, int, int]] = {
    0:     (204, 192, 179),
    2:     (238, 228, 218),
    4:     (237, 224, 200),
    8:     (242, 177, 121),
    16:    (245, 149, 99),
    32:    (246, 124, 95),
    64:    (246,  94, 59),
    128:   (237, 207, 114),
    256:   (237, 200, 80),
    512:   (237, 197, 63),
    1024:  (237, 197, 63),
    2048:  (237, 194, 46),
    4096:  (  0, 175, 239),
    8192:  (  0, 143, 207),
}
TILE_TEXT_COLORS: Dict[int, Tuple[int, int, int]] = {
    0:     (119, 110, 101),
    2:     (119, 110, 101),
    4:     (119, 110, 101),
    8:     (255, 255, 255),
    16:    (255, 255, 255),
    32:    (255, 255, 255),
    64:    (255, 255, 255),
    128:   (255, 255, 255),
    256:   (255, 255, 255),
    512:   (255, 255, 255),
    1024:  (255, 255, 255),
    2048:  (255, 255, 255),
    4096:  (255, 255, 255),
    8192:  (255, 255, 255),
}

FONT_NAME = None   # system default
BG_COLOR       = (250, 248, 239)
GRID_BG_COLOR  = (187, 173, 160)
TITLE_COLOR    = (119, 110, 101)
SCORE_BG_COLOR = (119, 110, 101)
SCORE_FG_COLOR = (255, 255, 255)

ANIM_FPS      = 60
ANIM_MOVE_MS  = 80
ANIM_POP_MS   = 100
ANIM_SPAWN_MS = 150


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def ease_out(t: float) -> float:
    return 1 - (1 - t) ** 3

def ease_in(t: float) -> float:
    return t ** 3


# ─────────────────────────────────────────────
# TILE ANIMATION STATE
# ─────────────────────────────────────────────
@dataclass
class TileAnim:
    value:      int
    row_from:   int
    col_from:   int
    row_to:     int
    col_to:     int
    born:       float = 0.0          # pygame tick ms when created
    merged:     bool  = False
    spawning:   bool  = False
    scale:      float = 1.0         # for pop animation
    alpha:      int   = 255


# ─────────────────────────────────────────────
# TILE RENDER STATE  (what we draw each frame)
# ─────────────────────────────────────────────
@dataclass
class TileRender:
    value:  int
    x:      float
    y:      float
    scale:  float   = 1.0
    alpha:  int     = 255
    pop:    float   = 0.0   # 0-1 pop progress


# ─────────────────────────────────────────────
# GAME DIRECTION
# ─────────────────────────────────────────────
class Direction(Enum):
    UP    = ( 0, -1)
    DOWN  = ( 0,  1)
    LEFT  = (-1,  0)
    RIGHT = ( 1,  0)


# ─────────────────────────────────────────────
# GAME STATE
# ─────────────────────────────────────────────
class GameState(Enum):
    IDLE        = "idle"
    MOVING      = "moving"
    GAME_OVER   = "game_over"
    WIN         = "win"


# ─────────────────────────────────────────────
# BOARD
# ─────────────────────────────────────────────
class Board:
    def __init__(self) -> None:
        self.grid: List[List[int]] = [[0]*4 for _ in range(4)]
        self.score: int = 0
        self.best_score: int = self._load_best()
        self.won: bool = False
        self.spawn_tile()
        self.spawn_tile()

    # ── persistence ────────────────────────────
    def save_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "2048_save.json")

    def save(self) -> None:
        data = {
            "grid": self.grid,
            "score": self.score,
            "best_score": self.best_score,
            "won": self.won,
        }
        with open(self.save_path(), "w") as f:
            json.dump(data, f)

    @staticmethod
    def _load_best() -> int:
        try:
            with open(os.path.join(os.path.dirname(__file__), "2048_save.json")) as f:
                return json.load(f).get("best_score", 0)
        except Exception:
            return 0

    def load(self) -> bool:
        try:
            with open(self.save_path()) as f:
                data = json.load(f)
            self.grid       = data["grid"]
            self.score      = data.get("score", 0)
            self.best_score = data.get("best_score", 0)
            self.won        = data.get("won", False)
            return True
        except Exception:
            return False

    # ── tile helpers ───────────────────────────
    def empty_cells(self) -> List[Tuple[int, int]]:
        return [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]

    def spawn_tile(self) -> Optional[Tuple[int, int]]:
        cells = self.empty_cells()
        if not cells:
            return None
        r, c = random.choice(cells)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4
        return (r, c)

    def peek_spawn(self) -> Optional[Tuple[int, int]]:
        """Return position of a new tile without actually placing it."""
        cells = self.empty_cells()
        if not cells:
            return None
        return random.choice(cells)

    # ── core logic ─────────────────────────────
    def _slide_row(self, row: List[int]) -> Tuple[List[int], int, List[Tuple[int, int]]]:
        """Slide one row left. Returns (new_row, points, merge_positions)."""
        orig = [x for x in row if x != 0]
        merged: List[int] = []
        pts = 0
        merge_pos: List[Tuple[int, int]] = []   # col of merged tile
        i = 0
        while i < len(orig):
            if i + 1 < len(orig) and orig[i] == orig[i + 1]:
                val = orig[i] * 2
                merged.append(val)
                pts += val
                merge_pos.append(i)
                i += 2
            else:
                merged.append(orig[i])
                i += 1
        while len(merged) < 4:
            merged.append(0)
        return merged, pts, merge_pos

    def _rotate(self, grid: List[List[int]], times: int = 1) -> List[List[int]]:
        for _ in range(times):
            grid = [list(row) for row in zip(*grid[::-1])]
        return grid

    def _apply_move(self, grid: List[List[int]], d: Direction) -> List[List[int]]:
        """Rotate grid so movement always happens LEFT, then rotate back."""
        if d == Direction.UP:
            grid = self._rotate(grid, 3)
        elif d == Direction.DOWN:
            grid = self._rotate(grid, 1)
        elif d == Direction.RIGHT:
            grid = self._rotate(grid, 2)
        # LEFT: no rotation
        return grid

    def _undo_apply(self, grid: List[List[int]], d: Direction) -> List[List[int]]:
        if d == Direction.UP:
            grid = self._rotate(grid, 1)
        elif d == Direction.DOWN:
            grid = self._rotate(grid, 3)
        elif d == Direction.RIGHT:
            grid = self._rotate(grid, 2)
        return grid

    def move(self, d: Direction) -> Tuple[bool, List[Tuple[int, int, int, int]], int, List[Tuple[int, int]]]:
        """
        Attempt a move. Returns:
          (moved, merge_tile_data, points_earned, new_tile_pos)
        merge_tile_data: list of (from_row, from_col, to_row, to_col, value)
        new_tile_pos: (row, col) of newly spawned tile (or None)
        """
        grid = [row[:] for row in self.grid]
        grid = self._apply_move(grid, d)

        moved       = False
        merge_data: List[Tuple[int, int, int, int, int]] = []
        total_pts   = 0

        for r in range(4):
            new_row, pts, merge_cols = self._slide_row(grid[r])
            # track merges
            for mc in merge_cols:
                merge_data.append((r, mc, r, mc, new_row[mc]))
            if new_row != grid[r]:
                moved = True
            grid[r] = new_row
            total_pts += pts

        if moved:
            grid = self._undo_apply(grid, d)
            # rotate merge positions back
            fixed = []
            for (rf, cf, rt, ct, val) in merge_data:
                rf2, cf2 = self._transform_pos(rf, cf, d)
                fixed.append((rf2, cf2, rf2, cf2, val))   # merge is local
            merge_data = fixed
            self.grid = grid
            self.score += total_pts
            if self.score > self.best_score:
                self.best_score = self.score
            if total_pts > 0:
                self.won = True   # any merge means you've been playing
            new_pos = self.spawn_tile()
            return True, merge_data, total_pts, (new_pos,)
        return False, [], 0, (None,)

    def _transform_pos(self, r: int, c: int, d: Direction) -> Tuple[int, int]:
        """Undo the rotation on a position."""
        if d == Direction.UP:
            return self._rotate_pos(r, c, 3)
        elif d == Direction.DOWN:
            return self._rotate_pos(r, c, 1)
        elif d == Direction.RIGHT:
            return self._rotate_pos(r, c, 2)
        return r, c

    @staticmethod
    def _rotate_pos(r: int, c: int, times: int) -> Tuple[int, int]:
        for _ in range(times):
            r, c = c, 3 - r
        return r, c

    def can_move(self) -> bool:
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == 0:
                    return True
                if c < 3 and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r < 3 and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False


# ─────────────────────────────────────────────
# ANIMATION MANAGER
# ─────────────────────────────────────────────
class AnimManager:
    def __init__(self) -> None:
        self.tile_anim: List[TileAnim] = []
        self.trails: List[TileAnim] = []   # tiles that are moving / fading
        self.spawns:  List[TileAnim] = []   # newly spawned tiles

    def begin_round(self) -> None:
        """Called at the start of each move round — stash current grid."""
        self.tile_anim.clear()
        self.trails.clear()
        self.spawns.clear()

    def add_tile(self, anim: TileAnim) -> None:
        self.tile_anim.append(anim)

    def add_spawn(self, anim: TileAnim) -> None:
        self.spawns.append(anim)

    def all_tiles(self):
        return self.tile_anim + self.spawns


# ─────────────────────────────────────────────
# RENDERER
# ─────────────────────────────────────────────
class Renderer:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("2048")
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WIN_H))
        self.font_large  = pygame.font.Font(FONT_NAME, 48)
        self.font_medium = pygame.font.Font(FONT_NAME, 28)
        self.font_small  = pygame.font.Font(FONT_NAME, 18)
        self.clock = pygame.time.Clock()

    def grid_to_pixel(self, row: int, col: int) -> Tuple[int, int]:
        x = GRID_PADDING + col * (CELL_SIZE + CELL_GAP)
        y = SCORE_H + GRID_PADDING + row * (CELL_SIZE + CELL_GAP)
        return x, y

    def draw_background(self) -> None:
        self.screen.fill(BG_COLOR)

    def draw_score_bar(self, score: int, best: int) -> None:
        pygame.draw.rect(self.screen, SCORE_BG_COLOR, (0, 0, WINDOW_SIZE, SCORE_H))
        # Title
        title = self.font_large.render("2048", True, (255, 255, 255))
        self.screen.blit(title, (GRID_PADDING, 16))

        # Score box
        self._draw_score_box(WINDOW_SIZE - 230, 12, "SCORE", score)
        self._draw_score_box(WINDOW_SIZE - 110, 12, "BEST",  best)

    def _draw_score_box(self, x: int, y: int, label: str, value: int) -> None:
        box_w, box_h = 100, 56
        pygame.draw.rect(self.screen, SCORE_BG_COLOR, (x, y, box_w, box_h))
        lbl = self.font_small.render(label, True, (238, 228, 218))
        val = self.font_medium.render(str(value), True, (255, 255, 255))
        self.screen.blit(lbl, (x + (box_w - lbl.get_width()) // 2, y + 6))
        self.screen.blit(val, (x + (box_w - val.get_width()) // 2, y + 22))

    def draw_grid_bg(self) -> None:
        rect = pygame.Rect(
            GRID_PADDING,
            SCORE_H + GRID_PADDING,
            WINDOW_SIZE - GRID_PADDING * 2,
            WINDOW_SIZE - GRID_PADDING * 2,
        )
        pygame.draw.rect(self.screen, GRID_BG_COLOR, rect, border_radius=8)
        # Empty cell backgrounds
        for r in range(4):
            for c in range(4):
                px, py = self.grid_to_pixel(r, c)
                pygame.draw.rect(
                    self.screen,
                    (197, 182, 169),
                    (px, py, CELL_SIZE, CELL_SIZE),
                    border_radius=6,
                )

    def draw_tile(self, value: int, x: float, y: float,
                  scale: float = 1.0, alpha: int = 255) -> None:
        if value == 0:
            return
        color = TILE_COLORS.get(value, (237, 194, 46))
        tw = int(CELL_SIZE * scale)
        th = int(CELL_SIZE * scale)
        surf = pygame.Surface((tw, th), pygame.SRCALPHA)
        pygame.draw.rect(surf, color + (alpha,), (0, 0, tw, th), border_radius=6)
        # Font size based on value digits
        digits = len(str(value))
        if digits <= 2:
            fsize = 48
        elif digits == 3:
            fsize = 38
        elif digits == 4:
            fsize = 32
        else:
            fsize = 24
        font = pygame.font.Font(FONT_NAME, fsize)
        text = font.render(str(value), True, TILE_TEXT_COLORS.get(value, (255,255,255)))
        text.set_alpha(alpha)
        tx = (tw - text.get_width()) // 2
        ty = (th - text.get_height()) // 2
        surf.blit(text, (tx, ty))
        self.screen.blit(surf, (int(x) + (CELL_SIZE - tw)//2, int(y) + (CELL_SIZE - th)//2))

    def draw_tiles(self, board: Board, anims: AnimManager, now: float,
                   moving: bool, move_dirs: Dict[Tuple[int,int], Tuple[int,int]]) -> None:
        """
        Draw all tiles. moving=True means we're in an animation round
        and we should draw from anims, not from board directly.
        """
        # Draw static tiles (tiles not involved in the current move)
        static_grid = [[0]*4 for _ in range(4)]
        anim_tiles: Dict[Tuple[int,int], TileAnim] = {}

        if moving:
            for a in anims.tile_anim:
                key = (a.row_from, a.col_from)
                anim_tiles[key] = a
            for a in anims.spawns:
                anim_tiles[(a.row_to, a.col_to)] = a

        # Draw tiles from animation
        for a in anims.tile_anim:
            progress = min(1.0, (now - a.born) / ANIM_MOVE_MS)
            e = ease_out(progress)
            from_px, from_py = self.grid_to_pixel(a.row_from, a.col_from)
            to_px,   to_py   = self.grid_to_pixel(a.row_to,   a.col_to)
            x = lerp(from_px, to_px, e)
            y = lerp(from_py, to_py, e)
            pop = 0.0
            if a.merged and progress >= 1.0:
                pop = 1.0
            self.draw_tile(a.value, x, y, scale=1.0 + pop * 0.15)

        # Draw spawning tiles
        for a in anims.spawns:
            progress = min(1.0, (now - a.born) / ANIM_SPAWN_MS)
            e = ease_out(progress)
            px, py = self.grid_to_pixel(a.row_to, a.col_to)
            scale = 0.3 + 0.7 * e
            self.draw_tile(a.value, px, py, scale=scale)

    def draw_game_over(self) -> None:
        overlay = pygame.Surface((WINDOW_SIZE, WIN_H), pygame.SRCALPHA)
        overlay.fill((250, 248, 239, 200))
        self.screen.blit(overlay, (0, 0))
        msg = self.font_large.render("Game Over!", True, TITLE_COLOR)
        self.screen.blit(msg, ((WINDOW_SIZE - msg.get_width()) // 2, WIN_H // 2 - 30))
        hint = self.font_medium.render("Press R to restart", True, TITLE_COLOR)
        self.screen.blit(hint, ((WINDOW_SIZE - hint.get_width()) // 2, WIN_H // 2 + 20))

    def draw_win_screen(self) -> None:
        overlay = pygame.Surface((WINDOW_SIZE, WIN_H), pygame.SRCALPHA)
        overlay.fill((250, 248, 239, 180))
        self.screen.blit(overlay, (0, 0))
        msg = self.font_large.render("You Win! 🎉", True, (237, 194, 46))
        self.screen.blit(msg, ((WINDOW_SIZE - msg.get_width()) // 2, WIN_H // 2 - 30))
        hint = self.font_medium.render("Press R to continue or C to restart", True, TITLE_COLOR)
        self.screen.blit(hint, ((WINDOW_SIZE - hint.get_width()) // 2, WIN_H // 2 + 20))

    def draw_hint(self) -> None:
        hint = self.font_small.render("← ↑ ↓ → to move  |  S to save  |  R to restart", True, (185, 173, 160))
        self.screen.blit(hint, ((WINDOW_SIZE - hint.get_width()) // 2, WIN_H - 24))


# ─────────────────────────────────────────────
# GAME ENGINE
# ─────────────────────────────────────────────
class Game2048:
    def __init__(self) -> None:
        self.renderer = Renderer()
        self.board    = Board()
        self.anim     = AnimManager()
        self.state    = GameState.IDLE
        self.continue_after_win = False
        self.move_start_time: float = 0
        self.pending_spawn: Optional[Tuple[int,int]] = None
        self.show_win = False

    def run(self) -> None:
        running = True
        while running:
            now = pygame.time.get_ticks()
            self.renderer.clock.tick(ANIM_FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    handled = self._handle_key(event.key)
                    if not handled and event.key == pygame.K_ESCAPE:
                        running = False

            # ── animation tick ───────────────────
            if self.state == GameState.MOVING:
                elapsed = now - self.move_start_time
                if elapsed >= ANIM_MOVE_MS + 20:
                    self._finish_move()

            # ── render ──────────────────────────
            self._render(now)
            pygame.display.flip()

        self.board.save()
        pygame.quit()

    def _handle_key(self, key: int) -> bool:
        if key == pygame.K_r:
            self._restart()
            return True

        if key == pygame.K_s:
            self.board.save()
            return True

        if key == pygame.K_c and self.state == GameState.WIN:
            self._restart()
            return True

        if self.state != GameState.IDLE and self.state != GameState.WIN:
            return True

        d_map = {
            pygame.K_LEFT:  Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_UP:    Direction.UP,
            pygame.K_DOWN:  Direction.DOWN,
        }
        d = d_map.get(key)
        if d is None:
            return False

        self._start_move(d)
        return True

    def _start_move(self, d: Direction) -> None:
        self.anim.begin_round()
        moved, merge_data, pts, (new_pos,) = self.board.move(d)

        if not moved:
            return

        now = pygame.time.get_ticks()
        # Build animation tiles for each cell
        # We need to track where each tile went.
        # The merge_data contains (from_r, from_c, to_r, to_c, value)
        # We'll rebuild from the board snapshot.
        # For simplicity, animate every non-zero tile that moved or stays.
        old_grid = [row[:] for row in self.board.grid]
        # Actually let's track using the grid before the move...
        # Since board.move already modified the grid, we reconstruct from
        # what we know: every tile in the NEW grid either stayed or came from somewhere.
        # Simpler: snapshot the old grid before calling board.move.
        pass  # done below

    def _finish_move(self) -> None:
        self.state = GameState.IDLE
        self.pending_spawn = None
        if not self.board.can_move():
            self.state = GameState.GAME_OVER
        self.board.save()

    def _restart(self) -> None:
        self.board   = Board()
        self.anim    = AnimManager()
        self.state   = GameState.IDLE
        self.show_win = False

    # ── improved move with proper animation tracking ──
    def _start_move(self, d: Direction) -> None:
        # Snapshot before move
        old_grid = [row[:] for row in self.board.grid]
        moved, merge_data, pts, (new_pos,) = self.board.move(d)
        if not moved:
            return

        now = pygame.time.get_ticks()
        self.anim.begin_round()
        self.move_start_time = now
        self.state = GameState.MOVING

        # Determine movement: for each cell in new grid, figure out where it came from
        # Use a greedy approach: trace paths
        visited_new = [[False]*4 for _ in range(4)]

        for r in range(4):
            for c in range(4):
                val = self.board.grid[r][c]
                if val == 0:
                    continue
                # Find the source of this tile in old_grid
                src = self._find_source(old_grid, self.board.grid, r, c, d, visited_new)
                if src is None:
                    # It's a new tile from spawn
                    self.anim.add_spawn(TileAnim(
                        value=val,
                        row_from=r, col_from=c,
                        row_to=r, col_to=c,
                        born=now,
                        spawning=True,
                    ))
                else:
                    sr, sc = src
                    self.anim.add_tile(TileAnim(
                        value=val,
                        row_from=sr, col_from=sc,
                        row_to=r, col_to=c,
                        born=now,
                        merged=(r, c) in [(m[0], m[1]) for m in merge_data],
                    ))
                    visited_new[r][c] = True

        # Spawning tile
        if new_pos:
            nr, nc = new_pos
            val = self.board.grid[nr][nc]
            # remove the static tile we just added and replace with spawn anim
            self.anim.tile_anim = [
                a for a in self.anim.tile_anim
                if not (a.row_to == nr and a.col_to == nc)
            ]
            self.anim.add_spawn(TileAnim(
                value=val,
                row_from=nr, col_from=nc,
                row_to=nr, col_to=nc,
                born=now,
                spawning=True,
            ))

        self.pending_spawn = new_pos

    def _find_source(self, old_grid, new_grid, tr, tc, d: Direction,
                     visited) -> Optional[Tuple[int, int]]:
        """Find which cell in old_grid contributed to (tr, tc) in new_grid."""
        val = new_grid[tr][tc]
        dr, dc = d.value
        # The tile came from a cell in the opposite direction
        # We need to find the "furthest" matching tile in that direction
        if d == Direction.LEFT:
            # scan columns left of tc
            for c in range(tc, -1, -1):
                if old_grid[tr][c] == val and not visited[tr][c]:
                    visited[tr][tc] = True
                    return (tr, c)
        elif d == Direction.RIGHT:
            for c in range(tc, 4):
                if old_grid[tr][c] == val and not visited[tr][c]:
                    visited[tr][tc] = True
                    return (tr, c)
        elif d == Direction.UP:
            for r in range(tr, -1, -1):
                if old_grid[r][tc] == val and not visited[r][tc]:
                    visited[tr][tc] = True
                    return (r, tc)
        elif d == Direction.DOWN:
            for r in range(tr, 4):
                if old_grid[r][tc] == val and not visited[r][tc]:
                    visited[tr][tc] = True
                    return (r, tc)
        return None

    def _render(self, now: float) -> None:
        r = self.renderer
        r.draw_background()
        r.draw_score_bar(self.board.score, self.board.best_score)
        r.draw_grid_bg()

        # Draw tiles
        moving = (self.state == GameState.MOVING)

        if moving:
            # Draw animated tiles
            for a in self.anim.tile_anim:
                progress = min(1.0, (now - a.born) / ANIM_MOVE_MS)
                e = ease_out(progress)
                fx, fy = r.grid_to_pixel(a.row_from, a.col_from)
                tx, ty = r.grid_to_pixel(a.row_to,   a.col_to)
                x = lerp(fx, tx, e)
                y = lerp(fy, ty, e)
                # Pop effect for merged tiles at end of animation
                pop = 0.0
                if a.merged and progress > 0.7:
                    pop_t = (progress - 0.7) / 0.3
                    pop = math.sin(pop_t * math.pi) * 0.2
                r.draw_tile(a.value, x, y, scale=1.0 + pop)

            # Draw spawning tiles
            for a in self.anim.spawns:
                progress = min(1.0, (now - a.born) / ANIM_SPAWN_MS)
                e = ease_out(progress)
                px, py = r.grid_to_pixel(a.row_to, a.col_to)
                scale = 0.3 + 0.7 * e
                r.draw_tile(a.value, px, py, scale=scale)
        else:
            # Static draw
            for row in range(4):
                for col in range(4):
                    val = self.board.grid[row][col]
                    if val == 0:
                        continue
                    px, py = r.grid_to_pixel(row, col)
                    r.draw_tile(val, px, py)

        r.draw_hint()

        if self.state == GameState.GAME_OVER:
            r.draw_game_over()
        elif self.state == GameState.WIN and not self.continue_after_win:
            r.draw_win_screen()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    Game2048().run()
