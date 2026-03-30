import pygame
import random
import importlib
import os
import gameOfLife
from grid import Grid, COLS, ROWS, CELL_SIZE
from state import save_slot, load_slot, slot_exists

def step(grid):
    gameOfLife.step(grid)

_gol_mtime = os.path.getmtime(gameOfLife.__file__)
_gol_error = False

def _reload_if_changed():
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
    def __init__(self, rect, label, base_color, callback, filled_fn=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.base_color = base_color
        self.callback = callback
        self.filled_fn = filled_fn

    def draw(self, surface, font):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = COLOR_HOVER if hovered else self.base_color
        if self.filled_fn and self.filled_fn():
            color = COLOR_BTN_LOAD_FILLED if not hovered else COLOR_HOVER
        pygame.draw.rect(surface, color, self.rect, border_radius=3)
        text = font.render(self.label, True, (210, 210, 210))
        surface.blit(text, text.get_rect(center=self.rect.center))

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            return True
        return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
font = pygame.font.SysFont("monospace", 11)

grid = Grid()
clock = pygame.time.Clock()

SX = GRID_WIDTH + 8
BW = SIDEBAR_WIDTH - 16
BH = 22
HW = (BW - 4) // 2


def make_buttons():
    buttons = []
    y = 10

    def clear():
        grid.cells[:] = [[False] * COLS for _ in range(ROWS)]

    def randomize():
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

    return buttons, step_btn


def _load(slot):
    data = load_slot(slot)
    if data is not None:
        grid.cells = data


buttons, step_btn = make_buttons()


def _draw_error_triangle(surface):
    r = step_btn.rect
    x = r.right + 6
    cy = r.centery
    h, w = 14, 12
    pygame.draw.polygon(surface, (200, 40, 40), [
        (x + w // 2, cy - h // 2),
        (x + w,      cy + h // 2),
        (x,          cy + h // 2),
    ])


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not any(b.handle_click(event.pos) for b in buttons):
                px, py = event.pos
                col = px // CELL_SIZE
                row = py // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    grid.toggle(row, col)

    _reload_if_changed()
    grid.draw(screen)
    pygame.draw.rect(screen, COLOR_SIDEBAR, (GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
    for b in buttons:
        b.draw(screen, font)
    if _gol_error:
        _draw_error_triangle(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
