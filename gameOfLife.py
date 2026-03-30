from grid import Grid, COLS, ROWS

def step(grid: Grid, count: int = 1) -> None:
    for _ in range(count):
        doOneStep(grid)


def doOneStep(grid: Grid) -> None:
    new_grid = Grid()

    for row in range(COLS):
        for col in range(ROWS):
            buduZit = evalCell(grid, row, col)

            new_grid.set(row,col, buduZit)

    grid.setFromGrid(new_grid)

def evalCell(grid: Grid, row: int, col: int) -> bool:
    pocet_sousedu = 0
    pocet_sousedu = pocet_sousedu + (1 if grid.safeGet(row-1, col)     else 0) # nadeMnou
    pocet_sousedu = pocet_sousedu + (1 if grid.safeGet(row+1, col)     else 0) # podeMnou
    pocet_sousedu = pocet_sousedu + (1 if grid.safeGet(row-1, col-1)   else 0) # vlevoNahore
    pocet_sousedu = pocet_sousedu + (1 if grid.safeGet(row+1, col-1)   else 0) #vlevoDole
    pocet_sousedu = pocet_sousedu + (1 if grid.safeGet(row-1, col+1)   else 0) #vpravoNahore
    pocet_sousedu = pocet_sousedu + (1 if grid.safeGet(row+1, col+1)   else 0) #vpravoDole
    pocet_sousedu = pocet_sousedu + (1 if grid.safeGet(row, col-1)     else 0) # vlevo
    pocet_sousedu = pocet_sousedu + (1 if grid.safeGet(row, col+1)     else 0) # vpravo
    
    print(f"{row}, {col}, pocet sousedu {pocet_sousedu}")

    ziju: bool = grid.get(row,col)

    buduZit = False
    if not ziju and pocet_sousedu == 3:
        buduZit = True
    elif ziju and pocet_sousedu in (2,3):
        buduZit = True
    else:
        buduZit = False
    
    return buduZit