import pygame

COLS = 50
ROWS = 50
CELL_SIZE = 20

COLOR_BG = (20, 20, 20)
COLOR_ALIVE = (0, 200, 100)
COLOR_GRID = (50, 50, 50)


class Grid:
    def __init__(self):
        self.cells = [[False] * COLS for _ in range(ROWS)]

    def toggle(self, row, col):
        self.cells[row][col] = not self.cells[row][col]

    def draw(self, surface):
        surface.fill(COLOR_BG)
        for row in range(ROWS):
            for col in range(COLS):
                if self.cells[row][col]:
                    pygame.draw.rect(
                        surface, COLOR_ALIVE,
                        (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
        for x in range(0, COLS * CELL_SIZE + 1, CELL_SIZE):
            pygame.draw.line(surface, COLOR_GRID, (x, 0), (x, ROWS * CELL_SIZE))
        for y in range(0, ROWS * CELL_SIZE + 1, CELL_SIZE):
            pygame.draw.line(surface, COLOR_GRID, (0, y), (COLS * CELL_SIZE, y))
