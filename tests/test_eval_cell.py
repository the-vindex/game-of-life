import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
pygame.init()

from grid import Grid
from gameOfLife import evalCell


def make_grid(*live_cells: tuple[int, int]) -> Grid:
    g = Grid()
    for row, col in live_cells:
        g.cells[row][col] = True
    return g


# Conway's rules:
#   Live cell, <2 neighbors  -> dies
#   Live cell, 2-3 neighbors -> survives
#   Live cell, >3 neighbors  -> dies
#   Dead cell, 3 neighbors   -> becomes alive
#   Dead cell, !=3 neighbors -> stays dead

def test_live_cell_no_neighbors_dies():
    g = make_grid((5, 5))
    assert evalCell(g, 5, 5) == False

def test_live_cell_one_neighbor_dies():
    g = make_grid((5, 5), (5, 6))
    assert evalCell(g, 5, 5) == False

def test_live_cell_two_neighbors_survives():
    g = make_grid((5, 5), (5, 6), (5, 4))
    assert evalCell(g, 4, 5) == True

def test_live_cell_three_neighbors_survives():
    g = make_grid((5, 5), (5, 6), (5, 4), (4, 5))
    assert evalCell(g, 5, 5) == True

def test_live_cell_four_neighbors_dies():
    g = make_grid((5, 5), (5, 6), (5, 4), (4, 5), (6, 5))
    assert evalCell(g, 5, 5) == False

def test_dead_cell_three_neighbors_becomes_alive():
    g = make_grid((4, 5), (6, 5), (5, 6))
    assert evalCell(g, 5, 5) == True

def test_dead_cell_two_neighbors_stays_dead():
    g = make_grid((4, 5), (6, 5))
    assert evalCell(g, 5, 5) == False

def test_dead_cell_four_neighbors_stays_dead():
    g = make_grid((4, 5), (6, 5), (5, 4), (5, 6))
    assert evalCell(g, 5, 5) == False
