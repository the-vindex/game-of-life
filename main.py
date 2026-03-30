import pygame
import random
import importlib
import os
import sys
import traceback
from collections.abc import Callable
import gameOfLife
from grid import Grid, COLS, ROWS, CELL_SIZE
from state import save_slot, load_slot, slot_exists

_step_error = False
_iterations: int = 0
class StepTimer:
    def __init__(self, interval: int = 10) -> None:
        self.interval = interval
        self._counter: int = 0

    def tick(self) -> bool:
        self._counter += 1
        if self._counter >= self.interval:
            self._counter = 0
            return True
        return False

_step_timer = StepTimer()

def setIterations(count: int) -> None:
    global _iterations
    _iterations = count

def step(grid: Grid, count: int = 1) -> None:
    global _step_error
    try:
        gameOfLife.step(grid, count)
        _step_error = False
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        _step_error = True

_gol_mtime = os.path.getmtime(gameOfLife.__file__)
_gol_error = False

def _reload_if_changed() -> None:
    global _gol_mtime, _gol_error
    try:
        mtime = os.path.getmtime(gameOfLife.__file__)
        if mtime != _gol_mtime:
            importlib.reload(gameOfLife)
            _gol_mtime = mtime
            _gol_error = False
    except Exception:
        _gol_error = True

SIDEBAR_WIDTH = 130
GRID_WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
WIDTH = GRID_WIDTH + SIDEBAR_WIDTH

COLOR_SIDEBAR = (28, 28, 28)
COLOR_BTN = (55, 55, 55)
COLOR_BTN_SAVE = (45, 75, 50)
COLOR_BTN_LOAD = (40, 55, 85)
COLOR_BTN_LOAD_FILLED = (55, 80, 130)
COLOR_HOVER = (85, 85, 85)


class Button:
    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect, label: str, base_color: tuple[int, int, int], callback: Callable[[], None], filled_fn: Callable[[], bool] | None = None) -> None:
        self.rect = pygame.Rect(rect)
        self.label = label
        self.base_color = base_color
        self.callback = callback
        self.filled_fn = filled_fn

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = COLOR_HOVER if hovered else self.base_color
        if self.filled_fn and self.filled_fn():
            color = COLOR_BTN_LOAD_FILLED if not hovered else COLOR_HOVER
        pygame.draw.rect(surface, color, self.rect, border_radius=3)
        text = font.render(self.label, True, (210, 210, 210))
        surface.blit(text, text.get_rect(center=self.rect.center))

    def handle_click(self, pos: tuple[int, int]) -> bool:
        if self.rect.collidepoint(pos):
            self.callback()
            return True
        return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
font = pygame.font.SysFont("monospace", 11)
font_large = pygame.font.SysFont("monospace", 18)

grid = Grid()
clock = pygame.time.Clock()

SX = GRID_WIDTH + 8
BW = SIDEBAR_WIDTH - 16
BH = 22
HW = (BW - 4) // 2


# Glider pattern (relative offsets from top-left origin)
GLIDER: list[tuple[int, int]] = [
    (0, 1),
    (1, 2),
    (2, 0), (2, 1), (2, 2),
]

def place_glider() -> None:
    for dr, dc in GLIDER:
        r, c = 1 + dr, 1 + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            grid.cells[r][c] = True


# Gosper Glider Gun
GLIDER_GUN: list[tuple[int, int]] = [
    (0, 24),
    (1, 22), (1, 24),
    (2, 12), (2, 13), (2, 20), (2, 21), (2, 34), (2, 35),
    (3, 11), (3, 15), (3, 20), (3, 21), (3, 34), (3, 35),
    (4,  0), (4,  1), (4, 10), (4, 16), (4, 20), (4, 21),
    (5,  0), (5,  1), (5, 10), (5, 14), (5, 16), (5, 17), (5, 22), (5, 24),
    (6, 10), (6, 16), (6, 24),
    (7, 11), (7, 15),
    (8, 12), (8, 13),
]

def place_glider_gun() -> None:
    for dr, dc in GLIDER_GUN:
        r, c = 1 + dr, 1 + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            grid.cells[r][c] = True

