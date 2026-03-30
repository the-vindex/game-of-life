import pygame

COLS = 50
ROWS = 50
CELL_SIZE = 20

COLOR_BG = (20, 20, 20)
COLOR_ALIVE = (0, 200, 100)
COLOR_GRID = (50, 50, 50)


class Grid:
    def __init__(self) -> None:
        self.cells: list[list[bool]] = [[False] * COLS for _ in range(ROWS)]

    def toggle(self, row: int, col: int) -> None:
        self.checkCoordsInBounds(row, col)
        self.cells[row][col] = not self.cells[row][col]

    def set(self, row: int, col: int, value: bool) -> None:
        self.checkCoordsInBounds(row, col)
        self.cells[row][col] = value

    def setOn(self, row: int, col: int) -> None:
        self.checkCoordsInBounds(row, col)
        self.cells[row][col] = True

    def setOff(self, row: int, col: int) -> None:
        self.checkCoordsInBounds(row, col)
        self.cells[row][col] = False

    def get(self, row: int, col: int) -> bool:
        self.checkCoordsInBounds(row, col)
        return self.cells[row][col]

    def safeGet(self, row: int, col: int) -> bool:
        if self.isCoordsInBounds(row,col):
            return self.cells[row][col]
        else:
            return False

    def isCoordsInBounds(self, row: int, col: int) -> bool:
        return not(row <0 or col <0 or row>= ROWS or col >= COLS)

    def checkCoordsInBounds(self, row: int, col: int) -> None:
        if not self.isCoordsInBounds(row,col):        
            raise Exception(f"Out of bounds: {row}, {col}")

    def draw(self, surface: pygame.Surface) -> None:
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


    def setFromGrid(self, other_grid: "Grid") -> None:
        for row in range(ROWS):
            for col in range(COLS):
                self.cells[row][col] = other_grid.cells[row][col]