def make_buttons() -> tuple[list["Button"], "Button"]:
    buttons: list[Button] = []
    y: int = 10

    def clear() -> None:
        grid.cells[:] = [[False] * COLS for _ in range(ROWS)]

    def randomize() -> None:
        grid.cells[:] = [[random.random() < 0.3 for _ in range(COLS)] for _ in range(ROWS)]

    buttons.append(Button((SX, y, BW, BH), "Clear", COLOR_BTN, clear))
    y += BH + 6
    buttons.append(Button((SX, y, BW, BH), "Random", COLOR_BTN, randomize))
    y += BH + 14

    for slot in range(1, 11):
        s = slot
        buttons.append(Button(
            (SX, y, HW, BH), f"S{s}", COLOR_BTN_SAVE,
            lambda s=s: save_slot(grid.cells, s)
        ))
        buttons.append(Button(
            (SX + HW + 4, y, HW, BH), f"L{s}", COLOR_BTN_LOAD,
            lambda s=s: _load(s),
            filled_fn=lambda s=s: slot_exists(s)
        ))
        y += BH + 4

    step_btn = Button((SX, y, HW, BH), "Step", COLOR_BTN, lambda: step(grid))
    buttons.append(step_btn)

    y += BH + 4
    buttons.append(Button((SX, y, HW, BH), "Step x10", COLOR_BTN, lambda: setIterations(10)))

    y += BH + 4
    buttons.append(Button((SX, y, HW, BH), "Step x1000", COLOR_BTN, lambda: setIterations(1000)))

    y += BH + 4
    buttons.append(Button((SX, y, HW, BH), "Stop", COLOR_BTN, lambda: setIterations(0)))

    y += BH + 4
    buttons.append(Button((SX, y, BW, BH), "Plane", COLOR_BTN, place_glider))

    y += BH + 4
    buttons.append(Button((SX, y, BW, BH), "Launcher", COLOR_BTN, place_glider_gun))

    return buttons, step_btn


def _load(slot: int) -> None:
    data = load_slot(slot)
    if data is not None:
        grid.cells = data


buttons, step_btn = make_buttons()

dragging = False
drag_value = True  # True = painting alive, False = erasing

# (row, col, will_live: bool, start_ticks) or None
_cell_eval: tuple[int, int, bool, int] | None = None
EVAL_DURATION = 2000  # ms
EVAL_BLINK_PERIOD = 200  # ms


def _eval_cell_at(px: int, py: int) -> None:
    global _cell_eval
    col = px // CELL_SIZE
    row = py // CELL_SIZE
    if not (0 <= row < ROWS and 0 <= col < COLS):
        return
    try:
        result = gameOfLife.evalCell(grid, row, col)
        _cell_eval = (row, col, bool(result), pygame.time.get_ticks())
    except Exception:
        traceback.print_exc(file=sys.stderr)


def _draw_cell_eval(surface: pygame.Surface) -> None:
    if _cell_eval is None:
        return
    row, col, will_live, start = _cell_eval
    elapsed = pygame.time.get_ticks() - start
    if elapsed >= EVAL_DURATION:
        return
    if elapsed % EVAL_BLINK_PERIOD < EVAL_BLINK_PERIOD // 2:
        color = (50, 255, 80) if will_live else (255, 50, 50)
        pygame.draw.rect(surface, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def apply_drag(px: int, py: int) -> None:
    col = px // CELL_SIZE
    row = py // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        grid.cells[row][col] = drag_value


def _draw_error_triangle(surface: pygame.Surface) -> None:
    r = step_btn.rect
    x = r.right + 6
    cy = r.centery
    h, w = 14, 12
    pygame.draw.polygon(surface, (200, 40, 40), [
        (x + w // 2, cy - h // 2),
        (x + w,      cy + h // 2),
        (x,          cy + h // 2),
    ])

def _draw_step_error(surface: pygame.Surface) -> None:
    if pygame.time.get_ticks() % 600 < 300:
        r = step_btn.rect
        x = r.right + 6
        cy = r.centery
        text = font.render("!", True, (220, 40, 40))
        surface.blit(text, text.get_rect(center=(x + 5, cy)))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                _eval_cell_at(*event.pos)
            elif event.button == 1 and not any(b.handle_click(event.pos) for b in buttons):
                dragging = True
                px, py = event.pos
                col = px // CELL_SIZE
                row = py // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    drag_value = not grid.cells[row][col]
                    apply_drag(px, py)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                apply_drag(*event.pos)

    _reload_if_changed()

    if _iterations > 0 and _step_timer.tick():
        step(grid)
        _iterations -= 1

    grid.draw(screen)
    _draw_cell_eval(screen)
    pygame.draw.rect(screen, COLOR_SIDEBAR, (GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
    for b in buttons:
        b.draw(screen, font)
    if _gol_error:
        _draw_error_triangle(screen)
    if _step_error:
        _draw_step_error(screen)

    mx, my = pygame.mouse.get_pos()
    col = mx // CELL_SIZE
    row = my // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        coord_text = font_large.render(f"{col}, {row}", True, (160, 160, 160))
        screen.blit(coord_text, (SX, HEIGHT - BH))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
